from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from .module_interface import ModuleInterface


class BasePreparation(ABC):
	"""Base class for data preparation.

	This class defines the strcuture for all preparation classes.
	For example is Cityscapes differently merged together (e.g. labels) than for example
	SYNTHIA.
	"""

	def __init__(
		self, src_path: Union[str, Path], dest_path: Union[str, Path], label_subdir: str = "", image_subdir: str = ""
	):
		"""Initialize the class.

		Args:
			src_path (Union[str, Path]): The source path to the data.
			dest_path (Union[str, Path]): The destination path to the data.
		"""

		self.src_path = Path(src_path)
		self.dest_path = Path(dest_path)
		self.label_subdir = label_subdir
		self.image_subdir = image_subdir

	@abstractmethod
	def labels_for_semantic_segmentation(self):
		"""Prepare the labels for semantic segmentation."""
		pass

	@abstractmethod
	def visualize_labels(self):
		"""Visualize the labels."""
		pass


class CityscapesPreprocessor(BasePreparation):
	def labels_for_semantic_segmentation(self):
		return super().labels_for_semantic_segmentation()

	def visualize_labels(self):
		return super().visualize_labels()


PREPROCESSOR = {
	"cityscapes": CityscapesPreprocessor,
	# "synthia": SynthiaPreprocessor,
}


class Starter(ModuleInterface):
	def __init__(self, **kwargs):
		self.src_path = kwargs.get("src_path")
		self.dest_path = kwargs.get("dest_path")
		self.dataset_name = kwargs.get("dataset_name")
		if self.dataset_name not in PREPROCESSOR:
			raise ValueError(f"Dataset {self.dataset_name} is not supported")

		self.preprocessor = PREPROCESSOR.get(self.dataset_name)

	def run(self, **kwargs):
		print(self.src_path, self.dest_path, self.dataset_name)


def run(**kwargs):
	src_path = kwargs.get("src_path")
	dest_path = kwargs.get("dest_path")
	dataset_name = kwargs.get("dataset_name")
	print(src_path, dest_path, dataset_name)
