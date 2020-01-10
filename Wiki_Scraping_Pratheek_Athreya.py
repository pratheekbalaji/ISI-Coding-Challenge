import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
url = requests.get('https://en.wikipedia.org/wiki/2019_in_spaceflight#Human_spaceflight')
soup = BeautifulSoup(url.content,'html.parser')
table = soup.find("table",class_="wikitable collapsible")
result = []
for items in table.find_all("tr")[4:]:
    
    a= [' '.join(item.text.split()) for item in items.find_all(['td','th'])]
    if re.search(r'\d',a[0][0]) and ('January' in a[0] or 'February' in a[0] or re.match (r"\d+\sMarch",a[0]) or 'April' in a[0] or 'May' in a[0]\
                                     or 'June' in a[0] or 'July' in a[0] or 'August' in a[0] or 'September' in a[0] or 'October' in a[0]\
                                     or 'November' in a[0] or 'December' in a[0]):
        pattern = r'\[.*?\]'
        pattern_2 =r'\(.*\)'
        temp = re.sub(pattern, '', a[0])
        temp = re.sub(pattern_2,'',temp)
        result.append([temp,0])
    else:
        if  'Operational' in a  or 'Successful' in a  or 'En Route' in a:
            result[-1][1]+=1
        
df =pd.DataFrame(result,columns =['Date','Value'])
date_time =[]
for a in df['Date']:
    l =a.split()
    s = re.sub(r'[a-zA-Z]\d', lambda m: ' '.join(m.group()), l[-1] )
    l[-1] = s
    l.append('2019')
    temp =' '.join(l)
    date_time.append(temp)
df['Date']=date_time     
df['Date'] = pd.to_datetime(df.Date)
df['Date'] = df['Date'].apply(lambda x:datetime.isoformat(x))
df.to_csv('results.csv',index=False)