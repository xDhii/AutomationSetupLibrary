from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from .keywordgroup import KeywordGroup

import os

class _SelibKeywords(KeywordGroup):

    def __init__(self):
        self.builtin = BuiltIn()

    @property
    def curdir(self):
        return os.getcwd()

    @property
    def selib(self):
        return BuiltIn().get_library_instance("SeleniumLibrary")

    def wait_for_keyword(self, keyword, *args, retry="7x", interval="3s"):
        """Executes a given keyword until it pass or fail in the range of wait time

        Arguments:
            - keyword: robot keyword to be executed. Can be any keyword from the project or any library keyword (String)
            - args: list of arguments that the keyword given needs
            - (optional) retry: time or times that it should try again and execute the keyword. For usage see BuiltIn
            documentation
            - (optional) interval: interval of time that it wait to try again and execute the keyword. For usage see
            BuiltIn documentation

        Examples:
        | wait for keyword | "click element" | id=element |
        | wait for keyword | "click element" | id=element | retry=10x | interval=10s |
        """
        self.builtin.wait_until_keyword_succeeds(retry, interval, keyword, *args)

    def wait_for_click(self, locator, input_retry="10x", input_interval="3s", slow_down=False, slow_speed=0.2):
        """Executes a click until it pass or fail in the range of wait time

        Arguments:
            - locator: the xpath of the element to click on it
            - (optional) retry: time or times that it should try again and execute the keyword. For usage see BuiltIn
            documentation
            - (optional) interval: interval of time that it wait to try again and execute the keyword. For usage see
            BuiltIn documentation
            - (optional) slow_down: True or False argument to slow down the key with the selenium speed method. Speed will be set to the original
            value on the end of the keyword. If the user don't set the argument to True, it will still as False.
            - (optional) slow_speed: Choose the time to be set on the set_selenium_speed keyword. If the user don't set any value,
            it will be 0.2 (slow_down variable should be set as True to make this argument working properly)

        Examples:
        | wait input text | id=element | text to insert |
        | wait input text | id=element | text to insert | retry=10x | interval=10s |
        | wait input text | id=element | text to insert | retry=10x | interval=10s |
        | wait input text | id=element | text to insert | retry=10x | interval=10s | slow_down=True |
        | wait input text | id=element | text to insert | retry=10x | interval=10s | slow_down=True | slow_speed=0.5"""

        if slow_down:
            original_speed = self.selib.get_selenium_speed()
            self.selib.set_selenium_speed(slow_speed)
        self.selib.wait_until_page_contains_element(locator)
        status = self.builtin.run_keyword_and_return_status("element should be visible", locator)
        if not status:
            try:
                self.wait_for_keyword("scroll element into view", args[0])
            except:
                pass
            self.wait_for_keyword("set focus to element", locator)
        self.wait_for_keyword("click element",  locator, retry=input_retry, interval=input_interval)
        if slow_down:
            self.selib.set_selenium_speed(original_speed)

    def wait_input_text(self, *args, retry="5x", interval="3s", slow_down=False, slow_speed=0.2):
        """Executes a input text until it pass or fail in the range of wait time

        Arguments:
            - locator: the xpath of the element to click on it
            - (optional) retry: time or times that it should try again and execute the keyword. For usage see BuiltIn
            documentation
            - (optional) interval: interval of time that it wait to try again and execute the keyword. For usage see
            BuiltIn documentation
            - (optional) slow_down: True or False argument to slow down the key with the selenium speed method. Speed will be set to the original
            value on the end of the keyword. If the user don't set the argument to True, it will still as False.
            - (optional) slow_speed: Choose the time to be set on the set_selenium_speed keyword. If the user don't set any value,
            it will be 0.2 (slow_down variable should be set as True to make this argument working properly)

        Examples:
        | wait input text | id=element | text to insert |
        | wait input text | id=element | text to insert | retry=10x | interval=10s |
        | wait input text | id=element | text to insert | retry=10x | interval=10s |
        | wait input text | id=element | text to insert | retry=10x | interval=10s | slow_down=True |
        | wait input text | id=element | text to insert | retry=10x | interval=10s | slow_down=True | slow_speed=0.5"""

        if slow_down:
            original_speed = self.selib.get_selenium_speed()
            self.selib.set_selenium_speed(slow_speed)
        self.selib.wait_until_page_contains_element(args[0])
        status = self.builtin.run_keyword_and_return_status("element should be visible", args[0])
        if not status:
            try:
                self.wait_for_keyword("scroll element into view", args[0])
                self.wait_for_keyword("set focus to element", args[0])
            except:
                pass
        self.clear_text(args[0])
        self.wait_for_keyword("input text", args[0], args[1])
        if slow_down:
            self.selib.set_selenium_speed(original_speed)


    def search_element_on_component(self, locator, text, attribute=False):
        """Get a webelement given a component and reference text

        Arguments:
            - locator: selib component to search locator (String)
            - text: target text to return the webelement when find it (String)
            - (optional) attribute: if the value is not a text use this parameter to overwrite the
            text argument, it will change the search method to find by element attribute instead of text.

        Examples:
        | search element on component | css=.component | client 01 |
        | search element on component | css=.component | client 01 | cliente 02 | # it will search for client 02 |
        """
        component = self.selib.get_webelements(locator)
        for element in component:
            if not attribute:
                if text in self.selib.get_text(element): return element
            else:
                if text in self.selib.get_element_attribute(element, attribute): return element
        raise Exception("Could not found the " + text + " in the component")

    def clear_text(self, locator):
        """Clear the text on a given field

        Arguments:
            - locator: selib text field element locator (String)

        Examples:
        | clear text | css=.textField |
        """
        self.selib.wait_until_page_contains_element(locator)
        value = self.selib.get_element_attribute(locator, 'value')
        chars = len(value)
        x = 0
        while x < chars:
            x += 1
            self.selib.press_key(locator, "\\8")

    def get_match_element_by_target_and_reference_text(self, target_column_locator, reference_column_locator,
                                                       target_text, reference_text):
        """Get element that matches the target and reference text given as parameters

        Arguments:
            - target_column_locator: selib webelements that will return all cells for the target column to get
            - reference_column_locator: selib webelements that will return all cells for the reference cell value to be matched
            - target_text: text to be matched with the one on reference text so that it can return
            - reference_text: text to be searched on reference column to find the right cell of the targe column

        Examples:
        | Get match element by target and text reference | css=.columnA | css=.columnB | BR2010 | New Establishment |

        =>

        | (selib webelement) |
        | (boolean) False # if did not find the cell with the given parameters |
        """
        target_column = self.selib.get_webelements(target_column_locator)
        reference_column = self.selib.get_webelements(reference_column_locator)
        i = 0
        r = False
        for reference in reference_column:
            if reference_text.lower() in self.selib.get_text(reference).lower():
                if target_text.lower() in self.selib.get_text(target_column[i]).lower():
                    r = target_column[i]
                    break
            i += 1
        return r

    def get_table_cell_element_by_text_reference(self, target_column_locator, reference_column_locator, reference_text):
        """Get a table cell element giving a text reference

        Arguments:
            - target_column_locator: selib webelements that will return all cells for the target column to get
            - reference_column_locator: selib webelements that will return all cells for the reference cell value to be matched
            - reference_text: text to be searched on reference column to find the right cell of the targe column

        Examples:
        | Get table cell element by text reference | css=.columnA | css=.columnB | invoice A |
        =>

        | (selib webelement) |
        | (boolean) False # if did not find the cell with the given parameters |
        """
        target_column = self.selib.get_webelements(target_column_locator)
        reference_column = self.selib.get_webelements(reference_column_locator)
        i = 0
        r = False
        for reference in reference_column:
            if reference_text.lower() in self.selib.get_text(reference).lower():
                r = target_column[i]
                break
            i += 1
        return r

    def upload_file(self, locator, path, file_name, fixtures_path='\\resources\\fixtures\\'):
        """Upload a file to the browser

        Arguments:
            - locator: selib upload form element locator (String)
            - path: relative path where to save the file. If the file is not inside fixtures path, please,
            overwrite the fixtures_path parameter and use that one to concatenate with, or, just give it
            an empty string ''. Do not use '\\' if not overwrite fixtures_path. Follow the examples to see
            its usage.
            - file_name: file name with the extension to be uploaded.
            - (optional) fixtures_path: Parameter to overwrite the dafault value '\\resources\\fixtures\\'.
            You should use two '\\' with this parameter

        Examples:
        | Upload file | id=uploadBatch | reinf | R2010.json |
        | Upload file | id=uploadBatch | reinf | R2010.json | \\\\resources\\\\support\\\\ |
        """
        file_path = self.curdir + fixtures_path + path + file_name
        self.selib.choose_file(locator, file_path)
