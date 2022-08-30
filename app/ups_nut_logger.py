#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import pathlib
import datetime
import time
import fluent.sender

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "lib"))

import nut_client
from config import load_config
import logger

UPS_CONFIG = "../ups.yml"


def get_power_list(ups_list):
    power_list = []
    for ups_info in ups_list:
        load = nut_client.get_ups_load(ups_info["host"], ups_info["model"])
        power = load * ups_info["rated_power"] / 100.0

        logging.info(
            "Fetch {model}@{host}: {power:.0f} W".format(
                model=ups_info["model"], host=ups_info["host"], power=power
            )
        )

        power_list.append(
            {
                "hostname": ups_info["label"],
                "power": int(power),
            }
        )

    return power_list


def fluent_send(sender, power_list):
    for power_info in power_list:
        if sender.emit("ups", power_info):
            logging.info("Send: {power_info}".format(power_info=str(power_info)))
            pathlib.Path(config["liveness"]["file"]).touch()
        else:
            logging.error(sender.last_error)


######################################################################
logger.init("hems.wattmeter.ups")

logging.info("Load config...")
config = load_config()
ups_list = load_config(UPS_CONFIG)

sender = fluent.sender.FluentSender("hems", host=config["fluent"]["host"])

while True:
    logging.info("Start.")

    fluent_send(sender, get_power_list(ups_list))

    logging.info("Finish.")
    pathlib.Path(config["liveness"]["file"]).touch()

    sleep_time = config["sense"]["interval"] - datetime.datetime.now().second
    logging.info("sleep {sleep_time} sec...".format(sleep_time=sleep_time))
    time.sleep(sleep_time)
