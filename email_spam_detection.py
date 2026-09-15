"""
EMAIL SPAM DETECTION WITH MACHINE LEARNING
============================================
This script performs email spam detection using:
- Random Forest Classifier
- Decision Tree Classifier
- Multinomial Naive Bayes

Dataset: SMS Spam Collection (spam.csv)
"""

# ============================================
# Importing the Required Libraries
# ============================================

# Numpy Library for Numerical Calculations
import numpy as np
# Pandas Library for Dataframe
import pandas as pd
# Matplotlib for Plottings
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid blocking on plt.show()
import matplotlib.pyplot as plt
# Seaborn for heatmap
import seaborn as sns
# Pickle Library for Saving the Model
import pickle
# RE Library for Regular Expression
import re
# OS Library
import os

# NLTK Library for Natural Language Processing
import nltk
nltk.download('stopwords')  # Downloading the Stopwords

# Stopwords for removing stopwords in the Text
from nltk.corpus import stopwords
# PorterStemmer for Stemming the Words
from nltk.stem.porter import PorterStemmer

# CountVectorizer for Bagging of Words and Vectorizing it
from sklearn.feature_extraction.text import CountVectorizer
# Train_Test_Split for splitting the Dataset
from sklearn.model_selection import train_test_split

# Decision Tree Classifier, Random Forest Classifier and Multinomial Naive Bayes are Models
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB

# Accuracy Score, Confusion Matrix and Classification Report for Analysis of Models
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# ============================================
# Reading information in the Dataset
# ============================================
print("=" * 60)
print("EMAIL SPAM DETECTION WITH MACHINE LEARNING")
print("=" * 60)

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "spam.csv")

spam = pd.read_csv(csv_path, encoding='ISO-8859-1')

# Checking for null values in Data
print("\n--- Checking for Null Values ---")
print(spam.isnull().sum())

# Checking the First Five Values in the Data
print("\n--- First Five Rows ---")
print(spam.head())

# Checking the Last Five Values in the Data
print("\n--- Last Five Rows ---")
print(spam.tail())

# ============================================
# Taking the required Columns in the Dataset
# ============================================
spam = spam[['v1', 'v2']]
spam.columns = ['label', 'message']
print("\n--- After Renaming Columns ---")
print(spam.head())

# Dimensions of the Dataset
print("\n--- Shape of Dataset ---")
print(spam.shape)

# Checking for the classes in the Data
print("\n--- Class Distribution ---")
print(spam.groupby('label').size())

# ============================================
# Plotting the Label in the Dataset
# ============================================
print("\n--- Plotting Label Distribution ---")
plt.figure(figsize=(8, 5))
spam['label'].value_counts().plot(kind='bar', color=['#2ecc71', '#e74c3c'])
plt.title('Email Spam vs Ham Distribution')
plt.xlabel('Label')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'label_distribution.png'), dpi=150)
plt.show()
print("Saved: label_distribution.png")

# ============================================
# NLP - Preprocessing the Text in the Dataset
# ============================================
print("\n--- Preprocessing Text (NLP) ---")

ps = PorterStemmer()
corpus = []

for i in range(0, len(spam)):
    review = re.sub('[^a-zA-Z]', ' ', spam['message'][i])
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus.append(review)

# Printing the first 5 values in the corpus list
print("First 5 preprocessed texts:")
for i, text in enumerate(corpus[1:6], 1):
    print(f"  {i}. {text}")

# ============================================
# Creating Bag of Words Model
# ============================================
print("\n--- Creating Bag of Words Model ---")
cv = CountVectorizer(max_features=4000)
X = cv.fit_transform(corpus).toarray()
Y = pd.get_dummies(spam['label'])
Y = Y.iloc[:, 1].values

print(f"Feature Matrix Shape: {X.shape}")
print(f"Target Vector Shape: {Y.shape}")

# ============================================
# Data Modeling - Splitting the Dataset
# ============================================
print("\n--- Splitting Dataset (80% Train, 20% Test) ---")
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)
print(f"Training Set: {X_train.shape[0]} samples")
print(f"Testing Set: {X_test.shape[0]} samples")

# ============================================
# Model Building - Creating the Models
# ============================================
print("\n--- Training Models ---")

# Model 1 - Random Forest Classifier
print("Training Random Forest Classifier...")
model1 = RandomForestClassifier()
model1.fit(X_train, Y_train)

# Model 2 - Decision Tree Classifier
print("Training Decision Tree Classifier...")
model2 = DecisionTreeClassifier()
model2.fit(X_train, Y_train)

# Model 3 - Multinomial Naive Bayes
print("Training Multinomial Naive Bayes...")
model3 = MultinomialNB()
model3.fit(X_train, Y_train)

print("All models trained successfully!")

# ============================================
# Prediction
# ============================================
pred1 = model1.predict(X_test)
pred2 = model2.predict(X_test)
pred3 = model3.predict(X_test)

# ============================================
# Model Testing - Testing the Models
# ============================================
print("\n" + "=" * 60)
print("MODEL EVALUATION RESULTS")
print("=" * 60)

# Model 1 - Random Forest Classifier
print("\n--- Random Forest Classifier ---")
print("Confusion Matrix:")
print(confusion_matrix(Y_test, pred1))
print(f"Accuracy: {accuracy_score(Y_test, pred1):.4f}")

# Model 2 - Decision Tree Classifier
print("\n--- Decision Tree Classifier ---")
print("Confusion Matrix:")
print(confusion_matrix(Y_test, pred2))
print(f"Accuracy: {accuracy_score(Y_test, pred2):.4f}")

# Model 3 - Multinomial Naive Bayes
print("\n--- Multinomial Naive Bayes ---")
print("Confusion Matrix:")
print(confusion_matrix(Y_test, pred3))
print(f"Accuracy: {accuracy_score(Y_test, pred3):.4f}")

# ============================================
# Confusion Matrix Heatmap for Best Model (MNB)
# ============================================
print("\n--- Confusion Matrix Heatmap (Multinomial Naive Bayes) ---")
cm = confusion_matrix(Y_test, pred3)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Ham', 'Spam'],
            yticklabels=['Ham', 'Spam'])
plt.title('Confusion Matrix - Multinomial Naive Bayes')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'confusion_matrix_mnb.png'), dpi=150)
plt.show()
print("Saved: confusion_matrix_mnb.png")

# ============================================
# Classification Reports
# ============================================
print("\n" + "=" * 60)
print("CLASSIFICATION REPORTS")
print("=" * 60)

report1 = classification_report(Y_test, pred1)
print("\nClassification Report for Random Forest Classifier:")
print(report1)

report2 = classification_report(Y_test, pred2)
print("Classification Report for Decision Tree Classifier:")
print(report2)

report3 = classification_report(Y_test, pred3)
print("Classification Report for Multinomial Naive Bayes:")
print(report3)

# ============================================
# Best Model is Multinomial Naive Bayes
# ============================================
print("=" * 60)
print("BEST MODEL: Multinomial Naive Bayes")
print("=" * 60)

# ============================================
# Saving all the Models
# ============================================
print("\n--- Saving Models ---")

pickle.dump(model1, open(os.path.join(script_dir, "RFC.pkl"), 'wb'))
print("Saved: RFC.pkl (Random Forest Classifier)")

pickle.dump(model2, open(os.path.join(script_dir, "DTC.pkl"), 'wb'))
print("Saved: DTC.pkl (Decision Tree Classifier)")

pickle.dump(model3, open(os.path.join(script_dir, "MNB.pkl"), 'wb'))
print("Saved: MNB.pkl (Multinomial Naive Bayes)")

# Also save the CountVectorizer for future predictions
pickle.dump(cv, open(os.path.join(script_dir, "CountVectorizer.pkl"), 'wb'))
print("Saved: CountVectorizer.pkl")

print("\n" + "=" * 60)
print("ALL MODELS SAVED SUCCESSFULLY!")
print("=" * 60)
