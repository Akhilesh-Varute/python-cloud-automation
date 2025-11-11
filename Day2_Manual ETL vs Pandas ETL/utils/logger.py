import logging
from pathlib import Path


def get_logger(name: str):
    """
    Returns a configured logger instance.
    Logs both to console and to a file in /logs/app.log
    """
    # Define log directory and file path
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "app.log"

    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate log entries if logger is reused
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Log message format
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
