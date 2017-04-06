import os
import sys
import pandas as pd
from collections import deque, defaultdict

path = os.getcwd()
input_file, hosts_file, hours_file, resources_file, blocked_file = sys.argv[1:]

column_names = ['host','timestamp','timezone', 'request', 'code', 'bytes']
df = pd.read_table(os.path.join(path, input_file.replace('./', '')),
                    header=None,
                    sep=' ', 
                    usecols=[0,3,4,5,6,7],
                    encoding ='latin1',
                    names=column_names,
                    dtype={k:'object' for k in column_names},
                    error_bad_lines=False
                   )

df.drop('timezone', axis=1, inplace=True)
df.timestamp = pd.to_datetime(df.timestamp, format='[%d/%b/%Y:%H:%M:%S') # slow but neccessary formatting

# Feature 1
top_hosts = df.host.value_counts().head(10)
n = min(10, len(top_hosts)) # In case there are fewer than 10 entries

with open(os.path.join(path, hosts_file.replace('./', '')), 'w') as f:
    for i in range(n):
        f.write(str(top_hosts.index[i]) + ',' + str(top_hosts.values[i]) + '\n')

# Feature 2
def request_split(request): # Get the URN from the request
    try:
        return request.split()[1]
    except:
        return ''
          
df.bytes = pd.to_numeric(df.bytes, downcast='integer', errors='coerce').fillna(0)
df['request_urn'] = df.request.apply(request_split) 
          
top_resources = df[['request_urn','bytes']].groupby('request_urn').sum().sort_values(by='bytes', ascending=False).head(10)
n = min(10, len(top_resources)) # In case there are fewer than 10 entries
          
with open(os.path.join(path, resources_file.replace('./', '')), 'w') as f:
    for i in range(n):
        f.write(str(top_resources.index[i]+'\n'))       
            
# Feature 4 should be run first to save memory since Feature 3 will require transforming the dataframe    
# Feature 4 
watchlist = defaultdict(deque)
jail = {}           
blocked = open(os.path.join(path, blocked_file.replace('./', '')), 'w')

for i in range(len(df)):
    row = df.iloc[i]
    if row.host in jail:
        if (row.timestamp - jail[row.host]).seconds > 300: # Greater than 5 minutes, release from jail
            del jail[row.host] 
        else: # Still in jail, log the attempt
            blocked.write('{} - - [{} -0400] "{}" {} {}\n'.format(row.host, row.timestamp.strftime("%d/%b/%Y:%H:%M:%S"), row.request, row.code, row.bytes))
            continue
            
    if row.code == '401': # Failed attempt, add to watchlist
        watchlist[row.host].append(row.timestamp)
        if len(watchlist[row.host]) == 3 and (watchlist[row.host][2] - watchlist[row.host][0]).seconds <= 20: # Check if 3 login attempts within 20 sec
            jail[row.host] = row.timestamp
            del watchlist[row.host]
            
    else: # Successful login, delete host from watchlist
        try: 
            del watchlist[row.host]
        except:
            pass
    
blocked.close()          
          
# Feature 3
df.index = df.timestamp
df.drop('timestamp', axis=1, inplace=True)
df = df.groupby(pd.TimeGrouper(freq="1s"), sort=False).count().rolling(window=3600).sum().shift(-3599)
# The shift is needed because pandas rolling is right-aligned by default and we want left-aligned
top_hours = df.sort_values(by='host', ascending=False).head(10)  
n = min(10, len(top_hours)) # In case there are fewer than 10 entries      

with open(os.path.join(path, hours_file.replace('./', '')), 'w') as f:
    for i in range(n):
        f.write(str(top_hours.index[i].strftime("%d/%b/%Y:%H:%M:%S")) + ' -0400,' + str(int(top_hours.host[i])) + '\n')          
