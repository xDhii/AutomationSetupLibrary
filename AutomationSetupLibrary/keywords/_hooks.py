# -*- coding: utf-8 -*-
from ._configuration import _Configuration
from .keywordgroup import KeywordGroup
from robot.libraries.BuiltIn import BuiltIn
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from selenium import webdriver
from robot.api import logger
from pathlib import Path
import os

class _Hooks(KeywordGroup):

    def __init__(self):
        self.builtin = BuiltIn()
        self.configuration = _Configuration()

    @property
    def user_home_path(self):
        return self.__home

    @user_home_path.setter
    def user_home_path(self, home):
        self.__home = home
        self.builtin.set_global_variable("${USER_HOME_PATH}", self.__home.replace("\\", "\\\\"))

    @property
    def selib(self):
        return self.builtin.get_library_instance('SeleniumLibrary')

    @property
    def mass(self):
        return self.__mass

    @mass.setter
    def mass(self, value):
        self.builtin.set_global_variable("${MASS}", value)
        self.__mass = value

    @property
    def env(self):
        return self.__env

    @env.setter
    def env(self, value):
        self.builtin.set_global_variable("${ENV}", value)
        self.__env = value

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        self.builtin.set_global_variable("${CONFIG}", value)
        self.__config = value

    @property
    def browser(self):
        return self.__browser

    @browser.setter
    def browser(self, value):
        r = self.builtin.get_variable_value("${BROWSER}", value)
        self.config["browser"] = r
        self.__browser = r

    @property
    def headless(self):
        return self.__headless

    @headless.setter
    def headless(self, value):
        r = self.builtin.get_variable_value("${HEADLESS}", value)
        self.config["headless"] = r
        self.__headless = r

    @property
    def run_env(self):
        return self.__run_env

    @run_env.setter
    def run_env(self, value):
        r = self.builtin.get_variable_value("${ENV_NAME}", value)
        self.config["run_env"] = r
        self.__run_env = r

    @property
    def download_folder(self):
        return self.__download_folder

    @download_folder.setter
    def download_folder(self, folder="SVR"):
        path = self.user_home_path
        self.builtin.set_global_variable("${DOWNLOAD_FOLDER}", folder)
        f = self.builtin.get_variable_value("${DOWNLOAD_FOLDER}", folder)
        self.__download_folder = path + "\\Downloads\\" + f

        if not os.path.isdir(self.__download_folder):
            try:
                logger.console("Creating %s download folder..." % folder)
                os.mkdir(self.__download_folder)
                logger.console("%s download folder created!!" % folder)
            except:
                logger.console("We are not able to create %s folder!!" % folder)

        self.config["download_dir"] = self.__download_folder
        return self.__download_folder

    def __start_environment(self, config):
        """Starts the automation environment (choosing and openning the webdriver browser)

        Arguments:
            - config: python dictionary of configuration
        """
        self.browser = config["browser"]
        if   (self.browser == "chrome"):
            self.chrome(config)
        elif (self.browser == "firefox"):
            self.firefox(config)
        elif (self.browser == "ie"):
            self.ie(config)
        elif (self.browser == "remote"):
            self.remote(config)

        if (self.headless == False):
            self.selib.maximize_browser_window()

        self.selib.go_to("about:blank")


    # Public
    def start_automation(self):
        """Performs the default initial configuration for running test automation
        Using the architecture designed for test automation.
        """
        logger.console('Setting global variables...')


        self.mass = self.configuration.get_mass()
        self.env = self.configuration.get_env()
        self.config = self.configuration.get_config()
        self.run_env = self.config['run_env'].upper()
        self.headless = self.config['headless']
        self.user_home_path = str(Path.home())
        self.download_folder = self.config['download_dir']

        logger.console('Starting automation')
        self.__start_environment(self.config)

        self.selib.go_to(self.env[self.run_env]["root"])
        logger.console('...Done initial configuration')


    def enable_download_in_headless_chrome(self):
        """ Enables Download on Headless Chrome """
        logger.console('Getting SeleniumLibrary Instance')
        instance = self.selib
        driver = instance.driver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {
            'cmd': 'Page.setDownloadBehavior',
            'params': {
                'behavior': 'allow',
                'downloadPath': self.download_folder
            }
        }
        driver.execute("send_command", params)

    def chrome(self, config):
        """Creates the selenium chromedriver

        Arguments:
            - config: python dictionary of configuration
        """
        executable_path = ChromeDriverManager().install()
        chrome_options = webdriver.ChromeOptions()
        if (self.headless == True) or (self.headless == "True"):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--no-sandbox')

            prefs = {
                "download.default_directory": self.download_folder,
                "download.prompt_for_download": False
            }

            chrome_options.add_experimental_option("prefs", prefs)

        args = {
            "executable_path": executable_path,
            "chrome_options": chrome_options
        }
        index = self.selib.create_webdriver("Chrome", kwargs=args)
        self.enable_download_in_headless_chrome()
        return index


    def firefox(self, config):
        """Creates the selenium geckodriver

        Arguments:
            - config: python dictionary of configuration
        """
        executable_path = GeckoDriverManager().install()
        args = {"executable_path": executable_path}
        return self.selib.create_webdriver("Firefox", kwargs=args)


    def ie(self, config):
        """Creates the selenium iedriver

        Arguments:
            - config: python dictionary of configuration
        """
        executable_path = IEDriverManager().install()
        args = {"executable_path": executable_path}
        return self.selib.create_webdriver("Ie", kwargs=args)


    def remote(self, config):
        """Creates the selenium remote driver

        Arguments:
            - config: python dictionary of configuration
        """
        return self.selib.create_webdriver("Remote")


    def after_suite(self):
        """Performs the default configuration at the end of all test executions."""
        logger.console('Closing browser...')
        self.selib.close_browser()
        logger.console('Bye Bye!!!')
