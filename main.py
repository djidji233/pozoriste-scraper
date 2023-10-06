from flask import Flask

from Voz_ZvezdaraTeatar import check_dates

app = Flask(__name__)

@app.route("/")
def index():
    return check_dates()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)