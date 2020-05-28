class ParseConstants(object):

    URL_KEY = "url"
    LATEST_PUBLISHED_TIME = "latest_published_time"
    CUSTOM_PARSER_PROPERTIES = "custom_parser_params"

    PARAMETER_TYPES = {
        URL_KEY: list,
        LATEST_PUBLISHED_TIME: float,
        CUSTOM_PARSER_PROPERTIES: dict
    }

    COMPULSORY_PARSER_PARAMETERS = [URL_KEY, LATEST_PUBLISHED_TIME, CUSTOM_PARSER_PROPERTIES]

    # default parser required parameters, use commented lines for references, little confusing otherwise
    # default parser specific
    # DEFAULT_PARSER_SINK_NAME = "sink_file"
    # DEFAULT_PARSER_SINK_LAST_TIME_FILE_NAME = "last_time_file"
    #
    # DEFAULT_PARSER_PROPERTIES = [DEFAULT_PARSER_SINK_NAME, DEFAULT_PARSER_SINK_LAST_TIME_FILE_NAME]
    DEFAULT_PARSER_PROPERTIES = []
