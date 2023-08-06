# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""

from invenio_drafts_resources.services.records.schema import RecordSchema
from marshmallow import EXCLUDE, fields, post_dump
from marshmallow_utils.fields import NestedAttribute
from marshmallow_utils.permissions import FieldPermissionsMixin

from .access import AccessSchema
from .metadata import MetadataSchema
from .parent import RDMParentSchema
from .pids import PIDSchema
from .versions import VersionsSchema


class RDMRecordSchema(RecordSchema, FieldPermissionsMixin):
    """Record schema."""

    class Meta:
        """Meta class."""

        # TODO: RAISE instead!
        unknown = EXCLUDE

    field_load_permissions = {
        'access': 'manage',
        'files': 'update',
    }

    field_dump_permissions = {
        'files': 'read_files',
    }

    pids = fields.List(NestedAttribute(PIDSchema))
    metadata = NestedAttribute(MetadataSchema)
    # ext = fields.Method('dump_extensions', 'load_extensions')
    # tombstone
    # provenance
    access = fields.Nested(AccessSchema)
    # files = NestedAttribute(FilesSchema, dump_only=True)
    # notes = fields.List(fields.Nested(InternalNoteSchema))
    revision = fields.Integer(dump_only=True)
    versions = NestedAttribute(VersionsSchema, dump_only=True)
    parent = NestedAttribute(RDMParentSchema, dump_only=True)

    is_published = fields.Boolean(dump_only=True)

    # communities = NestedAttribute(CommunitiesSchema)
    # stats = NestedAttribute(StatsSchema, dump_only=True)
    # relations = NestedAttribute(RelationsSchema, dump_only=True)
    # schema_version = fields.Interger(dump_only=True)

    # def dump_extensions(self, obj):
    #     """Dumps the extensions value.

    #     :params obj: invenio_records_files.api.Record instance
    #     """
    #     current_app_metadata_extensions = (
    #         current_app.extensions['invenio-rdm-records'].metadata_extensions
    #     )
    #     ExtensionSchema = current_app_metadata_extensions.to_schema()
    #     return ExtensionSchema().dump(obj.get('extensions', {}))

    # def load_extensions(self, value):
    #     """Loads the 'extensions' field.

    #     :params value: content of the input's 'extensions' field
    #     """
    #     current_app_metadata_extensions = (
    #         current_app.extensions['invenio-rdm-records'].metadata_extensions
    #     )
    #     ExtensionSchema = current_app_metadata_extensions.to_schema()

    #     return ExtensionSchema().load(value)

    @post_dump
    def default_nested(self, data, many, **kwargs):
        """Serialize metadata as empty dict for partial drafts.

        Cannot use marshmallow for Nested fields due to issue:
        https://github.com/marshmallow-code/marshmallow/issues/1566
        https://github.com/marshmallow-code/marshmallow/issues/41
        and more.
        """
        if not data.get("metadata"):
            data["metadata"] = {}

        return data


__all__ = (
    'RDMParentSchema',
    'RDMRecordSchema',
)
