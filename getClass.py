#!/usr/local/bin/python2.7

import argparse as ap
import cv2
import imutils
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from scipy.cluster.vq import *
from scipy._lib.six import xrange

# Sınıflandırıcıyı, sınıf adlarını, ölçekleyiciyi, küme sayısını ve kelime bilgisini yükleyin
clf, classes_names, stdSlr, k, voc = joblib.load("bof.pkl")

# Test setinin yolunu bulun
parser = ap.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-t", "--testingSet", help="Path to testing Set")
group.add_argument("-i", "--image", help="Path to image")
parser.add_argument('-v', "--visualize", action='store_true')
args = vars(parser.parse_args())

# Test görüntülerinin yolunu bulun) ve bir listede saklayın
image_paths = []
if args["testingSet"]:
    test_path = args["testingSet"]
    try:
        testing_names = os.listdir(test_path)
    except OSError:
        print("No such directory {}\nCheck if the file exists".format(test_path))
        exit()
    for testing_name in testing_names:
        dir = os.path.join(test_path, testing_name)
        class_path = imutils.imlist(dir)
        image_paths += class_path
else:
    image_paths = [args["image"]]

# Özellik çıkarma ve anahtar nokta dedektörü nesneleri oluşturma
fea_det = cv2.ORB_create(edgeThreshold=1)

# Tüm tanımlayıcıların depolandığı liste
des_list = []

for image_path in image_paths:
    im = cv2.imread(image_path)
    kpts, des = fea_det.detectAndCompute(im, None)
    des_list.append((image_path, des))

# Tüm tanımlayıcıları sayısal bir dizide dikey olarak yığınlama
descriptors = des_list[0][1]
print(descriptors.shape)
for image_path, descriptor in des_list[0:]:
    descriptors = np.vstack((descriptors, descriptor))

# Özelliklerin histogramını hesaplama
test_features = np.zeros((len(image_paths), k), "float32")
for i in xrange(len(image_paths)):
    words, distance = vq(des_list[i][1], voc)
    for w in words:
        test_features[i][w] += 1

# Tf-Idf vektörleştirmesi yapın
nbr_occurences = np.sum((test_features > 0) * 1, axis=0)
idf = np.array(np.log((1.0 * len(image_paths) + 1) / (1.0 * nbr_occurences + 1)), 'float32')

# Özellikleri ölçeklendirme
test_features = stdSlr.transform(test_features)

# Tahminleri gerçekleştirin
predictions = [classes_names[i] for i in clf.predict(test_features)]
fig= plt.figure(figsize=(60, 100))
columns = 12
rows = 4
sayac = 1

# Kullanıcı tarafından "true" olarak ayarlanmış bayrak görselleştirilirse sonuçları görselleştirin
if args["visualize"]:
    for image_path, prediction in zip(image_paths, predictions):
        img = cv2.imread(image_path)
        pt = (0, 3 * img.shape[0] // 4)
        cv2.putText(img, prediction, pt, cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 0], 3)
        fig.add_subplot(rows, columns, sayac)
        plt.imshow(img)
        sayac += 1
plt.show()


cv2.putText()