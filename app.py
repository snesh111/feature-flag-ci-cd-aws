from flask import Flask, Response, jsonify
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "unknown")
FEATURE_FLAG = os.getenv("FEATURE_X", "false").lower()


@app.route("/")
def home():
    status = "ON" if FEATURE_FLAG == "true" else "OFF"
    mode = "NEW FEATURE" if FEATURE_FLAG == "true" else "OLD FEATURE"
    description = (
        "New functionality is active and controlled using feature flags."
        if FEATURE_FLAG == "true"
        else "Stable legacy functionality is running."
    )

    text = (
        "Feature Toggle Application\n"
        "==========================\n\n"
        f"App Version   : {APP_VERSION}\n"
        f"Feature Flag  : {status}\n"
        "Deployment    : ECS Blue/Green (Zero Downtime)\n"
        "Config Source : AWS SSM Parameter Store\n\n"
        f"{mode}\n"
        "------------\n"
        f"{description}\n"
    )

    return Response(text, mimetype="text/plain")


@app.route("/status")
def status():
    return jsonify({
        "app_version": APP_VERSION,
        "feature_flag": FEATURE_FLAG,
        "deployment": "blue-green",
        "config_source": "aws-ssm"
    })


@app.route("/health")
def health():
    return "OK",200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

