# ${copyright}

import importlib
import logging
import re

from itsimodels.core.fields import (
    DictField,
    ForeignKey,
    ForeignKeyList,
    ForeignKeyListStr,
    ListField,
    TypeField
)
from itsimodels.core.base_models import BaseModel
from itsimodels.team import GLOBAL_TEAM_KEY


class KeysUpdater(object):

    def __init__(self, remapped_keys):
        self.remapped_keys = remapped_keys

    def update(self, model):
        for field_name, field in model.fields.items():
            field_value = getattr(model, field_name, None)
            if field_value is None:
                continue

            if isinstance(field, ForeignKeyListStr):
                self.update_foreign_key_list_str(model, field_name, field)

            elif isinstance(field, ForeignKey):
                self.update_foreign_key(model, field_name, field)

            elif isinstance(field, ForeignKeyList):
                self.update_foreign_key_list(model, field_name, field)

            elif isinstance(field, ListField) and field.subtype and issubclass(field.subtype, BaseModel):
                self.update_list_of_models(field_value)

            elif isinstance(field, DictField) and field.subtype and issubclass(field.subtype, BaseModel):
                self.update_dict_of_models(field_value)

            elif isinstance(field, TypeField) and field.type and issubclass(field.type, BaseModel):
                self.update(field_value)

        return model

    def update_foreign_key(self, model, field_name, field):
        old_key = getattr(model, field_name)

        if not old_key or (field.refers and field.refers == 'itsimodels.team.Team' and
                           field_name == 'team_id' and old_key == GLOBAL_TEAM_KEY):
            return

        if field.key_regex:
            match = re.search(field.key_regex, old_key, flags=re.IGNORECASE)
            if not match:
                logging.warning('Not able to find match for field_name={} using regex={}'.format(
                    field_name, field.key_regex
                ))
                return

            parsed_old_key = match.groups()[0]

            remapped_key = self.get_remapped_key(field.refers, parsed_old_key)

            new_key = old_key.replace(parsed_old_key, remapped_key)

            if not field.refers:
                logging.info('glass table eventhandlers mapped old_key={} to new_key={}'.format(
                    old_key, new_key
                ))
        else:
            new_key = self.get_remapped_key(field.refers, old_key)

        if not new_key or new_key == old_key:
            logging.warning('WARNING: Not able to find any new key to map to old key={} for model={} field_name={}'.format(
                old_key, model, field_name
            ))

        setattr(model, field_name, new_key)

    def update_foreign_key_list(self, model, field_name, field):
        foreign_key_list = getattr(model, field_name)

        if not foreign_key_list:
            return

        new_keys = []

        for old_key in foreign_key_list:
            new_key = self.get_remapped_key(field.refers, old_key)
            new_keys.append(new_key)

        setattr(model, field_name, new_keys)


    def update_foreign_key_list_str(self, model, field_name, field):
        old_key_str = getattr(model, field_name)

        if not old_key_str:
            return

        # if no regex is provided, assume ids split by ','
        key_regx = r',?([^,]+)' if not field.key_regex else field.key_regex

        match = re.findall(field.key_regex, old_key_str)
        if not match:
            logging.warning('Not able to find any foreign keys for field_name={} using regex={}'.format(
                field_name, key_regx
            ))
            return

        new_key_list = []
        for parsed_old_key in match:
            remapped_key = self.get_remapped_key(field.refers, parsed_old_key)
            if not remapped_key or remapped_key == parsed_old_key:
                logging.warning('WARNING: Not able to find any new key to map to old key={} for model={} field_name={}'.format(
                    parsed_old_key, model, field_name
                ))
            new_key_list.append(remapped_key) if remapped_key else parsed_old_key

        setattr(model, field_name, ','.join(new_key_list))


    def update_list_of_models(self, child_models):
        for child_model in child_models:
            self.update(child_model)

    def update_dict_of_models(self, dict_models):
        for _, child_model in dict_models.items():
            self.update(child_model)

    def get_remapped_key(self, model_import_name, old_key):
        if model_import_name:
            parts = model_import_name.split('.')
            pkg_name = '.'.join(parts[:-1])
            model_name = parts[-1]

            try:
                pkg = importlib.import_module(pkg_name)
            except ImportError as exc:
                logging.exception(exc)

                return old_key

            model_class = getattr(pkg, model_name)

            new_keys = self.remapped_keys.get(model_class, {})

            new_key = new_keys.get(old_key, old_key)

            return new_key
        else:
            # this foreign key has no 'refers' (i.e. url in glass table
            # eventHandlers(event_handlers)-->options-->url)
            # we will go through all objects' remmapped keys
            for _, model_key_map_dict in self.remapped_keys.items():
                new_key = model_key_map_dict.get(old_key, None)

                if new_key:
                    return new_key

            return old_key



