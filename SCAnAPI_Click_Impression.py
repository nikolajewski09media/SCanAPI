from __future__ import print_function

import argparse
import sys
from googleapiclient import sample_tools
import datetime
import sys
import time
from SCAnAPI import execute_request, chosetherightwebmaster, startEndDialog
import os
import csv

domains = []
with open('domains.csv') as csvDataFile:
    reader = csv.reader(csvDataFile, delimiter=';')
    for row in reader:
        for item in row:
            if item not in row:
                domains.append('')
            else:
                domains.append(item)

location = os.getcwd()

argparser = argparse.ArgumentParser(add_help=False)

start_date, end_date = startEndDialog()

def main(argv):
    toolbar_width = len(domains)
    responseStartArray = []
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['
    for domain in domains:
        if domain != '':
          try:
              responseArray = do(domain, argv, responseStartArray)
          except Exception:
              chosetherightwebmaster()
              responseArray = do(domain, argv, responseStartArray)
          sys.stdout.write("-")
          sys.stdout.flush()
    print2csv(responseArray)
    sys.stdout.write("]\n")  # this ends the progress bar
    print('finished')

def do(domain, argv, responseStartArray):
    service, flags = sample_tools.init(
        argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/webmasters.readonly')
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'searchType': 'web',
    }
    response = execute_request(service, domain, request)
    #print_table(response, 'domain', domain)
    return response2array(domain, responseStartArray, response)


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
        keys, row['clicks'], row['impressions'], row['ctr'], row['position']))


def response2array(domain, responseArray, response):
    if 'rows' not in response:
        responseArray.append(domain)
        #responseArray.append('-')
        responseArray.append('-')
        # responseArray.append('-')
        # responseArray.append('-')
        responseArray.append('Empty Response')
        return responseArray
    rows = response['rows']
    for row in rows:
        keys = ''
        # Keys are returned only if one or more dimensions are requested.
        if 'keys' in row:
            keys = u','.join(row['keys']).encode('utf-8').decode()
        responseArray.append(domain)
        #responseArray.append(keys)
        responseArray.append(int(row['clicks']))
        responseArray.append(int(row['impressions']))
        # responseArray.append(row['ctr'])
        # responseArray.append(round(row['position'], 2))
    return responseArray

def print2csv(array):
    with open(f'{location}\\Reports\\REPORT_Clicks_{datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")}.csv', 'w', newline='') as csvfile:
        fieldnames = ['domain',
                      #'device',
                      'clicks', 
                      'impressions'
                      # 'ctr',
                      # 'position'
                      ]
        csvWriter = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames, quoting=csv.QUOTE_NONE)
        newIterator = iter(array)
        csvWriter.writeheader()
        for item in range(0, int(len(array)/3)):
            csvWriter.writerow({'domain': next(newIterator),
                                #'device': next(newIterator),
                                'clicks': next(newIterator),
                                'impressions': next(newIterator),
                                # 'ctr': next(newIterator),
                                # 'position': next(newIterator)
                                })

if __name__ == '__main__':
    main(sys.argv)
