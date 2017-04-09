import numpy
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

def classify_scripts(file_name):
    request_content, request_labels = read_file_content(file_name)

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(request_content)

    transformer = TfidfTransformer()
    normalized_counts = transformer.fit_transform(counts)

    gnb = GaussianNB()
    scores = cross_val_score(gnb, normalized_counts.toarray(), request_labels, cv=10)

    print("\nEvalauated script identification with NB bag of words:")
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    return

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