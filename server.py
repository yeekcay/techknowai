from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
