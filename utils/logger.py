import logging


def setup_logger(run_id):
    logging.basicConfig(
        filename=f"logs/automation_{run_id}.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )