from collections import namedtuple

import boto3
#import cv2
#import mxnet as mx
#import numpy as np
import utils


class FaceRecognizer:
    def __init__(self, image):
        self.image = image
        self.reko = boto3.client('rekognition')
        self.__batchTuple = namedtuple('Batch', ['data'])
        self.faces = []
        self.prevalent_emotions = []
        self.__recognize()

    def __recognize(self):
        with open(self.image, "rb") as image:
            self.faces = self.reko.detect_faces(
                Image={'Bytes': image.read()},
                Attributes=['ALL']
            )
            self.__find_prevalent_emotions()
#            self.__predict_categories_locally()

    def __find_prevalent_emotions(self):
        for face in self.faces['FaceDetails']:
            emotions = face['Emotions']
            self.prevalent_emotions.append(utils.filter_item_by_attribute(emotions, 'Confidence'))

"""
    def __predict_categories_locally(self):
        print('downloading imagenet model...')
        folder = 'resnet'
        path = 'http://data.mxnet.io/models/imagenet-11k/'
        [mx.test_utils.download(path + 'resnet-152/resnet-152-symbol.json', folder),
         mx.test_utils.download(path + 'resnet-152/resnet-152-0000.params', folder),
         mx.test_utils.download(path + 'synset.txt', folder)]
        print('loading imagenet mxnet model...')
        sym, arg_params, aux_params = mx.model.load_checkpoint('resnet/resnet-152', 0)
        mod = mx.mod.Module(symbol=sym, context=mx.cpu(), label_names=None)
        mod.bind(for_training=False, data_shapes=[('data', (1, 3, 224, 224))],
                 label_shapes=mod._label_shapes)
        mod.set_params(arg_params, aux_params, allow_missing=True)
        print('loading category labels...')
        with open('resnet/synset.txt', 'r') as f:
            labels = [l.rstrip() for l in f]

        print('converting image %s for model evaluation...' % self.image)
        img = cv2.cvtColor(cv2.imread(self.image), cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 1, 2)
        img = img[np.newaxis, :]

        print('evaluating image with mxnet model...')
        mod.forward(self.__batchTuple([mx.nd.array(img)]))
        prob = mod.get_outputs()[0].asnumpy()

        print('top 5 image classifications detected:')
        prob = np.squeeze(prob)
        a = np.argsort(prob)[::-1]
        for i in a[0:5]:
            print('-> probability=%f, class=%s' % (prob[i], labels[i]))
"""