from django import template
from django.template import defaultfilters
from django.utils.translation import ngettext, round_away_from_one


register = template.Library()


intword_converters = (
    (3, lambda number: ngettext('%(value)sK', '%(value)sK', number)),
    (6, lambda number: ngettext('%(value)sM', '%(value)sM', number)),
    (9, lambda number: ngettext('%(value)sB', '%(value)sB', number)),
    (12, lambda number: ngettext('%(value)sT', '%(value)sT', number)),
    (
        15,
        lambda number: ngettext(
            '%(value)sQa', '%(value)sQa', number
        ),
    ),
    (
        18,
        lambda number: ngettext(
            '%(value)sQi', '%(value)sQi', number
        ),
    ),
    (
        21,
        lambda number: ngettext('%(value)sSx', '%(value)sSx', number),
    ),
    (
        24,
        lambda number: ngettext('%(value)sSp', '%(value)sSp', number),
    ),
    (27, lambda number: ngettext('%(value)sOc', '%(value)sOc', number)),
    (30, lambda number: ngettext('%(value)sNo', '%(value)sNo', number)),
    (33, lambda number: ngettext('%(value)sDc', '%(value)sDc', number)),
    (100, lambda number: ngettext('%(value)s googol', '%(value)s googol', number)),
)


@register.filter(is_safe=False)
def intword(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    abs_value = abs(value)
    if abs_value < 1000:
        return value

    for exponent, converter in intword_converters:
        large_number = 10**exponent
        if abs_value < large_number * 1000:
            new_value = value / large_number
            rounded_value = round_away_from_one(new_value)
            return converter(abs(rounded_value)) % {
                'value': defaultfilters.floatformat(new_value, -1),
            }
    return value
