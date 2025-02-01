import logging

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ])

logger = logging.getLogger('fastapi-logger')

logging.getLogger('uvicorn').setLevel(logging.INFO)