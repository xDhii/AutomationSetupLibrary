# -*- coding: utf-8 -*-

import os
from AutomationSetupLibrary.keywords._configuration import _Configuration
from AutomationSetupLibrary.keywords._generator import _Generator
from AutomationSetupLibrary.keywords._selibkeywords import _SelibKeywords
from AutomationSetupLibrary.keywords._excel import _Excel
from AutomationSetupLibrary.keywords._hooks import _Hooks
from AutomationSetupLibrary.keywords._tasks import _Tasks
from AutomationSetupLibrary.version import __version__
from robot.libraries.BuiltIn import BuiltIn


class AutomationSetupLibrary(
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
        """AutomationSetupLibrary for test automation on SVR

        Examples:
        | Library | AutomationSetupLibrary |
        """
        for base in AutomationSetupLibrary.__bases__:
            base.__init__(self)
