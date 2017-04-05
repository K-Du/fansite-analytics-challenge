## Insight Fansite Analytics Challenge Submission by Kevin Du

### Language
Python 3.5

### Dependencies
pandas

### Overview
#### Feature 1
I used Pandas to group 

#### Feature 2
I used Pandas aggregate function sum 

#### Feature 3
I used the " function in pandas

#### Feature 4
I created a dictionary called "failed" to store IP addresses when there is a failed login attempt. The values in this dict are deques with a max length of 3 that stores the the timestamps of the failed login attempts. If the time difference between the first and third failed logins is less than or equal to 20 seconds, the IP address gets blocked. Any successful login will remove the IP from the dict.   
I created another dictionary called "jail" to store the temporarily blocked IPs, log any further access attempts, and keep track of when they should be released. 


#### Bonus Features
For feature 3, it is not effective to group by seconds since all the hour-long segments would be consecutive.
It would be much better to just group by hour instead to find the busiest hours of the day. 
For feature . This was easily accomplished with pandas See [bonus_4.py](src/bonus_4.py)


#### Further thoughts
Pandas should be efficient at handling large amount of data, which is why I chose it for features 1-3. The bottleneck is probably the datetime parsing in pandas.  
For feature 4, the main concern is that the dictionary could become very large and take up a lot of memory space. One simple way to deal with this is to keep track of when the most recent failed login attempt occurred, and if the timestamp of the current attempt is more than 20 seconds later, the entire dictionary can be deleted. Doing this for each invidual IP will be more effective at saving memory but will also sacrifice more speed. 
 

