from flask import Flask, render_template, request, jsonify
# render_template is to render the HTML code
# jsonify is to convert the dictionary to json
from dotenv import load_dotenv

from ice_breaker import ice_break_with

load_dotenv()

app = Flask(__name__)
# Initializes a new flask application


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    # We extract the name from the form submitted
    summary, profile_pic_url = ice_break_with(name=name)
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url,
        }
    )


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)