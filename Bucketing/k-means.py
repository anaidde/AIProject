import json
import numpy as np
import kmeans1d
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from datetime import datetime


def create_lists():
    json_file = open("fakeTweets.json", "r")

    json_content = json.load(json_file)

    fc_l = []
    frc_l = []
    lc_l = []
    fac_l = []
    sc_l = []
    rt_l = []
    text_l = []
    time_l = []

    for i in json_content["tweets"]:
        fc_l.append(i["u"]["fc"])
        frc_l.append(i["u"]["frc"])
        lc_l.append(i["u"]["lc"])
        fac_l.append(i["u"]["fac"])
        sc_l.append(i["u"]["sc"])
        rt_l.append((i["rt"]))
        text_l.append(i["t"])
        time_l.append(i["ca"])

    return fc_l, frc_l, lc_l, fac_l, sc_l, rt_l, text_l, time_l


def make_array_of_int(arr):
    int_arr = []
    for element in arr:
        int_arr.append(int(element))

    return int_arr


def make_json_data_file(fc, frc, lc, fac, sc, rt, txt, date):
    file_data = {"features": []}
    tb = Blobber(analyzer=NaiveBayesAnalyzer())

    for index in range(0, len(fc)):
        analysis = TextBlob(txt[index]).sentiment

        sentiment_analysis = tb(txt[index]).sentiment

        print(index)

        objectivity = 1 - analysis[1]

        file_data["features"].append({
            "index": index,
            "retweets": rt[index],
            "follower_bucket": fc[index],
            "friends_bucket": frc[index],
            "listed_bucket": lc[index],
            "favourites_bucket": fac[index],
            "statuses_bucket": sc[index],
            "sentiment": analysis[1],
            "objectivity": objectivity,
            "time_bucket": date[index]
        })

    with open('fakeResultTweets.json', 'w') as outfile:
        json.dump(file_data, outfile)


def create_time_bucket(dates_list):
    formatted_date_list = []
    returned_date_list = []

    for date in dates_list:
        date_time_obj = datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y')
        formatted_date_list.append(date_time_obj)

    for dte in formatted_date_list:
        returned_date_list.append(dte.hour)

    return returned_date_list


if __name__ == "__main__":
    fc_list, frc_list, lc_list, fac_list, sc_list, rt_list, text_list, time_list = create_lists()

    date_list = create_time_bucket(time_list)

    print(date_list)

    k = 11

    fc_array = np.array(fc_list)
    fc_clusters, fc_centroids = kmeans1d.cluster(fc_array, k)

    print("fc_plot: ", fc_array)
    print("fc_cluster: ", fc_clusters)
    print("fc_centroids: ", make_array_of_int(fc_centroids))

    k = 16

    frc_array = np.array(frc_list)
    frc_clusters, frc_centroids = kmeans1d.cluster(frc_array, k)

    print("frc_plot: ", frc_array)
    print("frc_cluster: ", frc_clusters)
    print("frc_centroids: ", make_array_of_int(frc_centroids))

    k = 7

    lc_array = np.array(lc_list)
    lc_clusters, lc_centroids = kmeans1d.cluster(lc_array, k)

    print("lc_plot: ", lc_array)
    print("lc_cluster: ", lc_clusters)
    print("lc_centroids: ", make_array_of_int(lc_centroids))

    k = 16

    fac_array = np.array(fac_list)
    fac_clusters, fac_centroids = kmeans1d.cluster(fac_array, k)

    print("fac_plot: ", fac_array)
    print("fac_cluster: ", fac_clusters)
    print("fac_centroids: ", make_array_of_int(fac_centroids))

    k = 11

    sc_array = np.array(sc_list)
    sc_clusters, sc_centroids = kmeans1d.cluster(sc_array, k)

    print("sc_plot: ", sc_array)
    print("sc_cluster: ", sc_clusters)
    print("sc_centroids: ", make_array_of_int(sc_centroids))

    print(len(sc_clusters), len(fac_clusters), len(fc_clusters), len(lc_clusters), len(frc_clusters))

    make_json_data_file(fc_clusters,
                        frc_clusters,
                        lc_clusters,
                        fac_clusters,
                        sc_clusters,
                        rt_list,
                        text_list,
                        date_list)
