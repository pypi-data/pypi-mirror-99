import logging


class YandexMetrikaApiError(Exception):
    def __init__(self, response, message=None, *args, **kwargs):
        self.response = response
        self.message = message

    def __str__(self):
        logging.info("HEADERS = " + str(self.response.headers))
        logging.info("URL = " + self.response.url)
        return "{} {} {} {}".format(
            self.response.status_code,
            self.response.reason,
            self.message or "",
            self.response.text
        )


class YandexMetrikaClientError(YandexMetrikaApiError):
    def __init__(self, response, message=None, code=None, errors=None):
        super().__init__(response, message)
        self.code = code
        self.message = message
        self.errors = errors

    def __str__(self):
        return "code={}, message={}, errors={}".format(
            self.code, self.message, self.errors
        )


class YandexMetrikaTokenError(YandexMetrikaClientError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class YandexMetrikaLimitError(YandexMetrikaClientError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class YandexMetrikaDownloadReportError(YandexMetrikaClientError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.message


class BackwardCompatibilityError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return (
            "Starting from version 2021.2.21, this {} is deprecated and not supported. "
            "Install a later version "
            "'pip install --upgrade tapi-yandex-metrika==2020.10.20'. "
            "Info https://github.com/pavelmaksimov/tapi-yandex-metrika"
        ).format(self.name)
