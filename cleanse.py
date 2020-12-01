"""

US Domestic Airfare Predictor - Import & Cleanse v2
This program imports files containing flight data, merges the files, cleanse
them and then outputs the result to a csv file for use by a model.

"""

import pandas as pd
from datetime import datetime
import random

# Print time stamp to track progress of code execution.
def timestamp(p):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(p, " =", current_time)

timestamp("Starting")

# ===========================================================================================================
# Import and concatenate flight data files.
# ===========================================================================================================
coupon_19Q1 = pd.read_csv('Origin_and_Destination_Survey_DB1BCoupon_19Q1.csv')
coupon_19Q2 = pd.read_csv ('Origin_and_Destination_Survey_DB1BCoupon_19Q2.csv')
coupon_19Q3 = pd.read_csv ('Origin_and_Destination_Survey_DB1BCoupon_19Q3.csv')
coupon_19Q4 = pd.read_csv ('Origin_and_Destination_Survey_DB1BCoupon_19Q4.csv')
coupon_19 = pd.concat([coupon_19Q1, coupon_19Q2, coupon_19Q3, coupon_19Q4], ignore_index=True)
coupon_19 = coupon_19.drop(coupon_19.columns[-1],axis=1).copy()

market_19Q1 = pd.read_csv('Origin_and_Destination_Survey_DB1BMarket_19Q1.csv')
market_19Q2 = pd.read_csv ('Origin_and_Destination_Survey_DB1BMarket_19Q2.csv')
market_19Q3 = pd.read_csv ('Origin_and_Destination_Survey_DB1BMarket_19Q3.csv')
market_19Q4 = pd.read_csv ('Origin_and_Destination_Survey_DB1BMarket_19Q4.csv')
market_19 = pd.concat([market_19Q1, market_19Q2, market_19Q3, market_19Q4], ignore_index=True)
market_19 = market_19.drop(market_19.columns[-1],axis=1).copy()

flight_data = pd.merge(coupon_19, market_19, on ='ITIN_ID')

timestamp("Completed Merge")
print(flight_data.shape)


# ===========================================================================================================
# Cleanse the combined dataset.
# ===========================================================================================================

# Drop all records for flights not operated by the leading 11 domestic carriers.
flight_data.drop(flight_data[(~flight_data['TICKET_CARRIER'].isin(['AA', 'AS', 'B6', 'DL', 'F9', 'G4', 'HA', 'NK', 'SY', 'UA', 'WN']))].index, inplace = True)

timestamp("Completed Carrier Drop")
print(flight_data.shape)

# Drop records with no Fare Class, as these records can not be used in the predictive model.
flight_data = flight_data.dropna(axis=0, subset=['FARE_CLASS'])

timestamp("Completed Fare Class Drop")
print(flight_data.shape)

# Drop records which are builk fares, as these records may skew the predictive model.
flight_data = flight_data[flight_data['BULK_FARE'] == 0]

timestamp("Completed Bulk Fare Drop")
print(flight_data.shape)

# Drop records where there are multiple passengers, as these records may skew the predictive model.
flight_data = flight_data[flight_data['PASSENGERS'] == 1]

timestamp("Completed Passenger Drop")
print(flight_data.shape)

# Drop records where the ticketing carrier is invalid.
flight_data = flight_data[flight_data['TICKET_CARRIER'] != '99']
flight_data = flight_data[flight_data['TICKET_CARRIER'] != '--']

timestamp("Completed Invalid Carrier Drop")
print(flight_data.shape)

# Drop columns unnecessary for the prediction model.
flight_data = flight_data.drop(['ITIN_ID', 'YEAR', 'ORIGIN', 'DEST', 'BULK_FARE', 'PASSENGERS', 'NONSTOP_MILES'], axis = 1)

timestamp("Completed Unnecessary Columns Drop")
print(flight_data.shape)

# ===========================================================================================================
# Extract random sample of 10m records, from dataset containing approximately 70m records.
# ===========================================================================================================

flight_data_sample = flight_data.sample(n = 10000000)

timestamp("Completed Sample Selection")
print(flight_data_sample.shape)


# ===========================================================================================================
# Feature Encoding
# ===========================================================================================================

# Replace AIRPORT_GROUP with non-stop indicator, 1 if flight is non-stop and 0 if there are stops.  The flight has
# stops if 3 or more airport codes are listed (this is determined by measuring the length of the data).
def stops(airports):
    if len(airports) > 7:
        return 0
    else:
        return 1

flight_data_sample['NON_STOP'] = flight_data_sample.apply(lambda x: stops(x['AIRPORT_GROUP']), axis=1)

timestamp("Completed Nonstop")
print(flight_data_sample.shape)

# Replace FARE_CLASS with simpler designation of Coach, Business or First.
def fareClass(code):
    if code == 'C' or code == 'D':
        return 'Business'
    elif code == 'F' or code == 'G':
        return 'First'
    else:
        return 'Coach'

flight_data_sample['FARE_CLASS'] = flight_data_sample.apply(lambda x: fareClass(x['FARE_CLASS']), axis=1)

timestamp("Completed Fare Class")
print(flight_data_sample.shape)

# Replace quarter with a month randomly selected from within that quarter, e.g. Q1 becomes Jan, Feb or Mar.
def months(quarter):
    if quarter == 1:
        return random.randint(1,3)
    elif quarter == 2:
        return random.randint(4, 6)
    elif quarter == 3:
       return random.randint(7, 9)
    else:
       return random.randint(10, 12)
    
flight_data_sample['MONTH'] = flight_data_sample.apply(lambda x: months(x['QUARTER']), axis=1)

timestamp("Completed Months")
print(flight_data_sample.shape)

# Add states for origin and destination airports, to allow for join with other datasets which are at the state level.
f = open("airport_codes_all.csv")
content = f.read()
f.close()

rows = content.split("\n")
states = {}

for row in rows:
    if(row != ""):
        state = row.split(",")
        states[state[1]] = state[6]
    
def state(airportID):
    return states[str(airportID)]
    
flight_data_sample['ORIGIN_STATE'] = flight_data_sample.apply(lambda x: state(x['ORIGIN_AIRPORT_ID']), axis=1)
flight_data_sample['DEST_STATE'] = flight_data_sample.apply(lambda x: state(x['DEST_AIRPORT_ID']), axis=1)

timestamp("Completed State")
print(flight_data_sample.shape)

# Read file of state specific data containing high temperatures, political leaning and happiness.
f = open("state_info.csv")
content = f.read()
f.close()

rows = content.split("\n")
weather = {}
politics = {}
happiness = {}
mcdonalds = {}
prosperity = {}

for row in rows:
    if(row != ""):
        state = row.split(",")
        weather[state[1]] = [state[2], state[3], state[4], state[5], state[6], state[7], state[8], state[9], state[10], state[11], state[12], state[13]]
        politics[state[1]] = state[14]
        happiness[state[1]] = state[15]
        mcdonalds[state[1]] = state[16]
        prosperity[state[1]] = state[17]

# Add average high temperature for origin and destination airports based on month of travel.
def temp(state, month):
    return weather[state][month - 1]

flight_data_sample['ORIGIN_TEMP'] = flight_data_sample.apply(lambda x: temp(x['ORIGIN_STATE'], x['MONTH']), axis=1)
flight_data_sample['DEST_TEMP'] = flight_data_sample.apply(lambda x: temp(x['DEST_STATE'], x['MONTH']), axis=1)

timestamp("Completed Weather")
print(flight_data_sample.shape)

# Add average monthly oil price based on month of travel.
oil = [69.36, 70.18, 72.26, 74.94, 73.92	, 71.1, 72.13, 69.83	, 69.97, 68.42, 66.11, 64.19]

def oilPrice(month):
    return oil[month - 1]

flight_data_sample['OIL_PRICE'] = flight_data_sample.apply(lambda x: oilPrice(x['MONTH']), axis=1)

timestamp("Completed Oil")
print(flight_data_sample.shape)


# Add volume of domestic travelers based on month of travel.
monthlyDemand = [55.8, 54.1, 66.6, 64.6, 67.8, 70.3, 72.5, 70.3, 60.5, 67.1, 64.6, 63.6]

def demand(month):
    return monthlyDemand[month - 1]

flight_data_sample['DEMAND'] = flight_data_sample.apply(lambda x: demand(x['MONTH']), axis=1)

timestamp("Completed Demand")
print(flight_data_sample.shape)

# Add political leaning for origin and destination states.
def political(state):
    return politics[state]

flight_data_sample['ORIGIN_POLITICS'] = flight_data_sample.apply(lambda x: political(x['ORIGIN_STATE']), axis=1)
flight_data_sample['DEST_POLITICS'] = flight_data_sample.apply(lambda x: political(x['DEST_STATE']), axis=1)

timestamp("Completed Politics")
print(flight_data_sample.shape)

# Add happiness for origin and destination airports.
def happy(state):
    return happiness[state]

flight_data_sample['ORIGIN_HAPPINESS'] = flight_data_sample.apply(lambda x: happy(x['ORIGIN_STATE']), axis=1)
flight_data_sample['DEST_HAPPINESS'] = flight_data_sample.apply(lambda x: happy(x['DEST_STATE']), axis=1)

timestamp("Completed Happiness")
print(flight_data_sample.shape)

# Add mcdonalds for origin and destination airports.
def mcd(state):
    return mcdonalds[state]

flight_data_sample['ORIGIN_MCDONALDS'] = flight_data_sample.apply(lambda x: mcd(x['ORIGIN_STATE']), axis=1)
flight_data_sample['DEST_MCDONALDS'] = flight_data_sample.apply(lambda x: mcd(x['DEST_STATE']), axis=1)

timestamp("Completed McDonalds")
print(flight_data_sample.shape)

# Add prosperity for origin and destination airports.
def prospIndex(state):
    return prosperity[state]

flight_data_sample['ORIGIN_PROSPERITY'] = flight_data_sample.apply(lambda x: prospIndex(x['ORIGIN_STATE']), axis=1)
flight_data_sample['DEST_PROSPERITY'] = flight_data_sample.apply(lambda x: prospIndex(x['DEST_STATE']), axis=1)

timestamp("Completed Prosperity")
print(flight_data_sample.shape)

      
# Drop columns unnecessary for the prediction model.
flight_data_sample = flight_data_sample.drop(['AIRPORT_GROUP'], axis = 1)

# Filter out outliers based on MARKET_FARE.  The filters differ depending on FARE_CLASS.
flight_data_sample = flight_data_sample[flight_data_sample['MARKET_FARE'] > 30]
flight_data_sample.drop(flight_data_sample[(flight_data_sample['MARKET_FARE'] > 480) & (flight_data_sample['FARE_CLASS'] == 'Coach')].index, inplace = True)
flight_data_sample.drop(flight_data_sample[(flight_data_sample['MARKET_FARE'] > 1050) & (flight_data_sample['FARE_CLASS'] == 'Business')].index, inplace = True)
flight_data_sample.drop(flight_data_sample[(flight_data_sample['MARKET_FARE'] > 1450) & (flight_data_sample['FARE_CLASS'] == 'First')].index, inplace = True)
        
# Output final dataset to csv file for use by the model.
flight_data_sample.to_csv ('cleaned_data.csv', index = False, header=True)