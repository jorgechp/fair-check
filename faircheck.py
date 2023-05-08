import argparse
import csv
import logging

import requests
import sys

from dataclasses import dataclass
from typing import List, Dict, Tuple, Set

from requests import Response


class BCOLORS:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    END = '\033[0m'


@dataclass
class TestInfo:
    test: str
    is_success: bool
    comment: str


def __extract_from_file(path: str) -> List[str]:
    with open(path, 'r') as file:
        return file.read().splitlines()


def __execute_request(subject: str, test_url: str) -> List[Dict] or None:
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = '{"subject": "%s"}' % subject

    response: Response = requests.post(test_url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Error calling interface: {}. Status code: {}. Reason: {}".format(test_url,
                                                                                        response.status_code,
                                                                                        response.reason))
        return None


def __launch_test(resources_list: List[str], name_list: List[str], interface_list: List[str]) \
        -> Tuple[Dict[str, Dict[str, TestInfo]], List[str], List[str]]:

    results_dict: Dict[str, Dict[str, TestInfo]] = dict()
    temp_name_set: Set[str] = set()
    temp_interface_set: Set[str] = set()

    for resource in resources_list:
        results_dict[resource] = dict()

        for test_name, test_interface in zip(name_list, interface_list):
            results: List[Dict] or None = __execute_request(resource, test_interface)
            if results is not None:
                comment_value: str = results[0]['http://schema.org/comment'][0]['@value']
                result: int = int(results[0]['http://semanticscience.org/resource/SIO_000300'][0]['@value'])
                results_dict[resource][test_name] = TestInfo(test_name, bool(result), comment_value)
                temp_name_set.add(test_name)
                temp_interface_set.add(test_interface)
            else:
                logging.info("Removing indicator {} from list.".format(test_name))

    return results_dict, list(temp_name_set), list(temp_interface_set)


def __print_results(results: Dict[str, Dict[str, TestInfo]], name_list: List[str]) -> None:
    for resource, tests in results.items():
        print(f"{BCOLORS.HEADER} Testing resource: %r{BCOLORS.END}" % resource)
        success_counter: int = 0
        for name in name_list:
            test = results[resource][name]
            print(f"\t{BCOLORS.BLUE} Test: %r{BCOLORS.END}" % test.test)
            if test.is_success:
                print(f"\t\t{BCOLORS.GREEN} SUCCESS: %r{BCOLORS.END}" % test.comment)
                success_counter = success_counter + 1
            else:
                print(f"\t\t{BCOLORS.FAIL} FAILED!: %r{BCOLORS.END}" % test.comment)
        print(f"\t{BCOLORS.CYAN} Passed: %s/%s {BCOLORS.END}" % (success_counter, len(tests)))


def __export_csv(path: str,
                 results: Dict[str, Dict[str, TestInfo]],
                 name_list: List[str]) -> None:

    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['resource'] + name_list)

        for resource, tests in results.items():
            results_line = [resource]

            for name in name_list:
                results_line.append(results[resource][name].is_success)
            writer.writerow(results_line)


def __process_tests_list(test_list: List[str]) -> Tuple[List[str], List[str]]:
    name_list: List[str] = []
    interface_list: List[str] = []
    if len(test_list) > 0:
        first_string_len: int = len(test_list[0].split(','))
        if first_string_len == 1:
            name_list = test_list
            interface_list = test_list
        else:
            name_list, interface_list = zip(*[x.split(',') for x in test_list])

    return list(name_list), list(interface_list)


def main():
    parser = argparse.ArgumentParser(
        prog='faircheck.py',
        description="Check the degree of compliance with FAIR principles of a resource.",
        epilog='Jorge Chamorro Padial - GNU GPLv3')
    parser.add_argument('resources_list', nargs='*', default=[])
    parser.add_argument('tests_list', nargs='*', default=[])
    parser.add_argument('-e', '--export', help="Specify a path to export the results as a csv file.")
    parser.add_argument('-nv', '--no-verbosity', help="Don't display the test results on the default output.")
    parser.add_argument('-r', '--resources', help="Path to a resource file")
    parser.add_argument('-t', '--tests', help="Path to a test file")

    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_help()
        exit(0)

    resource_list: List[str] = args.resources_list if len(args.resources_list) > 0 \
        else __extract_from_file(args.resources)

    if len(args.tests_list) > 0 or args.tests is not None:
        test_list: List[str] = args.tests_list if len(args.tests_list) > 0 \
            else __extract_from_file(args.tests)
    else:
        test_list: List[str] = __extract_from_file("config/tests")

    name_list, interface_list = __process_tests_list(test_list)

    print("Executing tests")
    results_dict, name_list, interface_list = __launch_test(resource_list, name_list, interface_list)

    print("Generating output file")
    if args.no_verbosity is None:
        __print_results(results_dict, name_list)

    if args.export is not None:
        __export_csv(args.export, results_dict, name_list)
    print("Done")


if __name__ == '__main__':
    main()
