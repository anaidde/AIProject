from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
import json
import random
import numpy as np

tweet_temp_dictionary = {}
tweets_list = []
# fakedata
# with open('tweetsFeatures.json', 'r+') as f:
#     tweets_features_json = json.load(f)
#
#     for i in range(1, 80000):
#         tweet_temp_dictionary['index'] = i
#         tweet_temp_dictionary['retweets'] = int(random.expovariate(1) * 100)
#         tweet_temp_dictionary['follower_bucket'] = random.randint(0, 12)
#         tweet_temp_dictionary['friends_bucket'] = random.randint(0, 12)
#         tweet_temp_dictionary['listed_bucket'] = random.randint(0, 12)
#         tweet_temp_dictionary['favourites_bucket'] = random.randint(0, 12)
#         tweet_temp_dictionary['statuses_bucket'] = random.randint(0, 12)
#         tweet_temp_dictionary['sentiment'] = random.uniform(0, 1)
#         tweet_temp_dictionary['objectivity'] = random.uniform(0, 1)
#         tweet_temp_dictionary['time_bucket'] = random.randint(1, 12)
#         tweets_list.append(tweet_temp_dictionary.copy())
#
#     tweets_features_json['features'] = tweets_list
#     f.seek(0)
#     json.dump(tweets_features_json, f, indent=4)
#     f.truncate()

# print(tweets_features_json)
with open('tweetsFeatures.json', 'r+') as f:
    tweets_features_json = json.load(f)
    x_array_train = []
    y_array_train = []
    x_array_validate = []
    y_array_validate = []
    json_length = len(tweets_features_json['features'])
    random.shuffle(tweets_features_json['features'])

    for index in range(1, (json_length*8)//10):
        x_array_train.append(
            [tweets_features_json['features'][index]['follower_bucket'],
             tweets_features_json['features'][index]['friends_bucket'],
             # tweets_features_json['features'][index]['listed_bucket'],
             # tweets_features_json['features'][index]['favourites_bucket'],
             # tweets_features_json['features'][index]['statuses_bucket'],
             # tweets_features_json['features'][index]['sentiment'],
             # tweets_features_json['features'][index]['objectivity'],
             tweets_features_json['features'][index]['time_bucket']
             ])
        y_array_train.append(tweets_features_json['features'][index]['retweets'])
    for index in range((json_length * 8) // 10, json_length):
        x_array_validate.append(
            [tweets_features_json['features'][index]['follower_bucket'],
             tweets_features_json['features'][index]['friends_bucket'],
             # tweets_features_json['features'][index]['listed_bucket'],
             # tweets_features_json['features'][index]['favourites_bucket'],
             # tweets_features_json['features'][index]['statuses_bucket'],
             # tweets_features_json['features'][index]['sentiment'],
             # tweets_features_json['features'][index]['objectivity'],
             tweets_features_json['features'][index]['time_bucket']
             ])
        y_array_validate.append(tweets_features_json['features'][index]['retweets'])

    # print(x_array_train)
    # print(y_array_train)
    # print(x_array_validate)
    # print(y_array_validate)

    reg = LinearRegression().fit(x_array_train, y_array_train)
    print("Train Score:", reg.score(x_array_train, y_array_train))
    print("Validation Score:", reg.score(x_array_validate, y_array_validate))
    # print("R2 Score", r2_score(y_array_validate, list(reg.predict(np.array(x_array_validate)))))
    # print(y_array_train)
    # print("Predict", list(reg.predict(np.array(x_array_train))))
    # print(y_array_validate)
    # print("Predict", list(reg.predict(np.array(x_array_validate))))
    neigh = KNeighborsRegressor(n_neighbors=7, weights='uniform')
    neigh.fit(x_array_train, y_array_train)
    print("KNN Train score: ", neigh.score(x_array_train, y_array_train))
    print("KNN Validation score: ", neigh.score(x_array_validate, y_array_validate))

    print([x for x in neigh.predict(x_array_validate) if x != 0])

    predicted_list = list(neigh.predict(x_array_validate)[0:1000])
    for index in range(0, 1000):
        print(f' {predicted_list[index]} : {y_array_validate[index]}')

