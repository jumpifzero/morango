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
		self.base_path = os.getcwd()
		self.models = models
		self.text = {'generated_proj':'Generated project %s.'}
	#
	def generate_models(self, prj_name, app_name):
		PATH = os.path.dirname(os.path.abspath(__file__))
		TEMPLATE_ENVIRONMENT = Environment(
		    autoescape=False,
		    loader=FileSystemLoader(
		    	os.path.join(PATH, 'data/DjangoGenerator')),
		    trim_blocks=True,
		    lstrip_blocks=True)
		#
		def render_models(template_filename, context):
			return (TEMPLATE_ENVIRONMENT.get_template(template_filename)
								.render(context))
		#
		def create_models_py(prj_name, app_name):
		  # TODO: join paths better
		  fname = "%s/%s/%s/models.py" % (self.base_path, 
		  																prj_name, 
		  																app_name)
		  context = {
		    'models': self.models
		  }
		  #
		  with open(fname, 'w') as f:
		    code = render_models('models.template.py', context)
		    print(code)
		    f.write(code)
		#
		create_models_py(prj_name, app_name)
	#
	def go(self):
		# TODO: hacky code to fix later
		app_name = 'webapp'
		prj_name = ''.join(
				random.choice(string.ascii_lowercase) for _ in range(6))
		os.system('django-admin startproject %s' % prj_name)
		os.chdir(prj_name)
		os.system('django-admin startapp %s' % app_name)
		self.generate_models(prj_name, app_name)
		print(self.text['generated_proj'] % prj_name)
