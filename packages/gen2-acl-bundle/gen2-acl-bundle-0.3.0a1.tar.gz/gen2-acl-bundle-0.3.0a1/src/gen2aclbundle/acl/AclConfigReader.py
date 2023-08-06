from injecta.parameter.ParametersParser import ParametersParser
import yaml


class AclConfigReader:
    def read_config(self, yaml_path: str):
        parsed_yaml_config = yaml.safe_load(self.__read_yaml(yaml_path))
        config = ParametersParser().parse(parsed_yaml_config)
        return config

    def __read_yaml(self, file_path: str):
        yml_file = open(file_path, "r")
        yaml_text = yml_file.read()
        yml_file.close()
        return yaml_text
