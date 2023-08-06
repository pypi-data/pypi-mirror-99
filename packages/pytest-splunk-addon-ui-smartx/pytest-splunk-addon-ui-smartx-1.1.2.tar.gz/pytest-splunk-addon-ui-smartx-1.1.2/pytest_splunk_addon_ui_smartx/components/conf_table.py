# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from .table import Table

class ConfigurationTable(Table):
    """
    The table located in the configuration page.
    """
    def __init__(self, browser, container, mapping={}):
        super(ConfigurationTable, self).__init__(browser, container, mapping)