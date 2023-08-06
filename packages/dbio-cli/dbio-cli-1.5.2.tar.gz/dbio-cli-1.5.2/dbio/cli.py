# coding: utf-8
"""
Human Cell Atlas Command Line Interface

For general help, run ``{prog} help``.
For help with individual commands, run ``{prog} <command> --help``.
"""
import os
import sys
import argparse
import logging
import json
import datetime
import traceback
import platform
import argcomplete
from io import open
from botocore.exceptions import NoRegionError
import xmlrpc.client as xmlrpclib

from .version import __version__
from .dss import cli as dss_cli
from .auth import cli as auth_cli
from . import logger, get_config, clear_dbio_cache


class DataBiosphereArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        argparse.ArgumentParser.__init__(self, *args, **kwargs)
        self._subparsers = None

    def add_parser_func(self, func, **kwargs):
        if self._subparsers is None:
            self._subparsers = self.add_subparsers()
        subparser = self._subparsers.add_parser(func.__name__.replace("_", "-"), **kwargs)
        subparser.set_defaults(entry_point=func)
        command = subparser.prog[len(self.prog) + 1:].replace("-", "_").replace(" ", "_")
        subparser.set_defaults(**get_config().get(command, {}))
        if subparser.description is None:
            subparser.description = kwargs.get("help", func.__doc__)
        self._defaults.pop("entry_point", None)
        return subparser

    def print_help(self, file=None):
        formatted_help = self.format_help()
        formatted_help = formatted_help.replace('positional arguments:', 'Positional Arguments:')
        formatted_help = formatted_help.replace('optional arguments:', 'Optional Arguments:')
        formatted_help = formatted_help.replace('{prog}', 'dbio')  # not converted from the swagger proper
        print(formatted_help)
        self.exit()


def check_if_release_is_current(log):
    """Warns the user if their release is behind the latest PyPi __version__."""
    if __version__.endswith('dev'):
        return
    client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
    latest_pypi_version = client.package_releases('dbio')

    latest_version_nums = [int(i) for i in latest_pypi_version[0].split('.')]
    this_version_nums = [int(i) for i in __version__.split('.')]
    for i in range(max([len(latest_version_nums), len(this_version_nums)])):
        try:
            if this_version_nums[i] < latest_version_nums[i]:
                log.warning('WARNING: Python (pip) package "dbio" is not up-to-date!\n'
                            'You have dbio version:              ' + str(__version__) + '\n'
                            'Please use the latest dbioversion:  ' + str(latest_pypi_version[0]))
            # handles the odd case where a user's current __version__ is higher than PyPi's
            elif this_version_nums[i] > latest_version_nums[i]:
                break
        # if 4.2 compared to 4.3.1, this handles the missing element
        except IndexError:
            pass


def get_parser(help_menu=False):
    parser = DataBiosphereArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    version_string = "%(prog)s {version} ({python_impl} {python_version} {platform})"
    parser.add_argument("--version", action="version", version=version_string.format(
        version=__version__,
        python_impl=platform.python_implementation(),
        python_version=platform.python_version(),
        platform=platform.platform()
    ))
    parser.add_argument("--log-level", default=get_config().get("log_level"),
                        help=str([logging.getLevelName(i) for i in range(10, 60, 10)]),
                        choices={logging.getLevelName(i) for i in range(10, 60, 10)})
    parser.add_parser_func(clear_dbio_cache, help=clear_dbio_cache.__doc__)

    def help(args):
        """Print help message"""
        parser.print_help()

    parser.add_parser_func(help)

    dss_cli.add_commands(parser._subparsers, help_menu=help_menu)
    auth_cli.add_commands(parser._subparsers, help_menu=help_menu)

    argcomplete.autocomplete(parser)
    return parser


def main(args=None):
    if not args:
        args = sys.argv[1:]
    if '--help' in args or '-h' in args:
        parser = get_parser(help_menu=True)
    else:
        parser = get_parser()

    if len(args) < 1:
        parser.print_help()
        parser.exit(1)

    parsed_args = parser.parse_args(args=args)
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(parsed_args.log_level)

    logging.getLogger("urllib3").setLevel(parsed_args.log_level)
    logging.getLogger("requests").setLevel(parsed_args.log_level)

    # TODO: Disable when called as a service (i.e. GOOGLE_APPLICATION_CREDENTIALS is set)
    # This caused some slowdown on the query-service and needs to be fixed
    # A good pattern for this is to write the last time that the version was checked into the config.
    # *If the config is writable* (not on a read only filesystem), *and* the check was last done more than
    # T seconds ago (e.g. 1 week ago), *then* perform a check.
    # check_if_release_is_current(logger)  # warns the user

    try:
        result = parsed_args.entry_point(parsed_args)
    except Exception as e:
        if isinstance(e, NoRegionError):
            msg = "The AWS CLI is not configured."
            msg += " Please configure it using instructions at"
            msg += " http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html"
            exit(msg)
        elif logger.level < logging.ERROR:
            raise
        else:
            err_msg = traceback.format_exc()
            try:
                err_log_filename = os.path.join(get_config().user_config_dir, "error.log")
                with open(err_log_filename, "ab") as fh:
                    print(datetime.datetime.now().isoformat(), file=fh)  # noqa
                    print(err_msg, file=fh)
                exit("{}: {}. See {} for error details.".format(e.__class__.__name__, e, err_log_filename))
            except Exception:
                print(err_msg, file=sys.stderr)
                exit(os.EX_SOFTWARE)
    if isinstance(result, SystemExit):
        raise result
    elif result is not None:
        if isinstance(result, bytes):
            sys.stdout.buffer.write(result)
        else:
            print(json.dumps(result, indent=2, default=lambda x: str(x)))
