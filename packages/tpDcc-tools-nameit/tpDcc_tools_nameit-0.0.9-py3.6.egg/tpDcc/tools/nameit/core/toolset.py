#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool that manages the nomenclature of your pipelines
"""

from __future__ import print_function, division, absolute_import

from tpDcc.libs.qt.widgets import toolset

from tpDcc.libs.nameit.core import namelib
from tpDcc.tools.nameit.widgets import nameit


class NameItToolset(toolset.ToolsetWidget, object):
    def __init__(self, *args, **kwargs):

        self._naming_lib = kwargs.pop('naming_lib', None)
        self._naming_file = kwargs.pop('naming_file', None)

        super(NameItToolset, self).__init__(*args, **kwargs)

    def contents(self):

        naming_lib = self._naming_lib or namelib.NameLib(naming_file=self._naming_file)
        name_it = nameit.NameIt(naming_lib=naming_lib, parent=self)
        return [name_it]
