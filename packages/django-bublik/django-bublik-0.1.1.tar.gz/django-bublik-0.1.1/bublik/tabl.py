import datetime
import inspect

from django.db.models.fields.related_descriptors import ManyToManyDescriptor


def tabl(model_or_qs,
         field_names: str = '',
         limit: int = 300,
         skip_authored: bool = True,
         max_columns=10,
         value_max_length=32):
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

    tabler = Tabler(model_or_qs=model_or_qs,
                    field_names=field_names,
                    limit=limit,
                    skip_authored=skip_authored,
                    max_columns=max_columns,
                    value_max_length=value_max_length)
    tabler.tablify()


class Tabler:

    def __init__(self,
                 model_or_qs,
                 field_names,
                 limit,
                 skip_authored,
                 max_columns,
                 value_max_length):
        # TODO make string trim optional
        # TODO add option to skip all file/image fields
        # TODO move max_columns to kwargs
        # TODO use "key words only" feature
        # TODO add optional arg to set separator
        # TODO tabl(Group) leads to TypeError: argument of type 'AutoField' is not iterable
        self.model_or_qs = model_or_qs
        self.field_names = field_names
        self.limit = limit
        self.skip_authored = skip_authored
        self.max_columns = max_columns
        self.value_max_length = value_max_length if not field_names else 80
        self.fields_to_skip = 'created_by', 'updated_by'

        if inspect.isclass(model_or_qs):
            model = model_or_qs
            qs = model.objects.all()
        else:
            model = model_or_qs.model
            qs = model_or_qs

        self.model = model
        self.qs = qs

    def get_value(self, obj, field_name):
        if '.' in field_name:
            attr = None
            for f_name in field_name.split('.'):
                attr = getattr((attr or obj), f_name)
                if not attr:
                    break
        else:
            attr = getattr(obj, field_name)

        if isinstance(attr, datetime.datetime):
            attr = attr.isoformat(' ', 'seconds')
        elif isinstance(getattr(self.model, field_name), ManyToManyDescriptor):
            attr = '; '.join([str(obj) for obj in attr.all()])
        elif callable(attr):
            attr = attr()
        value = str(attr)

        if len(value) > self.value_max_length:
            return value[:self.value_max_length - 3] + '...'
        else:
            return value[:self.value_max_length]

    def tablify(self):
        field_names = self.field_names
        limit = self.limit
        skip_authored = self.skip_authored
        max_columns = self.max_columns
        value_max_length = self.value_max_length
        fields_to_skip = self.fields_to_skip
        model = self.model
        qs = self.qs

        if field_names:
            fields_names_list = field_names.split(',')
        else:
            fields_names_list = [f.name for f in (model._meta.fields + model._meta.many_to_many)]
            if max_columns:
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
                columns_widths[field_name].append(len(str(self.get_value(obj, field_name))))
        columns_widths = {
            f_name: min(
                max([len(f_name), *v]), value_max_length) for f_name, v in columns_widths.items()}

        print(' | '.join([f_name.ljust(columns_widths[f_name]) for f_name in fields_names_list]))
        print('-' * (sum(columns_widths.values()) + len(columns_widths) * 3))

        for obj in qs_list:
            line_items = []
            for field_name in fields_names_list:
                line_items.append(
                    str(self.get_value(obj, field_name)).ljust(columns_widths[field_name]))
            print(' | '.join(line_items))
