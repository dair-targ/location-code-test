# Introduction

Welcome to the coding challenge.

You are taking a spontaneous trip to a European city and want to find out a bit about it before you go. Being a 
rather nerdy type, you want to create an API that can be used to pull together multiple sources of information about 
a city. 

This repository is the start of making that API. The API uses the python Tornado web framework (the version is in the requirements.txt 
file and can be installed with pip) to expose an api that allows you to request information about a city. 

The minimum data points that you want the API to return about a city are:

* Current temperature in celsius. 
* A text description of the current weather
* The population of the city
* The number of bars in the city
* The quality of the public transport in the city

There is no limit to the amount of information that you can collect, but there are basic tests that check for the minimum data 
listed above.

You also want to develop a method of ranking cities. To do this, you need to create a unique 'city score' per city based 
on information of your choosing. There are no restrictions on how you decide to score a city, but given that you are
planning on travelling to the city today, the current weather needs to be taken into account. 

There is an accompanying csv file (details below) with other city data that can be used to assist you in creating the city score.
Each city score should be out of 10, and multiple cities should be comparable with a single call to the API. 


## Instructions

Clone this repository and then create your own new repository for your code changes. Bitbucket have a free tier in case 
you don't already have an account on a GIT host. Once complete, please send a link to your repository to 
info@edgetier.com.

To get started on the coding, install [Tornado](http://www.tornadoweb.org/en/stable/) via Pip and run the tests in 'test_location_handler.py' to 
exercise the code. You can also run the API by running the 'location\_api.py' file.

There are two routes that need to be completed which can be found in files:

* /app/location/_data/_handler.py 
* /app/location/_comparison\_handler.py 

In both cases you must complete the GET route. In tornado this is achieved by completing the get() function and 
returning data as shown in the initial version of the get() functions.

The location\_data\_handler get() function expects a city name to be passed into the URL and returns data about that city. 

The location\_comparison\_handler route expects a list of cities to be passed in and returns the city score and rank for 
that city. E.g. if five cities are passed in, it will calculate the city score for each city and the rank of each city 
compared to the other cities that were passed in.

If running the server locally, sample valid routes are:

* http://127.0.0.1:8484/location-data/cityname
* http://127.0.0.1:8484/location-comparison/cities=[cityname1,cityname2,cityname3]

There are sample test in /tests/test\_location\_handler.py file that exercise the calls to the GET routes. Currently, 
these tests do not all pass, or pass because dummy data is returned from the routes. The objective of this 
exercise is not to make the tests pass, but to complete the APIs so that they return accurate and relevant data and 
allow you to make the right decision on what city to visit. 

Please structure and write code as if it is to be used in a production environment, or clearly document changes you 
would make before putting the code into production. Use Python 3.5+.


## Useful Data Sources
Feel free to use whatever data sources you see fit, but here are some sample ones:

Meta weather API for real-time weather information: https://www.metaweather.com/api/

There is a CSV file in the 'data' directory that contains sample information about 500 European cities. In this file,
the cities are ranked by population and there are various other details about each city. Aside from the population, 
all other columns contain random data. The columns in this file are:

* Index: The numeric index for each row/city
* City: The city name
* Country: The country the city is in
* Population: The population of the city within city limits
* Bars: Number of bars within the city limits 
* Museums: Number of museums within the city limits
* Public Transport: Public transport rating out of 10 (10 being the best service)
* Crime Rate: Crime rate out of 10 (10 being highest rate of crime)
* Average Hotel Room Price: The average price in Euros of a hotel room per night


List of other open APIs that can be used to retrieve data: https://github.com/toddmotto/public-apis#weather


