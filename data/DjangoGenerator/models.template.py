from django.db import models

{% for m in models %}
class {{m.model}}(models.Model):
	{% for f in m.fields %}
  {{f.name}} = models.CharField(max_length=30)
	{% endfor %}

{% endfor %}
