import os
import re
from command_checker import CommandChecker
import collections

class BcomChecker(CommandChecker):
    def __init__(self):
        self.component = "Bcom"
        self.bcom_env = "dev"
        self.error_message = ""
        self.status = 1
        self.config_file = os.path.dirname(__file__) +  '/bcom_command.json'
        super().__init__()
        super().generate_command_list()

    def check_universe(self):
        if re.match("int:memb:write|int:memb:commit", self.command):
            valid_int_univ = re.compile("memberships(_\w+)*")
        elif re.match("col.*", self.command):
            valid_int_univ = re.compile("idx(_\w+)*|cons(_\w+)*|memberships(_\w+)*")
        else:
            valid_int_univ = re.compile("idx(_\w+)*|cons(_\w+)*")

        if re.match(valid_int_univ, self.param.value):
            return True
        else:
            super().return_error("{0} is an invalid universe for command {1}".format(self.param.value, self.command))
            return None

    def encoding_check(self):
        if self.param.value != "utf-8":
            super().return_error("Please use utf-8 encoding in {0}".format(self.param.base_command))

    def date_check(self):
        valid_date = re.compile("\d{8}(-\d{8})*")
        if not re.match(valid_date, self.param.value):
            super().return_error("Invalid Date range {0}".format(self.param.value))
        else:
            (start_date, end_date) = (int(date) for date in self.param.value.split("-"))
        if start_date > end_date:
            super().return_error("Start Date is greater than End Date")

    def out_file_check(self):
        file_dir = os.path.dirname(self.param.value)
        if not os.path.exists(file_dir):
            super().return_error("Directory {0} does not exists".format(file_dir))

    def check_bcom_db(self, bcom_db):

        db, feed_name, env = bcom_db.split(":")
        if not (db and feed_name and env):
            super().return_error("Invalid Bcom Database: {0}".format(bcom_db))
        if env != self.bcom_env:
            super().return_error("Current bcom environment is {0} but bcom database env is {1}".format(self.bcom_env, env))
        

    def run_command_check(self, command_line):
        parameter_list = command_line.split()
        self.reinitialize_status()
        self.set_command(parameter_list)
        component_regex = re.compile("bcom.*|bdi_pub|{0}".format(self.command), re.IGNORECASE)
        bcom_db_regex = re.compile("cts_pool:\w+:\w+")
        command_parameter = self.list_of_command[self.command]

        if self.command:
            self.check_required_parameters(parameter_list)
            for parameter in parameter_list:
                if re.match(bcom_db_regex, parameter):
                    self.check_bcom_db(parameter)
                elif not re.match(component_regex, parameter):
                    self.set_value_and_param(parameter) 
                    parameter_check = self.find_parameter(command_parameter)
                    if parameter_check:
                        self.run_parameter_check(parameter_check)

        status_message = collections.namedtuple('status_message', 'status message')
        return status_message(status=-self.status, message=self.error_message)
