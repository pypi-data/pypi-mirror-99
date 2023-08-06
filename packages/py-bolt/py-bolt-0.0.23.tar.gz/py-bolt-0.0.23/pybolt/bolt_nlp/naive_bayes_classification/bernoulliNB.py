from sklearn.feature_extraction.text import CountVectorizer
import os
from sklearn.naive_bayes import BernoulliNB
import joblib
import time
import numpy as np
import json
from pybolt.utils import default_logger as logging


class ClassificationModel(object):

    def __init__(self, alpha=0.1, is_train=True):
        self.vec_model = CountVectorizer(lowercase=False, token_pattern=r"(?u)[^ \n]+")
        self.classification_model = BernoulliNB(alpha=alpha)
        self.__save_path = "./models/" + str(int(time.time()))
        self.accuracy = 0.0

        if not os.path.exists(self.__save_path) and is_train:
            os.makedirs(self.__save_path)

    def fit(self, inputs, targets):
        inputs = self.vec_model.fit_transform(inputs)
        self.classification_model.fit(inputs, targets)
        # self.accuracy = self.score(inputs, targets)
        # logging.info(f"\nAccuracy: {self.accuracy}")

        self.__save()
        logging.info(f"Save model and parameters, at: {self.__save_path}")

    def load_model(self, preprocess, clf_file, vectorizer_file):
        self.preprocess = preprocess
        self.vec_model = joblib.load(vectorizer_file)
        self.classification_model = joblib.load(clf_file)

    def predict(self, inputs):
        inputs = self.preprocess(inputs)
        count_vec = self.vec_model.transform(inputs)
        ret = list(self.classification_model.predict(count_vec))
        return ret

    def score(self, inputs, targets):
        return self.classification_model.score(inputs, targets)

    def __save(self):
        joblib.dump(self.vec_model, os.path.join(self.__save_path, "vectorizer.model"))
        joblib.dump(self.classification_model,
                    os.path.join(self.__save_path, "clf_bernoulli_nb.model"))
        self.export_parameter()

    def export_parameter(self):
        features = self.vec_model.get_feature_names()
        vocab = self.vec_model.vocabulary_
        classes_ = self.classification_model.classes_
        pos_log_prob = self.classification_model.feature_log_prob_
        neg_prob = np.log(1 - np.exp(self.classification_model.feature_log_prob_))
        del_prob = (pos_log_prob - neg_prob).T
        class_log_prob = self.classification_model.class_log_prior_

        json_data = {
            "Classes": classes_.tolist(),
            # "Features": features,
            "Vocab": {k: int(v) for k, v in vocab.items()},
            "DelProb": del_prob.tolist(),
            "NegProb": neg_prob.tolist(),
            "ClassLogProb": class_log_prob.tolist()
        }

        with open(os.path.join(self.__save_path, "model.json"), 'w', encoding='utf-8') as f:
            json.dump(json_data, f)


if __name__ == '__main__':
    import jieba


    def preprocess(txts: list):
        return [" ".join(jieba.cut(txt, cut_all=True)) for txt in txts]


    cl = ClassificationModel()
    cl.load_model(preprocess,
                  "/home/geb/PycharmProjects/adrec/bernoulliNB2/models/1608199130/clf_bernoulli_nb.model",
                  "/home/geb/PycharmProjects/adrec/bernoulliNB2/models/1608199130/vectorizer.model")

    res = cl.predict(["	聚划算 日入3000w zeny 咨询ro1721"])
    print(res)
