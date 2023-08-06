import json
import logging
import re

import six

from .base import ReboticsBaseProvider, remote_service

logger = logging.getLogger(__name__)


class DatasetProvider(ReboticsBaseProvider):
    @remote_service('/api/v1/')
    def api_root(self):
        return self.session.get()

    def validate_feature(self, feature_vector):
        if len(feature_vector) != 512:
            raise ValueError('Feature length is inconsistent')

    def clean_features(self, features):
        if isinstance(features, six.string_types):
            return features
        elif isinstance(features, list):
            for feature in features:
                self.validate_feature(feature)
            else:
                return json.dumps(features)

    @remote_service('/api/v1/classifications/classify/', timeout=120)
    def classify(self, facenet, features, threshold=0.6, closeness_range=0.03):
        return self.session.post(data=dict(
            facenet=facenet,
            features=self.clean_features(features),
            threshold=threshold,
            closeness_range=closeness_range
        ))

    @remote_service('/api/v1/classifications/classify_width_dims/', timeout=120)
    def classify_with_dimensions(self, facenet, features, threshold=0.6, closeness_range=0.03):
        return self.session.post(data=dict(
            facenet=facenet,
            feature=self.clean_features(features),
            threshold=threshold,
            closeness_range=closeness_range
        ))

    @remote_service('/api/v1/classifications/classify_width_price_tags_dims/', timeout=120)
    def classify_with_dimensions_and_price_tags(self, facenet, features, price_tags, classification_policy):
        return self.session.post(data=dict(
            facenet=facenet,
            features=self.clean_features(features),
            price_tags=price_tags,
            classification_policy=classification_policy
        ))

    @remote_service('/api/v1/classifications/reference-codes/batch/')
    def save_feature_vector_batch(self, data):
        assert isinstance(data, list), "Should be a list of data, %s type supplied" % type(data)
        return self.session.post(json=data)

    @remote_service('/api/v1/classifications/reference-codes/')
    def save_feature_vector_single(self, data):
        return self.session.post(data=data)

    def inject_retailer_reference(self, data, retailer):
        if 'x-retailer-id' not in self.get_provider_headers().keys():
            if retailer is None:
                raise ValueError('You need to specify retailer '
                                 'if you are not using retailer-in-admin authentication')
            data['retailer'] = retailer.strip()
        return data

    def construct_reference_entry(self, upc, feature, threshold,
                                  retailer, facenet):
        """
        Make dict for threshold
        :param str upc:
        :param str feature:
        :param float threshold:
        :param str retailer:
        :param str facenet:
        :return:
        """
        data = {
            'upc': upc.strip(),
            'feature': feature.strip(),
            'facenet': facenet.strip(),
            'threshold': threshold,
        }

        self.inject_retailer_reference(data, retailer)
        return data

    def save_feature_vector(self, upc, facenet, feature, threshold=0.3, retailer=None, batch_size=1):
        if batch_size > 1:
            raise NotImplementedError(
                'Implement batch upload yourself using provider.save_feature_vector_batch(list[data])'
            )

        return self.save_feature_vector_single(
            data=self.construct_reference_entry(upc, feature, threshold, retailer, facenet)
        )

    @remote_service('/api/v1/classifications/reference-codes/delete/')
    def delete_feature_vector(self, upc, facenet_version, feature, retailer=None):
        data = self.inject_retailer_reference({
            'upc': upc,
            'facenet': facenet_version,
            'feature': feature,
        }, retailer)
        return self.session.post(data=data)

    @remote_service('/api/v1/classifications/reference-codes/{object_id}/')
    def delete_feature_vector_by_id(self, object_id):
        response = self.session.delete(object_id=object_id)
        return response

    @remote_service('/api/v1/token-auth/')
    def token_auth(self, username, password):
        json_data = self.session.post(data=dict(
            username=username,
            password=password
        ))
        self.headers['Authorization'] = 'Token %s' % json_data['token']
        return json_data

    @remote_service('/api/v1/classifications/reference-codes/backup/', raw=True)
    def download_reference_database(self, retailer, facenet):
        response = self.session.post(data=dict(
            retailer=retailer,
            facenet=facenet,
        ), stream=True)
        filename = re.findall("filename=(.+)", response.headers['content-disposition'])[0].strip('"')
        return filename, response.raw

    @remote_service('/api/v1/retailer/settings/features/limit/')
    def set_feature_limit_for_product(self, limit, upc, retailer=None):
        data = dict(
            upc=upc,
            limit=limit
        )
        self.inject_retailer_reference(data, retailer)
        response = self.session.post(data=data)
        return response

    @remote_service('/api/v1/retailer/settings/')
    def set_settings(self, data, retailer=None):
        data = self.inject_retailer_reference(data, retailer)
        response = self.session.post(data=data)
        return response

    @remote_service('/api/v1/check_feature_vector_exists/', timeout=300000)
    def test_feature_vector_existence_bulk(self, data, retailer=None):
        data = self.inject_retailer_reference(data, retailer)
        response = self.session.post(json=data)
        return response

    @remote_service('/api/v1/import_training_data/', timeout=10000)
    def import_training_data(self, data):
        return self.session.post(json=data)

    @remote_service('/api/v1/classifications/reference-codes-read/')
    def get_feature_fectors_by_reatailer_and_model(self, retailer, facenet_model, page=None):
        return self.session.get(
            params={'product__retailer__code': retailer, 'facenet_model': facenet_model, 'page': page})

    @remote_service('/api/v1/classifications/reference-codes/{id}/')
    def update_upc_for_feature_vector(self, fv_id, upc):
        return self.session.patch(id=fv_id, data={'upc': upc})
