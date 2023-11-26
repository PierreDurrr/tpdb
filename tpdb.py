from argparse import ArgumentParser
from pathlib import Path
from re import compile as re_compile
from typing import Iterable, Literal
from datetime import datetime
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    print(f'Missing required packages - execute "pipenv install"')
    exit(1)

PRIMARY_CONTENT_CLASS: str = 'row d-flex flex-wrap m-0 w-100 mx-n1 mt-n1'

# Create ArgumentParser object and arguments
parser = ArgumentParser(description='TPDb Collection Maker')
parser.add_argument(
    'html',
    type=Path,
    metavar='HTML_FILE',
    help='file with TPDb Collection page HTML to scrape')
parser.add_argument(
    '-p', '--primary-only',
    action='store_true',
    help='only parse the primary set (ignore any Additional Sets)')
parser.add_argument(
    '-q', '--always-quote',
    action='store_true',
    help='put all titles in quotes ("")')

ContentType = Literal['Category', 'Collection', 'Show', 'Movie', 'Company']

class Content:
    # ... (existing code)

if __name__ == '__main__':
    args = parser.parse_args()

    if not args.html.exists():
        print(f'File "{args.html.resolve()}" does not exist')
        exit(1)

    with args.html.open('r') as file_handle:
        html = file_handle.read()

    webpage = BeautifulSoup(html, 'html.parser')

    if args.primary_only:
        webpage = webpage.find('div', class_=PRIMARY_CONTENT_CLASS)

    current_date_time = datetime.now().strftime('%Y-%m-%d-%H%M')
    output_file_name = f"{args.html.stem}-{current_date_time}.txt"

    with open(output_file_name, 'w') as output_file:
        sys.stdout = output_file

        content_list = ContentList()
        for poster_element in webpage.find_all('div', class_='overlay rounded-poster'):
            content = Content(
                poster_element.attrs['data-poster-id'],
                poster_element.attrs['data-poster-type'],
                poster_element.find('p', class_='p-0 mb-1 text-break').string,
                must_quote=args.always_quote,
            )
            content_list.add_content(content)

        content_list.print()
