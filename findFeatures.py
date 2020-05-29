#!/usr/local/bin/python2.7
# updated to python 3.x

import argparse as ap
import cv2
import imutils
import numpy as np
import os
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from scipy.cluster.vq import *
from sklearn.preprocessing import StandardScaler
from scipy._lib.six import xrange

# Eğitim setinin yolunu bulun
parser = ap.ArgumentParser()
parser.add_argument("-t", "--trainingSet", help="Path to Training Set", required="True")
args = vars(parser.parse_args())

# Eğitim sınıfı adlarını alın ve bunları bir listede saklayın
train_path = args["trainingSet"]
training_names = os.listdir(train_path)

#Görüntülerin tüm yolunu alın ve bunları image_paths listesine
# ve image_paths içindeki ilgili etikete kaydedin
image_paths = []
image_classes = []
class_id = 0
for training_name in training_names:
    dir = os.path.join(train_path, training_name)
    class_path = imutils.imlist(dir)
    image_paths += class_path
    image_classes += [class_id] * len(class_path)
    class_id += 1

# ORB kullanarak özellik çıkarma ve anahtar nokta dedektörü nesneleri oluşturma
fea_det = cv2.ORB_create(edgeThreshold=1)

# Tüm tanımlayıcıların depolandığı liste
des_list = []

for image_path in image_paths:
    im = cv2.imread(image_path)
    kpts, des = fea_det.detectAndCompute(im, None)
    des_list.append((image_path, des))

# Tüm tanımlayıcıları sayısal bir dizide dikey olarak yığınlama
descriptors = des_list[0][1]
for image_path, descriptor in des_list[1:]:
    descriptors = np.vstack((descriptors, descriptor))

# K-Ortalamaları Kümeleme işlemi
descriptors = descriptors.astype(float)
k = 100
voc, variance = kmeans(descriptors, k, 1)

# Özelliklerin histogramını hesapla
im_features = np.zeros((len(image_paths), k), "float32")
for i in xrange(len(image_paths)):
    words, distance = vq(des_list[i][1], voc)
    for w in words:
        im_features[i][w] += 1

# Tf-Idf vektörleştirmesi işlemi
nbr_occurences = np.sum((im_features > 0) * 1, axis=0)
idf = np.array(np.log((1.0 * len(image_paths) + 1) / (1.0 * nbr_occurences + 1)), 'float32')

# Kelimeleri ölçeklendirme
stdSlr = StandardScaler().fit(im_features)
im_features = stdSlr.transform(im_features)

# Doğrusal SVM'yi eğitin
clf = LinearSVC()
clf.fit(im_features, np.array(image_classes))

# Eğitimi kaydet
joblib.dump((clf, training_names, stdSlr, k, voc), "bof.pkl", compress=3)

#python findFeatures.py -t dataset/train/
#python getClass.py -t dataset/test --visualize