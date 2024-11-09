import logging
import argparse

from requests.exceptions import RequestException

from . import enphaseenergy
from .sampling_loop import SamplingLoop
from .cfg import load_cfg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s]: %(message)s"
)

parser = argparse.ArgumentParser()
parser.add_argument("cfg_path")
args = parser.parse_args()

cfg = load_cfg(args.cfg_path)
retries = 3;
tries = 0;
while tries<retries:
    # Loop forever so that if an exception occurs, logger will restart
    try:
        tries=tries+1;
        if cfg.enphase_token == '':
            envoy_token = enphaseenergy.get_token(
                cfg.enphase_email,
                cfg.enphase_password,
                cfg.envoy_serial
            )
            tries=0;
        else:
            envoy_token=cfg.enphase_token;
        S = SamplingLoop(envoy_token, cfg)

        S.run()
    except RequestException as e:
        logging.error("%s: %s", str(type(e)), e)
        logging.info("Restarting data logger")
