import pandas as pd
import json

# Load your CSV
df = pd.read_csv("train_data_chatbot.csv")

# Ensure consistent formatting
df = df.dropna(subset=["short_question", "short_answer"])

# Convert each row into a pattern-response pair
intents = []
for i, row in df.iterrows():
    intent_name = f"intent_{i}"
    pattern = row["short_question"].strip()
    answer = row["short_answer"].strip()

    # Try to reuse intents with the same answer
    existing = next((item for item in intents if item["response"] == answer), None)
    if existing:
        existing["patterns"].append(pattern)
    else:
        intents.append({
            "intent": intent_name,
            "patterns": [pattern],
            "response": answer
        })

# Save as JSON
with open("chat_data.json", "w") as f:
    json.dump(intents, f, indent=2)

print("✅ chat_data.json generated successfully!")
