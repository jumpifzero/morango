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

class DjangoGenerator():
	def __init__(self, models):
		self.models = models
	
	def go(self):
		# hacky code to fix later TODO:
		app_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
		os.system('django-admin startproject %s' % app_name)