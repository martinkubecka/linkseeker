import os
import logging
import sys
import time
import argparse
from sys import platform
import warnings
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException


def banner():
    print(r"""
  __________       ______                  ______              
  ___  /__(_)_________  /_____________________  /______________
  __  /__  /__  __ \_  //_/_  ___/  _ \  _ \_  //_/  _ \_  ___/
  _  / _  / _  / / /  ,<  _(__  )/  __/  __/  ,<  /  __/  /    
  /_/  /_/  /_/ /_//_/|_| /____/ \___/\___//_/|_| \___//_/                                                              
    """)


def extract_links(url):
    try:
        print(f"\n[{time.strftime('%H:%M:%S')}] [INFO] Loading Firefox webdriver in headless mode ...")
        logging.info("Loading Firefox webdriver in headless mode")
        options = Options()
        options.headless = True
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Firefox(options=options, service_log_path="logs/geckodriver.log")

        print(f"[{time.strftime('%H:%M:%S')}] [INFO] Loading '{url}' in the current browser session ...")
        logging.info(f"Loading '{url}' in the current browser session")
        driver.get(url=url)

        print(f"[{time.strftime('%H:%M:%S')}] [INFO] Fetching website source code after javascript is loaded ...")
        logging.info(f"Fetching website source code after javascript is loaded")
        source_code = driver.execute_script(
            "return document.documentElement.innerHTML;")

        driver.quit()

    except WebDriverException as e:
        if "dnsNotFound" in str(e):
            print(f"[{time.strftime('%H:%M:%S')}] [ERROR] Unknown host")
            logging.error(f"Unknown host", exc_info=True)
        else:
            print(f"[{time.strftime('%H:%M:%S')}] [ERROR] Error encountered while working with Firefox webdriver")
            logging.error(f"Error encountered while working with Firefox webdriver", exc_info=True)
        print("\nExiting program ...\n")
        exit(1)

    print(f"[{time.strftime('%H:%M:%S')}] [INFO] Parsing website source code ...")
    logging.info("Parsing website source code")
    soup = BeautifulSoup(source_code, 'html.parser')

    base_tag = soup.find('base')
    if not base_tag:
        base = False
    else:
        base = True
        base_url = base_tag.get('href')
        print(f"[{time.strftime('%H:%M:%S')}] [INFO] Found HTML <base> tag : '{base_url}'")
        logging.info(f"Found HTML <base> tag : '{base_url}'")

    print(f"[{time.strftime('%H:%M:%S')}] [INFO] Extracting hyperlink tags ...")
    logging.info(f"Extracting hyperlink tags")
    extracted_urls = []
    a_tags = soup.find_all('a')
    for tag in a_tags:
        extracted_urls.append(tag.get('href'))

    prefix = ["http", "https"]
    if base:    # EXPERIMENTAL
        print(f"[{time.strftime('%H:%M:%S')}] [INFO] Rebuilding links with found base tag ...")
        logging.info(f"Rebuilding links with found base tag")
        for index, value in enumerate(extracted_urls):
            if not any(p in value for p in prefix):
                if value.startswith("/"):
                    value = value[1:]
                extracted_urls[index] = base_url + value
    else:
        print(f"[{time.strftime('%H:%M:%S')}] [INFO] Filtering out invalid links from extracted hyperlink tags ...")
        logging.info(f"Filtering out invalid links from extracted hyperlink tags")
        extracted_urls_temp = []
        for value in extracted_urls:
             if any(value.startswith(p) for p in prefix):
                extracted_urls_temp.append(value)
        extracted_urls = extracted_urls_temp

    extracted_urls_holder = set(extracted_urls)
    extracted_urls = (list(extracted_urls_holder))

    return extracted_urls


def save_to_file(filename, extracted_links):
    with open(filename, 'w') as output_file:
        for link in extracted_links:
            output_file.write(f"{link}\n")


def arg_formatter():
    def formatter(prog): return argparse.HelpFormatter(
        prog, max_help_position=52)
    return formatter


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=arg_formatter(
    ), description='Extract all hyperlinks from the website source code after javascript is loaded.')

    parser.add_argument('url', metavar="URL", help='target website URL')
    parser.add_argument('-q', '--quiet', help="do not print banner", action='store_true')
    parser.add_argument('-p', '--print', action='store_true',
                        help='print extracted links to console')
    parser.add_argument('-o', '--output', metavar="FILENAME", default="extracted_links.txt",
                        help='output file for extracted links (default: extracted_links.txt)')

    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])


def init_logger():
    logging_path = f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/logs"
    if not os.path.isdir(logging_path):
        os.mkdir(logging_path)
    logging.basicConfig(format='%(created)f; %(asctime)s; %(levelname)s; %(name)s; %(message)s',
                        filename=f"{logging_path}/{(os.path.splitext(__file__)[0]).split('/')[-1]}.log", level=logging.DEBUG)
    logger = logging.getLogger('__name__')


def main():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    init_logger()

    if not platform.startswith('linux'):
        print(f"[{time.strftime('%H:%M:%S')}] [ERROR] Unsupported platform")
        logging.error(f"Unsupported platform")
        print("\nExiting program ...\n")
        exit(1)

    args = parse_args()

    if not args.quiet:
        banner()

    url = args.url
    print_arg = args.print

    # "https://posta.sk/"
    # "https://sk-posta.net/"

    extracted_links = extract_links(url)
    print(f"[{time.strftime('%H:%M:%S')}] [INFO] Successfully extracted {len(extracted_links)} unique links")
    logging.info(f"Successfully extracted {len(extracted_links)} unique URLs")

    if print_arg:
        print("\n")
        for url in extracted_links:
            print(url)
        print("\n")

    output_file = args.output
    print(f"[{time.strftime('%H:%M:%S')}] [INFO] Writing extracted links to '{output_file}' ...")
    logging.info(f"Writing extracted links to '{output_file}'")
    save_to_file(output_file, extracted_links)


if __name__ == '__main__':
    main()
