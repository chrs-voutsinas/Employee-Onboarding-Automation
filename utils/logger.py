import logging

from config.settings import LOGS_DIR


def setup_logger(run_id):
    log_file = LOGS_DIR / f"automation_{run_id}.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )