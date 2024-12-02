import glob
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

	def _get_subdirs(self):
		"""Get the subdirectories of the source path."""
		label_path = self.src_path / self.label_subdir
		label_dirs = list((label_path).glob("**"))
		subdir_strings = [str(subdir.relative_to(label_path)) for subdir in label_dirs]
		print(subdir_strings)
		return label_dirs

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
		super().labels_for_semantic_segmentation()
		self._get_subdirs()

	def visualize_labels(self):
		super().visualize_labels()


PREPROCESSOR = {
	"cityscapes": CityscapesPreprocessor,
	# "synthia": SynthiaPreprocessor,
}


class Starter(ModuleInterface):
	def __init__(self, **kwargs):
		self.src_path = kwargs.get("src_path")
		self.dest_path = kwargs.get("dest_path")
		label_path = kwargs.get("label_path", "")
		image_path = kwargs.get("image_path", "")
		self.dataset_name = kwargs.get("dataset_name")

		if not isinstance(self.src_path, str):
			self.src_path = str(self.src_path)
		if not isinstance(self.dest_path, str):
			self.dest_path = str(self.dest_path)

		if self.dataset_name not in PREPROCESSOR:
			raise ValueError(f"Dataset {self.dataset_name} is not supported")

		self.preprocessor = PREPROCESSOR.get(self.dataset_name)
		self.preprocessor = self.preprocessor(self.src_path, self.dest_path, label_path, image_path)

	def run(self, **kwargs):
		self.preprocessor.labels_for_semantic_segmentation()
		self.preprocessor.visualize_labels()
