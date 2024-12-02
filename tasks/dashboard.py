import cv2
import fiftyone as fo
import numpy as np

from .module_interface import ModuleInterface


class Starter(ModuleInterface):
	def __init__(self, **kwargs):
		self.src_path = kwargs.get("src_path")
		self.dest_path = kwargs.get("dest_path")
		self.dataset_name = kwargs.get("dataset_name")

	def run(self, **kwargs):
		src_dir = kwargs.get("src_dir")
		dataset_name = kwargs.get("dataset_name")

		dataset = fo.Dataset.from_dir(
			dataset_dir=src_dir,
			dataset_type=fo.types.ImageSegmentationDirectory,
			name=dataset_name,
		)

		session = fo.launch_app(dataset)
		session.wait()
