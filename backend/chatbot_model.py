import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

class IntentClassifier:
    def __init__(self, intents_path='intents.json'):
        self.intents = json.load(open(intents_path))
        self.vectorizer = CountVectorizer()
        self.model = LogisticRegression()
        self._train()

    def _train(self):
        patterns = []
        tags = []
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                patterns.append(pattern)
                tags.append(intent['tag'])
        self.X = self.vectorizer.fit_transform(patterns)
        self.model.fit(self.X, tags)

    def predict_intent(self, message):
        X_test = self.vectorizer.transform([message])
        tag = self.model.predict(X_test)[0]
        for intent in self.intents['intents']:
            if intent['tag'] == tag:
                return np.random.choice(intent['responses'])

# Example usage
if __name__ == "__main__":
    classifier = IntentClassifier()
    print(classifier.predict_intent("Hello"))
