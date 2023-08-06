# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
# Copyright (C)      2021 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM Record Service."""

from flask_babelex import lazy_gettext as _
from invenio_drafts_resources.services.records import RecordDraftServiceConfig
from invenio_drafts_resources.services.records.components import \
    DraftFilesComponent, PIDComponent
from invenio_records_resources.services import RecordServiceConfig
from invenio_records_resources.services.files.config import FileServiceConfig
from invenio_records_resources.services.records.search import terms_filter

from ..records import RDMDraft, RDMRecord
from .components import AccessComponent, MetadataComponent
from .permissions import RDMRecordPermissionPolicy
from .result_items import SecretLinkItem, SecretLinkList
from .schemas import RDMParentSchema, RDMRecordSchema
from .schemas.parent.access import SecretLink
from .search_params import AllVersionsUserRecordsParam


class RDMRecordServiceConfig(RecordDraftServiceConfig):
    """RDM record draft service config."""

    # Record class
    record_cls = RDMRecord

    # Draft class
    draft_cls = RDMDraft

    schema = RDMRecordSchema

    schema_parent = RDMParentSchema

    schema_secret_link = SecretLink

    permission_policy_cls = RDMRecordPermissionPolicy

    search_sort_options = {
        "bestmatch": dict(
            title=_('Best match'),
            fields=['_score'],  # ES defaults to desc on `_score` field
        ),
        "newest": dict(
            title=_('Newest'),
            fields=['-created'],
        ),
        "oldest": dict(
            title=_('Oldest'),
            fields=['created'],
        ),
        "version": dict(
            title=_('Version'),
            fields=['-versions.index'],
        ),
    }

    link_result_item_cls = SecretLinkItem

    link_result_list_cls = SecretLinkList

    search_facets_options = dict(
        aggs={
            'resource_type': {
                'terms': {'field': 'metadata.resource_type.type'},
                'aggs': {
                    'subtype': {
                        'terms': {'field': 'metadata.resource_type.subtype'},
                    }
                }
            },
            # 'access_right': {
            #     'terms': {'field': 'access.access_right'},
            # },
            # 'languages': {
            #     'terms': {'field': 'metadata.languages.id'},
            # },
        },
        post_filters={
            'subtype': terms_filter('metadata.resource_type.subtype'),
            'resource_type': terms_filter('metadata.resource_type.type'),
            # 'access_right': terms_filter('access.access_right'),
            # 'languages': terms_filter('metadata.languages.id'),
        }
    )

    components = [
        MetadataComponent,
        AccessComponent,
        DraftFilesComponent,
        PIDComponent,
    ]


class RDMRecordVersionsServiceConfig(RDMRecordServiceConfig):
    """Record versions service config."""

    search_sort_default = 'version'
    search_sort_default_no_query = 'version'
    search_sort_options = {
        "version": dict(
            title=_('Version'),
            fields=['-versions.index'],
        ),
    }
    search_facets_options = dict(
        aggs={},
        post_filters={},
    )


class RDMUserRecordsServiceConfig(RDMRecordServiceConfig):
    """RDM user records service configuration."""

    search_sort_default = 'bestmatch'
    search_sort_default_no_query = 'updated-desc'
    search_sort_options = {
        "bestmatch": dict(
            title=_('Best match'),
            fields=['_score'],  # ES defaults to desc on `_score` field
        ),
        "updated-desc": dict(
            title=_('Recently updated'),
            fields=['-updated'],
        ),
        "updated-asc": dict(
            title=_('Least recently updated'),
            fields=['updated'],
        ),
        "newest": dict(
            title=_('Newest'),
            fields=['-created'],
        ),
        "oldest": dict(
            title=_('Oldest'),
            fields=['created'],
        ),
        "version": dict(
            title=_('Version'),
            fields=['-versions.index'],
        ),
    }

    search_facets_options = dict(
        aggs={
            'resource_type': {
                'terms': {'field': 'metadata.resource_type.type'},
                'aggs': {
                    'subtype': {
                        'terms': {'field': 'metadata.resource_type.subtype'},
                    }
                }
            },
            # 'access_right': {
            #     'terms': {'field': 'access.access_right'},
            # },
            # 'languages': {
            #     'terms': {'field': 'metadata.languages.id'},
            # },
            'is_published': {
                'terms': {'field': 'is_published'},
            },
        },
        post_filters={
            'subtype': terms_filter('metadata.resource_type.subtype'),
            'resource_type': terms_filter('metadata.resource_type.type'),
            # 'access_right': terms_filter('access.access_right'),
            # 'languages': terms_filter('metadata.languages.id'),
            'is_published': terms_filter('is_published'),
        }
    )

    search_params_interpreters_cls = [
       AllVersionsUserRecordsParam
    ] + RecordServiceConfig.search_params_interpreters_cls


#
# Record files
#
class RDMRecordFilesServiceConfig(RDMRecordServiceConfig, FileServiceConfig):
    """RDM record files service configuration."""


#
# Draft files
#
class RDMDraftFilesServiceConfig(
        RDMRecordServiceConfig, FileServiceConfig):
    """RDM draft files service configuration."""

    record_cls = RDMDraft
