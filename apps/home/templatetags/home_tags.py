from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


def get_topbar_content(context):
	request = context['request']

	return {
		'user': request.user,
	}

register.inclusion_tag("_topbar.html", takes_context=True)(get_topbar_content)