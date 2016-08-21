# ============================================================
# modelparser.py
#
# (C) Tiago Almeida 2016
#
# Still in early development stages.
#
# ============================================================
import os
import random
import string
from jinja2 import Environment, FileSystemLoader

class DjangoGenerator():
	def __init__(self, models):
		self.models = models
	#
	def generate_models(self, app_name):
		PATH = os.path.dirname(os.path.abspath(__file__))
		TEMPLATE_ENVIRONMENT = Environment(
		    autoescape=False,
		    loader=FileSystemLoader(os.path.join(PATH, 'data/DjangoGenerator')),
		    trim_blocks=False)
		#
		def render_models(template_filename, context):
			return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)
		#
		def create_models_py(app_name):
		  fname = "%s/models.py" % app_name
		  context = {
		    'models': self.models
		  }
		  #
		  with open(fname, 'w') as f:
		    code = render_models('models.template.py', context)
		    f.write(code)
		#
		create_models_py(app_name)
	#
	def go(self):
		# hacky code to fix later TODO:
		app_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
		os.system('django-admin startproject %s' % app_name)
		self.generate_models(app_name)
