import argparse
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib/")
import bcom_checker
import common_func as commonfunc

def parse_argument():
    # TODO: Add support to parse Change control from RPD
    parser = argparse.ArgumentParser()
    parser.add_argument("-ccf", "--change_control_file", help="Full path for the change control file", required=True)
    parser.add_argument("-r", "--rpd", help="RPD of the change control", required=True)
    parser.add_argument("-o", "--out_file", help="Output file for the comments", required=True)
    args = parser.parse_args()

    return args


def main():
    line_number = 0
    bcom=bcom_checker.BcomChecker()
    args = parse_argument()
    status_message = None
    with open(args.change_control_file) as command_list, open(args.out_file, 'w') as out_file:
        for command in command_list:
            line_number += 1
            component=commonfunc.parse_component(command)
            if component == "bcom":
                status_message = bcom.run_command_check(command) 
            if not status_message.status:
                out_file.write("Comments for Line Number:{0} - command:{1} ".format(line_number, command))
                out_file.write("{} \n".format(status_message.message))

    
if __name__ == "__main__":
    main()
