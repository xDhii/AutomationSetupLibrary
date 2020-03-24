from .keywordgroup import KeywordGroup
from ._configuration import _Configuration
from robot.api import logger
import os
import errno


class _Tasks(KeywordGroup):
    @property
    def robot_options(self):
        return self.__robot_options

    @robot_options.setter
    def robot_options(self, value):
        options = _Configuration().get_profiles()["profiles"]
        python_path = " "
        for path in os.walk("./resources/pages"):
            if not "pycache" in path[0]:
                p = path[0].replace("./", "").replace("\\", "/")
                if not p in options[value]["robot_options"]:
                    python_path += "-P " + p + " "

        if (value == "default"):
            r = options[value]["robot_options"] + python_path
        else:
            r = options["default"]["robot_options"] + \
                python_path + options[value]["robot_options"]
        self.__robot_options = r

    @property
    def rebot_options(self):
        return self.__rebot_options

    @rebot_options.setter
    def rebot_options(self, value):
        options = _Configuration().get_profiles()["profiles"]
        if (value == "default"):
            r = options[value]["rebot_options"]
        else:
            r = options["default"]["rebot_options"] + \
                options[value]["rebot_options"]
        self.__rebot_options = r

    def create_dir(self, dirName):
        """Creates a directory if it doesn't exist

        Arguments:
            - dirName: Path to create the directory
        """
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory ", dirName,  " Created ")
        else:
            print("Directory ", dirName,  " already exists")

    def create_file(self, dirName, content):
        """Creates a file with some content if the file doesn't exist

        Arguments:
            - dirName: Path to create the directory
            - content: Content to the file
        """
        if not(os.path.exists(dirName)):
            fd = open(dirName, 'w')
            fd.write(content)
            fd.close()

    def create_workspace(self):
        """Creates the default workspace for any project / Check if the project workspace has all the needed artifacts"""
        profile = "profiles:\n  default:\n    robot_options: '-d results -P resources/pages'\n    rebot_options: ''"
        index = "*** Settings ***\nLibrary     PageObjectLibrary\nLibrary     SeleniumLibrary\nLibrary     AutomationSetupLibrary"
        config = "browser: 'chrome'\nremote: False\nheadless: True\ndefault_max_wait_time: 10\nrun_env: 'QA2'"
        self.create_dir("resources")
        self.create_dir("resources/support")
        self.create_dir("resources/fixtures")
        self.create_dir("resources/config")
        self.create_dir("resources/keywords")
        self.create_dir("resources/pages")
        self.create_dir("resources/lib")
        self.create_dir("tests")
        self.create_file("profiles.yaml", profile)
        self.create_file("resources/support/index.robot", index)
        self.create_file("resources/config/config.yaml", config)
        self.create_file("resources/config/environment.yaml", "")
        self.create_file("resources/fixtures/mass.yaml", "")
