# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio RDM module to create REST APIs."""

from .resources import RDMDraftActionResource, RDMDraftFilesActionResource, \
    RDMDraftFilesResource, RDMDraftResource, RDMParentRecordLinksResource, \
    RDMRecordFilesActionResource, RDMRecordFilesResource, RDMRecordResource, \
    RDMRecordVersionsResource, RDMUserRecordsResource

__all__ = (
    "RDMDraftActionResource",
    "RDMDraftFilesResource",
    "RDMDraftFilesActionResource",
    "RDMDraftResource",
    "RDMParentRecordLinksResource",
    "RDMRecordFilesResource",
    "RDMRecordFilesActionResource",
    "RDMRecordVersionsResource",
    "RDMRecordResource",
    "RDMUserRecordsResource",
)
