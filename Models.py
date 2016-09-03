import morango.modelparser as modelparser
from collections import namedtuple

# This is the canonical definition of the field types which
# should be supported by the parser and any generator. 
standard_field_types = [
	'Boolean',
	'Integer',
	'Decimal',
	'Float',
	'String',
	'Text',
	'File',
	'Image', 
	'Video',
	'Audio',
	'Date',
	'TimeInstant',
	'Duration',
	'IP',
	'URL',
	'Email',
	'Phone',
	'Country'
]

FieldMultiplicity = namedtuple('FieldMultiplicity', ['min','max'])
FieldMultiplicity.unbounded = -1

class Field():
	def __init__(self):
		pass
	def init_multiplicity(self, field_data):
		minimum = 0
		if not field_data['null']:
			minimum = 1
		if field_data['mult'] == modelparser.MULT_SINGLE:
			return FieldMultiplicity(min=minimum, max=1)
		# TODO: for now we only support 0/1 to N
		return FieldMultiplicity(min=minimum, 
			max=FieldMultiplicity.unbounded)
	def init_from_parser(self, field_data):
		self.nullable = field_data['null']
		self.type = field_data['type']
		self.name = field_data['name']
		self.relationship = self.is_relationship(field_data)
		self.multiplicity = self.init_multiplicity(field_data)
		return self
	def is_relationship(self, field_data):
		"Predicate checking if type is one of the standard ones"
		return field_data['type'] not in standard_field_types


class Model():
	def __init__(self):
		pass
	
	def init_from_parser(self, data):
		"""
		Convenience method to initialize itself from the data structure
		provided by the modelparser
		"""
		self.name = data['model']
		self.fields = [Field().init_from_parser(x) for x in data['fields']]
		return self

	def get_field(self, name):
		"Return the field with name name."
		return next(iter([x for x in self.fields if x.name == name]))