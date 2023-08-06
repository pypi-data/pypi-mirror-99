import datetime
import inspect

from django.db import models


def tabl(model_or_qs, field_names: str = '', limit: int = 300, skip_authored: bool = True):
    #  TODO add handling of M2M
    """
    Examples:
    >>> tabl(User, 'first_name,last_name', 10)
    or
    >>> tabl(User.objects.filter(is_staff=True), 'first_name,last_name')
    or
    >>> tabl(User, 'created_by.first_name,created_by.last_name')
    or just
    >>> tabl(SomeTable)
    """
    value_max_length = 32 if not field_names else 80
    fields_to_skip = 'created_by', 'updated_by'
    max_columns = 10

    def get_value():
        if '.' in field_name:
            attr = None
            for f_name in field_name.split('.'):
                attr = getattr((attr or obj), f_name)
                if not attr:
                    break
        else:
            attr = getattr(obj, field_name)

        if callable(attr):
            attr = attr()
        if isinstance(attr, datetime.datetime):
            attr = attr.isoformat(' ', 'seconds')
        value = str(attr)
        if len(value) > value_max_length:
            return value[:value_max_length - 3] + '...'
        else:
            return value[:value_max_length]

    qs = model_or_qs.objects.all() if inspect.isclass(model_or_qs) else model_or_qs

    if field_names:
        fields_names_list = field_names.split(',')
    else:
        model = model_or_qs if inspect.isclass(model_or_qs) else model_or_qs.model
        fields_names_list = [
             f_name.name for f_name in model._meta.fields if not isinstance(f_name, models.TextField)]
        if skip_authored and len(fields_names_list) > max_columns:
            fields_names_list = [
                    f_name for f_name in fields_names_list if f_name not in fields_to_skip]
        fields_names_list = fields_names_list[:max_columns]

    if limit:  # can be explicitly set to None
        qs = qs[:limit]
    qs_list = list(qs)

    columns_widths = {f_name: [] for f_name in fields_names_list}

    for obj in qs_list:
        for field_name in fields_names_list:
            columns_widths[field_name].append(len(str(get_value())))
    columns_widths = {
        f_name: min(max([len(f_name), *v]), value_max_length) for f_name, v in columns_widths.items()}

    print(' | '.join([f_name.ljust(columns_widths[f_name]) for f_name in fields_names_list]))
    print('-' * (sum(columns_widths.values()) + len(columns_widths) * 3))

    for obj in qs_list:
        line_items = []
        for field_name in fields_names_list:
            line_items.append(str(get_value()).ljust(columns_widths[field_name]))
        print(' | '.join(line_items))
