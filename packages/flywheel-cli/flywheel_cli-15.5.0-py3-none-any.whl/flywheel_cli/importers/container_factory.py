"""Provides interface for container creation"""
import collections
import copy
import logging
import sys
from abc import ABC, abstractmethod

from .. import util

CONTAINERS = ["group", "project", "subject", "session", "acquisition"]
UID_CONTAINERS = {"acquisition": "acquisitions", "session": "sessions"}

log = logging.getLogger(__name__)


class ContainerNode:
    """Container node class"""

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        container_type,
        cid=None,
        label=None,
        uid=None,
        parent=None,
        exists=False,
        context=None,
    ):
        self.container_type = container_type
        self.id = cid  # pylint: disable=invalid-name
        self.uid = uid
        self.children = []
        self.exists = exists
        self.parent = parent
        self.files = []
        self.packfiles = []

        # property fields
        self._context = None
        self._label = None

        self.context = context
        self.label = label

    @property
    def context(self):
        """Context getter"""
        return self._context

    @context.setter
    def context(self, val):
        """Context setter that sanitize the label in it if present"""
        self._context = copy.deepcopy(val)
        if self._context and "label" in self._context:
            self._context["label"] = util.sanitize_filename(self._context["label"])

    @property
    def label(self):
        """Label getter"""
        return self._label

    @label.setter
    def label(self, val):
        """Label setter that sanitize the value"""
        self._label = util.sanitize_filename(val)


class ContainerResolver(ABC):
    """Container resolver class"""

    @staticmethod
    def path_el(container):
        """Get the path element for container"""
        if container.container_type == "group":
            return container.id
        if container.id:
            return f"<id:{container.id}>"
        if not container.label:
            log.error(f"Could not determine {container.container_type}")
            sys.exit(1)
        return container.label

    @abstractmethod
    def resolve_path(self, container_type, path):
        """Resolve a container id by path

        Arguments:
            container_type (str): The container type hint
            path (str): The resolver path

        Returns:
            str, str: The id and uid if the container exists, otherwise None
        """

    def resolve_children(self, container_type, path):
        """Return the child nodes of a container

        Arguments:
            container_type (str): The container type hint
            path (str): The resolver path

        Returns:
            list(dict): A list of child containers
        """
        raise NotImplementedError()

    @abstractmethod
    def create_container(self, parent, container):
        """Create the container described by container as a child of parent.

        Arguments:
            parent (ContainerNode): The parent container (or None if creating a group)
            container (ContainerNode): The container to create

        Returns:
            str: The id of the newly created container
        """

    @abstractmethod
    def check_unique_uids(self, request):
        """Given a dictionary of uids by container type, check which are unique

        Arguments:
            request (dict): The dictionary of UIDs to check

        Returns:
            dict: The subset of UIDs that are not unique
        """


class ContainerFactory:
    """Container factory class"""

    def __init__(self, resolver, uids=True):
        """Manages discovery and creation of containers by looking at context objects.

        Arguments:
            resolver (ContainerResolver): The container resolver strategy
        """
        self.resolver = resolver
        self.uids = uids

        # The root container
        self.root = ContainerNode("root", exists=True)

    def is_empty(self):
        """Check if any nodes have been added to the root node"""
        return not bool(self.root.children)

    def resolve(self, context, create=True):
        """Given a context with hierarchy definitions, returns a ContainerNode if resolved.

        If the node definition is ambiguous (i.e. missing an intermediate level such as project), then this
        function returns None. This is fine if there is nothing to upload at the given node.

        Arguments:
            context (dict): The context containing the node definition
            create (bool): Whether or not to create the container if it doesn't exist

        Returns:
            ContainerNode: If the container node was resolved in the tree.
        """
        # Create containers as we go
        last = None
        current = self.root
        path = []
        for container in CONTAINERS:
            if container in context:
                # Missing node, return None
                if current is None:
                    return None

                last = current
                current = self._resolve_child(current, container, context, path, create)
                if current is None:
                    return None
                path.append(self.resolver.path_el(current))
            else:
                if current:
                    last = current
                current = None

        return current or last

    def create_containers(self):
        """Invoke resolver.create_container for each container that doesn't exist"""
        for parent, child in self.walk_containers():
            if not child.exists:
                child.id = self.resolver.create_container(parent, child)
                child.exists = True

    def walk_containers(self):
        """Breadth-first walk of containers resolved by this factory

        Yields:
            ContainerNode, ContainerNode: parent, child container nodes
        """
        queue = collections.deque()
        for child in self.root.children:
            queue.append((None, child))

        while queue:
            parent, current = queue.popleft()

            for child in current.children:
                queue.append((current, child))

            yield parent, current

    def get_groups(self):
        """Get the top-level groups in the hierarchy

        Returns:
            list: The list of group nodes
        """
        return self.root.children

    def get_first_project(self):
        """Get the first project in the hierarchy.

        Returns:
            ContainerNode: The first project node, or None
        """
        groups = self.root.children
        if not groups:
            return None
        projects = groups[0].children
        if not projects:
            return None
        return projects[0]

    def check_container_unique_uids(self):
        """Check for unique uids in sessions and acquisitions.

        Returns:
            tuple(int, list): The number of containers with UIDs, and a list
                              of containers with non-unique UIDs.
        """
        uid_count = 0
        uid_check_containers = {}
        conflict_containers = []

        for _, container in self.walk_containers():
            uid = getattr(container, "uid", None)
            if not uid:
                continue

            collection_name = UID_CONTAINERS.get(container.container_type)
            if collection_name is None:
                continue

            uid_count += 1
            uid_map = uid_check_containers.setdefault(collection_name, {})
            if uid in uid_map:
                conflict_containers.append(container)
                continue

            uid_map[uid] = container

        # Invoke the UID check API
        log.debug(f"Checking {uid_count} UIDs")
        if uid_count:
            # Convert into a check UIDs request
            uid_request = {}
            for key, uid_map in uid_check_containers.items():
                uid_request[key] = list(uid_map.keys())

            log.debug(f"check_unique_uids, request={uid_request}")
            result = self.resolver.check_unique_uids(uid_request)
            log.debug(f"check_unique_uids, result={result}")

            for key, uid_list in result.items():
                uid_map = uid_check_containers.get(key, {})
                for uid in uid_list:
                    conflict_containers.append(uid_map[uid])

        return uid_count, conflict_containers

    def _resolve_child(self, parent, container_type, context, path, create):
        """Resolve a child by searching the parent, or creating a new node

        Arguments:
            parent (ContainerNode): The parent node
            container_type (str): The container type
            context (dict): The context object
            create (bool): Whether or not to create missing nodes

        Returns:
            ContainerNode: The new or existing container node
        """
        subcon = context[container_type]
        cid = subcon.get("_id")
        uid = subcon.get("uid")
        label = util.sanitize_filename(subcon.get("label"))

        for child in parent.children:
            # Prefer resolve by id
            if cid and child.id == cid:
                return child

            if label and child.label == label:
                if not self.uids or not child.uid or child.uid == uid:
                    # In case we resolved this elsewhere, update the child id
                    if cid and not child.id:
                        child.id = cid

                    if uid and not child.uid:
                        child.uid = uid

                    return child

        if not create:
            return None

        self._validate_container(cid, uid, label, container_type)

        # Create child
        child = ContainerNode(
            container_type, cid=cid, label=label, uid=uid, parent=parent, context=subcon
        )

        # Check if exists
        if self.resolver and parent.exists:
            # Try to resolve and scan children first
            target = None
            children = []
            if child.uid and self.uids:
                children = self._resolve_children(container_type, path)
                target = self.find_child_by_uid(child, children)

            # resolve by label if child does not have uid or self.uids is false
            if target is None and not (child.uid and self.uids):
                target = self._find_child_by_label(
                    child, container_type, path, children
                )

            if target:
                child.id, child.uid, child.label = target
                child.exists = True

        parent.children.append(child)
        return child

    @staticmethod
    def _validate_container(cid, uid, label, container_type):
        """Validate the container before creation"""
        if not any((cid, uid, label)):
            raise ValueError(
                f"Couldn't create {container_type} container because missing all of (id, uid, label)"
            )

        if (
            container_type
            in [
                "project",
                "session",
                "acquisition",
            ]
            and not label
        ):
            raise ValueError(
                f"Couldn't create {container_type} container because it does not have a label"
            )

    def _resolve_children(self, container_type, path):
        """Attempt to resolve child containers for a given path"""
        try:
            return self.resolver.resolve_children(container_type, path)
        except NotImplementedError:
            return []

    def _find_child_by_label(self, child, container_type, path, children):
        """Attempt to find the child by label"""
        if children:
            for container in children:
                if container.label == child.label:
                    return container.id, container.uid, container.label
        else:
            child_path = [*path, self.resolver.path_el(child)]
            cid, uid = self.resolver.resolve_path(container_type, child_path)
            if cid:
                return cid, uid, child.label
        return None

    @staticmethod
    def find_child_by_uid(child, children):
        """Attempt to find the child by uid"""
        for container in children:
            if container.uid == child.uid:
                return container.id, container.uid, container.label
        return None
