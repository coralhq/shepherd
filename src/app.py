from shepherd import start
from shepherd.config import Config
from shepherd.logging import log

if __name__ == "__main__":
    config = Config()
    config.check(log)
    config.info(log)
    start(config)
