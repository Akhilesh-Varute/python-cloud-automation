import logging

# Save logs to a file too
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # write to file
        logging.StreamHandler(),  # show in console
    ],
)

logging.info("Program started")
logging.warning("File not found, using default config")
logging.info("Processing complete")
