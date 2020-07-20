from __future__ import print_function
from sending import send
import argparse
import sys
from googleapiclient import sample_tools
import datetime
import sys
import time
import os
import SCAnAPI
from SCAnAPI import execute_request, chosetherightwebmaster, startEndDialog
import csv

keywords = []
with open('keywords.csv') as csvDataFile:
    reader = csv.reader(csvDataFile, delimiter=';')
    for row in reader:
        for item in row:
            if item not in row:
                keywords.append('')
            else:
                keywords.append(item)

ortschaften = []
with open('ortschaften.csv') as csvDataFile:
    reader = csv.reader(csvDataFile, delimiter=';')
    for row in reader:
        for item in row:
            if item not in row:
                ortschaften.append('')
            else:
                ortschaften.append(item)

keywordsPlusOrtschaftenArray = []
for keyword in keywords:
    if ortschaften != []:
        for ortschaft in ortschaften:
            keywordsPlusOrtschaftenArray.append(f'{keyword} {ortschaft}')
    else:
        keywordsPlusOrtschaftenArray.append(keyword)

location = os.getcwd()



argparser = argparse.ArgumentParser(add_help=False)
domain = input('Bitte geben sie eine domain ein (Bsp.: domainname.de): ')
property_uri = domain
start_date, end_date = startEndDialog()
device = input('Wenn Sie ein einzelnes Gerät herausfiltern wollen: mobile/desktop/tablet eingeben. Ansonsten bitte einfach ENTER drücken: ')

def main(argv):
    toolbar_width = len(keywordsPlusOrtschaftenArray)
    responseStartArray = []
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['
    for keyword in keywordsPlusOrtschaftenArray:
        if keyword != '':
          try:
              responseArray = do(keyword, argv, responseStartArray)
          except Exception:
              chosetherightwebmaster(location)
              responseArray = do(keyword, argv, responseStartArray)
          sys.stdout.write("-")
          sys.stdout.flush()
    filename, datei = print2csv(responseArray)
    sys.stdout.write("]\n") # this ends the progress bar
    send(filename, datei, domain)
    print('finished')

def do(keyword, argv, responseStartArray):
    service, flags = sample_tools.init(
        argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/webmasters.readonly')
    if device !='':
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['device'],
            'searchType': 'web',
            'dimensionFilterGroups': [{
                'filters': [{
                    'dimension': 'query',
                    'operator': 'contains',
                    'expression': keyword
                }, {
                'dimension': 'device',
                'expression': device
            }]
            }]
        }
    else:
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['device'],
            'searchType': 'web',
            'dimensionFilterGroups': [{
                'filters': [{
                    'dimension': 'query',
                    'operator': 'contains',
                    'expression': keyword
                }]
            }]
        }
    response = execute_request(service, property_uri, request)
    # print_table(response, 'Keyword', keyword)
    return response2array(keyword, responseStartArray, response)


def print_table(response, title, keyword):
  print(f'\n -- {title}: {keyword}')

  if 'rows' not in response:
    print('Empty response')
    return

  rows = response['rows']
  row_format = '{:<20}' + '{:>20}' * 4
  print(row_format.format('Keys', 'Clicks', 'Impressions', 'CTR', 'Position'))
  for row in rows:
    keys = ''
    # Keys are returned only if one or more dimensions are requested.
    if 'keys' in row:
      keys = u','.join(row['keys']).encode('utf-8').decode()
    print(row_format.format(
        keys, round(row['clicks'], 2), round(row['impressions'], 2), round(row['ctr'], 2), round(row['position'], 2)))


def response2array(keyword, responseArray, response):
    if 'rows' not in response:
        responseArray.append(keyword)
        responseArray.append('-')
        responseArray.append('-')
        responseArray.append('Empty Response')
        return responseArray
    rows = response['rows']
    for row in rows:
        keys = ''
        # Keys are returned only if one or more dimensions are requested.
        if 'keys' in row:
            keys = u','.join(row['keys']).encode('utf-8').decode()
        responseArray.append(keyword)
        responseArray.append(keys)
        responseArray.append(round(row['clicks'], 2))
        # responseArray.append(row['impressions'])
        # responseArray.append(row['ctr'])
        responseArray.append(round(row['position'], 2))
    return responseArray

def print2csv(array):
    datei = f'REPORT_{domain}_{device}_abgerufen_am_{datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")}.csv'
    filename = f'{location}\\Reports\\{datei}'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['keywords', 
                      'device',
                      'clicks', 
                      # 'impressions', 
                      # 'ctr', 
                      'position']
        csvWriter = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames, quoting=csv.QUOTE_NONE)
        newIterator = iter(array)
        csvWriter.writeheader()
        for item in range(0, int(len(array)/4)):
            csvWriter.writerow({'keywords': next(newIterator),
                                'device': next(newIterator),
                                'clicks': next(newIterator),
                                # 'impressions': next(newIterator),
                                # 'ctr': next(newIterator),
                                'position': next(newIterator)
                                })
    return filename, datei

if __name__ == '__main__':
  main(sys.argv)
