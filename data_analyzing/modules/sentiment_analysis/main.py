import data_analyzing.modules.sentiment_analysis.preprocessor as preprocessor
import data_analyzing.modules.sentiment_analysis.config as config
import data_analyzing.modules.sentiment_analysis.aws as aws
import data_analyzing.modules.sentiment_analysis.general_analysis as ga
import data_analyzing.modules.sentiment_analysis.in_match_analysis as ma


def analyze(collection, hashtags, kickoffs, highlights, create_analysis_file, fetch_data=False):
    if fetch_data:
        preprocessor.generate_files_for_analysis(collection, hashtags,
                                                 config.AWS_INPUT_TEXT_FILE_PATH, config.METADATA_FILE_PATH)
        aws.start_job("sentiment_job")
        aws.list_jobs()

    if create_analysis_file:
        analysis_data = preprocessor.merge_s3_and_metadata(config.S3_AWS_OUTPUT_FILE_PATH,
                                                           config.METADATA_FILE_PATH,
                                                           config.ANALYSIS_FILE_PATH)
    else:
        analysis_data = preprocessor.load_analysis_data(config.ANALYSIS_FILE_PATH)

    # ga.analyze(analysis_data, hashtags)
    ma.analyze(analysis_data, hashtags, kickoffs, highlights)

