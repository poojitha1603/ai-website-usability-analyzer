from flask import Flask, render_template, request
from scraper import extract_website_data
from analyzer import (
    analyze_readability,
    analyze_accessibility,
    calculate_usability_score
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        input_url = request.form["url"].strip()
        url = input_url

        if not url.startswith("http"):
            url = "https://" + url

        try:
            html, text = extract_website_data(url)

            readability = analyze_readability(text)
            accessibility_issues = analyze_accessibility(html)

            score, suggestions = calculate_usability_score(
                readability, accessibility_issues
            )

            result = {
                "input_url": input_url,
                "final_url": url,
                "score": score,
                "readability": readability,
                "issues": accessibility_issues,
                "suggestions": suggestions
            }

        except Exception:
            result = {
                "error": "We couldn’t analyze this website. It may block automated tools or the URL is invalid."
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
