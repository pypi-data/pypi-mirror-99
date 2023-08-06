# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Record and Draft database models."""

from invenio_db import db
from invenio_drafts_resources.records import DraftMetadataBase, \
    ParentRecordMixin, ParentRecordStateMixin
from invenio_files_rest.models import Bucket
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records.models import RecordFileBase
from sqlalchemy_utils.types import UUIDType


#
# Parent
#
class RDMParentMetadata(db.Model, RecordMetadataBase):
    """Metadata store for the parent record."""

    __tablename__ = 'rdm_parents_metadata'


#
# Records
#
class RDMRecordMetadata(db.Model, RecordMetadataBase, ParentRecordMixin):
    """Represent a bibliographic record metadata."""

    __tablename__ = 'rdm_records_metadata'
    __parent_record_model__ = RDMParentMetadata

    # Enable versioning
    __versioned__ = {}

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class RecordFile(db.Model, RecordFileBase):
    """File associated with a record."""

    record_model_cls = RDMRecordMetadata

    __tablename__ = 'rdm_records_files'


#
# Drafts
#
class RDMDraftMetadata(db.Model, DraftMetadataBase, ParentRecordMixin):
    """Draft metadata for a record."""

    __tablename__ = 'rdm_drafts_metadata'
    __parent_record_model__ = RDMParentMetadata

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class DraftFile(db.Model, RecordFileBase):
    """File associated with a draft."""

    record_model_cls = RDMDraftMetadata

    __tablename__ = 'rdm_drafts_files'


#
# Versions state
#
class RDMVersionsState(db.Model, ParentRecordStateMixin):
    """Store for the version state of the parent record."""

    __tablename__ = 'rdm_versions_state'

    __parent_record_model__ = RDMParentMetadata
    __record_model__ = RDMRecordMetadata
    __draft_model__ = RDMDraftMetadata
