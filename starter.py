import argparse
import importlib
import os


def parse_args():
	arg_parser = argparse.ArgumentParser(description="MA-datatool")
	arg_parser.add_argument(
		"-t", "--task", type=str, choices=["preprocess", "dashboard"], required=False, help="Task to perform"
	)
	args, unknownargs = arg_parser.parse_known_args()
	return args, unknownargs


def parse_unknown_args(unknown_args):
	"""
	Parse unknown arguments into a dictionary where keys are argument names
	(without dashes) and values are their associated values.
	"""
	unknown_dict = {}
	key = None  # Keep track of the last key

	for arg in unknown_args:
		if arg.startswith("-"):
			# New key encountered, reset for it
			key = arg.lstrip("-")
			if key not in unknown_dict:
				unknown_dict[key] = []  # Initialize with a list to handle multiple values
		else:
			# Add value to the current key
			if key is not None:
				unknown_dict[key].append(arg)

	# Simplify single-element lists to just the value
	for key in list(unknown_dict.keys()):
		if len(unknown_dict[key]) == 1:
			unknown_dict[key] = unknown_dict[key][0]

	return unknown_dict


def main():
	args, unknown_args = parse_args()
	unknown_args = parse_unknown_args(unknown_args)

	try:
		# Dynamically import the module based on the selected task
		module_name = f"tasks.{args.task}"  # Assuming modules are in a 'tasks' subpackage
		task_module = importlib.import_module(module_name)

		# Check if the module has a `run` function
		if hasattr(task_module, "Starter"):
			starter = task_module.Starter(**unknown_args)
			starter.run()
		else:
			print(f"Error: The module '{module_name}' does not define a callable 'run' function.")
	except ModuleNotFoundError:
		print(f"Error: The module for task '{args.task}' was not found.")
	except Exception as e:
		print(f"An error occurred while running the task: {e}")


if __name__ == "__main__":
	main()
