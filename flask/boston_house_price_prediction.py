# -*- coding: utf-8 -*-
"""boston_house_price_prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kWHj-c4uGQFO902O0f2RBlcx2DDMqNKP
"""

import seaborn as sns
from sklearn import datasets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

column_names = [
    "CRIM",     # per capita crime rate by town
    "ZN",       # proportion of residential land zoned for lots over 25,000 sq.ft.
    "INDUS",    # proportion of non-retail business acres per town
    "CHAS",     # Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
    "NOX",      # nitric oxides concentration (parts per 10 million)
    "RM",       # average number of rooms per dwelling
    "AGE",      # proportion of owner-occupied units built prior to 1940
    "DIS",      # weighted distances to five Boston employment centres
    "RAD",      # index of accessibility to radial highways
    "TAX",      # full-value property-tax rate per $10,000
    "PTRATIO",  # pupil-teacher ratio by town
    "B",        # 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
    "LSTAT",    # % lower status of the population
    "MEDV"      # Median value of owner-occupied homes in $1000's
]


# Load the Boston dataset from the provided URL
data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)

# Reconstruct the full dataset (features + target)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]  # Extract the target (house price)

# Create a Pandas DataFrame with the correct column names
df = pd.DataFrame(data, columns=column_names[:-1])  # Add only the feature names
df["MEDV"] = target  # Append the target column

# Display the first few rows
print(df.head())

df.info()

df.describe()

df.isnull().sum()

df.duplicated().sum()

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()

# prompt: can you decribe the heat map from above

The heatmap visualizes the correlation matrix of the features (and target variable 'MEDV') in the Boston Housing dataset.  Each square represents the correlation coefficient between two variables.

* **Color Intensity:**  The color intensity indicates the strength of the correlation.  Darker red shades represent strong positive correlations (as one variable increases, the other tends to increase), while darker blue shades represent strong negative correlations (as one variable increases, the other tends to decrease).  Lighter colors (near white) indicate weak or no correlation.

* **Values in Squares:** The numbers within each square are the correlation coefficients, ranging from -1 (perfect negative correlation) to +1 (perfect positive correlation).  A value of 0 means no linear relationship.

* **Diagonal:** The diagonal line from top-left to bottom-right always shows perfect positive correlation (1) because each variable is perfectly correlated with itself.

**Interpreting Key Relationships (examples, based on typical Boston Housing data correlations):**

* **Strong Positive Correlations:** You might see a strong positive correlation between `NOX` (nitric oxides concentration) and `INDUS` (proportion of non-retail business acres).  This makes sense – industrial areas tend to have higher pollution.  You might also observe a positive correlation between `RM` (average number of rooms) and `MEDV` (median house value) - more rooms generally correlate with higher house prices.

* **Strong Negative Correlations:**  `LSTAT` (% lower status of the population) will likely show a strong negative correlation with `MEDV`.  Areas with a higher percentage of lower-status population tend to have lower median house values.

* **Weak or No Correlation:** Some variables might show weak or no correlation with each other.  The presence of a near-zero correlation coefficient and light color in the heatmap would indicate this.


**Overall:** The heatmap provides a quick overview of the relationships between variables, helping identify features that might be highly influential in predicting the target variable (`MEDV` in this case) or features that might be redundant (highly correlated with each other).  It's a crucial step in feature selection and understanding the data before building predictive models.

df.hist(figsize=(12,10), bins=30)
plt.show()

X = df.loc[:, df.columns != 'MEDV']
X

y = df.loc[:,'MEDV']
y

plt.figure(figsize = ( 25 , 15 ))
features = list (X)
for i, col in enumerate (features):
    plt.subplot(3 , 6 ,i +1 )
    x = df[col]
    y = y
    plt.scatter(x, y, marker = 'o' )
    plt.xlabel(col)
    plt.ylabel( 'MEDV' )

df['LSTAT'] = np.log(df['LSTAT'])
df['DIS'] = np.log(df['DIS'])
df['CRIM'] = np.log(df['CRIM'])

fig, ax =plt.subplots(1,3, figsize=(15,5))
sns.scatterplot(data=df, color='r', x='LSTAT', y='MEDV', ax=ax[0])
sns.scatterplot(data=df, color='g', x='DIS',  y='MEDV', ax=ax[1])
sns.scatterplot(data=df, color='b', x='CRIM', y='MEDV', ax=ax[2])

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)
# print the sizes of our training and test set to verify if the splitting has occurred properly.
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

data_melted = pd.melt(df)
fig = sns.boxplot(x = "variable" ,y = "value" , data = data_melted)
plt.ylabel( 'MEDV' )
plt.xlabel( '' )
fig.set_xticklabels(fig.get_xticklabels(),rotation =30 )
plt.show()

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()
fit = lin_reg.fit(X_train,y_train)

y_pred_train = lin_reg.predict(X_train)
y_pred = lin_reg.predict(X_test)

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

model_evaluation = pd.DataFrame(
    {
        "Data": ["Train", "Test"],
        "RMSE": [np.sqrt(mean_squared_error(y_pred_train, y_train)),
                np.sqrt(mean_squared_error(y_test, y_pred))],
        "MSE": [mean_squared_error(y_pred_train, y_train),
                mean_squared_error(y_test, y_pred)],
        "R2": [r2_score(y_pred_train, y_train),
               r2_score(y_test, y_pred)],
    })

model_evaluation

from sklearn.model_selection import cross_val_score
cv_scores_1 = cross_val_score(lin_reg,X_train, y_train, cv=10) # R2
print("Average 10-Fold CV R2 Score: {}".format((np.mean(cv_scores_1)) ))
cv_Score_2 = cross_val_score(lin_reg, X_train, y_train, cv = 10, scoring='neg_mean_squared_error') # this return the negated value of the MSE, make sure to multiply it by -1 to get the positive one
print("Average 10-Fold CV MSE Score: {}".format(-1*(np.mean(cv_Score_2))))

from sklearn.pipeline import make_pipeline
pipeline = make_pipeline(StandardScaler(), LinearRegression())
scores_pipe_1 = cross_val_score(pipeline, X_train, y_train,cv=10)
print("Average 10-Fold CV R2 Score: {}".format((np.mean(scores_pipe_1)) ))
scores_pipe_2 = cross_val_score(pipeline, X_train, y_train,cv=10, scoring='neg_mean_squared_error') # this return the negated value of the MSE, make sure to multiply it by -1 to get the positive one
print("Average 10-Fold CV MSE Score: {}".format(-1*(np.mean(scores_pipe_2)) ))

import joblib

# Save the trained model
joblib.dump(pipeline, "boston_house_price_model.pkl")

# Save the scaler for consistent input processing
joblib.dump(scaler, "scaler.pkl")

print("Model saved successfully!")

from google.colab import files
files.download("boston_house_price_model.pkl")
files.download("scaler.pkl")