# AIProject
## Determining an optimal time and post for Twitter based on 80,000 tweets

### Creators:
* Razvan Mocanu (3B6)
* Laurentiu Niculae (3B6)
* Mihaela-Diana Pascariu (3B6)  
* Robert-Pavel Sucurei (3B4)

###1. Introduction

*To Be Completed*

###2. Tweepy and collecting data from Twitter

*To Be Completed-Laur*

###3. Bucketing

According to the documentation, we created buckets for followers, friends, listed, favourites, statuses and time.

Bucketing was made using K-Means algorithm according to the number of buckets needed(k=11, k=7, k=16,..) .

K-Means Algorithm classifies the data and "groups" it by calculated centroids, which we use as boundaries.
So, for example, the first cluster has 100 as centroid, so all data closer to this value will be grouped together. 

Each bucket for created separately and independent, with a specific k for each of it. As a result, we have two data 
structures for each bucket - clusters and centroids. Each value i of the data corresponds to the cluster i, having the 
the cluster(i) value. 

* Followers Bucket:
    * List, with i = 1, 11.

* Friends Bucket:
    * Having i=1, 16.
   
* Listed Bucket:
    * Having i = 1, 7.

* Favourites Bucket:
    * Having i = 1, 16.
    
* Statuses Bucket:
    * Having i = 1, 11.

* Time Bucket:
    * Having i = 1, 24.
    * For this bucket, we used a list in which we stored all time dates from our data set. We formatted it to match an 
    actual date format, then we used the hour the tweet was posted in order to classify the current time instance. 
    
### 3. Linear Regression
*To Be Completed - Razvan*

### 4. Conclusion
*To Be Completed - ??*

### 5. Resources
*TBC*