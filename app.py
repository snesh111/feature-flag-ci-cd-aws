from flask import Flask
import os

app = Flask(__name__)

# Read values from environment variables
APP_VERSION = os.getenv("APP_VERSION", "1.0")
FEATURE_FLAG = os.getenv("FEATURE_FLAG", "false").lower()

@app.route("/")
def home():
    if FEATURE_FLAG == "true":
        feature_status = "ON"
        message = "🎉 New Feature Enabled!"
    else:
        feature_status = "OFF"
        message = "New Feature is Disabled"

    return f"""
    <h1>Feature Toggle Application</h1>
    <p><b>App Version:</b> {APP_VERSION}</p>
    <p><b>Feature Flag:</b> {feature_status}</p>
    <p>{message}</p>
    """

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
