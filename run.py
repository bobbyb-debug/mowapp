from app import create_app
import logging
from logging.handlers import RotatingFileHandler
import os

app = create_app()

if __name__ == "__main__":
    app.debug = True

    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/mowapp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] in %(module)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('MowApp startup')

    app.run(host="0.0.0.0", port=5000)
