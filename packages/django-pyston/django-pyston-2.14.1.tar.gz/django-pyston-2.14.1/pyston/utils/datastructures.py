from django.utils.encoding import force_text
from django.db import models
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.template.defaultfilters import capfirst
from django.forms.utils import pretty_name

from chamber.utils import get_class_method

from collections import OrderedDict

from pyston.utils import split_fields, is_match, get_model_from_relation_or_none, LOOKUP_SEP, rfs
from pyston.utils.compatibility import get_all_related_objects_from_model, get_concrete_field, get_model_from_relation


class Field:

    def __init__(self, key_path, label_path):
        self.key_path = key_path
        self.label_path = label_path

    def __str__(self):
        return capfirst(' '.join(map(force_text, self.label_path))).strip()

    def __hash__(self):
        return hash(LOOKUP_SEP.join(self.key_path))

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __ne__(self, other):
        return not self.__eq__(other)


class FieldsetGenerator:

    def __init__(self, resource=None, fields_string=None, direct_serialization=False):
        self.resource = resource
        self.fields_string = fields_string
        self.direct_serialization = direct_serialization

    def _get_resource(self, obj):
        from pyston.serializer import get_resource_or_none

        if self.resource:
            return get_resource_or_none(self.resource.request, obj, self.resource.resource_typemapper)
        else:
            return None

    def _get_allowed_fieldset(self):
        from pyston.resource import DefaultRESTObjectResource

        # For security reasons only resource which defines allowed fields can be fully converted to the CSV/XLSX
        # or similar formats
        return self.resource.get_allowed_fields_rfs() if isinstance(self.resource, DefaultRESTObjectResource) else rfs()

    def _get_field_label_from_model_related_objects(self, model, field_name):
        for rel in get_all_related_objects_from_model(model):
            reverse_name = rel.get_accessor_name()
            if field_name == reverse_name:
                model = get_model_from_relation(model, field_name)
                if isinstance(rel.field, models.OneToOneField):
                    return model._meta.verbose_name
                else:
                    return model._meta.verbose_name_plural
        return None

    def _get_field_label_from_model_method(self, model, field_name):
        method = get_class_method(model, field_name)

        if not method:
            return None
        elif hasattr(method, 'short_description'):
            return method.short_description
        elif hasattr(method, 'field'):
            # Generic relation
            return getattr(method.field, 'verbose_name', pretty_name(field_name))
        else:
            return pretty_name(field_name)

    def _get_field_label_from_model_field(self, model, field_name):
        return get_concrete_field(model, field_name).verbose_name

    def _get_field_label_from_resource_method(self, resource, field_name):
        # Resources should be split to the serializers and views
        method_field = resource.get_method_returning_field_value(field_name) if resource else None
        return getattr(method_field, 'short_description', pretty_name(field_name)) if method_field else None

    def _get_field_label_from_model(self, model, resource, field_name):
        try:
            return self._get_field_label_from_model_field(model, field_name)
        except FieldDoesNotExist:
            return (
                self._get_field_label_from_resource_method(resource, field_name)
                or self._get_field_label_from_model_method(model, field_name)
                or self._get_field_label_from_model_related_objects(model, field_name)
                or pretty_name(field_name)
            )

    def _get_label(self, field_name, model):
        if model:
            return (
                self._get_field_label_from_model(model, self._get_resource(model), field_name) if field_name else ''
            )
        else:
            return field_name

    def _parse_fields_string(self, fields_string):
        fields_string = fields_string or ''

        parsed_fields = []
        for field in split_fields(fields_string):
            if LOOKUP_SEP in field:
                field_name, subfields_string = field.split(LOOKUP_SEP, 1)
            elif is_match('^[^\(\)]+\(.+\)$', field):
                field_name, subfields_string = field[:len(field) - 1].split('(', 1)
            else:
                field_name, subfields_string = field, None

            parsed_fields.append((field_name, subfields_string))
        return parsed_fields

    def _recursive_generator(self, fields, fields_string, model=None, key_path=None, label_path=None,
                             extended_fieldset=None):
        key_path = key_path or []
        label_path = label_path or []

        allowed_fieldset = self._get_allowed_fieldset()
        if extended_fieldset:
            allowed_fieldset.join(extended_fieldset)

        parsed_fields = [
            (field_name, subfields_string) for field_name, subfields_string in self._parse_fields_string(fields_string)
            if field_name in allowed_fieldset or self.direct_serialization
        ]

        for field_name, subfields_string in parsed_fields:
            self._recursive_generator(
                fields, subfields_string, get_model_from_relation_or_none(model, field_name) if model else None,
                key_path + [field_name],
                label_path + [self._get_label(field_name, model)],
                extended_fieldset=allowed_fieldset[field_name].subfieldset if allowed_fieldset[field_name] else None
            )
        if not parsed_fields:
            label = self.resource.get_field_labels().get(LOOKUP_SEP.join(key_path)) if self.resource else None
            fields.append(Field(key_path, [label] if label else label_path))

    def generate(self):
        fields = []
        self._recursive_generator(fields, self.fields_string, getattr(self.resource, 'model', None))
        return fields


class DataFieldset:

    def __init__(self, data):
        self.root = {}
        # OrderedDict is used as OrderedSet
        self.fieldset = OrderedDict()
        self._init_data(data)

    def _tree_contains(self, key_path):
        current = self.root.get(key_path[0])

        if current is None:
            return False

        for key in key_path[1:]:
            if not current:
                return True
            elif key not in current.keys():
                return False
            else:
                current = current.get(key)

        return not bool(current)

    def _remove_childs(self, key_path, tree):
        if not tree:
            del self.fieldset[LOOKUP_SEP.join(key_path)]
        else:
            for key, subtree in tree.items():
                self._remove_childs(key_path + [key], subtree)

    def _add(self, key_path):
        if not self._tree_contains(key_path):
            current = self.root
            for key in key_path:
                current[key] = current.get(key, {})
                prev = current
                current = current[key]

            if current:
                self._remove_childs(key_path, current)

            prev[key] = {}
            self.fieldset[LOOKUP_SEP.join(key_path)] = None

    def _init_data(self, converted_data, key_path=None):
        key_path = key_path or []

        if isinstance(converted_data, dict):
            for key, val in converted_data.items():
                self._init_data(val, list(key_path) + [key])
        elif isinstance(converted_data, (list, tuple, set)):
            is_last_list = False
            for val in converted_data:
                if isinstance(list, (list, tuple, set)):
                    is_last_list = True
                    break
                self._init_data(val, list(key_path))
            if is_last_list:
                self._add(key_path)
        elif converted_data is not None:
            self._add(key_path)

    def __iter__(self):
        return iter(self.fieldset.keys())

    def __nonzero__(self):
        return bool(self.fieldset)

    def __str__(self):
        return '%s' % ','.join(self.fieldset.keys())

    def __len__(self):
        return len(self.fieldset)
