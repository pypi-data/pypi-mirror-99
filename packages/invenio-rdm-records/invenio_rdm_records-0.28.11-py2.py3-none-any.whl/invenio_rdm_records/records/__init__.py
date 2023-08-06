# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Data access layer."""

from .api import RDMDraft, RDMParent, RDMRecord

__all__ = (
    "RDMDraft",
    "RDMParent",
    "RDMRecord",
)
