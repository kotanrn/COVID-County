#!/bin/usr/env python

####################################################################################################
### County.py
###
### Written in python 2.7
###
###
### Created by: CW2 Rob Kotan (350F)
###             robert.n.kotan.mil@mail.mil
###
###
### This script uses the John's Hopkins COVID-19 data to visualize infection and recovery rates
### of a user selected county using matplotlib. The goal is to calculate R sub t to identify if
### the selected county is "safe" for a Service Member to travel to.
###
###
### Special thanks to github user k-sys and the creators of Rt Tool.ipynb for inspiring use of
### matplotlib in a meaningful way.
###
###
### k-sys github: https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb
###
### Rt Tool collaberation: https://colab.research.google.com/drive/1hs1fAfqvx_z5-rh83-0WTVOGGVVRRBNL
####################################################################################################


### Can we set this up to run on a simple Apace2 instance?
### That would make selecting states and counties a fuck ton easier,
### plus we might be able to get someone to fund a VPS
###
### To do:
###        Account for countries with no states or states with no counties. Possibly use an if statement to ID
###        if the state or county set is empty. Then just set and return glb_chosen.
###
###        Add error handling if raw_input country, state, or county doesn't exist within the list

# Import dependencies
from datetime import date
from datetime import timedelta
import os
from pprint import pprint
import requests
import csv
from time import sleep
import matplotlib



# Declare a global variable for formatted dates
formatted_data = []


# Declare a global variable for most recent and available date / data
global most_recent
most_recent = ''


# Declare a global variable to store current working directory
cwd = os.getcwd()


# Declare a global variable to store the chosen location
global glb_chosen
glb_chosen = ''





def format_date():
    # Status update
    print "\n[+++] Formatting dates"
    
    # Get today's date, format properly as MM-DD-YYYY    
    formatted_data.append({'number': '0', 'date': ((date.today() - timedelta(days = 0)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    
    # Calculate last 16 days formats
    formatted_data.append({'number': '1', 'date': ((date.today() - timedelta(days = 1)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '2', 'date': ((date.today() - timedelta(days = 2)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '3', 'date': ((date.today() - timedelta(days = 3)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '4', 'date': ((date.today() - timedelta(days = 4)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '5', 'date': ((date.today() - timedelta(days = 5)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '6', 'date': ((date.today() - timedelta(days = 6)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '7', 'date': ((date.today() - timedelta(days = 7)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '8', 'date': ((date.today() - timedelta(days = 8)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '9', 'date': ((date.today() - timedelta(days = 9)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '10', 'date': ((date.today() - timedelta(days = 10)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '11', 'date': ((date.today() - timedelta(days = 11)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '12', 'date': ((date.today() - timedelta(days = 12)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '13', 'date': ((date.today() - timedelta(days = 13)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '14', 'date': ((date.today() - timedelta(days = 14)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '15', 'date': ((date.today() - timedelta(days = 15)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
    formatted_data.append({'number': '16', 'date': ((date.today() - timedelta(days = 16)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})

    
    #print "Values in formatted_data[]:"
    #pprint(formatted_data)

    print '\n[+++] Dates properly set'
    sleep(1.4)


def get_data():
    print "\n[+++] Checking data exists"
    # Set the base url for where we download data
    base_url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"


    # Do the data points exist?
    i = 16
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

    # What date / data is most recently available?
    #print "\n[+++] Most recent data: %s" % (most_recent)

    sleep(1.4)

    return most_recent



def select_region():
    # Give drop down using ??? to show states for user to select
    # Give drop down to show states for user to select
    print "\n[+++] Starting select_region()"

    # Get country
    with open('%s/%s.csv' % (cwd, most_recent), mode='r') as csv_file:
        columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
        csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')

        country_list = []
        for i, row in enumerate(csv_dict):
            country_list.append(row['Country_Region'])

        country_list.sort()
        country_uniq = set(country_list)
        pprint(country_uniq)

        csv_file.close()

        country = raw_input("\nChoose a country (enter **exactly** what is between the quotes or the script will fail. > ")
        
        print '\n\nYou have chosen %s' % (country)
        
    sleep(1.4)


    # Get state
    with open('%s/%s.csv' % (cwd, most_recent), mode='r') as csv_file:
        columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
        csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')

        state_list = []
        for j, row in enumerate(csv_dict):
            if row['Country_Region'] == '%s' % country:
                #print "%s" % (row['Province_State'])
                state_list.append(row['Province_State'])

        state_list.sort()
        state_uniq = set(state_list)
        pprint(state_uniq)

        csv_file.close()

        state = raw_input("\nChoose a state (enter it **exactly** what is between the quotes or the script will fail. > ")
        
        print '\n\nYou have chosen %s' % (state)
        
    sleep(1.4)
    

    # Get county
    with open('%s/%s.csv' % (cwd, most_recent), mode='r') as csv_file:
        columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
        csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')

        county_list = []
        for k, row in enumerate(csv_dict):
            if row['Country_Region'] == ('%s' % country):
                if row['Province_State'] == ('%s' % (state)):
                    county_list.append(row['Admin2'])

        county_list.sort()
        county_uniq = set(county_list)
        pprint(county_uniq)

        csv_file.close()
        

    county = raw_input("\nChoose a county (enter it **exactly** what is between the quotes or the script will fail. > ")

    print '[+] You have chosen %s' % (county)

    # Get Combined_Key
    with open('%s/%s.csv' % (cwd, most_recent), mode='r') as csv_file:
        columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
        csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')

        county_list = []
        for k, row in enumerate(csv_dict):
            if row['Country_Region'] == ('%s' % country):
                if row['Province_State'] == ('%s' % (state)):
                    if row['Admin2'] == ('%s' % (county)):
                        glb_chosen = row['Combined_Key']

        csv_file.close()
        
    print '\n[+] Your choices:'
    print '[+] \tCountry:\t%s' % (country)
    print '[+] \tState:\t\t%s' % (state)
    print '[+] \tCounty:\t\t%s' % (county)
    print '[+] \tCombined_Key:\t%s' % (glb_chosen)
    
    sleep(1.4)

    return glb_chosen


def process_data(glb_chosen):
    print "\n[+++] Starting process_data()"


    # Getting historical values
    print "[+] Getting historical values"
    i = 16

    while i >= 0:
        if formatted_data[i]['date'] != "Nope":
            with open('%s/%s.csv' % (cwd, formatted_data[i]['date']), mode='r') as csv_file:
                columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
                csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')
                
                for k, row in enumerate(csv_dict):
                    if row['Combined_Key'] == ('%s' % glb_chosen):
                        #print 'Setting formatted_data[%i][\'active\'] as %s' % (i,row['Active'])
                        formatted_data[i]['active'] = row['Active']

                        #print 'Value of formatted_data[%i][\'active\']: %s' % (i, formatted_data[i]['active'])

            csv_file.close()
            
        i -= 1


    # Calculate delta values
    print "[+] Calculating delta values"
    i = 15
    while i >= 0:
        if formatted_data[i]['date'] != "Nope":
            if formatted_data[i-1]['date'] != "Nope":
                formatted_data[i]['delta'] = ((int(formatted_data[i]['active']) - int(formatted_data[i-1]['active'])))

        i -= 1
    #pprint(formatted_data)


    # Calculate range high and low
    print "[+] Calculating range values"
    
    high = 0
    low = 1000000
    delta_range=0
    i = 15

    '''
    print(type(i))
    print(type(high))
    print(type(low))
    '''


    while i >= 0:
        if formatted_data[i]['date'] != "Nope":
            if int(formatted_data[i]['active']) > high:
                high = int(formatted_data[i]['active'])
                    
            if int(formatted_data[i]['active']) < low:
                low = int(formatted_data[i]['active'])


        i -= 1
    
    delta_range = high - low

    print '[+] High:   %i' % (high)
    print '[+] Low:    %i' % (low)
    print '[+] Range:  %i' % (delta_range)
    
    sleep(1.4)

    
    # Calculate Rt values
    
    
    # Save matplotlib graphics as formatted_date + County + State + .



format_date()
most_recent = get_data()

print '\n[+++] Most recently available data: %s' % (most_recent)

process_data(select_region())
