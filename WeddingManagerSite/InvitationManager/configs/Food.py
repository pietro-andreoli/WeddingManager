from collections import OrderedDict

# This is the list of food options.
# The first value in each tuple is the option ID.
# The second value in each tuple is the user-facing label.
options = OrderedDict([
	("Option 1", ("1", "Option 1")),
	("Option 2", ("2", "Option 2"))
])

class FoodOption():
	"""
	Class that represents a food option.
	"""

	def __init__(self, label, id) -> None:
		self.label = label
		self.option_id = id

def get_food_option_objs():
	"""
	Used to deserialize food options for programming related tasks.

	Returns:
		list<FoodOption>: A list of FoodOption objects representing all options.
	"""

	option_objs = []
	for opt_id, label in options:
		option_objs.append(FoodOption(label, opt_id))
	return option_objs