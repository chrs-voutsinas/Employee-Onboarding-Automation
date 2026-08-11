import time
import logging


def retry_action(action, max_retries, retry_delay):
    total_attempts = max_retries + 1

    for attempt in range(1, total_attempts + 1):
        try:
            logging.info(
                f"Attempt {attempt}/{total_attempts}"
            )

            return action()

        except Exception as error:
            if attempt == total_attempts:
                logging.error(
                    f"Final attempt failed: {error}"
                )
                raise

            logging.warning(
                f"Attempt {attempt}/{total_attempts} failed: {error}"
            )

            logging.info(
                f"Retrying in {retry_delay} seconds..."
            )

            time.sleep(retry_delay)