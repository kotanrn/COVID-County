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
###        Add error handling if raw_input country, state, or county doesn't exist within the list/set

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


# How many days of data do we want to process?
# First available day with county-levle fidelity: 03-22-2020
#global today
today = date(date.today().year,date.today().month,date.today().day)

#global first_available
first_available = date(2020,03,22)

#global days
days = (today - first_available).days






def format_date():
    # Allow function to modify global variables
    global most_recent
    global cwd
    global glb_chosen
    global days
    global formatted_data
    
    # Status update
    print "\n[+++] Formatting dates"
    
    # Calculate dates, format properly as MM-DD-YYYY
    i = 0
    while i <= days:
        formatted_data.append({'date': ((date.today() - timedelta(days = i)).strftime('%m-%d-%Y')), 'active': '0', 'delta': '0'})
        i += 1
        
    #pprint(formatted_data)
    #print len(formatted_data)

    
    #print "Values in formatted_data[]:"
    #pprint(formatted_data)

    print '\n[+++] Dates properly set'
    sleep(.75)


def get_data():
    # Allow function to modify global variables
    global most_recent
    global cwd
    global glb_chosen
    global days
    global formatted_data
    
    user_days = raw_input("\nHow many days of data do you want? (Hit enter to use current max of %i) > " % (days))

    if user_days != '':
        user_days = int(user_days)
        
        if user_days > days:
            print '\n\n[*****] Error! There aren\'t that many days of county-level data! Exiting...'
            sys.exit()
            
        elif user_days < 0:
            print '\n\n[*****] Error! You can\'t calculate negative days! Exiting...'
            sys.exit()
            
        elif user_days == 0:
            print '\n\n[*****] Zero days of analysis means do nothing! Exiting...'
            sys.exit()
            
        elif user_days < days:
            days = user_days

    
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

    # What date / data is most recently available?
    #print "\n[+++] Most recent data: %s" % (most_recent)

    sleep(.75)

    return most_recent



def select_region():
    # Allow function to modify global variables
    global most_recent
    global cwd
    global glb_chosen
    global days
    global formatted_data
    
    print "\n[+++] Starting select_region()"

    # Get Combined_key if the user has one already
    glb_chosen = raw_input("\nIf you have a Combined_key type / paste it here, otherwise just hit the enter key > ")
    if glb_chosen != '':
        return glb_chosen

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
        
    sleep(.75)


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
    csv_file.close()

    if len(state_uniq) == 1:
        with open('%s/%s.csv' % (cwd, most_recent), mode='r') as csv_file:
            columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
            csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')

            for r, rows in enumerate(csv_dict):
                if rows['Country_Region'] == '%s' % country:
                    glb_chosen = rows['Combined_Key']
                    print 'glb_chosen = %s' % (glb_chosen)
        csv_file.close()
        return glb_chosen
        
    else:
            pprint(state_uniq)
            state = raw_input("\nChoose a state (enter it **exactly** what is between the quotes or the script will fail. > ")
            print '\n\nYou have chosen %s' % (state)

        
    sleep(.75)
    

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

    csv_file.close()

    if len(county_uniq) == 1:
        with open('%s/%s.csv' % (cwd, most_recent), mode='r') as csv_file:
            columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
            csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')

            for r, rows in enumerate(csv_dict):
                if rows['Province_State'] == '%s' % state:
                    glb_chosen = rows['Combined_Key']
                    print 'glb_chosen = %s' % (glb_chosen)
        csv_file.close()
        return glb_chosen
        
    else:
        pprint(county_uniq)
        county = raw_input("\nChoose a county (enter it **exactly** what is between the quotes or the script will fail. > ")
        print '[+] You have chosen %s' % (county)

    csv_file.close()
            


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
    
    sleep(.75)

    return glb_chosen


def process_data():    
    # Allow function to modify global variables
    global most_recent
    global cwd
    global glb_chosen
    global days
    global formatted_data
    
    print "\n[+++] Starting process_data()"
    print '[+] Combined_Key:\t%s' % (glb_chosen)


    # Getting historical values
    print "[+] Getting historical values"
    i = days

    while i >= 0:
        if formatted_data[i]['date'] != "Nope":
            with open('%s/%s.csv' % (cwd, formatted_data[i]['date']), mode='r') as csv_file:
                columns = ['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']
                csv_dict = csv.DictReader(csv_file, fieldnames=columns, delimiter=',')
                
                for k, row in enumerate(csv_dict):
                    if row['Combined_Key'] == ('%s' % glb_chosen):
                        if row['Active'] == '0':
                            formatted_data[i]['active'] = row['Confirmed']    # If there are no cases in "Active" column, then use "Confirmed" column.
                        else:
                            formatted_data[i]['active'] = row['Active']

                        #print 'Value of formatted_data[%i][\'active\']: %s' % (i, formatted_data[i]['active'])

            csv_file.close()
            
        i -= 1


    # Calculate delta values
    print "[+] Calculating delta values"
    i = days
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
    i = days

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
    
    sleep(.75)


    # Format active infection data for plotting
    print '\n[+++] Processing data'
    print '[+] Preparing active infection data for plotting'
    
    fig = plt.gcf()
    fig.set_size_inches(10, 6)

    plot_active = []
    plot_date = []

    i = days
    while i >= 0:
        if formatted_data[i]['date'] != "Nope":
            plot_active.append(int(formatted_data[i]['active']))
            plot_date.append(formatted_data[i]['date'])
        i -= 1

    # Documentation for line styles, colors, etc: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
    plt.plot(plot_date, plot_active, color='r', marker='o', linewidth=3, label='Active infections')
    plt.xticks(rotation=270)                                                # Rotate x-axis label to make it readable
    plt.title('COVID infection data for %s (%i days)' % (glb_chosen, days)) # Set plot's title
    plt.xlabel('Date')                                                      # Set plot's x-axis label
    plt.ylabel('Active infections')                                         # Set plot's y-axis label

    
    # Calculate Rt values
    print '[+] Calculating Rt values'


    # Show plotted data
    print '[+] Saving diagram as %s %s %s days.png' % (most_recent, glb_chosen, days)
    plt.legend()                                                        # Show legend on plot
    plt.tight_layout()                                                  # Make sure labels fit on diagram
    plt.savefig('%s %s %s days.png' % (most_recent, glb_chosen, days))  # Save the diagram
    plt.show()                                                          # Show the diagram on the screen

    # Tell user combined key for future runs
    print '\n\n[+++] For future plotting of this same location, use the combined key: %s' % (glb_chosen)
    
    
    




#Common combined keys:
#   Bell, Texas, US
#   Coryell, Texas, US
#   Lampasas, Texas, US



format_date()

get_data()

select_region()

process_data()
