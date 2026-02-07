from flask import Flask, Response
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0")

FEATURE_FLAG_PARAM = os.getenv(
    "FEATURE_FLAG_PARAM",
    "/feature-flags/new_ui_enabled"
)

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")


def get_feature_flag():
    try:
        ssm = boto3.client("ssm", region_name=AWS_REGION)
        response = ssm.get_parameter(
            Name=FEATURE_FLAG_PARAM,
            WithDecryption=False
        )
        return response["Parameter"]["Value"].lower()
    except (ClientError, NoCredentialsError) as e:
        print(f"SSM error: {e}")
        return "false"


@app.route("/")
def home():
    feature_flag = get_feature_flag()

    if feature_flag == "true":
        text = (
            "Feature Toggle Application\n"
            "--------------------------\n"
            f"App Version   : {APP_VERSION}\n"
            "Feature Flag  : ON\n\n"
            "NEW FEATURE\n"
            "-----------\n"
            "New functionality is active.\n"
            "Behavior is controlled using AWS SSM Parameter Store.\n"
            "No redeployment is required to enable this feature.\n"
        )
    else:
        text = (
            "Feature Toggle Application\n"
            "--------------------------\n"
            f"App Version   : {APP_VERSION}\n"
            "Feature Flag  : OFF\n\n"
            "OLD FEATURE\n"
            "-----------\n"
            "Legacy functionality is running.\n"
            "This is the stable default behavior.\n"
            "The feature can be enabled at runtime.\n"
        )

    return Response(text, mimetype="text/plain")


@app.route("/status")
def status():
    return {
        "version": APP_VERSION,
        "feature_flag": get_feature_flag()
    }


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
