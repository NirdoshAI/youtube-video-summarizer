from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    """Basic health check for Kubernetes / load balancers."""
    return jsonify(status="ok", service="youtube-video-summarizer"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
