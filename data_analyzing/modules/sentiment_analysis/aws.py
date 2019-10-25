import boto3
import json
import datetime
import data_analyzing.modules.sentiment_analysis.config as config


def start_job(name) -> str:
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    print(json.dumps(comprehend.start_sentiment_detection_job(
            InputDataConfig={
                "InputFormat": "ONE_DOC_PER_LINE",
                "S3Uri": config.S3_AWS_INPUT_TEXT_FILE_URI
            },
            OutputDataConfig={
                "S3Uri": config.S3_AWS_OUTPUT_FILE_URI
            },
            DataAccessRoleArn="arn:aws:iam::780513940665:role/Boto3ComprehendToS3",
            LanguageCode="de", JobName=name
    ), sort_keys=True, indent=4))
    return "placeholder"


def list_jobs() -> str:
    # 1d1976d7dfac30605569ad71357b454e
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    print(json.dumps(comprehend.list_sentiment_detection_jobs(), sort_keys=True, indent=4, default=json_error_converter))
    return "placeholder"


def json_error_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
