#!/usr/bin/env python3

import sys
import argparse
import urllib.request
import urllib.error
import json


def main():
    parser = argparse.ArgumentParser(
        description='Check online status of a web page.')
    parser.add_argument(
        'url',
        help='URL of the web page starting with https:// or http://')
    parser.add_argument(
        '-c', '--checklist',
        help='JSON file of sites and contents to check against.')
    args = parser.parse_args()
    subdomain_list = split_to_subdomain_list(args.url)
    sites = {str.join('.', subdomain_list): []}
    if args.checklist:
        with open(args.checklist, 'r') as f:
            sites = json.load(f)
    for i in range(len(subdomain_list)):
        subdomain = str.join('.', subdomain_list[i:])
        if subdomain in sites:
            checkpage(url=args.url, checklist=sites[subdomain])
            break


def split_to_subdomain_list(url):
    if '://' in url:
        split_proto = url.split('://')
        split_domain = split_proto[1].split('/')
        return [split_proto[0]] + split_domain[0].split('.')
    else:
        split_domain = url.split('/')
        return split_domain[0].split('.')


def checkpage(url, checklist):
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print('Cannot connect to server. :(')
        print(e.reason)
        sys.exit(1)
    except urllib.error.HTTPError as e:
        print('HTTP error. :S')
        print('Error code:', e.code)
        sys.exit(1)

    print('Status: {0:n}'.format(response.status))
    html = response.read().decode()

    check_count = 0
    for check in checklist:
        if check in html:
            check_count = check_count + 1
            print(check + ' found!')
        else:
            print(check + ' not found... :(')

    if check_count == len(checklist):
        print(url + ' OK!')
    elif check_count < len(checklist):
        print(url + ' missing content!')
    else:
        raise Exception('We cannot possibly have checked more items than there'
                        ' is in the list!')

if __name__ == '__main__':
    main()
