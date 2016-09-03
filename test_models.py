# ============================================================
# Tests for the Model and Field Classes
#
# (C) Tiago Almeida 2016
#
# 
#
# ============================================================
import unittest
import morango.modelparser as modelparser
import morango.Models as Models

class TestModels(unittest.TestCase):
	def test_tests(self):
		self.assertEqual(True, True)

	def test_blog_models_py_generation(self):
		# We instantiate the blog by using the parser
		# so if the parser is incorrect, this will fail
		models_raw = modelparser.parse_files(['test/blog.mdl'])
		models = [Models.Model().init_from_parser(x) for x in models_raw]
		# TODO: this is poor
		self.assertIsNotNone(models)

	def test_multiplicity(self):
		models_raw = modelparser.parse_files(['test/multiplicity.mdl'])
		models = [Models.Model().init_from_parser(x) for x in models_raw]
		model = models[0]
		# Field standard should be optional, i.e. 0 or 1 
		field = model.get_field('standard')
		self.assertEqual(field.multiplicity.min, 0)
		self.assertEqual(field.multiplicity.max, 1)
		# Field standardMandatory should be 1-1 
		field = model.get_field('standardMandatory')
		self.assertEqual(field.multiplicity.min, 1)
		self.assertEqual(field.multiplicity.max, 1)
		# Field related should be 0-1 
		field = model.get_field('related')
		self.assertEqual(field.multiplicity.min, 0)
		self.assertEqual(field.multiplicity.max, 1)
		# Field relatedMandatory should be 1-1 
		field = model.get_field('relatedMandatory')
		self.assertEqual(field.multiplicity.min, 1)
		self.assertEqual(field.multiplicity.max, 1)
		# Field many should be 0 - +00 
		field = model.get_field('many')
		self.assertEqual(field.multiplicity.min, 0)
		self.assertEqual(field.multiplicity.max, field.multiplicity.unbounded)
		# Field manyRelated should be 0 - +00 
		field = model.get_field('manyMandatory')
		self.assertEqual(field.multiplicity.min, 1)
		self.assertEqual(field.multiplicity.max, field.multiplicity.unbounded)

if __name__ == '__main__':
	unittest.main()