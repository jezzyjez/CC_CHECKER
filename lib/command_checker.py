import abc

class CommandChecker:
    def __init__(self):
        self.config_file = 'dummy'

    def check_file_existence(self, file):
        pass

    def check_database_existence(self, db):
        pass

    def check_required_parameters(self, list_of_parameters, line):
        pass

    def run_checks(self, check_list):
        pass

    def determine_command(self, line)
