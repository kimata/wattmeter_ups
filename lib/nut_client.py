#!/usr/bin/env python3

from telnetlib import Telnet
import re
import time

NUT_PORT = 3493


def get_ups_status(host, model):
    status = {}
    with Telnet(host, NUT_PORT) as telnet:
        telnet.write("LIST VAR {model}\n".format(model=model).encode("utf-8"))
        time.sleep(0.1)
        var_list = telnet.read_very_eager().decode("utf-8")

        telnet.write("LOGOUT".encode("utf-8"))

        for var_line in var_list.split("\n"):
            var = var_line.split(" ", 4)
            if len(var) != 4:
                continue

            status[var[2]] = re.search(r'^"?(.+?)"?$', var[3]).group(1)

    return status


def get_ups_load(host, model):
    return int(get_ups_status(host, model)["ups.load"])


if __name__ == "__main__":
    import sys
    import logger

    logger.init("test")

    if len(sys.argv) > 2:
        host = sys.argv[1]
        model = sys.argv[2]
    else:
        host = "hems"
        model = "bl75t"

    print(
        "Load of {model}@{host} = {load}".format(
            model=model, host=host, load=get_ups_load(host, model)
        )
    )
