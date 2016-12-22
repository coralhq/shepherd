from shepherd import start
from shepherd.config import Config
from shepherd.logging import log
from sys import argv

if __name__ == "__main__":
    env = argv[1] if len(argv) > 1 else '.env'
    config = Config(log, dotenv=env)

    config.check()
    config.info()
    start(config)
