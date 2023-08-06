from argparse import Namespace, ArgumentParser
from logging import Logger
from box import Box
from gen2aclbundle.acl.check.AclChecker import AclChecker
from consolebundle.ConsoleCommand import ConsoleCommand


class AclCheckCommand(ConsoleCommand):
    def __init__(
        self,
        storages: Box,
        logger: Logger,
        acl_checker: AclChecker,
    ):
        self.__storages = storages
        self.__logger = logger
        self.__acl_checker = acl_checker

    def get_command(self) -> str:
        return "gen2datalake:acl:check"

    def get_description(self):
        return "Checks setting of Filesystem and Folders and compares it against definition in YAML."

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("filesystem", help="filesystem name")
        argument_parser.add_argument("path", help="relative path to stored YAML (not a filename)")

    def run(self, input_args: Namespace):
        self.__logger.info("Checking ACL in filesystem")

        storage = list(filter(lambda storage: storage["filesystem"] == input_args.filesystem, self.__storages))[0]

        self.__acl_checker.check(storage["filesystem"], input_args.path)

        self.__logger.info("ACL check done")
