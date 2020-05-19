#! /bin/bash

# Run COVID scripts in one shot
cd ~/VM\ xfer/COVID\ shit

./County.py 15 "Bell, Texas, US"
./County.py 15 "Coryell, Texas, US"
./County.py 15 "Germany"
./County.py 15 "Sweden"
./County.py 15 "Bulgaria"
./County.py 15 "Hungary"
./County.py 15 "Latvia"
./County.py 15 "Lithuania"
./County.py 15 "Poland"
./County.py 15 "Romania"

./US_time.py 15

./States.py
