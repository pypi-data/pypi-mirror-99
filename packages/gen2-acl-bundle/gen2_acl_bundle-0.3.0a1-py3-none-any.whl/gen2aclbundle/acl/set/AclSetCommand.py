from argparse import Namespace, ArgumentParser
from logging import Logger
from box import Box
from consolebundle.ConsoleCommand import ConsoleCommand
from gen2aclbundle.acl.set.AclSetter import AclSetter


class AclSetCommand(ConsoleCommand):
    def __init__(
        self,
        storages: Box,
        logger: Logger,
        acl_setter: AclSetter,
    ):
        self.__storages = storages
        self.__logger = logger
        self.__acl_setter = acl_setter

    def get_command(self) -> str:
        return "gen2datalake:acl:set"

    def get_description(self):
        return "Sets ACL permissions defined in YAML config to given GEN2 DataLake"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("filesystem", help="filesystem name")
        argument_parser.add_argument("path", help="relative path to stored YAML (not a filename)")

    def run(self, input_args: Namespace):
        self.__logger.info("Setting ACL to filesystem...")

        storage = list(filter(lambda storage: storage["filesystem"] == input_args.filesystem, self.__storages))[0]

        self.__acl_setter.set(storage["filesystem"], input_args.path)
