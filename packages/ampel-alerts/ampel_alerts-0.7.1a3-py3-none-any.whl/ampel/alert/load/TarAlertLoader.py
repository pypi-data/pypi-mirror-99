#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-alerts/ampel/alert/load/TarAlertLoader.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.05.2018
# Last Modified Date: 15.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import tarfile
from typing import Optional, IO
from ampel.log.AmpelLogger import AmpelLogger
from ampel.base.AmpelBaseModel import AmpelBaseModel


class TarAlertLoader(AmpelBaseModel):
	"""
	Load alerts from a ``tar`` file. The archive must be laid out like the
	`ZTF public alert archive <https://ztf.uw.edu/alerts/public/>`_, i.e. one
	alert per file.
	"""

	tar_mode: str = 'r:gz'
	start: int = 0
	file_obj: Optional[IO[bytes]]
	file_path: Optional[str]
	logger: AmpelLogger # actually optional

	def __init__(self, **kwargs) -> None:

		if kwargs.get('logger') is None:
			kwargs['logger'] = AmpelLogger.get_logger()

		super().__init__(**kwargs)

		self.chained_tal: Optional['TarAlertLoader'] = None

		if self.file_obj:
			self.tar_file = tarfile.open(fileobj=self.file_obj, mode=self.tar_mode)
		elif self.file_path:
			self.tar_file = tarfile.open(self.file_path, mode=self.tar_mode)
		else:
			raise ValueError("Please provide value either for 'file_path' or 'file_obj'")

		if self.start != 0:
			count = 0
			for tarinfo in self.tar_file:
				count += 1
				if count < self.start:
					continue


	def __iter__(self):
		return self


	def __next__(self) -> IO[bytes]:
		"""
		FYI:
		from io import IOBase
		In []: tar_file = tarfile.open("file.tar")
		In []: tar_info = tar_file.next()
		In []: isinstance(tar_file.extractfile(tar_info), IOBase)
		Out[]: True
		"""
		# Free memory
		# NB: .members is not in the typeshed stub because it's not part of the
		# public interface. Beware the temptation to call getmembers() instead;
		# while this does return .members, it also reads the entire archive as
		# a side-effect.
		self.tar_file.members.clear() # type: ignore

		if self.chained_tal is not None:
			file_obj = self.get_chained_next()
			if file_obj is not None:
				return file_obj

		# Get next element in tar archive
		tar_info = self.tar_file.next()

		# Reach end of archive
		if tar_info is None:
			if hasattr(self, "file_path"):
				self.logger.info("Reached end of tar file %s" % self.file_path)
				#self.tar_file.close()
			else:
				self.logger.info("Reached end of tar")
			raise StopIteration

		# Ignore non-file entries
		if tar_info.isfile():

			# extractfile returns a file like obj
			file_obj = self.tar_file.extractfile(tar_info)
			assert file_obj is not None

			# Handle tars with nested tars
			if tar_info.name.endswith('.tar.gz'):
				self.chained_tal = TarAlertLoader(file_obj=file_obj)
				if (subfile_obj := self.get_chained_next()) is not None:
					return subfile_obj
				else:
					return next(self)

			return file_obj

		return next(self)


	def get_chained_next(self) -> Optional[IO[bytes]]:
		assert self.chained_tal is not None
		file_obj = next(self.chained_tal, None)
		if file_obj is None:
			self.chained_tal = None
			return None

		return file_obj
