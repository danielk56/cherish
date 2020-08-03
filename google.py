import pandas as pd
import csv
import numpy as np
from pytrends.request import TrendReq
pytrend = TrendReq()
pytrend.build_payload(kw_list=['Parenting'])

related_queries = pytrend.related_queries()


with open('output.csv', 'w') as csv_file:
   csvwriter = csv.writer(csv_file, delimiter='\t')
   for type in related_queries:
      for query in related_queries[type]:
         csvwriter.writerow([query, related_queries[type][query]])

data = pd.read_csv('output.csv')
print(data)
