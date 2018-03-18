import pandas as pd
import numpy  as np
import requests
import json
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
data = [['Ticker'],'']
url = "https://api.intrinio.com/news"
ticker = ['AAPL','AXP','BA','CAT','CSCO','CVX','DIS','DWDP','GE','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','TRV','UNH','UTX','V','VZ','WMT','XOM']
array = []
for i in range(30):
	test = []
	querystring = {"identifier":ticker[i]}
	headers = {
    	'Authorization': "Basic ZTYzMWRhOTU4ZTIwYWEyOWJkMTYzOGFhYTg0NDAwNDg6Y2EyZjcxNzU3ZTY2MGZkYTE5ZjQ2M2FlMzg0YTg3NTQ=",
    	'Cache-Control': "no-cache",
    	'Postman-Token': "7c2b0d40-5121-ceb7-2cea-36ca8b41d099"
    	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	py = json.loads(response.text)
	data = pd.read_csv('Full-Economic-News-DFE-839861.csv')
	data['positivity'] = np.where(data['positivity']>5, 1, 0)
	train = data
	for i in range(10):
		test.append(py['data'][i]['title'])
	traintext = []
	for row in range(0,len(train.index)):
		traintext.append(' '.join(str(x) for x in train.iloc[row,4:]))
	basicvectorizer = CountVectorizer()
	basictrain = basicvectorizer.fit_transform(traintext)
	basicmodel = LogisticRegression()
	basicmodel = basicmodel.fit(basictrain, train["positivity"])
	basictest = basicvectorizer.transform(test)
	predictions = basicmodel.predict(basictest)
	array.append(sum(predictions))
print(array)

