from django.contrib import admin
from .models import *

{% for m in models %}
admin.site.register({{m.model}})
{% endfor %}