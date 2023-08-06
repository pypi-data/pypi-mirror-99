#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-alerts/ampel/logging/DBRejectedLogsHandler.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 29.09.2018
# Last Modified Date: 09.05.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from logging import DEBUG, WARNING, LogRecord
from typing import Dict, Any, List, Union, Optional
from pymongo.errors import BulkWriteError
from pymongo.operations import UpdateOne

from ampel.type import ChannelId
from ampel.log.AmpelLogger import AmpelLogger
from ampel.log.LightLogRecord import LightLogRecord
from ampel.log.AmpelLoggingError import AmpelLoggingError
from ampel.log.LoggingErrorReporter import LoggingErrorReporter
from ampel.core.AdminUnit import AdminUnit


class DBRejectedLogsHandler(AdminUnit):
	"""
	Saves rejected log events (by T0 filters) into the NoSQL database.
	This class does not inherit logging.Handler but implements the method handle()
	so that this class can be used together with RecordBufferingHandler.forward() or copy()
	Note: isinstance(<this class instance>, LoggingHandlerProtocol) will return true
	"""

	channel: ChannelId
	logger: AmpelLogger
	level: int = DEBUG
	single_rej_col: bool = False
	aggregate_interval: int = 1
	flush_len: int = 1000
	log_dicts: List[Dict[str, Any]] = []
	prev_record: Optional[Union[LightLogRecord, LogRecord]] = None
	run_id: Optional[Union[int, List[int]]] = None


	def __init__(self, **kwargs):
		"""
		:param single_rej_col:
		- False: rejected logs are saved in channel specific collections
		(collection name equals channel name)
		- True: rejected logs are saved in a single collection called 'logs'
		:param aggregate_interval: logs with similar attributes (log level,
		possibly stock id & channels) are aggregated in one document instead of being split
		into several documents (spares some index RAM). *aggregate_interval* is the max interval
		of time in seconds during which log aggregation takes place. Beyond this value,
		attempting a database bulk_write operation.
		:raises: None
		"""

		super().__init__(**kwargs)
		col_name = "rejected" if self.single_rej_col else self.channel
		self.context.db.enable_rejected_collections([col_name])
		self.col = self.context.db.get_collection(col_name)


	def set_run_id(self, run_id: Union[int, List[int]]) -> None:
		self.run_id = run_id


	def get_run_id(self) -> Optional[Union[int, List[int]]]:
		return self.run_id


	def handle(self, record: Union[LightLogRecord, LogRecord]) -> None:

		try:

			rd = record.__dict__
			pd = self.log_dicts[-1]

			# Same flag, date (+- 1 sec), tran_id and chans
			if (
				self.prev_record and rd['alert'] == pd['alert'] and rd.get('extra') == pd.get('extra') and
				record.created - self.prev_record.created < self.aggregate_interval
			):

				if 'msg' not in pd:
					pd['msg'] = "None log entry with identical fields repeated twice"
					return

				if isinstance(pd['msg'], list):
					pd['msg'].append(rd['msg'])
				else:
					pd['msg'] = [pd['msg'], rd['msg']]

			else:

				if len(self.log_dicts) > self.flush_len:
					self.flush()

				# If duplication exists between keys in extra and in standard rec,
				# the corresponding extra items will be overwritten (and thus ignored)
				if 'extra' in rd:
					d = {k: rd['extra'][k] for k in rd['extra']}
				else:
					d = {}

				# 'alert' and 'stock' must exist in the log record,
				# otherwise, the AP made a mistake
				d['_id'] = rd['alert']
				d['stock'] = rd['stock']
				d['dt'] = int(time())

				if record.levelno > WARNING:
					d['run'] = self.run_id

				if record.msg:
					d['msg'] = record.msg

				if not self.single_rej_col and 'channel' in rd:
					d['channel'] = rd['channel']

				if 'ac' in rd:
					d['ac'] = rd['ac']

				self.log_dicts.append(d)
				self.prev_record = record

		except Exception as e:
			LoggingErrorReporter.report(self, e)
			raise AmpelLoggingError from None


	def flush(self) -> None:
		""" Will raise Exception if DB issue occurs """

		# No log entries
		if not self.log_dicts:
			return

		try:

			# Empty referenced logs entries
			dicts = self.log_dicts
			self.log_dicts = []
			self.prev_record = None

			self.col.insert_many(dicts, ordered=False)

		except BulkWriteError as bwe:

			upserts = []

			# Recovery procedure for 'already existing logs'
			# In production, we should process alerts only once (per channel(s))
			# but during testing, reprocessing may occur.
			# In this case, we overwrite previous rejected logs
			for err_dict in bwe.details.get('writeErrors', []):

				# 'code': 11000, 'errmsg': 'E11000 duplicate key error collection: ...
				if err_dict.get("code") == 11000:
					lid = {'_id': err_dict['op'].pop('_id')}
					del err_dict['op']['stock']
					upserts.append(
						UpdateOne(lid, {'$set': err_dict['op']})
					)

			if len(upserts) != len(bwe.details.get('writeErrors', [])):
				LoggingErrorReporter.report(self, bwe, bwe.details)
				raise AmpelLoggingError from None

			self.logger.warn("Overwriting rejected alerts logs")

			try:
				# Try again, with updates this time
				self.col.bulk_write(upserts, ordered=False)
				return

			except BulkWriteError as bwee:
				LoggingErrorReporter.report(self, bwe, bwe.details)
				LoggingErrorReporter.report(self, bwee, bwee.details)

			raise AmpelLoggingError from None

		except Exception as e:

			LoggingErrorReporter.report(self, e)
			# If we can no longer keep track of what Ampel is doing,
			# better raise Exception to stop processing
			raise AmpelLoggingError from None
