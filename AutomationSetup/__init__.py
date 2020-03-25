# -*- coding: utf-8 -*-

import os
from AutomationSetup.keywords._configuration import _Configuration
from AutomationSetup.keywords._generator import _Generator
from AutomationSetup.keywords._selibkeywords import _SelibKeywords
from AutomationSetup.keywords._excel import _Excel
from AutomationSetup.keywords._hooks import _Hooks
from AutomationSetup.keywords._tasks import _Tasks
from AutomationSetup.version import __version__
from robot.libraries.BuiltIn import BuiltIn

class AutomationSetup(
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
        """Sovos Libraries for test automation on SVR

        Examples:
        | Library | AutomationSetup |
        """
        for base in AutomationSetup.__bases__:
                base.__init__(self)
