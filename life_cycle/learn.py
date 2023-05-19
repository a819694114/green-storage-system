import pandas as pd
import numpy as np  
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import mean_squared_error

RANDOM_STATE = 100

def preprocess_data(df):
    df = df.dropna()
    scaler = StandardScaler()
    scaler.fit(df)
    scaler.transform(df)
    return df
    
def regression_process(df, train = False):
    irdf = []
    qdf = []
    time = []
    ir=[]
    Q = []
    T = []
    new_df = pd.DataFrame()
    if train:
        y = []
    for bat in df['id'].unique():
        ir10 = df.loc[df['id'] == bat][df['cycle']==10]['IR']
        ir100 = df.loc[df['id'] == bat][df['cycle']==100]['IR']
        dif = float(ir100) - float(ir10)
        irdf.append(dif)
        q10 = df.loc[df['id'] == bat][df['cycle']==10]['QD']
        q100 = df.loc[df['id'] == bat][df['cycle']==100]['QD']
        dif = float(q100) - float(q10)
        qdf.append(dif)
        t10 = df.loc[df['id'] == bat][df['cycle']==10]['chargetime']
        t100 = df.loc[df['id'] == bat][df['cycle']==100]['chargetime']
        dif = float(t100)- float(t10)
        time.append(dif)
        ir.append(float(df.loc[df['id'] == bat][df['cycle']==100]['IR']))
        Q.append(float(df.loc[df['id'] == bat][df['cycle']==100]['QD']))
        T.append(float(df.loc[df['id'] == bat][df['cycle']==100]['Tmax']))
        if train:
            y.append(int(df.loc[df['id'] == bat][df['cycle'] == 10]['cycle_life']))
    new_df['id'] = df['id'].unique()
    new_df['IR_var'] = irdf
    new_df['QD_var'] = qdf
    new_df['time'] = time
    new_df['ir'] = ir
    new_df['Q'] = Q
    new_df['T'] = T
    if train:
        return new_df, y
    return new_df

def classify(df):
    df = df.copy()
    df['percent'] = df['cycle']/df['cycle_life']
    df.loc[df['percent'] < 0.3, 'condition'] = '2'
    df.loc[df['percent'] >= 0.3, 'condition'] = '1'
    df.loc[df['percent'] >= 0.7, 'condition'] = '0'
    del df['percent']
    X = df.copy()
    y = df['condition']
    del X['condition']
    clf = MLPClassifier(solver='adam', alpha=1e-5,hidden_layer_sizes=(32, 64), random_state=RANDOM_STATE, max_iter=300, early_stopping = False, validation_fraction=0.3)
    clf.fit(X,y)
    print("Classification score:")
    print(clf.score(X,y))
    return clf


def random_regressor(X_train, X_test, y_train, y_test):
    clf = RandomForestRegressor(max_depth = 10, random_state = RANDOM_STATE)
    clf.fit(X_train, y_train)
    print(clf.score(X_train, y_train))
    
    ypred = clf.predict(X_train)
    mse = mean_squared_error(y_train, ypred)

    print("The metrics on train set:")
    print("MSE: ", mse)
    print("RMSE: ", mse**(1/2.0))

    ypred = clf.predict(X_test)
    mse = mean_squared_error(y_test, ypred)
    print("The metrics on test set:")
    print("MSE: ", mse)
    print("RMSE: ", mse**(1/2.0))
    return clf

def linear_regressor(X_train, X_test, y_train, y_test): 
    clf = LinearRegression()
    clf.fit(X_train, y_train)
    print(clf.score(X_train, y_train))
    
    ypred = clf.predict(X_train)
    mse = mean_squared_error(y_train, ypred)

    print("The metrics on train set:")
    print("MSE: ", mse)
    print("RMSE: ", mse**(1/2.0))

    ypred = clf.predict(X_test)
    mse = mean_squared_error(y_test, ypred)
    print("The metrics on test set:")
    print("MSE: ", mse)
    print("RMSE: ", mse**(1/2.0))
    return clf




df = pd.read_csv('df.csv')
classify(df)



df = preprocess_data(df)
X, y = regression_process(df, train = True)
clf = RandomForestRegressor(max_depth = 10, random_state = RANDOM_STATE)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.7, random_state = RANDOM_STATE)
clf.fit(X_train, y_train)
print(clf.score(X, y))

ypred = clf.predict(X)
mse = mean_squared_error(y, ypred)
print("MSE: ", mse)
print("RMSE: ", mse**(1/2.0)) 


