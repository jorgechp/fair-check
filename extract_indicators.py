import argparse
import csv
import pandas as pd

from typing import List

COLUMN_INDICATOR_NAME = 'Tests Maturity Indicator Metric'
COLUMN_INDICATOR_INTERFACE = 'Interface'
COLUMN_INDICATOR_DEPRECATED = 'Deprecated?'

DEFAULT_URI = 'https://fairdata.services:7171/FAIR_Evaluator/metrics'


def main():
    parser = argparse.ArgumentParser(
        prog='extract_indicators.py',
        description="Extract indicators from Fairdata service and generate a services output",
        epilog='Jorge Chamorro Padial - GNU GPLv3')
    parser.add_argument('output', help="The path to the output csv file")
    parser.add_argument('uri', nargs='?', help="If specified, the uri of the list of indicators to be parsed. It "
                                               "should use the same format than " + DEFAULT_URI)
    args = parser.parse_args()

    uri: str = DEFAULT_URI
    if args.uri is not None:
        uri = args.uri

    table_extracted = pd.read_html(uri)[0]

    selected_columns = table_extracted[[COLUMN_INDICATOR_NAME, COLUMN_INDICATOR_INTERFACE, COLUMN_INDICATOR_DEPRECATED]]

    indicator_list: List[List[str]] = []
    for idx, row in selected_columns.iterrows():
        is_deprecated = bool(row[COLUMN_INDICATOR_DEPRECATED])
        if not is_deprecated:
            indicator_name: str = row[COLUMN_INDICATOR_NAME]
            indicator_interface: str = row[COLUMN_INDICATOR_INTERFACE]
            indicator_list.append([indicator_name, indicator_interface])

    with open(args.output, 'w', newline='') as file:
        writer = csv.writer(file)
        for indicator in indicator_list:
            writer.writerow(indicator)


if __name__ == '__main__':
    main()
