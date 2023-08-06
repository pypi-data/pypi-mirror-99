# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from .table import Table
from selenium.webdriver.common.by import By
from .base_component import Selector
import time
from selenium.common import exceptions


class InputTable(Table):
    """
    Component: Input Table
    Input table has enable/disable, more-info views additionally to configuration table.
    """
    def __init__(self, browser, container, mapping={}):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
            :param mapping= If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        super(InputTable, self).__init__(browser, container, mapping)

        self.elements.update({
            "switch_button_status":  Selector(select=" td.col-disabled .disabled"),
            "status_toggle":  Selector(select=" .switch-button .round"),
            "switch_to_page":  Selector(select=container.select + " .pull-right li a"),
            "input_status": Selector(select=container.select + " div.switch-label")
        })


    def input_status_toggle(self, name, enable):
        """
        This function sets the table row status as either enabled or disabled. If it is already enabled then it reuturns an exception
            :param name: Str The row that we want to enable st the status to as enabled or disabled
            :param enable: Bool Whether or not we want the table field to be set to enable or disable
            :return: Bool whether or not enabling or disabling the field was successful, If the field was already in the state we wanted it in, then it will return an exception
        """
        _row = self._get_row(name)
        input_status = _row.find_element(*list(self.elements["input_status"]._asdict().values()))
        status = input_status.text.strip().lower()
        if enable:
            if status == "enabled":
                raise Exception("The input is already {}".format(input_status.text.strip()))
            elif status == "disabled":
                status_button = _row.find_element(*list(self.elements["status_toggle"]._asdict().values()))
                status_button.click()
                self.wait_until("switch_button_status")
                return True
        else:
            if status == "disabled":
                raise Exception("The input is already {}".format(input_status.text.strip()))
            elif input_status.text.strip().lower() == "enabled":
                status_button = _row.find_element(*list(self.elements["status_toggle"]._asdict().values()))
                status_button.click()
                self.wait_until("switch_button_status")
                return True
            

