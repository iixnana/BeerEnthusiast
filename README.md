# BeerEnthusiast
Given starting location LATITUDE/LONGITUDE, there is a list of breweries. Helicopter has enough fuel for 2000km. The task is to visit breweries and collect as many beers as possible and go back home. Original location for starting is 51.355468, 11.100790.

# Greedy*
I've constructed an algorithm based on general ideas of A* and Greedy algorithms. First step is to filter the huge database to circle ratio of 1000km as it's impossible to go more far and still return home. Later, determine the best direction (North-East, South-East, North-West, South-West) and best layer (circle is divided into 3 smaller sections) by counting how many beer types are in the area. Then - the journey starts from there - from a sorted and filtered list, we pick best brewery (of course, the one which has most beer types) as our main goal, but also let it do some detours on the way (setting mini goals along the way). Once reached main goal, pick another big goal and repeat, until we run out of fuel - leaving us with only the right amount to go home. *Original starting point results in collecting 200 types of beer*

# Project
This project was developed on Python, using Django web framework. IDE: PyCharm, Database: MySQL (beertest.sql is located in data folder), Requirements: requirements.txt
