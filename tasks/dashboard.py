import cv2
import fiftyone as fo
import numpy as np

from .module_interface import ModuleInterface


class Starter(ModuleInterface):
	def __init__(self, **kwargs):
		self.src_path = kwargs.get("src_path")
		self.dataset_name = kwargs.get("dataset_name")

		if not self.src_path:
			raise ValueError("Source path is required")
		if not self.dataset_name:
			raise ValueError("Dataset name is required")

	def run(self, **kwargs):
		dataset = fo.Dataset.from_dir(
			dataset_dir=self.src_path,
			dataset_type=fo.types.ImageSegmentationDirectory,
			name=self.dataset_name,
		)

		session = fo.launch_app(dataset)
		session.wait()
