import cv2
import numpy as np
import math
from sklearn.cluster import KMeans

GREEN_INDEX = 0
BLUE_INDEX = 1
YELLOW_INDEX = 2
WHITE_INDEX = 3
RED_INDEX = 4
colors = [[0, 255, 0], [0, 0, 255], [255, 0, 0], [255, 255, 0], [255, 255, 255]]
colors_names = ['green', "blue", "yellow", "white", "red"]


def import_image(url):
    image = cv2.imread(url)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w, _ = image.shape
    w_new = int(100 * w / max(w, h))
    h_new = int(100 * h / max(w, h))
    image = cv2.resize(image, (w_new, h_new));
    image_array = image.reshape((image.shape[0] * image.shape[1], 3))
    return image_array


def create_cluster(image_array):
    clt = KMeans()
    clt.fit(image_array)
    return clt


def distance(point1, point2):
    sum = 0.0
    for i in range(len(point1)):
        sum += (float(point1[i]) - point2[i]) ** 2
    return math.sqrt(sum)


def min_distance(point1):
    min = np.Inf
    min_index = -1
    for i in range(len(colors)):
        temp = distance(point1, colors[i])
        if temp < min:
            min = temp
            min_index = i
    return min_index


def count_green(predections, indeces):
    counter = 0
    for i in predections:
        if i in indeces:
            counter += 1
    return counter


def get_green_indeces(cluster):
    arr_index = []
    for i in range(len(cluster.cluster_centers_)):
        min_dis = min_distance(cluster.cluster_centers_[i])
        if min_dis == 0:
            arr_index.append(i)
    return arr_index


def create_R_model(before, after, year1, year2):
    slope = (float(after) - float(before)) / (year2 - year1)
    intersept = (before - (slope * year1))
    return (slope, intersept)


def predict(model, year):
    y_hat = int((year * model[0]) + model[1])
    if y_hat < 0:
        return 0
    else:
        return y_hat


def predict(model, year, past):
    y_hat = int((year * model[0]) + model[1])
    if y_hat < 0:
        y_hat = 0
    return 100 - ((y_hat / float(past)) * 100)


def final(image_1, image_2, date_1=1999, date_2=2017, new_date=2030):
    image_before = import_image(image_1)
    image_after = import_image(image_2)
    cluster = create_cluster(image_before)
    arr_index = get_green_indeces(cluster)
    before_predictions = cluster.predict(image_before)
    after_predictions = cluster.predict(image_after)
    before_greens_number = count_green(before_predictions, arr_index)
    after_greens_number = count_green(after_predictions, arr_index)
    model = create_R_model(before_greens_number, after_greens_number, date_1, date_2)
    ratio = (float(after_greens_number) / before_greens_number) * 100
    before = int((before_greens_number / float(len(before_predictions))) * 100.0)
    after = int((float(after_greens_number) / len(after_predictions)) * 100.0)
    return (int(predict(model, new_date, after_greens_number)), int(100.0 - ratio), before, after)
