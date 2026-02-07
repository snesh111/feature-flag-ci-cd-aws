from flask import Flask
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0")

FEATURE_FLAG_PARAM = os.getenv(
    "FEATURE_FLAG_PARAM",
    "/feature-toggle/new-feature"
)

def get_feature_flag():
    """
    Fetch feature flag value from AWS SSM Parameter Store.
    Returns 'true' or 'false'
    """
    try:
        ssm = boto3.client("ssm", region_name=os.getenv("AWS_REGION", "ap-south-1"))
        response = ssm.get_parameter(
            Name=FEATURE_FLAG_PARAM,
            WithDecryption=False
        )
        return response["Parameter"]["Value"].lower()
    except (ClientError, NoCredentialsError):
        return "false"

@app.route("/")
def home():
    feature_flag = get_feature_flag()

    if feature_flag == "true":
        feature_status = "ON"
        message = "New Feature Enabled!"
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
