# -*- coding: utf-8 -*-
import yaml
import json
import os

from .keywordgroup import KeywordGroup

class _Configuration(KeywordGroup):

    # Public
    def get_mass(self):
        """Get the default test data of the project: mass.yaml."""
        sources = {}
        for path in os.walk("./resources/fixtures"):
            for f in path[2]:
                if  "yaml" in f or "yml" in f:
                    sources[f] = self.yaml_to_python((path[0] + "/" + f).replace("\\", "/"))
                elif "json" in f:
                    sources[f] = self.json_to_python((path[0] + "/" + f).replace("\\", "/"))
        mass = {}
        for key, value in sources.items():
            if value is not None:
                for key, value in value.items():
                    mass[key] = value
        return mass


    def get_env(self):
        """Get the default environment values of the project: environment.yaml."""
        return self.yaml_to_python("./resources/config/environment.yaml")


    def get_config(self):
        """Get the default configuration options of the project: config.yaml."""
        return self.yaml_to_python("./resources/config/config.yaml")


    def get_profiles(self):
        """Get the profiles options of the project: profiles.yaml."""
        return self.yaml_to_python("./profiles.yaml")


    def yaml_to_python(self, path):
        """Parse a yml file to a python dictionary object.

        Arguments:
            - path: Absolut or relative path of the yml file.

        Examples:
        | Yaml To Python | "./resources/fixtures/mass.yaml" |

        =>

        | Python dictionary object. |
        """
        with open(path, 'r') as stream:
            try:
                return yaml.load(stream, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(exc)

    def python_to_json(self, value):
        """Converts a python dict to a json object

        Arguments:
            - value: python dictionary
        """
        return json.dumps(value)

    def json_to_python(self, path):
        """Converts a json object to a python dictionary

        Arguments:
            - - path: Absolut or relative path of the yml file.
        """
        with open(path, 'r') as stream:
            return json.load(stream)
