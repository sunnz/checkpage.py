#!/usr/bin/env python3

import sys, argparse, urllib.request, urllib.error

def main():
    parser = argparse.ArgumentParser(description='Check online status of a web page.')
    parser.add_argument('url', help='URL of the web page starting with https:// or http://')
    args = parser.parse_args()
    checkpage(url=args.url)

def checkpage(url):
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

if __name__ == '__main__':
    main()
