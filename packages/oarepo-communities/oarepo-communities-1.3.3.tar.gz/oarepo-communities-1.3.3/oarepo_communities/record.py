# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that adds support for communities"""
from jsonpatch import apply_patch
from oarepo_fsm.decorators import transition
from oarepo_fsm.mixins import FSMMixin

from oarepo_communities.constants import PRIMARY_COMMUNITY_FIELD, SECONDARY_COMMUNITY_FIELD, \
    STATE_PENDING_APPROVAL, STATE_EDITING, STATE_APPROVED, STATE_PUBLISHED, STATE_DELETED
from oarepo_communities.permissions import request_approval_permission_impl, delete_draft_permission_impl, \
    request_changes_permission_impl, approve_permission_impl, revert_approval_permission_impl, \
    publish_permission_impl, unpublish_permission_impl
from oarepo_communities.signals import on_request_approval, on_delete_draft, on_request_changes, on_approve, \
    on_revert_approval, on_unpublish, on_publish


class CommunityRecordMixin(FSMMixin):
    """A mixin that keeps community info in the metadata."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def primary_community(self):
        return self[PRIMARY_COMMUNITY_FIELD]

    @property
    def secondary_communities(self) -> list:
        return self.get(SECONDARY_COMMUNITY_FIELD, []) or []

    def clear(self):
        """Preserves the schema even if the record is cleared and all metadata wiped out."""
        primary = self.get(PRIMARY_COMMUNITY_FIELD)
        super().clear()
        if primary:
            self[PRIMARY_COMMUNITY_FIELD] = primary

    def _check_community(self, data):
        if PRIMARY_COMMUNITY_FIELD in data:
            if data[PRIMARY_COMMUNITY_FIELD] != self.primary_community:
                raise AttributeError('Primary Community cannot be changed')

    def update(self, e=None, **f):
        """Dictionary update."""
        self._check_community(e or f)
        return super().update(e, **f)

    def __setitem__(self, key, value):
        """Dict's setitem."""
        if key == PRIMARY_COMMUNITY_FIELD:
            if PRIMARY_COMMUNITY_FIELD in self and self.primary_community != value:
                raise AttributeError('Primary Community cannot be changed')
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        """Dict's delitem."""
        if key == PRIMARY_COMMUNITY_FIELD:
            raise AttributeError('Primary Community can not be deleted')
        return super().__delitem__(key)

    @classmethod
    def create(cls, data=dict, id_=None, **kwargs):
        """
        Creates a new record instance and store it in the database.
        For parameters see :py:class:invenio_records.api.Record
        """
        if not data.get(PRIMARY_COMMUNITY_FIELD, None):
            raise AttributeError('Primary Community is missing from record')

        ret = super().create(data, id_, **kwargs)
        return ret

    def patch(self, patch):
        """Patch record metadata. Overrides invenio patch to check if community has changed
        :params patch: Dictionary of record metadata.
        :returns: A new :class:`Record` instance.
        """
        data = apply_patch(dict(self), patch)
        if self.primary_community != data[PRIMARY_COMMUNITY_FIELD]:
            raise AttributeError('Primary Community cannot be changed')
        return self.__class__(data, model=self.model)

    @transition(src=[None, STATE_EDITING], dest=STATE_PENDING_APPROVAL,
                permissions=request_approval_permission_impl)
    def request_approval(self, **kwargs):
        """Submit record for approval."""
        on_request_approval.send(self, **kwargs)

    @transition(src=[None, STATE_EDITING, STATE_PENDING_APPROVAL], dest=STATE_DELETED,
                permissions=delete_draft_permission_impl,
                commit_record=False)
    def delete_draft(self, **kwargs):
        """Completely delete a draft record."""
        on_delete_draft.send(self, **kwargs)

    @transition(src=STATE_PENDING_APPROVAL, dest=STATE_EDITING,
                permissions=request_changes_permission_impl)
    def request_changes(self, **kwargs):
        """Request changes to the record."""
        on_request_changes.send(self, **kwargs)

    @transition(src=[STATE_PENDING_APPROVAL], dest=STATE_APPROVED,
                permissions=approve_permission_impl,
                commit_record=False)
    def approve(self, **kwargs):
        """Approve the record to be included in the community."""
        on_approve.send(self, **kwargs)

    @transition(src=[STATE_APPROVED], dest=STATE_PENDING_APPROVAL,
                permissions=revert_approval_permission_impl,
                commit_record=False)
    def revert_approval(self, **kwargs):
        """Revert the record approval, requesting it to be re-approved."""
        on_revert_approval.send(self, **kwargs)

    @transition(src=[STATE_APPROVED], dest=STATE_PUBLISHED,
                permissions=publish_permission_impl)
    def publish(self, **kwargs):
        """Make the record visible outside of the community."""
        on_publish.send(self, **kwargs)

    @transition(src=[STATE_PUBLISHED], dest=STATE_APPROVED,
                permissions=unpublish_permission_impl)
    def unpublish(self, **kwargs):
        """Revert the record publication, returning it to approved state."""
        on_unpublish.send(self, **kwargs)
