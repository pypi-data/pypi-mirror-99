import logging


def configure_logger(noisy_pkgs=[], level=logging.DEBUG):
    logformat = "[%(levelname)s %(asctime)s] %(process)s-%(name)s: %(message)s"
    logging.basicConfig(format=logformat, datefmt="%m-%d %I:%M:%S", level=level)
    for noisy_pkg in noisy_pkgs:
        logging.getLogger(noisy_pkg).setLevel(logging.ERROR)
