import logging

def setup_logger() -> None:
    logging.basicConfig(
        filename="weather_app.log",
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

