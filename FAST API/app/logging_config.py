"""Structured logging configuration.

- Logs to stdout with timestamp, level, logger name, and message
- Initializes once to avoid duplicate handlers in dev reload
"""
import logging
import sys


def setup_logging() -> None:
	root = logging.getLogger()
	# Avoid re-adding handlers when reloads happen (uvicorn --reload)
	if root.handlers:
		return
	root.setLevel(logging.INFO)
	handler = logging.StreamHandler(sys.stdout)
	formatter = logging.Formatter(
		"%(asctime)s | %(levelname)s | %(name)s | %(message)s"
	)
	handler.setFormatter(formatter)
	root.addHandler(handler) 