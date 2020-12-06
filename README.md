## 🛩 CIS 9650 Fall 2020 Group Project: United States Domestic Airfare Prediction
**Group Members:** Anna Bae, Dewan Choudhury, Nick Cox, Janerisa Encarnacion, Rebeka Haque, Duyen Nguyen

### 1. Problem Statement

The objectives of this project are to:
1. Build a multiple regression model to predict the price of US domestic airfares using a base set of numeric and categorical features (origin, destination, airline, class, month of travel and number of stops enroute).  Develop a web interface to interact with the model.
2. Add additional features to determine if each individually has a positive or negative effect on the effectiveness of the model to predict airfares, e.g., weather, monthly demand, monthly oil price, politics, happiness, McDonalds locations and prosperity.  

Our hypothesis is that inclusion of demand and oil price would increase the effectiveness of the model, weather may increase the effectiveness of the model due to its likely impact on demand for flights, however politics, happiness, McDonalds locations and prosperity should not increase the effectiveness of the model.


### 2. Data Mining

#### AirFare Data:
The primary source of data for this project is the Airline Origin and Destination Survey (DB1B) database made available by the Bureau of Transportation Statistics (BTS) at https://www.transtats.bts.gov/DatabaseInfo.asp?DB_ID=125.  The Airline Origin and Destination Survey is a 10% sample of airline tickets from reporting carriers collected by the Office of Airline Information of the Bureau of Transportation Statistics. Data includes origin, destination and other itinerary details of passengers transported. This database is used to determine air traffic patterns, air carrier market shares and passenger flows.

The database has three tables: DB1BCoupon, DB1BMarket and DB1BTicket.  The first contains coupon-specific information for each domestic itinerary, the second contains directional market characteristics of each domestic itinerary and the last contains summary characteristics of each domestic itinerary.  The first two tables were used for the purposes of this project.  We downloaded data for the period January 1 to December 31, 2019.

For the purposes of this project a flight is defined as a journey from an origin airport to a destination airport with zero or more stops in between.

The data files we obtained from the BTS are available on this OneDrive: https://1drv.ms/u/s!AoQYKisAOe1libAJ8n00FqjMYMS7tA?e=jcbSLh, as they are too large to be hosted on GitHub.  The BTS Data folder contains 8 files, 4 from the DB1BCoupon table and 4 from the DB1BMarket table.  Each file contains data for a quarter in 2019.

#### Other Data:
The remaining data was obtained from a variety of sources, as listed below.  This data can be found either in the *state_info.csv* file on the OneDrive or in the *cleanse.py* file.  The data in the *state_info.csv* file represents the following, based on column: 1-2 state, 3-14 average temperature per month January to December, 15 democratic or republican state, 16 happiness index, 17 McDonalds locations per 100,000 capita, and 18 prosperity index.

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

**The United States Prosperity Index:** An index is calculated for each state based on safety and security, personal, freedom, governance, social capital, investment environment, enterprise conditions, market access and infrastructure, economic quality, living conditions, health, education and natural environment.\
Source: Legatum Institute\
https://li.com/wp-content/uploads/2019/07/USPI_web.pdf


### 3. Data Cleaning, Data Exploration and Feature Engineering

The *cleanse.py* file provides the code we used to clean the data obtained from the BTS.  The following steps were undertaken:
* Concatenation of the quarterly datasets into a single dataset for both DB1BCoupon and DB1BMarket and then to merge the resulting two datasets into one.
* Records that may skew the prediction model were removed, e.g. small regional airlines, null values, bulk reservations.
* Unneeded columns were dropped.

A random sample of 10 million flight records was taken from the cleaned dataset of approximately 72 million records to continue the process.

During data exploration we identified a significant number of outliers in both directions, e.g. coach fares over $50,000 and many fares at $5.50.  These outliers were removed from the dataset.

Next we engineered features to better represent non-stop flights, fare class and month of travel.  Features were then added per step 2 of our problem statement for weather, oil price, demand, politics, happiness, McDonalds locations and propensity.  This data either came from the *state_info.csv* file on the OneDrive or was included in the *cleanse.py* file.  A mapping of airport to the state it resides in was obtained from the *airport_codes_all.csv* file on the OneDrive.

Following all of these steps, 8.7 million records remained for model training and validation and were output to the *cleaned_data.csv* file, available from the OneDrive.


### 4. Predictive Modelling

Data for training the model was imported from the *cleaned_data.csv* file, as described in the section above.

The *model.py* file provides the code we used to train and vaildate several multiple regression models - Random Forest, Light BGM and XGBoost.  XGBoost proved to be the  most effective model, so we then used GridSearchCV to tune the hyperparameters, thus further enhancing the effectiveness of the predictive model.  The effectiveness of the model was determined by the R2 Score and Mean Absolute Value (avg. error of prediction).

Following training of the model using the base set of features, we introduced the additional features to the model one at a time to determine whether each would increase or decrease the effectiveness of the model compared to the model using just the base set of features.  The PPT file included in our GitHub repo provides the results.

The trained model, using the base set of features was saved to the *model.sav* file for use by the web user interface.


### 5. Web User Interface

The *app.py* files provides the code we used to create the Flask and Google Map web user interface.  Data from the *airport_codes.csv* file on the OneDrive was used to map from BTS airport codes to airport codes more familiar to users (e.g., JFK, LAX) and to provide GPS coordinates for the Google Map API to map flight routes.

The web application is available at http://nickdcox.pythonanywhere.com/ and can be used just like a standard airline booking engine, by selecting options from the drop-down boxes and clicking predict.  The web application utilizes the XGBoost model with the base set of features.
