import argparse
import os.path
import requests
import sys
from typing import List


def __extract_from_file(path: str) -> List[str]:
    with open(path, 'r') as file:
        return file.read().splitlines()


def __execute_request(subject: str, test_url: str) -> str:
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = '{"subject": "%s"}' % subject

    return requests.post(test_url, headers=headers, data=data).text


def __launch_test(resources_list: List[str], test_list: List[str]) -> None:
    for resource in resources_list:
        for test in test_list:
            results: str = __execute_request(resource, test)
            print(results)


def main():
    parser = argparse.ArgumentParser(
        prog='faircheck',
        description="Check the degree of compliance with FAIR principles of a resource.",
        epilog='Jorge Chamorro Padial - GNU GPLv3')
    parser.add_argument('resources_list', nargs='*', default=[])
    parser.add_argument('tests_list', nargs='*', default=[])
    parser.add_argument('-r', '--resources', help='Path to a resource file')
    parser.add_argument('-t', '--tests', help='Path to a test file')

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

    __launch_test(resource_list, test_list)



if __name__ == '__main__':
    main()
