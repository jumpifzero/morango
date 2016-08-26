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
	#
	class JinjaGenerator():
		def __init__(self):
			self.PATH = os.path.dirname(os.path.abspath(__file__))
			self.TEMPLATE_ENVIRONMENT = Environment(
		    autoescape=False,
		    loader=FileSystemLoader(
		    	os.path.join(self.PATH, 'data/DjangoGenerator')),
		    trim_blocks=True,
		    lstrip_blocks=True)
		#
		def render(self, template_filename, context):
			return (self.TEMPLATE_ENVIRONMENT
							.get_template(template_filename)
							.render(context))


	def __init__(self, models):
		"""
		DjangoGenerator constructor
		Initialize:
			- name of app
			- name of project
			- a jinja2 generator 
			- project base path
		"""
		self.app_name = 'webapp'
		self.prj_name = ''.join(
			random.choice(string.ascii_lowercase) for _ in range(6))
		self.base_path = os.getcwd()
		self.models = models
		self.text = {'generated_proj':'Generated project %s.'}
		self.generator = DjangoGenerator.JinjaGenerator()
		self.admin_email = 'a@b.com' #TODO (must come from outside)
	#
	#
	def get_app_path(self):
		# TODO: join paths better
		return '%s/%s/%s' % (self.base_path, 
													self.prj_name, 
													self.app_name)
	#
	def get_proj_path(self):
		# TODO: join paths better
		return '%s/%s' % (self.base_path, 
											self.prj_name)
	#
	#
	def generate_models(self):
		# TODO: join paths better
		fname = self.get_app_path() + "/models.py" 
		context = {
			'models': self.models
		}
		with open(fname, 'w') as f:
			code = self.generator.render('models.template.py', context)
			f.write(code)
	
	#
	def generate_admin(self):
		app_path = self.get_app_path()
		fname = app_path + "/admin.py"
		context = {
			'models': self.models
		}
		#
		with open(fname, 'w') as f:
			code = self.generator.render('admin.template.py', context)
			f.write(code)
	#
	def generate_settings(self):
		context = {
			'project_name': self.prj_name
		}
		code = self.generator.render('settings.template.py', context)
		proj_path = self.get_proj_path()
		fname = proj_path + "/%s/settings.py" % self.prj_name
		with open(fname, 'w') as f:
			f.write(code)
	#
	def go(self):
		# TODO: hacky code to fix later
		os.system('django-admin startproject %s' % self.prj_name)
		os.chdir(self.prj_name)
		os.system('django-admin startapp %s' % self.app_name)
		self.generate_models()
		self.generate_admin()
		self.generate_settings()
		os.system('python3 manage.py makemigrations')
		os.system('python3 manage.py migrate')
		os.system(' python3 manage.py createsuperuser \
								--noinput --username admin --email %s' %
							(self.admin_email))
		#	python3 manage.py changepassword admin
		print(self.text['generated_proj'] % self.prj_name)
