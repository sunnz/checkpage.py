#!/usr/bin/env python3

import sys
import argparse
import urllib.request
import urllib.error
import json


def main():
    """
    checks availability of sites using one or more metrics.
    """

    # define and read arguments into args.
    parser = argparse.ArgumentParser(
        description='check online status of a web page.')
    parser.add_argument(
        'checklist', help='checklist of sites and checks in json format.')
    args = parser.parse_args()

    # checklist may contain one or more sites to check against,
    # all URLs and tests defined in checklist.json file.
    if args.checklist:
        with open(args.checklist, 'r') as f:
            checklist = json.load(f)
        for sitename, setting in checklist.items():
            total = passed = 0
            print('=========')
            print(sitename)
            print('=========')

            # each url are checked against.
            for url in setting['urls']:
                print('check: {url}'.format(url=url))
                try:
                    status, content = getcontent(url)
                except urllib.error.URLError as e:
                    print('\tcannot connect to server. :(')
                    print('\t' + e.reason)
                    break
                except urllib.error.HTTPError as e:
                    print('\thttp error. :s')
                    print('\terror code:', e.code)
                    break
                print('status: {}'.format(status))

                # check each strings for this url.
                for string in setting['strings']:
                    total = total + 1
                    if string in content:
                        passed = passed + 1
                        print('\t"{string}" found!'.format(string=string))
                    else:
                        print('\t"{string}" NOT FOUND..'.format(
                            string=string))

            # per site result
            print('\nresult:')
            if total == passed:
                print('{site} passed all tests OK!'.format(site=sitename))
            else:
                print('{site} tests FAILED!'.format(site=sitename))
            print()
        sys.exit(0)


def getcontent(url):
    """
    downloads content located at given url and returns it with status code.

    may throw urllib.error.URLError when we can't connect to the server,
    or urllib.error.HTTPError if there is an error in the HTTP response.

    returns status, content
    """

    response = urllib.request.urlopen(url)
    return response.status, response.read().decode()


if __name__ == '__main__':
    main()
