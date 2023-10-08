from collections import defaultdict

def build_inverted_index(documents):
    inverted_index = defaultdict(list)

    for doc_id, doc_text in enumerate(documents):
        words = doc_text.split()
        for word in words:
            inverted_index[word].append(doc_id)

    inverted_index = dict(inverted_index)
    return inverted_index