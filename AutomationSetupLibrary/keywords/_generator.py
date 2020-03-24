from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from .keywordgroup import KeywordGroup
from datetime import datetime
from datetime import date

import random
import string

class _Generator(KeywordGroup):

    def __init__(self):
        self.builtin = BuiltIn()

    def generate_cnpj(self, punctuation=False):
        """Generates a valid and CNPJ number

        Arguments:
            - (optional) punctuation: Boolean that define if the result should be with the punctuation. False by default

        Examples:
        | Generate CNPJ | True |

        =>

        | (string) 95.140.944/0001-70 |
        """
        n = [random.randrange(10) for i in range(8)] + [0, 0, 0, 1]
        v = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 6]
        s = sum(x * y for x, y in zip(reversed(n), v))
        d1 = 11 - s % 11
        if d1 >= 10:
            d1 = 0
        n.append(d1)
        s = sum(x * y for x, y in zip(reversed(n), v))
        d2 = 11 - s % 11
        if d2 >= 10:
            d2 = 0
        n.append(d2)
        if punctuation:
            return "%d%d.%d%d%d.%d%d%d/%d%d%d%d-%d%d" % tuple(n)
        else:
            return "%d%d%d%d%d%d%d%d%d%d%d%d%d%d" % tuple(n)

    def generate_random_number(self, start=0, end=100):
        """Generates an random integer between the given parameter

        Arguments:
            - (optional) start: Integer that define the start boundary for the generator. Default: 0
            - (optional) end: Integer that define the start boundary for the generator. Default: 100

        Examples:
        | Generate random number |
        | Generate random number | 99 | 999999 |
        =>

        | (int) 7 |
        | (int) 565656 |
        """
        return str(random.randint(start, end))

    def generate_string_with_random_number(self, text, start=0, end=100):
        """Generates an random integer between the given parameter.

        Arguments:
            - initial_text: Integer that define the start boundary for the generator.
            - (optional) start: Integer that define the start boundary for the generator. Default: 0
            - (optional) end: Integer that define the start boundary for the generator. Default: 100

        Examples:
        | Generate string with random number | test_ | 999999 |
        =>

        | (string) test_99 |
        """
        return text + self.generate_random_number(start, end)

    def generate_random_string(self, string_length=10):
        """Generates a random string of fixed length

        Arguments:
            - (optional) string_length: Integer that define the length generator. Default: 10

        Examples:
        | Generate random string |
        | Generate random string | 20 |
        =>

        | (string) oskqlpsoke |
        | (string) oskqlpsokeaksloekdls |
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))

    def generate_current_date_time(self):
        """Get the current date time in the following format: d/m/Y I:M:S

        Examples:
        | Generate current date time |
        =>

        | (string) 23/12/2020 04:10:1000 |
        """
        return date.today().strftime("%d/%m/%Y %I:%M:%S")

    def generate_current_date(self):
        """Get the current date time in the following format: Y/m/d

        Examples:
        | Generate random string |
        =>

        | (string) 2020/11/30 |
        """
        return date.today().strftime("%Y-%m-%d")

    def get_current_date(self):
        """Get the current date time returned in an array (list): [year, month, day]

        Examples:
        | Generate current date |
        =>

        | (list) [2020, 02, 23] |
        """
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        currentDay = datetime.now().day
        date = [currentYear, currentMonth, currentDay]
        return date

    def get_date_from_previous_month(self):
        """Get the previous month date time returned in an array (list): [year, current_month - 1, day]

        Examples:
        | Get date from the previous month |
        =>

        | (list) [2020, 02, 23] | # current date [2020, 03, 23] |
        | (list) [2019, 12, 23] | # current date [2020, 01, 23] |
        """
        date = self.get_current_date()
        if date[1] == 1:
            date[1] = 12
            date[0] -= 1
        else:
            date[1] -= 1
        return date
