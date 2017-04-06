## Insight Fansite Analytics Challenge Submission by Kevin Du

### Language
Python 3.5

### Dependencies
pandas >= 0.19.2

### Overview
#### Feature 1
I used pandas value_counts function to find the top host names.
A bonus feature finds domain names rather than specific host names (e.g. piweba3y.prodigy.com and piweba4y.prodigy.com would both be considered prodigy.com). The bonus output is [domains.txt](log_output/domains.txt)

#### Feature 2
I used Pandas groupby and aggregate function sum to find the resources using up the most bandwith. A bonus feature would be to group the resources into subcategories such as "shuttle/technology" or "shuttle/missions". This can be done by making a new column in the dataframe, similar to bonus feature 1. 

#### Feature 3
I used the TimeGrouper and rolling functions in pandas to group the data into hour-long windows for every second then sorted the output to get the 10 top results. As expected, the top busiest periods were mostly within the same hour on the same day, so a bonus feature is finding the busiest hours regardless of day. A plot of this result is shown [here](hours.png).

#### Feature 4
I created a dictionary called "watchlist" to store IP addresses when there is a failed login attempt. The values in this dict are deques with a max length of 3 that stores the the timestamps of the failed login attempts. If the time difference between the first and third failed logins is less than or equal to 20 seconds, the IP address gets blocked. Any successful login will remove the IP from the dict.    
I created another dictionary called "jail" to store the temporarily blocked IPs, log any further access attempts, and keep track of when they should be released. A bonus feature is finding which hosts and domains tend to get blocked often, which is easily done by passing the blocked.txt file as input to feature 1.

#### Other thoughts
Pandas should be efficient at handling large amounts of data and it is very useful for visualization of the data, which is why I chose to it. The bottleneck is probably the datetime parsing in pandas. For feature 4, another concern is that the dictionary could become very large and take up a lot of memory space. One simple way to deal with this is to keep track of when the most recent failed login attempt occurred, and if the timestamp of the current attempt is more than 20 seconds later, the entire dictionary can be deleted. Doing this for each invidual IP will be more effective at saving memory but will also sacrifice more speed. 
 

