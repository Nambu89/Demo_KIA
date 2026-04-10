from flask import Flask, request, jsonify, render_template
from miapi.detector import analyze


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/check")
    def check():
        data = request.get_data()
        if not data:
            return jsonify({"error": "No image"}), 400
        try:
            return jsonify(analyze(data).to_dict())
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8000, debug=True)