"""Show Gears"""
import sys

from ...exchange import GearExchangeDB, gear_detail_str


def add_command(subparsers):
    """Adds gear show commands"""
    parser = subparsers.add_parser(
        "show", help="Show details about a gear on the exchange"
    )
    parser.add_argument("name", help="The name of the gear to show")
    parser.add_argument("version", nargs="?", help="The version of the gear to show")

    parser.set_defaults(func=show_gear)
    parser.set_defaults(parser=parser)

    return parser


def show_gear(args):
    """Show gear"""
    db = GearExchangeDB()
    db.update()

    if args.version:
        gear_doc = db.find_version(args.name, args.version)
    else:
        gear_doc = db.find_latest(args.name)

    if not gear_doc:
        print(f"Could not find {args.name}")
        sys.exit(1)

    print(gear_detail_str(gear_doc))
