from flask import Flask, request, send_file
import pandas as pd
import io

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
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),  # Convert to bytes
        mimetype="text/csv",
        as_attachment=True,
        download_name="questions.csv"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
