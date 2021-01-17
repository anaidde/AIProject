from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
import json
import random
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, mean_squared_error
from datetime import datetime


def special_append(x_array, y_array, features_dict, index):
    x_array.append(
        [features_dict['features'][index]['follower_bucket'],
         features_dict['features'][index]['friends_bucket'],
         features_dict['features'][index]['listed_bucket'],
         features_dict['features'][index]['favourites_bucket'],
         features_dict['features'][index]['statuses_bucket'],
         features_dict['features'][index]['sentiment'],
         features_dict['features'][index]['objectivity'],
         features_dict['features'][index]['time_bucket']
         ])
    y_array.append(features_dict['features'][index]['retweets'])


def return_training_validating_sets():
    with open('tweetsFeatures.json', 'r+') as features:
        tweets_features_dict = json.load(features)
        x_array_train = []
        y_array_train = []
        x_array_validate = []
        y_array_validate = []

        number_of_features = len(tweets_features_dict['features'])
        random.shuffle(tweets_features_dict['features'])

        for index in range(1, (number_of_features*8)//10):
            special_append(x_array_train, y_array_train, tweets_features_dict, index)
        for index in range((number_of_features * 8) // 10, number_of_features):
            special_append(x_array_validate, y_array_validate, tweets_features_dict, index)

    return x_array_train, y_array_train, x_array_validate, y_array_validate
    # print(x_array_train)
    # print(y_array_train)
    # print(x_array_validate)
    # print(y_array_validate)


def create_training_models():
    # seturile de validare si antrenare
    x_array_train, y_array_train, x_array_validate, y_array_validate = return_training_validating_sets()
    linear_regression_model = LinearRegression().fit(x_array_train, y_array_train)
    lt = linear_regression_model.score(x_array_train, y_array_train)
    lv = linear_regression_model.score(x_array_validate, y_array_validate)
    mse = mean_squared_error(y_array_validate, linear_regression_model.predict(x_array_validate))
    print("Train Score       (Linear Regression):", lt)
    print("Validation Score  (Linear Regression):", lv)
    print("Validation MSE    (Linear Regression):", mse)
    knn_model = KNeighborsRegressor(n_neighbors=7, weights='uniform')
    knn_model.fit(x_array_train, y_array_train)
    knnt = knn_model.score(x_array_train, y_array_train)
    knnv = knn_model.score(x_array_validate, y_array_validate)
    mse2 = mean_squared_error(y_array_validate, knn_model.predict(x_array_validate))
    print("Train Score       (KNN    Regression): ", knnt)
    print("Validation Score  (KNN    Regression):", knnv)
    print("Validation MSE    (KNN    Regression):", mse2)

    return linear_regression_model, knn_model, x_array_train, y_array_train, x_array_validate, y_array_validate, lt, lv, mse, knnt, knnv, mse2
    # print([x for x in knn_model.predict(x_array_validate) if x != 0])
    # predicted_list = list(knn_model.predict(x_array_validate)[0:1000])
    # for index in range(0, 1000):
    #     print(f' {predicted_list[index]} : {y_array_validate[index]}')


def load_centroids():
    with open('centroidsTweets.json', 'r+') as centroids:
        tweets_centroids_json = json.load(centroids)
    return tweets_centroids_json


def return_closest_bucket(tweet_feature, centroid_array):
    minimal = 999999999999999
    min_index = 0
    for i, centroid in enumerate(centroid_array):
        if abs(tweet_feature - centroid) < minimal:
            minimal = abs(tweet_feature - centroid)
            min_index = i
    return min_index


# print("Return Closest Bucket", return_closest_bucket(25000, tweets_centroids_json['frc_centroids']))


def take_input_from_user():
    tweets_centroids_json = load_centroids()
    followers_count = int(input("Followers Count: "))
    friends_count = int(input("Friends Count  : "))
    listed_count = int(input("Listed Count   : "))
    favourite_count = int(input("Favourite Count: "))
    statuses_count = int(input("Statuses Count : "))
    tweet_text = input("Tweet Text     : ")

    followers_bucket = return_closest_bucket(followers_count, tweets_centroids_json['fc_centroids'])
    friends_bucket = return_closest_bucket(friends_count, tweets_centroids_json['frc_centroids'])
    listed_bucket = return_closest_bucket(listed_count, tweets_centroids_json['lc_centroids'])
    favourite_bucket = return_closest_bucket(favourite_count, tweets_centroids_json['fac_centroids'])
    statuses_bucket = return_closest_bucket(statuses_count, tweets_centroids_json['sc_centroids'])
    text_analyser = Blobber(analyzer=NaiveBayesAnalyzer())
    sentiment_analysis = text_analyser(tweet_text).sentiment

    tweet_text = tweet_text + f' Followers:{followers_count}' + f'\n Friends:{friends_count}' + f'\n Listed:{listed_count}' + f'\n Favourite:{favourite_count}' + f'\n Statuses:{statuses_count}' + f'\n Sentiment:{sentiment_analysis[1]}'
    return tweet_text, [followers_bucket, friends_bucket, listed_bucket, favourite_bucket, statuses_bucket, sentiment_analysis[1], 0.5, 0]


def make_prediction(user_features, used_model):
    predictions_list = list()
    for time_bucket in range(24):
        user_features[7] = time_bucket
        print(f'Predict {time_bucket}: ', list(used_model.predict([user_features])))
        predictions_list.extend(list(used_model.predict([user_features])))
    return predictions_list


def create_plot(time, prediction, figure_number, text, training, validation, mse, keep_consistency=True):
    plot_n = plt.figure(figure_number)
    plt.plot(time, prediction)
    if keep_consistency:
        plt.axis([0, 24, 0, 130])
    plt.title("Text Used:" + text, fontsize=8, color="green")
    if keep_consistency:
        plt.savefig("../Plots/" + f'Training {training}, Validation {validation}, MSE {mse}' + datetime.now().strftime(" (%m-%d-%Y, %H-%M-%S)") + ".png", bbox_inches='tight')
    else:
        plt.savefig("../Plots/" + f'Training {training}, Validation {validation}, MSE {mse}' + datetime.now().strftime(" (%m-%d-%Y, %H-%M-%S) [F]") + ".png", bbox_inches='tight')
    plt.show()


def choose_best_time(predictions_array):
    max_retweets = 0
    good_index = []
    for prediction in predictions_array:
        if prediction > max_retweets:
            max_retweets = prediction

    for i in range(len(predictions_array)):
        if predictions_array[i] == max_retweets:
            good_index.append(i)

    return good_index, max_retweets


if __name__ == '__main__':
    tweet_text, user_input = take_input_from_user()
    linear_regression_model, knn_model, \
        x_array_train, y_array_train, x_array_validate, y_array_validate, lt, lv, mse, knnt, knnv, mse2 = create_training_models()

    fig_index = 1
    time_range = list(range(0, 24))
    # predictions = make_prediction(user_input, knn_model)
    # print(user_input)
    # create_plot(time_range, predictions, fig_index, tweet_text, knnt, knnv, mse2)
    # score = cross_val_score(knn_model, x_array_train, y_array_train, cv=5)
    # print(f'Score KNN Cross Validate: {score.mean()}')
    # predictions = make_prediction(user_input, linear_regression_model)
    # create_plot(time_range, predictions, 2, False)
    while tweet_text != '_exit':
        tweet_text, user_input = take_input_from_user()
        predictions = make_prediction(user_input, knn_model)
        create_plot(time_range, predictions, fig_index, tweet_text, knnt, knnv, mse2)
        create_plot(time_range, predictions, fig_index, tweet_text, knnt, knnv, mse2, False)
        fig_index += 1
        # score = cross_val_score(knn_model, x_array_train, y_array_train, cv=5)
        # print(f'Score KNN Cross Validate: {score.mean()}')
        predictions = make_prediction(user_input, linear_regression_model)
        create_plot(time_range, predictions, fig_index, tweet_text, lt, lv, mse, False)
        fig_index += 1












# tweet_temp_dictionary = {}
# tweets_list = []
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