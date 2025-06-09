import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load your dataset
df = pd.read_csv("train_data_chatbot.csv")
df.dropna(subset=['short_question', 'short_answer'], inplace=True)

# Extract lists
questions = df['short_question'].astype(str).tolist()
answers = df['short_answer'].astype(str).tolist()

# Build TF-IDF model
vectorizer = TfidfVectorizer(max_features=5000)
question_vectors = vectorizer.fit_transform(questions)

# Save vectorizer and matrix
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
joblib.dump(question_vectors, "question_vectors.pkl")

# Save question-answer pairs for lookup
df[['short_question', 'short_answer']].to_csv("qa_pairs.csv", index=False)

print("✅ TF-IDF vectorizer, question vectors, and Q&A CSV saved.")
