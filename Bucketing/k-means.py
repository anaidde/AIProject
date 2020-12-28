import json
import numpy as np
import kmeans1d


def create_lists():
    json_file = open("fakeTweets.json", "r")

    json_content = json.load(json_file)

    fc_l = []
    frc_l = []
    lc_l = []
    fac_l = []
    sc_l = []

    for i in json_content["tweets"]:
        fc_l.append(i["u"]["fc"])
        frc_l.append(i["u"]["frc"])
        lc_l.append(i["u"]["lc"])
        fac_l.append(i["u"]["fac"])
        sc_l.append(i["u"]["sc"])

    return fc_l, frc_l, lc_l, fac_l, sc_l


if __name__ == "__main__":

    fc_list, frc_list, lc_list, fac_list, sc_list = create_lists()

    k = 11

    fc_array = np.array(fc_list)
    fc_clusters, fc_centroids = kmeans1d.cluster(fc_array, k)

    frc_array = np.array(frc_list)
    frc_clusters, frc_centroids = kmeans1d.cluster(frc_array, k)

    lc_array = np.array(lc_list)
    lc_clusters, lc_centroids = kmeans1d.cluster(lc_array, k)

    fac_array = np.array(fac_list)
    fac_clusters, fac_centroids = kmeans1d.cluster(fac_array, k)

    sc_array = np.array(sc_list)
    sc_clusters, sc_centroids = kmeans1d.cluster(sc_array, k)
   


