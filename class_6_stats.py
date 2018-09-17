Descriptive Statistics For pandas Dataframe

Import modules
import pandas as pd

data = {'name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'], 
        'age': [42, 52, 36, 24, 73], 
        'preTestScore': [4, 24, 31, 2, 3],
        'postTestScore': [25, 94, 57, 62, 70]}
df = pd.DataFrame(data, columns = ['name', 'age', 'preTestScore', 'postTestScore'])
print(df)


df['age'].sum()

#Mean preTestScore
df['preTestScore'].mean()

#Cumulative sum of preTestScores, moving from the rows from the top
df['preTestScore'].cumsum()


#Summary statistics on preTestScore
df['preTestScore'].describe()

#Count the number of non-NA values
df['preTestScore'].count()

#Minimum value of preTestScore
df['preTestScore'].min()

#Maximum value of preTestScore
df['preTestScore'].max()

#Median value of preTestScore
df['preTestScore'].median()

#Sample variance of preTestScore values
df['preTestScore'].var()

#Sample standard deviation of preTestScore values
df['preTestScore'].std()

#Kurtosis of preTestScore values
df['preTestScore'].kurt()

#Correlation Matrix Of Values
df.corr()

#Covariance Matrix Of Values
df.cov()

