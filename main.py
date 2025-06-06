from flask import Flask, request, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route("/generate-excel", methods=["POST"])
def generate_excel():
    data = request.json
    rows = []

    for q in data:
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
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Questions")
    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="questions.xlsx"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
