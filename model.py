"""

US Domestic Airfare Predictor - Model v1  
This program trains and tunes XG Boost, Random Forest and Light GBM models. The
final model selected was XG Boost and the model is saved to a binary file for
use in a Flask web app.

"""

import random

import pandas as pd
import pandas_profiling

import numpy as np 
from matplotlib import pyplot as plt
import joblib

import seaborn as sns

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

from sklearn.preprocessing import StandardScaler
from joblib import dump

from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import xgboost as xgb
import lightgbm as lgb

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import r2_score

# ===========================================================================================================
# Functions to tune and fit XG Boost, Random Forest and Light GBM models.
# ===========================================================================================================

# Function for XG Boost model hyperparameter tuning.
def tuneXGB():

    # Original param_grid
    param_grid1 = {'learning_rate': [0.01,0.1,0.5,0.9],
                   'n_estimators': [200, 205],
                   'subsample': [0.3, 0.5, 0.9]}
    
    # New param_grid
    param_grid2 = {'learning_rate': [0.88, 0.9, 0.92],
                   'n_estimators': [203, 205],
                   'subsample': [0.95, 1.0],
                   'max_depth': [5, 6],
                   'reg_lambda': [2, 3],
                   'gamma': [0]}
    
    # Final param_grid
    param_grid3 = {'learning_rate': [0.92, 0.95],
                   'n_estimators': [203, 205, 207],
                   'subsample': [1.0],
                   'max_depth': [6],
                   'reg_lambda': [2, 2.1],
                   'gamma': [0]}

    # Use GridSearchCV for hyperparameter tuning.
    regressor = xgb.XGBRegressor()
    grid_search = GridSearchCV(estimator=regressor, param_grid=param_grid2, scoring='neg_mean_squared_error', cv=4, verbose=10, n_jobs=-1)
    grid_search.fit(X, y)
    
    printBestParams(grid_search)


# Function for fitting XGB model, making predictions on test data, printing model metrics and plotting results chart.
def fitXGB():
    
    # Final selection of hyperparameters following tuning.
    regressor = xgb.XGBRegressor(n_estimators=207,
                                reg_lambda=3,
                                gamma=0,
                                max_depth=6,
                                subsample=1.0,
                                learning_rate=0.88)
    
    # Fit the model with training data. 
    regressor.fit(X_train, y_train)
    
    # Make predictions on the testing data.
    y_pred = regressor.predict(X_test)

    printModelMetrics(y_test, y_pred)
    return regressor
    
    
# Function for Random Forest model hyperparameter tuning.
def tuneRF():

    # Original param_grid
    param_grid1 = {'n_estimators': [25, 30, 35],
               'max_features': [6, 8, 10],
               'max_depth': [10, 20],
               'min_samples_split': [2, 5],
               'min_samples_leaf': [1, 2]}
    
    # New param_grid
    param_grid2 = {'n_estimators': [29, 30, 31],
               'max_features': [5, 6, 7],
               'max_depth': [15, 20, 25],
               'min_samples_split': [5, 6],
               'min_samples_leaf': [2, 3]}
   
    # Use GridSearchCV for hyperparameter tuning.    
    regressor = RandomForestRegressor()
    grid_search = GridSearchCV(estimator=regressor, param_grid=param_grid2, scoring='neg_mean_squared_error', cv=5, verbose=10, n_jobs=-1)
    grid_search.fit(X, y)
   
    printBestParams(grid_search)


# Function for fitting Random Forest model, making predictions on test data, printing model metrics and plotting results chart.
def fitRF():

    # Final selection of hyperparameters following tuning.
    regressor = RandomForestRegressor(
        n_estimators=31,
        max_features=7,
        max_depth=20,
        min_samples_split=6,
        min_samples_leaf=3
        )

    # Fit the model with training data. 
    regressor.fit(X_train, y_train)
    
    # Make predictions on the testing data.
    y_pred = regressor.predict(X_test)

    printModelMetrics(y_test, y_pred)
    

# Function for XGBoost model hyperparameter tuning.
def tuneLGBM():

    # Original param_grid
    param_grid1 = {'learning_rate': [0.01,0.1,0.5,0.9],
                   'n_estimators': [200],
                   'subsample': [0.3, 0.5, 0.9]}
    
    # Use GridSearchCV for hyperparameter tuning.
    regressor = lgb.LGBMRegressor()
    grid_search = GridSearchCV(estimator=regressor, param_grid=param_grid1, scoring='neg_mean_squared_error', cv=4, verbose=10, n_jobs=-1)
    grid_search.fit(X, y)
    
    printBestParams(grid_search)


# Function for fitting Light GBM model, making predictions on test data, printing model metrics and plotting results chart.
def fitLGBM():
    
    # Final selection of hyperparameters following tuning.
    regressor = lgb.LGBMRegressor({'task': 'train',
                                  'boosting_type': 'gbdt',
                                  'objective': 'regression',
                                  'metric': ['l2', 'auc'],
                                  'learning_rate': 0.005,
                                  'feature_fraction': 0.9,
                                  'bagging_fraction': 0.7,
                                  'bagging_freq': 10,
                                  'verbose': 0,
                                  'max_depth': 8,
                                  'num_leaves': 128, 
                                  'max_bin': 512,
                                  'num_iterations': 1000,
                                  'n_estimators': 1000})

    # Fit the model with training data. 
    regressor.fit(X_train, y_train)
    
    # Make predictions on the testing data.
    y_pred = regressor.predict(X_test)

    printModelMetrics(y_test, y_pred)  
    

# ===========================================================================================================
# Functions to print hyperparameters and model metrics.
# ===========================================================================================================

# Function to print best hyperparameters.
def printBestParams(grid_search):
    
    print("Best parameters found: ", grid_search.best_params_)
    print("Lowest RMSE found: ", np.sqrt(np.abs(grid_search.best_score_)))


# Function to print model metrics and plot results chart.
def printModelMetrics(y_test, y_pred):
    
    # Print model metrics.
    print("R2 Score: ", r2_score(y_test, y_pred))
    print("Mean Squared Error: ", mean_squared_error(y_test, y_pred))
    print("Mean Absolute Value: ", mean_absolute_error(y_test, y_pred))
    
    # Plot target and predicted values.
    plt.scatter(y_test, y_pred, s=1)
    plt.xlabel("True Values")
    plt.ylabel("Predictions")
    

# ===========================================================================================================
# Transform cleansed data into training and validation data sets.
# ===========================================================================================================

# Import cleansed data file.
flight_data = pd.read_csv('cleaned_data.csv')

# Encode categorical fields as numeric.
flight_data = pd.get_dummies(data=flight_data,columns=['FARE_CLASS','TICKET_CARRIER'], drop_first = True)

# Define feature and target datasets.  Remove features from drop to add them to the model, e.g. happiness.
X = flight_data.drop(['MARKET_FARE', 'ORIGIN_STATE', 'DEST_STATE', 'QUARTER', 'ORIGIN_HAPPINESS', 'DEST_HAPPINESS',
                      'OIL_PRICE', 'DEMAND', 'ORIGIN_POLITICS', 'DEST_POLITICS', 'ORIGIN_TEMP', 'DEST_TEMP',
                      'ORIGIN_MCDONALDS', 'DEST_MCDONALDS', 'ORIGIN_PROSPERITY', 'DEST_PROSPERITY'], axis=1)
y = flight_data['MARKET_FARE']

# Create training and valdiation datasets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.10, random_state=42)


# ===========================================================================================================
# Tune and fit models. Then dump the model into a binary file.
# ===========================================================================================================

# Tune and fit XG Boost model.
#tuneXGB()
model = fitXGB()

# Tune and fit Random Forest model.
#tuneRF()
#model = fitRF()

# Tune and fit Light GBM model.
#tuneLGBM()
#model = fitLGBM()

# Dump model into a binary file.
filename = 'model.sav'
joblib.dump(model, filename)