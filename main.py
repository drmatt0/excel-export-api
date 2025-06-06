from flask import Flask, request, jsonify
import pandas as pd
import io
import os

app = Flask(__name__)

@app.route("/generate-excel", methods=["POST"])
def generate_excel():
    data = request.json
    rows = []

    for q in data.get("questions", []):
        rows.append({
            "Question Text": q.get("question"),
            "Correct Answer": q.get("correct_answer"),
            "Distractor 1": q.get("distractors", ["", "", ""])[0],
            "Distractor 2": q.get("distractors", ["", "", ""])[1],
            "Distractor 3": q.get("distractors", ["", "", ""])[2],
            "Rationale Summary": q.get("rationale"),
            "Why High-Discrimination": q.get("why_discriminating"),
            "Why High-Yield": q.get("why_high_yield"),
            "ePBS": q.get("epbs")
        })

df = pd.DataFrame(rows)

filename = "PHR921_Questions.csv"
filepath = os.path.join("static", filename)
df.to_csv(filepath, index=False)

file_url = request.url_root.rstrip('/') + f'/static/{filename}'
return jsonify({"url": file_url})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
