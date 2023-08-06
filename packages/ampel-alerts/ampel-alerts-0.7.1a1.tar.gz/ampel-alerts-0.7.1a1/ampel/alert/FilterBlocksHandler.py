#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-alerts/ampel/alert/FilterBlocksHandler.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 29.05.2020
# Last Modified Date: 12.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence
from ampel.core.AmpelContext import AmpelContext
from ampel.alert.FilterBlock import FilterBlock
from ampel.alert.IngestionHandler import IngestionHandler
from ampel.log.AmpelLogger import AmpelLogger
from ampel.model.AlertProcessorDirective import AlertProcessorDirective


class FilterBlocksHandler:
	"""
	:param db_log_format:
	  'compact' (saves RAM by reducing the number of indexed document) or 'standard'. \
	  Compact log entries can be later converted into 'standard' format using the aggregation pipeline.
	  Avoid using 'compact' if you run the alert processor with a single channel.
	  
	  Examples: (Abbreviations: s: stock, a: alert, f: flag, r: run, c: channel, m: msg)
	  
	  - 'compact': embed channel information withing log record 'msg' field::
	    
	      {
	      	"_id" : ObjectId("5be4aa6254048041edbac352"),
	      	"s" : NumberLong(1810101032122523),
	      	"a" : NumberLong(404105201415015004),
	      	"f" : 572784643,
	      	"r" : 509,
	      	"m" : [
	      		{
	      			"c" : "NO_FILTER",
	      			"m": "Alert accepted"
	      		},
	      		{
	      			"c" : "HU_RANDOM",
	      			"m": "Alert accepted"
	      		}
	      	]
	      }

	  - 'standard': channel info are encoded in log parameter 'extra'.
	    For a given alert, one log entry is created per channel since log concatenation
	    cannot happen (the 'extra' dicts from the two log entries differ)::
	      
	      [
	          {
	              "_id" : ObjectId("5be4aa6254048041edbac353"),
	              "s" : NumberLong(1810101032122523),
	              "a" : NumberLong(404105201415015004),
	              "f" : 572784643,
	              "r" : 509,
	              "c" : "NO_FILTER",
	              "m" : "Alert accepted"
	          },
	          {
	              "_id" : ObjectId("5be4aa6254048041edbac352"),
	              "s" : NumberLong(1810101032122523),
	              "a" : NumberLong(404105201415015004),
	              "f" : 572784643,
	              "r" : 509,
	              "c" : "HU_RANDOM",
	              "m" : "Alert accepted"
	          }
		  ]
	"""

	def __init__(self,
		context: AmpelContext, logger: AmpelLogger,
		directives: Sequence[AlertProcessorDirective],
		process_name: str,
		db_log_format: str = "standard"
	) -> None:
		"""
		:raises: ValueError if no process can be loaded or if a process is
		associated with an unknown channel
		"""

		embed = db_log_format == "compact"

		# Create FilterBlock instances (instantiates channel filter and loggers)
		self.filter_blocks = [
			FilterBlock(
				context,
				channel = model.channel,
				filter_model = model.filter,
				stock_match = model.stock_match,
				process_name = process_name,
				logger = logger,
				embed = embed
			)
			for model in directives
		]

		# Robustness
		if len(self.filter_blocks) == 0:
			raise ValueError("No directive loaded, please check your config")

		# Note: channel names can be integers
		self.chan_names = [
			f"{fb.channel}" for fb in self.filter_blocks
			if fb.channel in context.config._config['channel']
		]

		# Check that channels defined in directives exist in ampel config
		if len(self.chan_names) != len(self.filter_blocks):
			for fb in self.filter_blocks:
				if fb.channel not in context.config._config['channel']:
					raise ValueError(f"Channel {fb.channel} unknown in ampel config")

		if len(self.filter_blocks) == 1 and db_log_format == "compact":
			logger.warn(
				"You should not use db_log_format='compact' with only one channel"
			)

		# Deactivated for now partly because of lack of time
		"""
		'''
		:param single_rej_col: Currently inactive
		- False: rejected logs are saved in channel specific collections (collection name equals channel name)
		- True: rejected logs are saved in a single collection called 'logs'
		'''

		ampel_db = context.get_database()
		if single_rej_col:
			ampel_db.enable_rejected_collections(['rejected'])
		else:
			ampel_db.enable_rejected_collections(
				[f"{fb.channel}" for fb in self.filter_blocks]
			)
		"""


	def ready(self, logger: AmpelLogger, run_id: int, ing_hdlr: IngestionHandler) -> None:
		for fb in self.filter_blocks:
			fb.ready(logger, run_id, ing_hdlr)


	def done(self) -> None:
		for fb in self.filter_blocks:
			fb.done()
