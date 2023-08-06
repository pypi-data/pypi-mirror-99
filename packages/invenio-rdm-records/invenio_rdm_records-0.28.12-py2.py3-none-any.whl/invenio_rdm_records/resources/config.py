# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources configuration."""

from flask_resources.errors import HTTPJSONException, create_errormap_handler
from flask_resources.serializers import JSONSerializer
from invenio_drafts_resources.resources import DraftActionResourceConfig, \
    DraftFileActionResourceConfig, DraftFileResourceConfig, \
    DraftResourceConfig, RecordResourceConfig, RecordVersionsResourceConfig
from invenio_records_resources.resources import RecordResponse
from invenio_records_resources.resources.files import \
    FileActionResourceConfig, FileResourceConfig
from invenio_records_resources.resources.records.schemas_links import \
    ItemLink, LinksSchema, SearchLinksSchema

from .links import FileItemLink, SearchVersionsLinksSchema
from .serializers import UIJSONSerializer

#
# Links
#
RecordLinks = LinksSchema.create(links={
    "self": ItemLink(template='/api/records/{pid_value}'),
    "self_html": ItemLink(template='/records/{pid_value}'),
    "files": ItemLink(template='/api/records/{pid_value}/files'),
    "versions": ItemLink(template='/api/records/{pid_value}/versions'),
    "latest": ItemLink(template='/api/records/{pid_value}/versions/latest'),
    "latest_html": ItemLink(template='/records/{pid_value}/latest'),
    "access_links": ItemLink(
        template='/api/records/{pid_value}/access/links', permission="manage"
    ),
})


DraftLinks = LinksSchema.create(links={
    "self": ItemLink(template="/api/records/{pid_value}/draft"),
    "self_html": ItemLink(template="/uploads/{pid_value}"),
    "files": ItemLink(template="/api/records/{pid_value}/draft/files"),
    "versions": ItemLink(template='/api/records/{pid_value}/versions'),
    "latest": ItemLink(template='/api/records/{pid_value}/versions/latest'),
    "latest_html": ItemLink(template='/records/{pid_value}/latest'),
    "access_links": ItemLink(
        template='/api/records/{pid_value}/access/links', permission="manage"
    ),
    "publish": ItemLink(
        template="/api/records/{pid_value}/draft/actions/publish",
        permission="publish",
    ),
})


SearchLinks = SearchLinksSchema.create(
    template="/api/records{?params*}")


SearchVersionsLinks = SearchVersionsLinksSchema.create(
    template='/api/records/{pid_value}/versions{?params*}'
)


RecordVersionsLinks = LinksSchema.create(links={
    "self": ItemLink(template='/api/records/{pid_value}'),
    "self_html": ItemLink(template="/records/{pid_value}"),
})


UserSearchLinks = SearchLinksSchema.create(
    template="/api/user/records{?params*}")


RecordFileLinks = LinksSchema.create(links={
    "self": FileItemLink(
        template="/api/records/{pid_value}/files/{key}"),
    "content": FileItemLink(
        template="/api/records/{pid_value}/files/{key}/content"),
    "commit": FileItemLink(
        template="/api/records/{pid_value}/files/{key}/commit"),
})


DraftFileLinks = LinksSchema.create(links={
    "self": FileItemLink(
        template="/api/records/{pid_value}/draft/files/{key}"),
    "content": FileItemLink(
        template="/api/records/{pid_value}/draft/files/{key}/content"),
    "commit": FileItemLink(
        template="/api/records/{pid_value}/draft/files/{key}/commit"),
})


RecordListFilesLinks = LinksSchema.create(links={
    "self": ItemLink(template="/api/records/{pid_value}/files")
})


DraftListFilesLinks = LinksSchema.create(links={
    "self": ItemLink(template="/api/records/{pid_value}/draft/files")
})


#
# Response handlers
#
record_serializers = {
    "application/json": RecordResponse(JSONSerializer()),
    "application/vnd.inveniordm.v1+json": RecordResponse(UIJSONSerializer())
}


#
# Records and record versions
#
class RDMRecordResourceConfig(RecordResourceConfig):
    """Record resource configuration."""

    list_route = "/records"

    item_route = "/records/<pid_value>"

    links_config = {
        "record": RecordLinks,
        "search": SearchLinks,
    }

    draft_links_config = {
        "record": DraftLinks,
    }

    response_handlers = record_serializers


class RDMRecordVersionsResourceConfig(RecordVersionsResourceConfig):
    """Record resource version config."""

    list_route = "/records/<pid_value>/versions"

    item_route = "/records/<pid_value>/versions/latest"

    links_config = {
        "record": RecordVersionsLinks,  # TODO: "record" -> "item"
        "search": SearchVersionsLinks
    }

    draft_links_config = {
        "record": DraftLinks,
    }

    response_handlers = record_serializers


#
# Drafts and draft actions
#
class RDMDraftResourceConfig(DraftResourceConfig):
    """Draft resource configuration."""

    list_route = "/records/<pid_value>/draft"

    item_route = None

    links_config = {
        "record": DraftLinks
    }


class RDMDraftActionResourceConfig(DraftActionResourceConfig):
    """Mock service configuration."""

    list_route = "/records/<pid_value>/draft/actions/<action>"

    item_route = None

    record_links_config = {
        "record": RecordLinks,
        "search": SearchLinks,
    }

    action_commands = {
        "create": {
            "publish": "publish"
        }
    }


#
# User records
#
class RDMUserRecordsResourceConfig(RecordResourceConfig):
    """User records resource configuration."""

    list_route = "/user/records"

    links_config = {
        "search": UserSearchLinks,
    }

    response_handlers = record_serializers


#
# Record files
#
class RDMRecordFilesResourceConfig(FileResourceConfig):
    """Bibliographic record files resource config."""

    item_route = "/records/<pid_value>/files/<key>"

    list_route = "/records/<pid_value>/files"

    links_config = {
        "file": RecordFileLinks,
        "files": RecordListFilesLinks,
    }


class RDMRecordFilesActionResourceConfig(FileActionResourceConfig):
    """Bibliographic record files action resource config."""

    list_route = "/records/<pid_value>/files/<key>/<action>"

    links_config = {
        "file": RecordFileLinks,
        "files": RecordListFilesLinks,
    }

    action_commands = {
        'read': {
            'content': 'get_file_content'
        },
    }


#
# Draft files
#
class RDMDraftFilesResourceConfig(DraftFileResourceConfig):
    """Bibliographic record files resource config."""

    item_route = "/records/<pid_value>/draft/files/<key>"

    list_route = "/records/<pid_value>/draft/files"

    links_config = {
        "file": DraftFileLinks,
        "files": DraftListFilesLinks,
    }


class RDMDraftFilesActionResourceConfig(DraftFileActionResourceConfig):
    """Bibliographic record files action resource config."""

    list_route = "/records/<pid_value>/draft/files/<key>/<action>"

    links_config = {
        "file": DraftFileLinks,
        "files": DraftListFilesLinks,
    }


#
# Parent Record Links
#
record_links_error_map = RecordResourceConfig.error_map.copy()
record_links_error_map.update({
    LookupError: create_errormap_handler(
        HTTPJSONException(
            code=404,
            description="No secret link found with the given ID.",
        )
    ),
})


class RDMParentRecordLinksResourceConfig(RecordResourceConfig):
    """User records resource configuration."""

    item_route = "/records/<pid_value>/access/links/<link_id>"

    list_route = "/records/<pid_value>/access/links"

    links_config = {}

    response_handlers = {
        "application/json": RecordResponse(JSONSerializer())
    }

    error_map = record_links_error_map
