#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six
from k8s.base import Model
from k8s.fields import Field, RequiredField
from k8s.models.common import ObjectMeta


class PaasbetaApplicationSpec(Model):
    application = RequiredField(six.text_type)
    image = RequiredField(six.text_type)
    config = RequiredField(dict)


class PaasbetaApplication(Model):
    class Meta:
        url_template = "/apis/schibsted.io/v1beta/namespaces/{namespace}/paasbetaapplications/{name}"
        watch_list_url = "/apis/schibsted.io/v1beta/watch/paasbetaapplications"

    # Workaround for https://github.com/kubernetes/kubernetes/issues/44182
    apiVersion = Field(six.text_type, "schibsted.io/v1beta")
    kind = Field(six.text_type, "PaasbetaApplication")

    metadata = Field(ObjectMeta)
    spec = Field(PaasbetaApplicationSpec)


class PaasbetaStatus(Model):
    class Meta:
        url_template = "/apis/schibsted.io/v1beta/namespaces/{namespace}/paasbetastatuses/{name}"

    # Workaround for https://github.com/kubernetes/kubernetes/issues/44182
    apiVersion = Field(six.text_type, "schibsted.io/v1beta")
    kind = Field(six.text_type, "PaasbetaStatus")

    metadata = Field(ObjectMeta)
    result = Field(six.text_type)
