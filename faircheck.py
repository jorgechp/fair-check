import argparse
import csv
import requests
import sys

from dataclasses import dataclass
from typing import List, Dict


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


def __execute_request(subject: str, test_url: str) -> List[Dict]:
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = '{"subject": "%s"}' % subject

    return requests.post(test_url, headers=headers, data=data).json()


def __launch_test(resources_list: List[str], test_list: List[str]) -> Dict[str, List[TestInfo]]:
    results_dict: Dict[str, List[TestInfo]] = dict()
    for resource in resources_list:
        results_dict[resource] = []
        for test in test_list:
            results: List[Dict] = __execute_request(resource, test)
            comment_value: str = results[0]['http://schema.org/comment'][0]['@value']
            result: int = int(results[0]['http://semanticscience.org/resource/SIO_000300'][0]['@value'])
            results_dict[resource].append(TestInfo(test, bool(result), comment_value))

    return results_dict


def __print_results(results: Dict[str, List[TestInfo]]) -> None:
    for resource, tests in results.items():
        print(f"{BCOLORS.HEADER} Testing resource: %r{BCOLORS.END}" % resource)
        success_counter: int = 0
        for test in tests:
            print(f"\t{BCOLORS.BLUE} Test: %r{BCOLORS.END}" % test.test)
            if test.is_success:
                print(f"\t{BCOLORS.GREEN} SUCCESS: %r{BCOLORS.END}" % test.comment)
                success_counter = success_counter + 1
            else:
                print(f"\t{BCOLORS.FAIL} FAILED!: %r{BCOLORS.END}" % test.comment)
        print(f"\t{BCOLORS.CYAN} Passed: %s/%s {BCOLORS.END}" % (success_counter, len(tests)))


def __export_csv(path: str, test_list: List[str], results: Dict[str, List[TestInfo]]) -> None:
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['resource'] + test_list)
        for resource, tests in results.items():
            results_line = [resource] + [str(int(x.is_success)) for x in tests]
            writer.writerow(results_line)


def main():
    parser = argparse.ArgumentParser(
        prog='faircheck',
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

    results_dict: Dict[str, List[TestInfo]] = __launch_test(resource_list, test_list)
    if args.no_verbosity is None:
        __print_results(results_dict)

    if args.export is not None:
        __export_csv(args.export, test_list, results_dict)


if __name__ == '__main__':
    main()
