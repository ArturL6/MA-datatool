from abc import ABC, abstractmethod


class ModuleInterface(ABC):
	@abstractmethod
	def run(self, **kwargs):
		pass
