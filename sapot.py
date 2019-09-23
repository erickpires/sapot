from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlencode
import requests
import re

default_parser = 'html.parser'
paren_regex = re.compile(r"\(.*\)")
#
# Code
#

def find_tag_containing_text(soup, tag, text):
    for item in soup.find_all(tag):
        if text in item.getText():
            return item

    return None

def process_to_string(process):
    result = ''
    for step in process:
        result += process_step_to_string(step) + '\n\n'

    return result

def process_step_to_string(process_step):
    return """{}
    Status: {}
    Last page: {}
    Date: {}
    Days: {}""".format(process_step['location'],
                       process_step['status'],
                       process_step['last_page'],
                       process_step['date'],
                       process_step['days_at_location'])

def parse_table(table):
    result = []
    rows = [[cell.getText() for cell in row.find_all('td')] for row in table.find_all('tr')]

    # NOTE(erick): Discarding header
    rows = rows[1:]

    for row in rows:
        if len(row) <= 5: continue

        location, status = parse_first_column(row[1])

        result.append({
            'location' : location.strip(),
            'status' : status.strip(),
            'date' : row[0].strip(),
            'last_page' : row[4].strip(),
            'days_at_location' : row[5].strip()
        })

    return result

def parse_first_column(column):
    splited = column.split('-')

    location = paren_regex.sub('', splited[0])
    status = paren_regex.sub('', splited[1])
    return location, status

def get_process_status(process_id):
    sap_url = 'https://www.sap.ufrj.br/consultar.asp?{}'.format(process_id)

    # TODO(erick): Do not use 'verify=False'. Pass a CA bundle
    response = requests.get(sap_url, verify=False)
    if response.status_code != 200:
        raise Exception('Could not retrieve process page')

    process_page = response.content
    soup = BeautifulSoup(process_page, default_parser)

    process_table_html = find_tag_containing_text(soup, 'table', 'Despachado em')
    if not process_table_html:
        raise Exception('Process table not found')

    process_status = parse_table(process_table_html)

    return process_status
