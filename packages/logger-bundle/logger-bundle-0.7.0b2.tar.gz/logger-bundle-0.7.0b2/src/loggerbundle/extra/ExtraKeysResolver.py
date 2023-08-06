class ExtraKeysResolver:

    ignored_record_keys = [
        "name",
        "msg",
        "args",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
    ]

    @staticmethod
    def get_extra_keys(record):
        return record.__dict__.keys() - ExtraKeysResolver.ignored_record_keys
