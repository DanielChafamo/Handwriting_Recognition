import numpy as np
from naive_bayes import MultinomialNaiveBayes, GaussianNaiveBayes
from ova import OneVersusAll


class Train(object):
    def __init__(self, train_set=None, num_features=28*28, num_classes=62):
        self.num_features = num_features
        self.num_classes = num_classes
        if train_set is None:
            chars = np.load('data/chars.npz')
            train_set = chars['train_data'], np.vectorize(int)(chars['train_labels'])
        self.train_data, self.train_labels = train_set

    def multinomial_bayes(self, alpha=1e-2, save=False):
        mbayes = MultinomialNaiveBayes(self.num_features, self.num_classes)
        mbayes.train(self.train_data, self.train_labels, alpha)
        if save:
            np.save('models/multinomial_bayes', mbayes.params)
        return mbayes.params

    def gaussian_bayes(self, save=False):
        gbayes = GaussianNaiveBayes(self.num_features, self.num_classes)
        gbayes.train(self.train_data, self.train_labels)
        if save:
            np.save('models/gaussian_bayes', np.array([gbayes.means, gbayes.stdvs]))
        return gbayes.means, gbayes.stdvs

    def one_versus_all(self, episodes, epsilon=1e-3, num_batch=100, save=False):
        ova = OneVersusAll(self.num_features, self.num_classes, epsilon)
        ova.train(self.train_data, self.train_labels, episodes, num_batch)
        if save:
            np.save('models/one_versus_all', ova.params)
        return ova.params


class Predict(object):
    def __init__(self, num_features=28*28, num_classes=62):
        self.num_features = num_features
        self.num_classes = num_classes

    def multinomial_bayes(self, data=None, model=None):
        if model is None:
            model = np.load('models/multinomial_bayes.npy')
        mbayes = MultinomialNaiveBayes(self.num_features, self.num_classes)
        mbayes.set_model(model)
        prediction = np.array(map(mbayes.predict, np.atleast_2d(data)))
        return prediction

    def gaussian_bayes(self, data=None, model=None):
        if model is None:
            model = np.load('models/gaussian_bayes.npy')
        gbayes = GaussianNaiveBayes(self.num_features, self.num_classes)
        gbayes.set_model(model[0], model[1])
        prediction = np.array(map(gbayes.predict, np.atleast_2d(data)))
        return prediction

    def one_versus_all(self, data=None, model=None):
        if model is None:
            model = np.load('models/one_versus_all.npy')
        ova = OneVersusAll(self.num_features, self.num_classes)
        ova.set_model(model)
        prediction = ova.predict(np.atleast_2d(data))
        return prediction

class Tune(object):
    def __init__(self, num_features=28*28, num_classes=62):
        self.num_features = num_features
        self.num_classes = num_classes


"""
from classifier import *
train = Train()
predict = Predict()
chars = np.load('data/chars.npz')

ova = train.one_versus_all(20000, 1e-3, 150)
prediction = predict.one_versus_all(data=chars['test_data'], model=ova)
sum(prediction==chars['test_labels'])/float(len(prediction))

mbayes = train.multinomial_bayes()
prediction = predict.multinomial_bayes(data=chars['test_data'], model=mbayes)
sum(prediction==chars['test_labels'])/float(len(prediction))



"""
