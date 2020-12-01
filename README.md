## 🛩 CIS 9650 Fall 2020 Group Project: United States Domestic Airfare Prediction
**Group Members:** Anna Bae, Dewan Choudhury, Nick Cox, Janerisa Encarnacion, Rebeka Haque, Duyen Nguyen

### 1. Business Understanding

The objectives of this project are to:
1. Build a multiple regression model to predict the price of US domestic airfares using a base set of numeric and categorical features (origin, destination, airline, class, month of travel and number of stops on route).
2. Add additional features to the data-set to determine if each individually has a positive or negative effect on the effectiveness of the model to predict airfares, e.g., weather, monthly demand, monthly oil price, politics and happiness.


### 2. Data Mining

#### AirFare Data:
The primary source of data for this project is the Airline Origin and Destination Survey (DB1B) database made available by the Bureau of Transportation Statistics (BTS) at https://www.transtats.bts.gov/DatabaseInfo.asp?DB_ID=125.  The Airline Origin and Destination Survey is a 10% sample of airline tickets from reporting carriers collected by the Office of Airline Information of the Bureau of Transportation Statistics. Data includes origin, destination and other itinerary details of passengers transported. This database is used to determine air traffic patterns, air carrier market shares and passenger flows.

The database has three tables: DB1BCoupon, DB1BMarket and DB1BTicket.  The first contains coupon-specific information for each domestic itinerary, the second contains directional market characteristics of each domestic itinerary and the last contains summary characteristics of each domestic itinerary.  The first two tables were used for the purposes of this project.  We downloaded data for the period January 1 to December 31, 2019.

For the purposes of this project a flight is defined as a journey from an origin airport to a destination airport with zero or more stops in between.

**DB1BCoupon:** 
* ITIN_ID - To join with the DB1BMarket table.
* FARE_CLASS - The class of travel for the flight: Coach (X, Y), Business (C, D) First (F, G).  This field is not available in the DB1BMarket table.

**DB1BMarket:** 
* ITIN_ID - To join with the DB1BCoupon table.
* YEAR - Year the flight took place.  This field was not used.
* QUARTER - Quarter the flight took place.
* ORIGIN_AIRPORT_ID	ORIGIN - ID for the origin airport of the flight.
* ORIGIN - Three letter code for the origin airport of the flight.
* DEST_AIRPORT_ID	DEST - ID for the destination airport of the flight.
* DEST - Three letter code for the destination airport of the flight.
* AIRPORT_GROUP - List of airports that the flight operated through, including origin and destination.
* TICKET_CARRIER - Airline operating the flight.
* BULK_FARE - An indicator to signify whether the flight was purchased in bulk.
* PASSENGERS - Number of passengers booked together on the flight.
* MARKET_FARE - Actual fare for the flight.  This is the target value that we will be trying to predict.
* MARKET_MILES_FLOWN - Actual miles flown.
* NONSTOP_MILES - Nonstop mies directly from origin to destination.


#### Other Data:
The remaining data was obtained from a variety of sources, as listed below.

**Historical Crude Oil Prices (2011 – 2019):** An average of oil prices was calculated for each month of the year based on data from 2011 to 2019.\
Source: Inflation Data\
https://inflationdata.com/articles/inflation-adjusted-prices/historical-crude-oil-prices-table/

**Monthly Domestic Scheduled Enplanements on U.S. Airlines 2018:** The total number of domestic enplanements was collected for each month of 2018, the most recent year for which such data is available.\
Source: Bureau of Transportation Statistics (BTS)\
https://www.bts.dot.gov/newsroom/2018-traffic-data-us-airlines-and-foreign-airlines-us-flights

**Electoral College Map for 2016 Presidential Election:** The electoral college map was used to determine if a state voted predominately republican or democrat.\
Source: Business Insider\
https://www.businessinsider.com/final-electoral-college-map-trump-clinton-2016-11

**State Climate Data:** An average high temperature was calculated for each state for each month of the year.\
Source: US Climate Data\
https://www.usclimatedata.com/

**Happiest States in the United States:** A score was calculated for each state based on emotional and physical well-being, work environment and community and environment.\
Source: Wallet Hub\
https://wallethub.com/edu/happiest-states/6959


### 3. Data Cleaning

The first step in cleaning the data was to concatenate the quaterly datasets into a single dataset for both DB1BCoupon and DB1BMarket and then to merge the resulting two datasets into one.

The following cleaning steps were then undertaken to avoid the model being skewed:
* Flights for all airlines (TICKET_CARRIER) other than the top 11 domestic airlines were dropped from the dataset (Top 11: AA, AS, B6, DL, F9, G4, HA, NK, SY, UA, WN)
* Flights without a FARE_CLASS recorded were dropped.
* Flights that were booked as part of a bulk reservation were dropped.
* Flights that were booked for more than 1 passenger were dropped.
* Fields not required for model training were dropped (ITIN_ID, YEAR, ORIGIN, DEST, BULK_FARE, PASSENGERS, NONSTOP_MILES)

This resulted in approximately 72 million flight records.  We then used a Python function to select a random sample of 10 million flight records for model training and validation.


### 4. Data Exploration

Prior to training a model it was important to understand the data we would be using, particularly the MARKET_FARE field.

The first boxplot below shows a distribution of the 10 million fares split by FARE_CLASS.  It shows that there are clearly outliers in the dataset, showing coach fares of more than $50,000.  The second boxplot shows the same distribution but filtered to show only fares under $2,000.  The plots give a very good idea of outliers to remove and also where the majority of the fares are distributed.  The final box plot shows the distribution after the outliers were dropped from the dataset.  We took a conservative approach and removed all fares above and below the box plot whiskers.

<box plot 1> <box plot 2><box plot 3>

In analyzing the MARKET_FARE data we also used a violin chart and histogram to understand the distribution and identify outliers.  The violin plot shows an unusual distribution close to $0 for all fare classes.  Upon inspecting the raw data we saw that there were many fares of $5.50.  Unable to obtain an explanation from the data source, we came to the conclusion that the fares relate to mileage award tickets where the passenger only paid the passenger facility charge for the airports they were transiting through.  The first histogram plot below also shows this unusual distribution.  We dropped all flight records where the MARKET_FARE was less than $30.  The second histogram plot shows the distribution of MARKET_FARE after the outliers were dropped.

<violin plot><hist plot 1><hist plot 2>


### 5. Feature Engineering

In this phase we engineered features to use in model training and validation:
* NON_STOP - To simply the model we converted the AIRPORT_GROUP feature to a binary feature NON_STOP equal to 1 or 0.
* FARE_CLASS - To simply the model we converted FARE_CLASS to Coach, Business and First, rather than C, D, F, G, X and Y.
* QUARTER - Was converted into MONTH to allow for joining with other datasets.  This had no material adverse impact on the model.

The following features were added to extend the base model and determine if they have a positive or negative impact on the prediction of fares:
* TEMP_ORIGIN, TEMP_DEST – Average monthly temperature for origin and destination states.
* OIL_PRICE – Average monthly oil price.
* DEMAND – Monthly US domestic travel demand for origin and destination states.
* POLITICS_ORIGIN, POLITICS_DEST – Political leaning of origin and destination states in the 2016 presidential election.
* HAPPINESS_ORIGIN, HAPPINESS DEST – Happiness of origin and destination states based on multiple factors.

Following feature engineering we checked the correlation between MARKET_FARE and all other features, with the following results:
Feature | Correlation Score
--------|------------------
MARKET_FARE            |	1.000000
FARE_CLASS_Business    |	0.378455
MARKET_MILES_FLOWN     |	0.292465
FARE_CLASS_First      |	0.170475
TICKET_CARRIER_AA     | 	0.077141
TICKET_CARRIER_UA     | 	0.066777
TICKET_CARRIER_DL     | 	0.063281
ORIGIN_HAPPINESS      | 	0.042429
DEST_HAPPINESS       | 	0.040588
TICKET_CARRIER_HA    |  	0.026969
DEMAND                | 	0.020645
OIL_PRICE             | 	0.017098
ORIGIN_TEMP           | 	0.01666
TICKET_CARRIER_AS     | 	0.015838
DEST_TEMP            |	0.014682
DEST_AIRPORT_ID      |  	0.011019
ORIGIN_AIRPORT_ID    | 	0.010058
MONTH                |  	0.005757
TICKET_CARRIER_B6    |	-0.014762
TICKET_CARRIER_SY    |	-0.024571
DEST_POLITICS        |	-0.025608
ORIGIN_POLITICS      | 	-0.027026
TICKET_CARRIER_F9    | 	-0.093829
TICKET_CARRIER_G4    | 	-0.113678
NON_STOP             | 	-0.137562
TICKET_CARRIER_WN    |	-0.144303
TICKET_CARRIER_NK    | 	-0.160832
FARE_CLASS_Coach     | 	-0.415193

Our key observations include the following:
* FARE_CLASS and MARKET_MILES_FLOWN are strongly correlated with MARKET_FARE.
* The airline (TICKET_CARRIER) is generally not strongly correlated with the MARKET_FARE.
* It is noticeable that lower-cost carriers (G4, WN, NK) have a stronger correlation with the MARKET_FARE.
* The origin and destination are not strongly correlated with the MARKET_FARE.
* The month of travel is not strongly correlated with the MARKET_FARE.

Our observations about ORIGIN_HAPPINESS, DEST_HAPPINESS, DEMAND, OIL_PRICE, ORIGIN_TEMP, DEST_TEMP, DEST_POLITICS and ORIGIN_POLITICS are shared below.


### 6. Predictive Modelling

xxx


### 7. Data Visualization
