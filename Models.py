import modelparser
from collections import namedtuple

FieldMultiplicity = namedtuple('FieldMultiplicity', ['min','max'])
FieldMultiplicity.unbounded = -1

class Field():
	def __init__(self):
		pass
	def init_multiplicity(self, field_data):
		if field_data['mult'] == modelparser.MULT_SINGLE:
			return FieldMultiplicity(min=1, max=1)
		# TODO: for now we only support 0 to N
		return FieldMultiplicity(min=0, max=FieldMultiplicity.unbounded)
	def init_from_parser(self, field_data):
		self.nullable = field_data['null']
		self.type = field_data['type']
		self.name = field_data['name']
		self.relationship = False
		self.multiplicity = self.init_multiplicity(field_data)

class Model():
	def __init__(self):
		pass
	def init_from_parser(self, data):
		"""
		Convenience method to initialize itself from the data structure
		provided by the modelparser
		"""
		self.name = data['model']
		self.fields = [Field().init_from_parser(x) for x in data.fields]