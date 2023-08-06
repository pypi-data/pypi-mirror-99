# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Service config."""

from invenio_drafts_resources.services.records import RecordDraftServiceConfig
from invenio_records_resources.services.files.config import FileServiceConfig
from invenio_records_resources.services.records.components import MetadataComponent
from invenio_records_resources.services.records.search import terms_filter

from ..records import Marc21Draft, Marc21Record
from .components import AccessComponent, PIDComponent
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21RecordSchema, MetadataSchema


class Marc21RecordServiceConfig(RecordDraftServiceConfig):
    """Marc21 record service config."""

    # Record class
    record_cls = Marc21Record
    # Draft class
    draft_cls = Marc21Draft

    schema = Marc21RecordSchema
    # TODO: ussing from invenio-permissions
    permission_policy_cls = Marc21RecordPermissionPolicy

    search_facets_options = dict(
        aggs={},
        post_filters={
            "access_right": terms_filter("access.access_right"),
        },
    )

    components = [
        MetadataComponent,
        AccessComponent,
        PIDComponent,
    ]


#
# Record files
#
class Marc21RecordFilesServiceConfig(Marc21RecordServiceConfig, FileServiceConfig):
    """Marc21 record files service configuration."""


#
# Draft files
#
class Marc21DraftFilesServiceConfig(Marc21RecordServiceConfig, FileServiceConfig):
    """Marc21 draft files service configuration."""

    record_cls = Marc21Draft
