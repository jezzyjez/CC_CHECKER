import os
import re

from command_checker import CommandChecker

class BcomChecker(CommandChecker):
    def __init__(self):
        self.component = "Bcom"
        self.error_message = ""
        self.status = 1
        self.config_file = os.path.dirname(__file__) +  '/bcom_command.json'
        super().__init__()
        super().generate_command_list()

    def check_universe(self, full_param):
        param = super().split_value_and_param(full_param) 
        if re.match("int:memb:write|int:memb:commit", self.command):
            valid_int_univ = re.compile("memberships(_\w+)*")
        elif re.match("col.*", self.command):
            valid_int_univ = re.compile("idx(_\w+)*|cons(_\w+)*|memberships(_\w+)*")
        else:
            valid_int_univ = re.compile("idx(_\w+)*|cons(_\w+)*")

        if re.match(valid_int_univ, param.value):
            return True
        else:
            super().return_error("{0} is an invalid universe for command {1}".format(param.value, self.command))
            return None


        



