from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def query(context, **kwargs):
    request = context.get('request')
    query = request.GET.copy()

    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()

@register.simple_tag(takes_context=True)
def remove_query(context, **kwargs):
    request = context.get('request')
    query = request.GET.copy()

    query.pop(kwargs.get('key'), None)

    return query.urlencode()
