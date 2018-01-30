import json
import os
import re
import collections


class CommandChecker:
    def __init__(self):
        self.error_message = ""
        self.status = 1
        self.command = ""
        self.param = ""
        self.queried_files = []

    def generate_command_list(self): 
        """This will generate the list of accepted checks per bcom or fdb commands"""
        with open(self.config_file) as json_data_file:
            self.list_of_command = json.load(json_data_file)
        return self.list_of_command

        
    def set_value_and_param(self, param):
        """"This will set the base parameter and value"""
        param_value = collections.namedtuple('param_value', 'base_param value')
        self.param = param_value(base_param = param.split('=')[0], value = param.split('=')[1] or None)


    def check_file_existence(self):
        """This will check if file exist or included in queried file"""
        
        if (not os.path.isfile(self.param.value)) and (self.param.value not in self.queried_files):
            self.return_error("File {0} does not exist".format(self.param.value)) 

    def check_database_existence(self, db):
        pass

    def check_required_parameters(self, parameter_list):
        missing_param_list = []
        base_param_list = []
        for parameter in parameter_list:
           base_param_list.append(parameter.split("=")[0])

        for required_param in self.list_of_command[self.command]['required']:
            required_param_regex = re.compile(required_param)
            if required_param not in base_param_list:
                missing_param_list.append(required_param)
        if missing_param_list:   
            self.return_error("Missing required parameters: " + ','.join(missing_param_list))

    def return_error(self, error):
        self.error_message += "\t{0}\n".format(error)
        self.status = 0

    def run_checks(self, check_list):
        pass

    def set_command(self, parameter_list):
        for command in self.list_of_command:
            if command in parameter_list:
                if self.command:
                    self.return_error("multiple command found. No other checks will be perform for this line".format(self.component))
                    self.command = None
                    return None
                self.command = command

        if not self.command:
            self.return_error("{0} commmand not found. Check for sytanx error".format(self.component))
        return None

    def find_parameter(self, command_parameter):
        if self.param.base_param in command_parameter['required']:
            return command_parameter['required'][self.param.base_param]
        elif self.param.base_param in command_parameter['optional']:
            return command_parameter['optional'][parameter]
        else:
            self.return_error("Unrecognized parameter {}".format(self.param.base_param))
        return None

    def run_parameter_check(self, parameter_check):
         method = None
         try: 
             method = getattr(self, parameter_check)
         except AttributeError:
             raise NotImplementedError("Class {} does not implement {}".format(self.__class__.__name__, parameter_check))
         method()

    def reinitialize_status(self):
        self.status = 1
        self.error_message = ""
        self.command = ""

