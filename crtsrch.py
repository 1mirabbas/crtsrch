#!/usr/bin/env python3
# Version: v2.0.0 @2023

###########################################
#    Author: Mirabbas Agalarov            #
#    Youtube: mirabbasagalarov            #
###########################################

import sys
import time
import requests
import argparse

CRTSH_URL = "https://crt.sh/?q={}&output=json"
DEFAULT_TIMEOUT = 90
MAX_RETRIES = 3
RETRY_DELAY = 5

parser = argparse.ArgumentParser()
parser.add_argument("-d", help="target domain", dest="domain")
parser.add_argument("-o", help="output file", dest="output")
parser.add_argument("-t", "--timeout", type=int, default=DEFAULT_TIMEOUT,
                    help="request timeout in seconds (default: %d)" % DEFAULT_TIMEOUT)
args = parser.parse_args()
domain = args.domain
output = args.output
timeout = args.timeout


def pr_red(msg):
    print("\033[91m{}\033[00m".format(msg))


def pr_cyan(msg):
    print("\033[96m{}\033[00m".format(msg))


def pr_green(msg):
    print("\033[92m{}\033[00m".format(msg))


def fetch_common_names(domain, timeout_sec, max_retries=MAX_RETRIES):
    """Fetch certificate data from crt.sh, return list of common_name."""
    url = CRTSH_URL.format(domain)
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                pr_cyan("Retry {} of {}...".format(attempt, max_retries))
                time.sleep(RETRY_DELAY)
            response = requests.get(url, timeout=timeout_sec)
            response.raise_for_status()
            data = response.json()
            break
        except requests.RequestException as e:
            last_error = e
            if attempt == max_retries:
                pr_red("Network error: {}".format(e))
                return None
            continue
        except ValueError as e:
            pr_red("Invalid response (JSON): {}".format(e))
            return None
    else:
        if last_error:
            pr_red("Network error: {}".format(last_error))
        return None

    if not data:
        return []

    names = []
    for entry in data:
        cn = entry.get("common_name")
        if cn is not None:
            names.append(str(cn).strip())
    return names


def process_names(names, strip_wildcard):
    """Remove duplicates, optionally strip *. prefix, return sorted."""
    seen = set()
    result = []
    for name in names:
        s = name.replace("*.", "") if strip_wildcard else name
        if s and s not in seen:
            seen.add(s)
            result.append(s)
    return sorted(result)


def main():
    if domain is None:
        pr_red('Missing target domain. Usage: crtsrch.py -d target.com')
        sys.exit(1)

    pr_cyan("""
  ____      _                _     
 / ___|_ __| |_ ___ _ __ ___| |__  
| |   | '__| __/ __| '__/ __| '_ \\ 
| |___| |  | |_\\__ \\ | | (__| | | |
 \\____|_|   \\__|___/_|  \\___|_| |_|
       Author: Mirabbas Agalarov                           

""")
    pr_green("""
1) Default result (common_name as-is)
2) Domain (strip *. prefix)
""")

    try:
        value = input("Select mode (1 or 2): ").strip()
        value = int(value)
    except ValueError:
        pr_red("Invalid mode. Enter 1 or 2.")
        sys.exit(1)

    if value not in (1, 2):
        pr_red("Please choose 1 or 2.")
        sys.exit(1)

    strip_wildcard = value == 2
    names = fetch_common_names(domain, timeout)
    if names is None:
        sys.exit(1)

    result = process_names(names, strip_wildcard)

    if output:
        try:
            with open(output, "w", encoding="utf-8") as f:
                for name in result:
                    f.write(name + "\n")
            pr_green("Results written to {} ({} entries).".format(output, len(result)))
        except OSError as e:
            pr_red("Could not write file: {}".format(e))
            sys.exit(1)
    else:
        for name in result:
            print(name)
        pr_green("\nTotal {} entries.".format(len(result)))


if __name__ == "__main__":
    main()
