import os
from flask import Flask, jsonify, render_template
from monitor import shared_data

base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(base_dir, "templates"))

def get_threat(count):
    if count < 200:
        return "LOW"
    elif count < 500:
        return "MEDIUM"
    else:
        return "HIGH"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    result = []
    for ip, count in shared_data.items():
        result.append({
            "ip": ip,
            "packets": count,
            "threat": get_threat(count)
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)