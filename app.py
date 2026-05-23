from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/url", methods=["POST"])
def url_detection():

    user_url = request.form["url"]

    suspicious_words = [
        "login",
        "verify",
        "secure",
        "bank",
        "free",
        "bonus",
        "gift"
    ]

    result = "Benign"

    for word in suspicious_words:
        if word in user_url.lower():
            result = "Malicious"
            break

    return render_template(
        "index.html",
        prediction=result,
        entered_url=user_url
    )


@app.route("/scan", methods=["POST"])
def scan_file():

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return render_template(
            "index.html",
            file_result="No File Selected"
        )

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        uploaded_file.filename
    )

    uploaded_file.save(file_path)

    suspicious_text = [
        "win money",
        "free recharge",
        "claim prize",
        "urgent",
        "lottery"
    ]

    result = "Safe File"

    if uploaded_file.filename.endswith(".txt"):

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            content = f.read().lower()

            for word in suspicious_text:
                if word in content:
                    result = "Malicious File"
                    break

    return render_template(
        "index.html",
        file_result=result
    )


if __name__ == "__main__":
    app.run(debug=True)