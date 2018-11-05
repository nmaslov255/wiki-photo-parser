#!/usr/bin/python3
import logging

QUERY_LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

Querylog = logging.getLogger('querylog')
Querylog.setLevel(logging.INFO)

Filehandler = logging.FileHandler("query.log")
Fileformatter = logging.Formatter(QUERY_LOG_FORMAT)

Filehandler.setFormatter(Fileformatter)
Querylog.addHandler(Filehandler)

# CLI logger
CLI_LOG_FORMAT = "%(levelname)s: %(message)s"

CLIlog = logging.getLogger('CLI')
CLIlog.setLevel(logging.DEBUG)

CLIhandler = logging.StreamHandler()
CLIformat = logging.Formatter(CLI_LOG_FORMAT)

CLIhandler.setFormatter(CLIformat)
CLIlog.addHandler(CLIhandler)
