# ============================================================
# zipf Exception classes
#
# (C) Tiago Almeida 2016
#
# Still in early development stages.
#
# ============================================================

class ModelNotUnique(BaseException):
	def __init__(self, model_name):
		self.name = model_name