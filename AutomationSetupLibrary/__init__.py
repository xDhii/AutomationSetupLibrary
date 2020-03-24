# -*- coding: utf-8 -*-

import os
from automationsetuplibrary.keywords._configuration import _Configuration
from automationsetuplibrary.keywords._generator import _Generator
from automationsetuplibrary.keywords._selibkeywords import _SelibKeywords
from automationsetuplibrary.keywords._excel import _Excel
from automationsetuplibrary.keywords._hooks import _Hooks
from automationsetuplibrary.keywords._tasks import _Tasks
from automationsetuplibrary.version import __version__
from robot.libraries.BuiltIn import BuiltIn


class automationsetuplibrary(
    _Hooks,
    _Configuration,
    _Generator,
    _SelibKeywords,
    _Excel,
    _Tasks,
):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        """automationsetuplibrary for test automation on SVR

        Examples:
        | Library | automationsetuplibrary |
        """
        for base in automationsetuplibrary.__bases__:
            base.__init__(self)
