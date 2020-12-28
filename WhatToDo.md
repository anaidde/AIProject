# Data collection(Laurentiu)
## Output
O sa dau ca output un fisier `tweets.json` care va avea urmatoare forma:
```json
{
    "tweets" : [tweet]  // practic un array de obiecte json (de tweet-uri)
}
```
Fiecare obiect tweet va avea urmatoarea forma:
```json
tweet
{
    "i":  int,     //current index in the array
    "ca": string,  //created_at, a string with the time
    "t":  string,  //the text of the tweet
    "rt": int      //number of retweets
    "u":{            //user data
        "fc" : int //followers_count
        "frc": int //friends_count
        "lc" : int //listed_count
        "fac": int //favourites_count
        "sc" : int //statuses_count
    }
}
```
Example:
```json
{
    "i": 1,
    "ca": "Mon Dec 28 11:30:14 +0000 2020", 
    "t": "Simple. This is my tweet.", 
    "rt": 20,
    "u": {
        "fc": 510, 
        "frc": 546, 
        "lc": 3, 
        "fac": 19118, 
        "sc": 35879
        }
}
```

# Data bucketing(Diana & Robert)

## What you have to do
Trebuie sa scoate niste feature-uri din obiectele de mai sus sub forma asta:
```json
Derived Feature
{
    "index": int,            // the same as before
    "retweets": int,         // the same as before
    "follower_bucket": int,  // derived from followers_count
    "friends_bucket": int,    // derived from friends_count
    "listed_bucket": int,     // derived from listed_count
    "favourites_bucket": int, // derived from favourites_count
    "statuses_bucket": int,    // derived from statuses_count
    "sentiment": float,        // derived from text
    "objectivity": float,      // derived from text
    "time_bucket": int,        // derived from created_at
    "time_bucket_and_feature": // no idea, daca stiti ce este puneti daca nu, aia e :))
}
```
## Output
Trebuie sa creati un fisier tweetsFeatures.json in care aveti toate feature-urile pentru fiecare tweet din tweets.json

EXEMPLU:

Iput:
```json
tweets.json
{
    "tweets":[
        {
            "i": 1,
            "ca": "Mon Dec 28 11:30:14 +0000 2020", 
            "t": "Simple. This is my tweet.", 
            "rt": 20,
            "u": {
                "fc": 510, 
                "frc": 546, 
                "lc": 3, 
                "fac": 19118, 
                "sc": 35879
                }
        },
        {
            "i": 2,
            "ca": "Mon Dec 28 12:30:14 +0000 2020", 
            "t": "Simple. This is my second tweet.", 
            "rt": 30,
            "u": {
                "fc": 510, 
                "frc": 546, 
                "lc": 3, 
                "fac": 19118, 
                "sc": 35879
                }
        }
    ]
}
```
Output:
```json
tweetsFeatures.json
{
    "features":[
        {
            "index": 1  ,             
            "retweets": 20,          
            "follower_bucket": 1,   
            "friends_bucket": 1,    
            "listed_bucket": 1,     
            "favourites_bucket": 1, 
            "statuses_bucket": 1,   
            "sentiment": 0,       
            "objectivity": 0,     
            "time_bucket": 11,       
        },
        {
            "index": 2  ,             
            "retweets": 30,          
            "follower_bucket": 1,   
            "friends_bucket": 1,    
            "listed_bucket": 1,     
            "favourites_bucket": 1, 
            "statuses_bucket": 1,   
            "sentiment": 0,       
            "objectivity": 0,     
            "time_bucket": 12,       
        },
    ]
}
```

# Training(Razvan)

Later