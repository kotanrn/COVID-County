#!/bin/usr/env python

####################################################################################################
### States.py
###
### Written in python 2.7
###
###
### Created by: CW2 Rob Kotan (350F)
###             robert.n.kotan.mil@mail.mil
###
###
### This script uses the John's Hopkins COVID-19 data to get all US state's active infection number
###
####################################################################################################




# Import dependencies
from datetime import date
from datetime import timedelta
import os
from pprint import pprint
import requests
import csv
from time import sleep
from matplotlib import pyplot as plt
import sys
from operator import itemgetter



# Declare a global variable for formatted dates
formatted_data = []


# Declare a global variable for most recent and available date / data
#global most_recent
most_recent = ''


# Declare a global variable to store current working directory
#global cwd
cwd = os.getcwd()


# Declare a global variable to store the chosen location
#global glb_chosen
glb_chosen = ''


#global days
days = 1


US_Total = 0





def format_date():
    # Allow function to modify global variables
    global days
    global formatted_data
    
    # Status update
    print "\n[+++] Formatting dates"
    
    # Calculate dates, format properly as MM-DD-YYYY
    i = 0
    while i <= days:
        formatted_data.append({'date': ((date.today() - timedelta(days = i)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
        i += 1

    print '\n[+++] Dates properly set'
    sleep(.75)


def get_data():
    # Allow function to modify global variables
    global most_recent
    global cwd
    global glb_chosen
    global days
    global formatted_data
    global US_Total

    
    print "\n[+++] Checking data exists"
    # Set the base url for where we download data
    base_url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"


    # Do the data points exist?
    i = days

    #print "%s" % (formatted_data[i])
    while i >= 0:
        check = cwd + '/' + formatted_data[i]['date'] + '.csv'
        #print "%s" % check

        # Does the data exist locally?
        if os.path.exists(check):
            print "[+] %s exists locally" % formatted_data[i]['date']
            most_recent = formatted_data[i]['date']
        
        else:
            #print "%s doesn't exist locally, checking GitHub" % check
            url=base_url+formatted_data[i]['date']+'.csv'
            #print "%s" % (url)
            response = requests.get(url)
            print "[+] %s does not exist locally, checking GitHub" % formatted_data[i]['date']
        
            if response.status_code == 200:
                print "[+] %s exists on GitHub; downloading..." % formatted_data[i]['date']
                # Save the data
                fd = open("%s.csv" % (formatted_data[i]['date']),"w")
                #fd = open("test.csv","w")
                fd.write(response.content)
                fd.close()
                most_recent = formatted_data[i]['date']
            else:
                print "[***] %s doesn't exist on locally or on GitHub" % formatted_data[i]['date']
                formatted_data[i]['date'] = "Nope"
        i -= 1


    sleep(.75)

    return most_recent



def select_region():
    # Allow function to modify global variables
    global most_recent
    global cwd
    global glb_chosen
    global days
    global formatted_data
    global US_Total
    
    print "\n[+++] Starting select_region()"
    

    # Set country
    country = 'US'

    with open('%s/%s.csv' % (cwd, most_recent), mode='r') as csv_file:
        columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
        csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')

        state_list = []
        for j, row in enumerate(csv_dict):
            if row['Country_Region'] == '%s' % country:
                state_list.append(row['Province_State'])
                US_Total += int(row['Active'])

    csv_file.close()
    print "US Total: %i\n\n" % US_Total
    state_list = []
    state_totals = []

    # Get state data
    with open('%s/%s.csv' % (cwd, most_recent), mode='r') as csv_file:
        columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
        csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')

    

        for j, row in enumerate(csv_dict):
            if row['Country_Region'] == '%s' % country:
                #print "%s" % (row['Province_State'])
                state_list.append(row['Province_State'])

        state_list.sort()
        state_uniq = set(state_list)
        #pprint(state_uniq)

    csv_file.close()

    for i in state_uniq:
        #print i
        state_totals.append({'name': i, 'active': 0})

    for state in state_totals:
        #print state['name']

        with open('%s/%s.csv' % (cwd, most_recent), mode='r') as csv_file:
            columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
            csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')

            for j, row in enumerate(csv_dict):
                if row['Province_State'] == '%s' % state['name']:
                    state['active'] += int(row['Active'])
                    #print "State var name: %s, state var total: %i, row state %s, row active %s" % (state['name'], state['active'], row['Province_State'], row['Active'])
        csv_file.close()

    sorted_list = sorted(state_totals, key=itemgetter('name'))
    pprint(sorted_list)
    #pprint()





#Common combined keys:
#   Bell, Texas, US
#   Coryell, Texas, US
#   Lampasas, Texas, US



format_date()

get_data()

select_region()

#process_data()
