import pandas as pd
import re
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("phishing.csv")

def extract_features(url):
    return [
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        1 if url.startswith("https") else 0,
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    ]

X = data["url"].apply(lambda x: extract_features(x)).tolist()
y = data["label"].map({"legitimate": 0, "phishing": 1})

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = GaussianNB()
model.fit(X_scaled, y)

def predict_url(url):
    features = scaler.transform([extract_features(url)])
    prediction = model.predict(features)[0]
    confidence = max(model.predict_proba(features)[0]) * 100
    return prediction, round(confidence, 2)


from sklearn.metrics import accuracy_score

predictions = model.predict(X_scaled)
accuracy = accuracy_score(y, predictions)
print("Model Accuracy:", accuracy * 100)