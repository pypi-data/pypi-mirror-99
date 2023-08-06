import logging

from copy import deepcopy
from slugify import slugify

from itsimodels.core.base_models import KEY_FIELD_NAME, ValidationError
from itsimodels.correlation_search import CorrelationSearch
from itsimodels.deep_dive import DeepDive
from itsimodels.entity_type import EntityType
from itsimodels.glass_table import GlassTable
from itsimodels.glass_table_icon import GlassTableIcon
from itsimodels.glass_table_image import GlassTableImage
from itsimodels.kpi_base_search import KpiBaseSearch, SearchMetric
from itsimodels.kpi_threshold_template import KpiThresholdTemplate
from itsimodels.neap import NotableEventAggregationPolicy
from itsimodels.service import Kpi, Service
from itsimodels.service_analyzer import ServiceAnalyzer
from itsimodels.service_template import ServiceTemplate
from itsimodels.team import Team, GLOBAL_TEAM_KEY
from itsicli.content_packs.backup.field_decode import BackupFieldDecoder


def extractor_registry():
    return {
        'base_service_template': (ServiceTemplate, Extractor),
        'correlation_search': (CorrelationSearch, ConfExtractor),
        'deep_dive': (DeepDive, Extractor),
        'entity_type': (EntityType, Extractor),
        'glass_table': (GlassTable, GlassTableExtractor),
        'glass_table_icons': (GlassTableIcon, GlassTableImageExtractor),
        'glass_table_images': (GlassTableImage, GlassTableImageExtractor),
        'home_view': (ServiceAnalyzer, Extractor),
        'kpi_base_search': (KpiBaseSearch, KpiBaseSearchExtractor),
        'kpi_threshold_template': (KpiThresholdTemplate, Extractor),
        'notable_aggregation_policy': (NotableEventAggregationPolicy, Extractor),
        'service': (Service, ServiceExtractor),
        'team': (Team, TeamExtractor)
    }


class Extractor(object):

    def __init__(self, model_class, remapped_keys, prefix=''):
        self.model_class = model_class
        self.remapped_keys = remapped_keys
        self.prefix = prefix

    def extract(self, raw_data):
        models = []

        for content in raw_data:
            model_data = self.extract_model_data(content)
            if not model_data:
                continue

            try:
                logging.debug('Validating model_data="{}"'.format(model_data))

                model = self.model_class(model_data, field_decoder=BackupFieldDecoder())
            except ValidationError as exc:
                logging.warning('Failed to extract {}'.format(self.model_class))
                logging.exception(exc)
            else:
                models.append(model)

        return models

    def extract_model_data(self, raw_data):
        immutable = str(raw_data.get('_immutable', 0))
        if immutable == '1' or immutable == 'True':
            return None

        object_key = self.get_object_key(raw_data)
        if not object_key:
            return None

        object_title = self.get_object_title(raw_data)
        if not object_title:
            return None

        old_object_key, new_object_key = self.apply_prefix(raw_data)

        self.remap_keys(old_object_key, new_object_key)

        raw_data[self.key_field] = new_object_key

        return raw_data

    def apply_prefix(self, raw_data):
        old_object_key = raw_data.get(self.raw_key_field)

        object_title = self.get_object_title(raw_data)

        new_object_key = '{}{}'.format(self.prefix, slugify(object_title))

        return old_object_key, new_object_key

    def remap_keys(self, old_object_key, new_object_key):
        if not old_object_key:
            return

        remapped_keys = self.remapped_keys.setdefault(self.model_class, {})
        remapped_keys[old_object_key] = new_object_key

    def get_object_key(self, raw_data):
        return raw_data.get(self.raw_key_field)

    def get_object_title(self, raw_data):
        return raw_data.get('title', '')

    @property
    def raw_key_field(self):
        key_field = getattr(self.model_class, KEY_FIELD_NAME)
        return key_field.alias

    @property
    def key_field(self):
        return self.raw_key_field


class ConfExtractor(Extractor):

    def extract_model_data(self, raw_data):
        content = super(ConfExtractor, self).extract_model_data(raw_data)

        data = deepcopy(content)
        data.pop('object_type', None)

        return data

    def get_object_title(self, raw_data):
        return self.get_object_key(raw_data)

    @property
    def raw_key_field(self):
        return 'name'

    @property
    def key_field(self):
        return KEY_FIELD_NAME


class ServiceExtractor(Extractor):

    SERVICE_HEALTH_SEARCH_RE = r'`get_full_itsi_summary_service_health_events\((.+)\)`'

    def extract_model_data(self, raw_data):
        old_service_key = raw_data[self.raw_key_field]

        model_data = super(ServiceExtractor, self).extract_model_data(raw_data)

        service_key = model_data[self.raw_key_field]

        kpi_remapped_keys = self.remapped_keys.setdefault(Kpi, {})

        kpis = raw_data.get('kpis', [])

        for kpi in kpis:
            old_kpi_key = kpi.get('_key', '')

            if kpi.get('type') == 'service_health':
                new_kpi_key = 'SHKPI-{}'.format(service_key)

                base_search = kpi.get('base_search', '')
                kpi['base_search'] = base_search.replace(old_service_key, service_key)

                search = kpi.get('search', '')
                kpi['search'] = search.replace(old_service_key, service_key)
            else:
                new_kpi_key = '{}{}'.format(self.prefix, old_kpi_key)

            kpi['_key'] = new_kpi_key
            kpi_remapped_keys[old_kpi_key] = new_kpi_key

        service_tags = raw_data.get('service_tags', {})
        if isinstance(service_tags, list) and not service_tags:
            # The default value of service tags is unfortunately an empty list, but
            # the model definition expects a dictionary in order to pass model validation
            raw_data['service_tags'] = {}

        return model_data


class TeamExtractor(Extractor):

    def extract_model_data(self, raw_data):
        if raw_data[self.raw_key_field] == GLOBAL_TEAM_KEY:
            return None

        return super(TeamExtractor, self).extract_model_data(raw_data)


class GlassTableExtractor(Extractor):

    def extract_model_data(self, raw_data):
        definition = raw_data.get('definition')
        if not definition:
            return None

        return super(GlassTableExtractor, self).extract_model_data(raw_data)


class GlassTableImageExtractor(Extractor):

    def extract_model_data(self, raw_data):
        object_key = self.get_object_key(raw_data)
        if not object_key:
            return None

        old_object_key, new_object_key = self.apply_prefix(raw_data)

        self.remap_keys(old_object_key, new_object_key)

        raw_data[self.raw_key_field] = new_object_key

        return raw_data

    def apply_prefix(self, raw_data):
        old_object_key = raw_data.get(self.raw_key_field)

        new_object_key = '{}{}'.format(self.prefix, old_object_key)

        return old_object_key, new_object_key


class KpiBaseSearchExtractor(Extractor):

    def extract_model_data(self, raw_data):
        model_data = super(KpiBaseSearchExtractor, self).extract_model_data(raw_data)
        if not model_data:
            return None

        metric_remapped_keys = self.remapped_keys.setdefault(SearchMetric, {})

        metrics = raw_data.get('metrics', [])

        for metric in metrics:
            old_metric_key = metric.get(self.raw_key_field)
            new_metric_key = slugify(metric.get('title', ''))

            metric[self.raw_key_field] = new_metric_key
            metric_remapped_keys[old_metric_key] = new_metric_key

        return model_data
