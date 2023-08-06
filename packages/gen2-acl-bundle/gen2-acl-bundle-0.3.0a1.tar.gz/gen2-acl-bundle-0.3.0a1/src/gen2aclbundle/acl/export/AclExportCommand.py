from argparse import Namespace, ArgumentParser
from logging import Logger
from box import Box
from consolebundle.ConsoleCommand import ConsoleCommand
from gen2aclbundle.acl.export.AclExporter import AclExporter


class AclExportCommand(ConsoleCommand):
    def __init__(
        self,
        storages: Box,
        logger: Logger,
        acl_exporter: AclExporter,
    ):
        self.__storages = storages
        self.__logger = logger
        self.__acl_exporter = acl_exporter

    def get_command(self) -> str:
        return "gen2datalake:acl:export"

    def get_description(self):
        return "Exports ACL settings of given Azure Storage to YAML file"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("filesystem", help="filesystem name")
        argument_parser.add_argument("path", help="relative path to store data")

    def run(self, input_args: Namespace):
        self.__logger.info("Exporting ACL...")

        storage = list(filter(lambda storage: storage["filesystem"] == input_args.filesystem, self.__storages))[0]

        self.__acl_exporter.export(storage["filesystem"], storage["max_level"], input_args.path)
