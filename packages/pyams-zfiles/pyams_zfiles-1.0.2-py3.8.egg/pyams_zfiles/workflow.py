#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_zfiles.workflow module

This module defines base ZFiles workflow.
"""

from datetime import datetime

from zope.copy import copy
from zope.interface import implementer
from zope.location import locate
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.date import format_datetime
from pyams_utils.registry import get_pyramid_registry, utility_config
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_workflow.interfaces import IWorkflow, IWorkflowInfo, IWorkflowPublicationInfo, \
    IWorkflowState, IWorkflowStateLabel, IWorkflowVersions, ObjectClonedEvent
from pyams_workflow.workflow import Transition, Workflow
from pyams_zfiles.interfaces import ARCHIVED_STATE, DELETED_STATE, DRAFT_STATE, \
    IDocument, IDocumentFolder, IDocumentWorkflow, MANAGE_DOCUMENT_PERMISSION, PUBLISHED_STATE, \
    ZFILES_WORKFLOW_NAME


__docformat__ = 'restructuredtext'

from pyams_zfiles import _


STATES_IDS = (
    DRAFT_STATE,
    PUBLISHED_STATE,
    ARCHIVED_STATE,
    DELETED_STATE
)

STATES_LABELS = (
    _("Draft"),
    _("Published"),
    _("Archived"),
    _("Deleted")
)

STATES_VOCABULARY = SimpleVocabulary([
    SimpleTerm(STATES_IDS[i], title=t)
    for i, t in enumerate(STATES_LABELS)
])

STATES_HEADERS = {
    DRAFT_STATE: _("draft created"),
    PUBLISHED_STATE: _("published"),
    ARCHIVED_STATE: _("archived")
}

UPDATE_STATES = (DRAFT_STATE, PUBLISHED_STATE)
'''Default states available in update mode'''

READONLY_STATES = (ARCHIVED_STATE, DELETED_STATE)
'''Retired and archived contents can't be modified'''

PROTECTED_STATES = ()
'''Protected states are available to managers in update mode'''

MANAGER_STATES = ()
'''No custom state available to managers!'''

PUBLISHED_STATES = (PUBLISHED_STATE,)
'''Pre-published and published states are marked as published'''

VISIBLE_STATES = (PUBLISHED_STATE,)
'''Only published state is visible in front-office'''

WAITING_STATES = ()

RETIRED_STATES = ()

ARCHIVED_STATES = (ARCHIVED_STATE,)


#
# Workflow conditions
#

def can_create_new_version(wf, context):  # pylint: disable=invalid-name,unused-argument
    """Check if we can create a new version"""
    # can't create new version when previous draft already exists
    versions = IWorkflowVersions(context)
    return not versions.has_version(DRAFT_STATE)


#
# Workflow actions
#

def publish_action(wf, context):  # pylint: disable=invalid-name,unused-argument
    """Publish version"""
    request = check_request()
    translate = request.localizer.translate
    publication_info = IWorkflowPublicationInfo(context)
    publication_info.publication_date = datetime.utcnow()
    publication_info.publisher = request.principal.id
    version_id = IWorkflowState(context).version_id
    for version in IWorkflowVersions(context).get_versions((PUBLISHED_STATE, )):
        if version is not context:
            IWorkflowInfo(version).fire_transition_toward(
                ARCHIVED_STATE,
                comment=translate(_("Published version {0}")).format(version_id))


def clone_action(wf, context):  # pylint: disable=invalid-name,unused-argument
    """Create new version"""
    result = copy(context)
    locate(result, context.__parent__)
    registry = get_pyramid_registry()
    registry.notify(ObjectClonedEvent(result, context))
    return result


def delete_action(wf, context):  # pylint: disable=invalid-name,unused-argument
    """Delete draft version, and parent if single version"""
    versions = IWorkflowVersions(context)
    versions.remove_version(IWorkflowState(context).version_id)
    if not versions.get_last_versions():
        document = get_parent(versions, IDocument)
        folder = get_parent(document, IDocumentFolder)
        del folder[document.__name__]


#
# Workflow transitions
#

init = Transition(transition_id='init',
                  title=_("Initialize"),
                  source=None,
                  destination=DRAFT_STATE,
                  history_label=_("Draft creation"))

draft_to_published = Transition(transition_id='draft_to_published',
                                title=_("Publish"),
                                source=DRAFT_STATE,
                                destination=PUBLISHED_STATE,
                                permission=MANAGE_DOCUMENT_PERMISSION,
                                action=publish_action,
                                menu_icon_class='far fa-fw fa-thumbs-up',
                                view_name='wf-publish.html',
                                history_label=_("Content published"),
                                order=1)

published_to_archived = Transition(transition_id='published_to_archived',
                                   title=_("Archive content"),
                                   source=PUBLISHED_STATE,
                                   destination=ARCHIVED_STATE,
                                   permission=MANAGE_DOCUMENT_PERMISSION,
                                   menu_icon_class='fas fa-fw fa-archive',
                                   view_name='wf-archive.html',
                                   history_label=_("Content archived"),
                                   order=2)

published_to_draft = Transition(transition_id='published_to_draft',
                                title=_("Create new version"),
                                source=PUBLISHED_STATE,
                                destination=DRAFT_STATE,
                                permission=MANAGE_DOCUMENT_PERMISSION,
                                condition=can_create_new_version,
                                action=clone_action,
                                menu_icon_class='far fa-fw fa-copy',
                                view_name='wf-clone.html',
                                history_label=_("New version created"),
                                order=3)

archived_to_draft = Transition(transition_id='archived_to_draft',
                               title=_("Create new version"),
                               source=ARCHIVED_STATE,
                               destination=DRAFT_STATE,
                               permission=MANAGE_DOCUMENT_PERMISSION,
                               condition=can_create_new_version,
                               action=clone_action,
                               menu_icon_class='far fa-fw fa-copy',
                               view_name='wf-clone.html',
                               history_label=_("New version created"),
                               order=4)

delete = Transition(transition_id='delete',
                    title=_("Delete version"),
                    source=DRAFT_STATE,
                    destination=DELETED_STATE,
                    permission=MANAGE_DOCUMENT_PERMISSION,
                    action=delete_action,
                    menu_icon_class='fa fa-fw fa-trash',
                    view_name='wf-delete.html',
                    history_label=_("Version deleted"),
                    order=99)

wf_transitions = {
    init,
    draft_to_published,
    published_to_archived,
    published_to_draft,
    archived_to_draft,
    delete
}


@implementer(IDocumentWorkflow)
class DocumentWorkflow(Workflow):
    """PyAMS basic workflow"""


ZFILES_WORKFLOW = DocumentWorkflow(wf_transitions,
                                   states=STATES_VOCABULARY,
                                   initial_state=DRAFT_STATE,
                                   update_states=UPDATE_STATES,
                                   readonly_states=READONLY_STATES,
                                   protected_states=PROTECTED_STATES,
                                   manager_states=MANAGER_STATES,
                                   published_states=PUBLISHED_STATES,
                                   visible_states=VISIBLE_STATES,
                                   waiting_states=WAITING_STATES,
                                   retired_states=RETIRED_STATES,
                                   archived_states=ARCHIVED_STATES)


@utility_config(name=ZFILES_WORKFLOW_NAME,
                provides=IWorkflow)
class WorkflowUtility:
    """PyAMS ZFiles workflow utility

    This is a basic workflow implementation for ZFiles documents.
    It only implements three states which are *draft*, *published* and *archived*.
    """

    def __new__(cls):
        return ZFILES_WORKFLOW


@adapter_config(required=IDocumentWorkflow,
                provides=IWorkflowStateLabel)
class WorkflowStateLabelAdapter(ContextAdapter):
    """Generic state label adapter"""

    @staticmethod
    def get_label(content, request=None, format=True):  # pylint: disable=redefined-builtin
        """Workflow state label getter"""
        if request is None:
            request = check_request()
        translate = request.localizer.translate
        state = IWorkflowState(content)
        header = STATES_HEADERS.get(state.state)
        if header is not None:
            state_label = translate(header)
            if format:
                state_label = translate(_('{state} {date}')).format(
                    state=state_label,
                    date=format_datetime(state.state_date))
        else:
            state_label = translate(_("Unknown state"))
        return state_label


@adapter_config(name=DRAFT_STATE,
                required=IDocumentWorkflow,
                provides=IWorkflowStateLabel)
class DraftWorkflowStateLabelAdapter(ContextAdapter):
    """Draft state label adapter"""

    @staticmethod
    def get_label(content, request=None, format=True):  # pylint: disable=redefined-builtin
        """Workflow state label getter"""
        if request is None:
            request = check_request()
        translate = request.localizer.translate
        state = IWorkflowState(content)
        if len(state.history) <= 2:
            header = STATES_HEADERS.get(state.state)
            if header is not None:
                if state.version_id == 1:
                    state_label = translate(header)
                else:
                    state_label = translate(_("new version created"))
            else:
                state_label = translate(_("Unknown state"))
        else:
            state_label = translate(_('publication refused'))
        if format:
            state_label = translate(_('{state} {date}')).format(
                state=state_label,
                date=format_datetime(state.state_date))
        return state_label
