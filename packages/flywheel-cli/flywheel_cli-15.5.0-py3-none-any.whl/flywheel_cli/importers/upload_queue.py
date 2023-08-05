"""Provides upload queue"""
import logging
import os
import tempfile
from abc import ABC, abstractmethod

from .packfile import create_zip_packfile
from .progress_reporter import ProgressReporter
from .work_queue import Task, WorkQueue

log = logging.getLogger(__name__)
MAX_IN_MEMORY_XFER = 32 * (2 ** 20)  # Files under 32mb send as one chunk


class Uploader(ABC):
    """Abstract uploader class, that can upload files"""

    verb = "Uploading"

    @abstractmethod
    def upload(self, container, name, fileobj, metadata=None):
        """Upload the given file-like object to the given container as name.

        Arguments:
            container (ContainerNode): The destination container
            name (str): The file name
            fileobj (obj): The file-like object, which supports read()
            metadata (dict): Container metadata

        Yields:
            int: Number of bytes uploaded (periodically)
        """

    @abstractmethod
    def file_exists(self, container, name):
        """Check if the given file object already exists on the given container.

        Arguments:
            container (ContainerNode): The destination container
            name (str): The file name

        Returns:
            bool: True if the file already exists, otherwise False
        """

    @staticmethod
    def supports_signed_url():
        """Check if signed url upload is supported.

        Returns:
            bool: True if signed url upload is supported
        """
        return False


class UploadFileWrapper:
    """Wrapper around file that measures progress"""

    def __init__(self, fileobj=None, walker=None, path=None):
        """Initialize a file wrapper, must specify fileobj OR walker and path"""
        self.fileobj = fileobj
        self.walker = walker
        self.path = path
        self._sent = 0
        self._total_size = None
        if fileobj and fileobj.name:
            self.name = fileobj.name
        else:
            self.name = path

    def _open(self):
        if not self.fileobj:
            self.fileobj = self.walker.open(self.path, "rb")

    def read(self, size=-1):
        """Read chunk from file"""
        self._open()
        chunk = self.fileobj.read(size)
        self._sent = self._sent + len(chunk)
        return chunk

    def reset(self):
        """Reset file offset"""
        if self.fileobj:
            self.fileobj.seek(0)
        self._sent = 0

    def close(self):
        """Close file"""
        if self.fileobj:
            self.fileobj.close()
        self.fileobj = None

    @property
    def len(self):
        """Get remaining size"""
        return self.total_size - self._sent

    @property
    def total_size(self):
        """Get total size"""
        if self._total_size is None:
            self._open()
            self.fileobj.seek(0, 2)
            self._total_size = self.fileobj.tell()
            self.fileobj.seek(0)
        return self._total_size

    @property
    def get_bytes_sent(self):
        """Get bytes sent"""
        return self._sent


class UploadTask(Task):
    """UploadTask class"""

    def __init__(
        self,
        uploader,
        audit_log,
        container,
        filename,
        fileobj=None,
        walker=None,
        path=None,
        metadata=None,
        deid_log=None,
    ):
        """Initialize an upload task, must specify fileobj OR walker and path"""
        # pylint: disable=too-many-arguments
        super().__init__("upload")
        self.uploader = uploader
        self.audit_log = audit_log
        self.container = container
        self.filename = filename
        self.fileobj = UploadFileWrapper(fileobj=fileobj, walker=walker, path=path)
        self._data = None
        self.metadata = metadata
        self.deid_log = deid_log or {}

    def execute(self):
        self.fileobj.reset()

        # in case of FSWrapper uploader we don't have to generate deid log
        # hasattr to avoid circular import
        if hasattr(self.uploader, "fw") and self.deid_log:
            self.metadata["deid_log_id"] = self.uploader.fw.post_deid_log(self.deid_log)

        # Under 32 MB, just read the entire file
        if self.fileobj.len == 0:
            # Skip and log 0-byte files
            log.info(f"Skipping 0-byte file upload: {self.filename}")
            self.audit_log.add_log(
                self.fileobj.name,
                self.container,
                self.filename,
                failed=True,
                message="Skipped 0-byte file",
            )
            self.skipped = True
        elif self.fileobj.len < MAX_IN_MEMORY_XFER:
            if self._data is None:
                self._data = self.fileobj.read(self.fileobj.len)
            self.uploader.upload(
                self.container, self.filename, self._data, metadata=self.metadata
            )
        else:
            self.uploader.upload(
                self.container, self.filename, self.fileobj, metadata=self.metadata
            )

        # Safely close the file object
        try:
            self.fileobj.close()
        except IOError:
            log.exception("Cannot close file object")

        # No more tasks so no priority
        return None, None

    def get_bytes_processed(self):
        return self.fileobj.get_bytes_sent

    def get_desc(self):
        return f"Upload {self.filename}"


class PackfileTask(Task):
    """PackfileTask class"""

    def __init__(
        self,
        uploader,
        audit_log,
        walker,
        packfile_type,
        deid_profile,
        container,
        filename,
        subdir=None,
        paths=None,
        compression=None,
        max_spool=None,
    ):
        """Initialize a packfile upload task"""
        # pylint: disable=too-many-arguments
        super().__init__("packfile")

        self.uploader = uploader
        self.audit_log = audit_log
        self.walker = walker
        self.packfile_type = packfile_type
        self.deid_profile = deid_profile

        self.container = container
        self.filename = filename
        self.subdir = subdir
        self.paths = paths
        self.compression = compression
        self.max_spool = max_spool

        self._bytes_processed = None
        self._logged_error = False

    def execute(self):
        if self.max_spool:
            tmpfile = tempfile.SpooledTemporaryFile(max_size=self.max_spool)
        else:
            tmpfile = tempfile.TemporaryFile()

        deid_log = None
        # store the packfile path
        audit_path = None
        if self.subdir:
            audit_path = self.subdir
        elif self.paths:
            audit_path = os.path.dirname(self.paths[0])
        else:
            audit_path = self.walker.get_fs_url()

        try:
            create_deid_log = hasattr(self.uploader, "fw") and self.uploader.fw.deid_log
            zip_member_count, deid_log = create_zip_packfile(
                tmpfile,
                self.walker,
                packfile_type=self.packfile_type,
                subdir=self.subdir,
                paths=self.paths,
                compression=self.compression,
                progress_callback=self.update_bytes_processed,
                deid_profile=self.deid_profile,
                create_deid_log=create_deid_log,
            )
        except Exception as exc:
            log.debug(f"Error processing packfile at {audit_path}", exc_info=True)
            if not self._logged_error:
                message = f"Error creating packfile: {exc}"
                self.audit_log.add_log(
                    audit_path,
                    self.container,
                    self.filename,
                    failed=True,
                    message=message,
                )
                self._logged_error = True
            raise

        # Rewind
        tmpfile.seek(0)

        # Remove walker reference
        self.walker = None

        metadata = {
            "name": self.filename,
            "zip_member_count": zip_member_count,
            "type": self.packfile_type,
        }

        # The next task is an uplad task
        next_task = UploadTask(
            self.uploader,
            self.audit_log,
            self.container,
            self.filename,
            fileobj=tmpfile,
            metadata=metadata,
            path=audit_path,
            deid_log=deid_log,
        )

        # Enqueue with higher priority than normal uploads
        return (next_task, 5)

    def get_bytes_processed(self):
        if self._bytes_processed is None:
            return 0
        return self._bytes_processed

    def get_desc(self):
        return f"Pack {self.filename}"

    def update_bytes_processed(self, bytes_processed):
        """Update processed bytes"""
        self._bytes_processed = bytes_processed


class UploadQueue(WorkQueue):
    """UploadQueue class"""

    def __init__(
        self, config, audit_log, packfile_count=0, upload_count=0, show_progress=True
    ):
        """Detect signed-url upload and start multiple upload threads"""
        upload_threads = 1
        uploader = config.get_uploader()
        if uploader.supports_signed_url():
            upload_threads = config.concurrent_uploads

        super().__init__({"upload": upload_threads, "packfile": config.cpu_count})

        self.uploader = uploader
        self.compression = config.get_compression_type()
        self.max_spool = config.max_spool
        self.audit_log = audit_log

        self.skip_existing = config.skip_existing_files

        self._progress_thread = None
        if show_progress:
            self._progress_thread = ProgressReporter(self)
            self._progress_thread.log_process_info(
                config.cpu_count, upload_threads, packfile_count
            )
            self._progress_thread.add_group("packfile", "Packing", packfile_count)
            self._progress_thread.add_group(
                "upload", self.uploader.verb, upload_count + packfile_count
            )

    def start(self):
        super().start()

        # make sure audit log is written
        self.audit_log.start_writing_file()

        if self._progress_thread:
            self._progress_thread.start()

    def add_audit_log(self, task, failed=False, message=None):
        """Add audit log, if this is not a packfile task"""
        if not isinstance(task, PackfileTask):
            self.audit_log.add_log(
                task.fileobj.name,
                task.container,
                task.filename,
                failed=failed,
                message=message,
            )

    def complete(self, task):
        if not task.skipped:
            self.add_audit_log(task)
        super().complete(task)

    def shutdown(self):
        # Shutdown reporting thread
        if self._progress_thread:
            self._progress_thread.shutdown()
            self._progress_thread.final_report()

        super().shutdown()

    def suspend_reporting(self):
        """Suspend reporting"""
        if self._progress_thread:
            self._progress_thread.suspend()

    def resume_reporting(self):
        """Resume reporting"""
        if self._progress_thread:
            self._progress_thread.resume()

    def error(self, task):
        self.add_audit_log(task, failed=True, message="Upload error")
        super().error(task)

    def log_exception(self, task, exc_info):
        self.suspend_reporting()

        super().log_exception(task, exc_info)

        self.resume_reporting()

    def upload(self, container, filename, fileobj):
        """Enque UploadTask or skip file"""
        if self.skip_existing and self.uploader.file_exists(container, filename):
            log.debug(
                f'Skipping existing file "{filename}" on {container.container_type} {container.id}'
            )
            self.skip_task(group="upload")
            self.audit_log.add_log(
                fileobj.name, container, filename, message="Skipped existing"
            )
            return

        self.enqueue(
            UploadTask(
                self.uploader, self.audit_log, container, filename, fileobj=fileobj
            )
        )

    def upload_file(self, container, filename, walker, path):
        """Enque UploadTask or skip file"""
        if self.skip_existing and self.uploader.file_exists(container, filename):
            log.debug(
                f'Skipping existing file "{filename}" on {container.container_type} {container.id}'
            )
            self.skip_task(group="upload")
            self.audit_log.add_log(
                path, container, filename, message="Skipped existing"
            )
            return

        self.enqueue(
            UploadTask(
                self.uploader,
                self.audit_log,
                container,
                filename,
                walker=walker,
                path=path,
            )
        )

    def upload_packfile(
        self,
        walker,
        packfile_type,
        deid_profile,
        container,
        filename,
        subdir=None,
        paths=None,
    ):
        """Enque PackfileTask or skip packfile"""
        if self.skip_existing and self.uploader.file_exists(container, filename):
            log.debug(
                f'Skipping existing packfile "{filename}" on {container.container_type} {container.id}'
            )
            self.skip_task(group="upload")
            self.skip_task(group="packfile")
            if paths:
                self.audit_log.add_log(
                    paths[0], container, filename, message="Skipped existing"
                )
            return

        self.enqueue(
            PackfileTask(
                self.uploader,
                self.audit_log,
                walker,
                packfile_type,
                deid_profile,
                container,
                filename,
                subdir=subdir,
                paths=paths,
                compression=self.compression,
                max_spool=self.max_spool,
            )
        )
