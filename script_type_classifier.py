import numpy
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

class script_classifier():


    def __init__(self, file_name):
        self.request_content, self.request_labels = read_file_content(file_name)

        self.vectorizer = CountVectorizer()
        self.counts = self.vectorizer.fit_transform(self.request_content)

        self.transformer = TfidfTransformer()
        self.normalized_counts = self.transformer.fit_transform(self.counts)

        return


    def learn_gnb(self):
        gnb = GaussianNB()
        gnb.fit(self.normalized_counts.toarray(), self.request_labels)
        return gnb


    def evaluate_gnb(self):
        gnb = GaussianNB()
        scores = cross_val_score(gnb, self.normalized_counts.toarray(), self.request_labels, cv=10)

        print("\nEvaluated script identification with NB bag of words:")
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        return


    def predict_script_type(self, gnb, script_request):
        counts = self.vectorizer.transform([script_request])
        normalized_counts = self.transformer.transform(counts)
        return gnb.predict(normalized_counts.toarray())


# def learn_script_classifier(file_name, content="", labels=""):
#     if content and labels:
#         request_content = content
#         request_labels = labels
#     else:
#         request_content, request_labels = read_file_content(file_name)
#
#     vectorizer = CountVectorizer()
#     counts = vectorizer.fit_transform(request_content)
#
#     transformer = TfidfTransformer()
#     normalized_counts = transformer.fit_transform(counts)
#
#     gnb = GaussianNB()
#     gnb.fit(normalized_counts, request_labels)
#     return gnb
#
#
# def eval_script_classifier(file_name, content="", labels=""):
#     if content and labels:
#         request_content = content
#         request_labels = labels
#     else:
#         request_content, request_labels = read_file_content(file_name)
#
#     vectorizer = CountVectorizer()
#     counts = vectorizer.fit_transform(request_content)
#
#     transformer = TfidfTransformer()
#     normalized_counts = transformer.fit_transform(counts)
#
#     gnb = GaussianNB()
#     scores = cross_val_score(gnb, normalized_counts.toarray(), request_labels, cv=10)
#
#     print("\nEvalauated script identification with NB bag of words:")
#     print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
#     return


def read_file_content(file_name):
    request_content = []
    request_labels = []
    file_handle = open(file_name, 'rb')
    file_content = file_handle.read().decode('utf-8').strip()
    labeled_requests = file_content.split('\r\n')
    for labeled_request in labeled_requests:
        split_request = labeled_request.split('-')
        request_content.append(split_request[0])
        request_labels.append(split_request[1])
    return request_content, request_labels