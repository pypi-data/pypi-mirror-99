import logging
import os
import platform
import warnings


from cvargparse import Arg
from cvargparse import ArgFactory
from cvargparse import GPUParser
from cvargparse.utils import logger_config

from cvfinetune.parser.dataset_args import add_dataset_args
from cvfinetune.parser.model_args import add_model_args
from cvfinetune.parser.training_args import add_training_args


def default_factory(extra_list=[]):
	return ArgFactory(extra_list)


class FineTuneParser(GPUParser):

	def _logging_config(self, simple=False):
		if not self.has_logging: return
		fmt = '{levelname:s} - [{asctime:s}] {filename:s}:{lineno:d} [{funcName:s}]: {message:s}'

		handler0 = logging.StreamHandler()
		handler0.addFilter(HostnameFilter())
		fmt0 = "<{hostname:^10s}>: " + fmt

		if self._args.logfile is None:
			filename = f"{platform.node()}.log"
		else:
			filename = self._args.logfile

		self._file_handler = handler1 = logging.FileHandler(filename=filename, mode="w")

		logger_config.init_logging_handlers([
			(handler0, fmt0, logging.INFO),
			(handler1, fmt, logging.INFO),
		])


	def __del__(self):
		try:
			if getattr(self, "_file_handler", None) is not None:
				self._file_handler.flush()
		except Exception as e:
			warnings.warn("Could not flush logs to file: {}".format(e))


	def __init__(self, *args, **kwargs):
		super(FineTuneParser, self).__init__(*args, **kwargs)
		self._file_handler = None

		add_dataset_args(self)
		add_model_args(self)
		add_training_args(self)


class HostnameFilter(logging.Filter):

	def filter(self, record):
		record.hostname = platform.node()
		return True
