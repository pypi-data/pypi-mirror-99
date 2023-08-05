"""Add support for Consul backups on backwork.
"""

import argparse
import time
import logging
import os
import subprocess
import urllib
from urllib.parse import urlparse, quote

LOG = logging.getLogger(__name__)


class ConsulBackup(object):
    """Backup a Consul cluster.

    It uses `consul` so it's required to have it installed and added to the
    system's PATH. You can use any of the arguments supported by `consul snapshot save`.
    Use `consul snapshot save --help` for more information.
    """

    command = "consul"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.result = ""

    @classmethod
    def parse_args(cls, subparsers):
        """Create the `consul` subparser for the `backup` command."""
        consul_parser = subparsers.add_parser(cls.command, description=cls.__doc__)
        consul_parser.add_argument("file", nargs="?", help="output snapshot file name")

    def backup(self):
        """Backup a Consul cluster.

        If no positional argument is specified it will
        run `consul snapshot save` and store it into
        `./dumps` with a timestamped name.
        """
        LOG.info("starting consul backup...")

        snapshot_path = (
            os.path.abspath(os.path.join(os.getcwd(), self.args.file))
            if self.args.file
            else os.path.join(
                os.getcwd(),
                "dumps",
                "consul_backup_{}.snap".format(time.strftime("%Y%m%d-%H%M%S")),
            )
        )

        LOG.info("saving file to %s", snapshot_path)

        cmd = ["consul", "snapshot", "save", snapshot_path, *self.extra]

        try:
            self.result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            LOG.info("\n\n" + self.result.decode("utf-8"))
            LOG.info("backup complete")

        except subprocess.CalledProcessError as error:
            self.result = error.output
            LOG.error("failed to back up consul cluster")
            LOG.error("return code was %s", error.returncode)
            LOG.error("\n\n" + self.result.decode("utf-8"))
            LOG.error("backup process failed")
            raise error


class ConsulRestore(object):
    """Restore a Consul cluster.

    Restore a Consul cluster. It uses `consul` so it's required to have it
    installed and added to the system's PATH. You can use any of the arguments
    supported by `consul snapshot restore`. Use `consul snapshot restore --help` for more information.
    """

    command = "consul"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.result = ""

    @classmethod
    def parse_args(cls, subparsers):
        """Create the `consul` subparser for the `backup` command."""
        consul_parser = subparsers.add_parser(cls.command, description=cls.__doc__)
        consul_parser.add_argument("file", help="input snapshot file name")

    def restore(self):
        """Restore a Consul cluster."""
        LOG.info("starting consul restore...")
        raise NotImplemented("Consult restore is not supported.")
