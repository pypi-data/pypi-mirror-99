#!/usr/bin/env python
import optparse
import json
import sys
import time
# import logging
import datetime
import sumologic

# logging.basicConfig(level=logging.DEBUG)

sumoUrl = "https://api.us2.sumologic.com/api"
byReceiptTime = False


def getCfg():
    from pathlib import Path
    from os import path
    import configparser

    home = str(Path.home())
    cfgPath = "{}/.sumo".format(home)
    config = configparser.ConfigParser()
    if not path.isfile(cfgPath):
        print("Error: cannot find sumo config file %s".format(cfgPath))
        sys.exit(-1)
    config.read(cfgPath)
    return (
        config["default"]["sumo_access_key_id"],
        config["default"]["sumo_secret_access_key"],
        config["default"]["timezone"]
    )


def getTimeRange(recent_hours):
    nowTime = datetime.datetime.now()
    fromTime = nowTime - datetime.timedelta(hours=recent_hours)
    toTimeStr = nowTime.strftime("%Y-%m-%dT%H:%M:%S")
    fromTimeStr = fromTime.strftime("%Y-%m-%dT%H:%M:%S")
    return (fromTimeStr, toTimeStr)


def query(sumo, q, fromTimeStr, toTimeStr, timeZone, limit):
    delay = 5
    sj = sumo.search_job(q, fromTimeStr, toTimeStr, timeZone, byReceiptTime)

    status = sumo.search_job_status(sj)
    while status["state"] != "DONE GATHERING RESULTS":
        if status["state"] == "CANCELLED":
            break
        time.sleep(delay)
        status = sumo.search_job_status(sj)
    if status["state"] == "DONE GATHERING RESULTS":
        r = sumo.search_job_messages(sj, limit=limit)
        json_formatted_str = json.dumps(r, indent=2)
        print(json_formatted_str)


def main():
    parser = optparse.OptionParser(
        "[-]echo 'query_string' | %prog [options]", version="%prog 0.1.0"
    )
    parser.add_option(
        "-r",
        "--recent_hours",
        action="store",
        dest="recent_hours",
        default="6",
        help="time range to query till now, default is 6 which means recent 6 hours (optional)",
    )
    parser.add_option(
        "-s",
        "--start_time",
        action="store",
        dest="start_time",
        help="start time to query, format is YYYY-MM-DDTH:M:S, such as 2021-01-01T00:00:00 (optional)",
    )
    parser.add_option(
        "-e",
        "--end_time",
        action="store",
        dest="end_time",
        help="end time to query, format is YYYY-MM-DDTH:M:S, such as 2021-01-01T00:00:00 (optional)",
    )
    parser.add_option(
        "-l",
        "--limit",
        action="store",
        default="10000",
        dest="limit",
        help="limited items' number to return (optional)",
    )

    (options, args) = parser.parse_args()
    q = ""
    if len(args) == 0:
        q = " ".join(sys.stdin.readlines())
    else:
        q = open(args[0], "r").read()
    startTime = options.start_time
    endTime = options.end_time
    if startTime is None and endTime is None:
        startTime, endTime = getTimeRange(int(options.recent_hours))
    elif startTime is None:
        print("--start_time is required")
        parser.print_help()
        sys.exit(-1)
    elif endTime is None:
        print("--end_time is required")
        parser.print_help()
        sys.exit(-1)
    accessId, accessKey, timezone = getCfg()
    sumo = sumologic.SumoLogic(accessId, accessKey, sumoUrl)

    query(sumo, q, startTime, endTime, timezone, int(options.limit))


if __name__ == "__main__":
    sys.exit(main())
