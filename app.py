from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "status": "OK",
        "message": "OJAS backend running"
    })


@app.route("/read", methods=["GET"])
def read_meter():
    try:
        # Run your Python script
        result = subprocess.run(
            ["python", "dlms_reader.py"],
            capture_output=True,
            text=True,
            timeout=30
        )

        return jsonify({
            "success": True,
            "stdout": result.stdout,
            "stderr": result.stderr
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "error": "Script timeout"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


# 🔥 Required for deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)