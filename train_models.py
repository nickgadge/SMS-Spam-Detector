import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os
import urllib.request
import zipfile


def download_dataset():
    """Download dataset if not found"""
    if not os.path.exists('SMSSpamCollection'):
        print("Downloading dataset...")
        try:
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
            urllib.request.urlretrieve(url, "smsspamcollection.zip")
            with zipfile.ZipFile("smsspamcollection.zip", 'r') as zip_ref:
                zip_ref.extractall()
            os.remove("smsspamcollection.zip")
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False
    return True


def train_model():
    if not download_dataset():
        return False

    try:
        # Read dataset properly
        df = pd.read_csv('SMSSpamCollection', sep='\t', names=['label', 'message'], encoding='utf-8')
        print(f"Loaded {len(df)} messages")

        # Simple cleaning
        df['message'] = df['message'].str.lower()
        df = df.dropna()

        # Train model
        vectorizer = CountVectorizer(stop_words='english', max_features=1000)
        X = vectorizer.fit_transform(df['message'])
        y = df['label'].map({'ham': 0, 'spam': 1})

        model = MultinomialNB()
        model.fit(X, y)

        # Save models
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, 'models/sms_model.pkl')
        joblib.dump(vectorizer, 'models/sms_vectorizer.pkl')

        print("Model trained successfully!")
        return True

    except Exception as e:
        print(f"Training failed: {e}")
        return False


if __name__ == '__main__':
    print("Starting training...")
    if train_model():
        print("Training completed!")
    else:
        print("Training failed")