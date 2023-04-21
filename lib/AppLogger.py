import logging


def setup_logger(file_name='app.log', level=logging.DEBUG):
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-15s %(levelname)-10s %(message)s')
    handler.setFormatter(formatter)
    file_handler = logging.FileHandler(f'logs/{file_name}')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(handler)
    logger.setLevel(level)
