# We use sentiment analysis provided by AWS Comprehend.
# AWS Comprehend supports three types of how to use the API.
# We can query every document one by one, which results in
# 40.000 API Calls and would be pretty bad. It also supports
# Batch sizes of 25, which would also be 1.600 API calls since
# we have > 40.000 documents. For that reason, we will use
# AWS S3 Bucket to store our documents in a file, where all
# documents are separated by a new line.

# However, if for example there is a link in a tweet,
# AWS Comprehend tends to mark the document more as neutral
# as we want to. For this reason, this class will preprocess
# the documents, removes links, hashtags, whitespaces and stuff
# and will generate a file which is ready-to-use for AWS Comprehend.
# Since this file will lose the other meta-information, such as
# timestamps, this class is also responsible for creating another
# file which holds these information to merge the files afterwards.
# With this merged file, the analysis can be visualized.

import re
import preprocessor as p
import json


def generate_files_for_analysis(collection, hashtags, aws_3_filename, meta_data_filename):
    aws_s3_file_data = __generate_aws_s3_bucket_ready_file(collection)
    meta_data = __generate_metadata(collection)
    indices_to_remove = __get_indices_with_no_hashtag(meta_data, hashtags)
    aws_s3_file_data = __remove_elements_from_list(aws_s3_file_data, indices_to_remove)
    meta_data = __remove_elements_from_list(meta_data, indices_to_remove)
    __write_file(aws_s3_file_data, aws_3_filename, json_encode=False)
    __write_file(meta_data, meta_data_filename, json_encode=True)


def merge_s3_and_metadata(aws_s3_file, meta_data_file, output_file) -> list:
    merged = []
    s3_file_content = []
    with open(aws_s3_file, "r") as f:
        for line in f.readlines():
            s3_json = json.loads(line)
            cutted_object = {
                "Sentiment": s3_json["Sentiment"],
                "SentimentScore": s3_json["SentimentScore"]
            }
            s3_file_content.append(cutted_object)
    with open(meta_data_file, "r") as f:
        i = 0
        for line in f.readlines():
            metadata_json = json.loads(line)
            merged_line = {
                "Hashtags": metadata_json["hashtags"],
                "Timestamp": metadata_json["timestamp_ms"],
                "Sentiment": s3_file_content[i]["Sentiment"],
                "SentimentScore": s3_file_content[i]["SentimentScore"]
            }
            merged.append(merged_line)
            i += 1
    __write_file(merged, output_file, json_encode=True)
    return merged


def load_analysis_data(analysis_file_path) -> list:
    analysis_data = []
    with open(analysis_file_path, "r") as f:
        for line in f.readlines():
            analysis_data.append(json.loads(line))
    return analysis_data


def __write_file(data: list, name: str, json_encode: bool = False):
    with open(name, "w") as f:
        for item in data:
            if json_encode:
                item = json.dumps(item)
            f.write("%s\n" % item)


def __remove_elements_from_list(target: list, indices: list) -> list:
    for index in sorted(indices, reverse=True):
        target.pop(index)
    return target


def __get_indices_with_no_hashtag(meta_data_file, hashtags) -> list:
    # sometimes twitter data sucks and doesn't include the
    # hashtags in the entities. We can't assign this data
    # so we get the indices and remove them from the lists
    indices = []
    for entry_index in range(len(meta_data_file)):
        entry = meta_data_file[entry_index]
        hashtag_found = False
        for hashtag in hashtags:
            if hashtag in entry["hashtags"]:
                hashtag_found = True
                break
        if not hashtag_found:
            indices.append(entry_index)
    return indices


def __generate_aws_s3_bucket_ready_file(collection):
    tweets = collection.find({}, {
        "text": 1,
        "entities": 1,
        "retweeted_status.text": 1,
        "retweeted_status.entitites": 1,
        "retweeted_status.extended_tweet.full_text": 1,
        "retweeted_status.extended_tweet.entities": 1
    })

    cleaned_tweets = []
    for tweet in tweets:
        text, _ = __get_text_and_entities_from_tweet(tweet)
        cleaned_text = p.clean(text)
        cleaned_tweets.append(cleaned_text)
    return cleaned_tweets


def __get_text_and_entities_from_tweet(tweet):
    text = tweet["text"]
    entities = tweet["entities"]

    if "retweeted_status" in tweet:
        if "text" in tweet["retweeted_status"]:
            text = tweet["retweeted_status"]["text"]
        if "entities" in tweet["retweeted_status"]:
            entities = tweet["retweeted_status"]["entities"]

        if "extended_tweet" in tweet["retweeted_status"]:
            if "full_text" in tweet["retweeted_status"]["extended_tweet"]:
                text = tweet["retweeted_status"]["extended_tweet"]["full_text"]
            if "entities" in tweet["retweeted_status"]["extended_tweet"]:
                entities = tweet["retweeted_status"]["extended_tweet"]["entities"]

    return text, entities


# The following lines are commented because the standard
# preprocessing library from twitter is used from now on
# https://pypi.org/project/tweet-preprocessor/

# def __remove_entities_from_text(text, entities: dict):
#     for entity_category in entities.values():
#         text = __remove_entity_category_from_text(text, entity_category)
#     return text
#
#
# def __remove_entity_category_from_text(text, entity_category):
#     for entity in entity_category:
#         start = entity["indices"][0]
#         end = entity["indices"][1]
#         text = __replace_substring_with_spaces(text, start, end)
#     return text
#
#
# def __replace_substring_with_spaces(text, start, end):
#     diff = end - start
#     new_text = text[0:start]
#     for i in range(diff):
#         new_text += " "
#     new_text += text[end:]
#     return new_text
#
#
# def __remove_spaces_from_text(text):
#     text = re.sub(' +', ' ', text)
#     text = text.strip()
#     return text


def __generate_metadata(collection) -> list:
    tweets = collection.find({}, {
        "text": 1,
        "entities": 1,
        "retweeted_status.text": 1,
        "retweeted_status.entitites": 1,
        "retweeted_status.extended_tweet.full_text": 1,
        "retweeted_status.extended_tweet.entities": 1,
        "timestamp_ms": 1,
    })

    metadata = []
    for tweet in tweets:
        _, entities = __get_text_and_entities_from_tweet(tweet)
        hashtags = ["#" + hashtag["text"] for hashtag in entities["hashtags"]]
        obj = {
            "hashtags": hashtags,
            "timestamp_ms": tweet["timestamp_ms"]
        }
        metadata.append(obj)
    return metadata


def __generate_metadata_file(metadata):
    return metadata
