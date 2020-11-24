## 🛩 CIS 9650 Fall 2020 Group Project: United States Domestic Airfare Prediction
Group Members: Anna Bae, Dewan Choudhury, Nick Cox, Janerisa Encarnacion, Rebeka Haque, Duyen Nguyen

### 1. Business Understanding

The objectives of this project are to:
1. Build a multiple regression model to predict the price of US domestic airfares using a base set of numeric and categorical features (origin, destination, airline, class, month of travel and number of stops on route).
2. Add additional features to the data-set to determine if each individually has a positive or negative effect on the effectiveness of the model to predict airfares, e.g., weather, monthly demand, monthly oil price, politics and happiness.



### 2. Data Mining

#### AirFare Data:
The primary source of data for this project is the Airline Origin and Destination Survey (DB1B) database made available by the Bureau of Transportation Statistics (BTS) at https://www.transtats.bts.gov/DatabaseInfo.asp?DB_ID=125.  The Airline Origin and Destination Survey is a 10% sample of airline tickets from reporting carriers collected by the Office of Airline Information of the Bureau of Transportation Statistics. Data includes origin, destination and other itinerary details of passengers transported. This database is used to determine air traffic patterns, air carrier market shares and passenger flows.

The database has three tables: DB1BCoupon, DB1BMarket and DB1BTicket.  The first contains coupon-specific information for each domestic itinerary, the second contains directional market characteristics of each domestic itinerary and the last contains summary characteristics of each domestic itinerary.  The first two tables were used for the purposes of this project.

For the purposes of this project a flight is defined as a journey from an origin airport to a destination airport with zero or more stops in between.

**DB1BCoupon:** 
ITIN_ID       To join with the DB1BMarket table.
FARE_CLASS    The class of travel for the flight: Coach (X, Y), Business (C, D) First (F, G).  This field is not available in the DB1BMarket table.

**DB1BMarket:** 
ITIN_ID                     To join with the DB1BCoupon table.
YEAR                        Yyear the flight took place.  This field was not used.
QUARTER                     Quarter the flight took place.
ORIGIN_AIRPORT_ID	ORIGIN    ID for the origin airport of the flight.
DEST_AIRPORT_ID	DEST        ID for the destination airport of the flight.
AIRPORT_GROUP               List of airports that the flight operated through, including origin and destination.
TICKET_CARRIER              Airline operating the flight.
BULK_FARE                   An indicator to signify whether the flight was purchased in bulk.
PASSENGERS                  Number of passengers booked together on the flight.
MARKET_FARE                 Actual fare for the flight.  This is the target value that we will be trying to predict.
MARKET_MILES_FLOWN          Actual miles flown.
NONSTOP_MILES               Nonstop miles directly from origin to destination.





### 3. Data Cleaning

xxx


### 4. Data Exploration

xxx


### 5. Feature Engineering

xxx


### 6. Predictive Modelling

xxx


### 7. Data Visualization
