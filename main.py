"""main"""
from logging import config

config.fileConfig("logging.conf", disable_existing_loggers=False)


def greet_all(names: list[str]) -> None:
    """Greet all.

    Args:
        names (list[str]): [description]
    """
    for name in names:
        print("hello", name)


if __name__ == "__main__":
    pass
