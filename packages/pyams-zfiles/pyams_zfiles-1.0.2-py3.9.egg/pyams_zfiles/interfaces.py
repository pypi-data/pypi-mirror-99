#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS zfiles.interfaces module

This module defines ZFiles global package interfaces.
"""

from enum import IntEnum

from zope.container.constraints import containers, contains
from zope.container.interfaces import IBTreeContainer
from zope.interface import Interface, implementer
from zope.schema import Choice, Dict, List, Password, TextLine
from zope.schema.interfaces import IDict
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_file.schema import FileField
from pyams_security.interfaces import IContentRoles
from pyams_security.schema import PrincipalField, PrincipalsSetField
from pyams_workflow.interfaces import IWorkflow, IWorkflowManagedContent, \
    IWorkflowPublicationSupport


__docformat__ = 'restructuredtext'

from pyams_zfiles import _


#
# API endpoints
#

REST_CONTAINER_ROUTE = 'zfiles.rest.container'
REST_DOCUMENT_ROUTE = 'zfiles.rest.document'

GRAPHQL_API_ROUTE = 'zfiles.graphql'

JSONRPC_ENDPOINT = 'zfiles.jsonrpc'
XMLRPC_ENDPOINT = 'zfiles.xmlrpc'


#
# Global application strings
#

PYAMS_ZFILES_SKIN_NAME = 'PyAMS.zfiles.skin'
"""Custom ZFiles skin name"""


PYAMS_ZFILES_APPLICATIONS_VOCABULARY = 'PyAMS.zfiles.applications'
"""Name of registered applications vocabulary"""


#
# ZFiles permissions
#

MANAGE_APPLICATION_PERMISSION = 'pyams.ManageZfilesApplication'
'''Permission required to manage ZFiles application'''

CREATE_DOCUMENT_PERMISSION = 'pyams.CreateDocument'
'''Permission required to create a new document'''

CREATE_DOCUMENT_WITH_OWNER_PERMISSION = 'pyams.CreateDocumentWithOwner'
'''Permission required to create a new document with a specific owner'''

MANAGE_DOCUMENT_PERMISSION = 'pyams.ManageDocument'
'''Permission required to manage document properties'''

READ_DOCUMENT_PERMISSION = 'pyams.ReadDocument'
'''Permission required to view document'''


ZFILES_ADMIN_ROLE = 'pyams.DocumentsAdministrator'
'''ZFiles application administrator role'''

ZFILES_IMPORTER_ROLE = 'pyams.DocumentsImporter'
'''Documents importer role'''

ZFILES_CREATOR_ROLE = 'pyams.DocumentCreator'
'''Document creator role'''

ZFILES_MANAGER_ROLE = 'pyams.DocumentsManager'
'''Documents manager role'''

ZFILES_OWNER_ROLE = 'pyams.DocumentOwner'
'''Document owner role'''

ZFILES_READER_ROLE = 'pyams.DocumentReader'
'''Document reader role'''


#
# Documents interfaces
#

ZFILES_WORKFLOW_NAME = 'pyams_zfiles.workflow'


class IDocumentWorkflow(IWorkflow):
    """Document workflow marker interface"""


DRAFT_STATE = 'draft'
PUBLISHED_STATE = 'published'
ARCHIVED_STATE = 'archived'
DELETED_STATE = 'deleted'

STATE_LABELS = {
    DRAFT_STATE: _("Draft"),
    PUBLISHED_STATE: _("Published"),
    ARCHIVED_STATE: _("Archived"),
    DELETED_STATE: _("Deleted")
}


class AccessMode(IntEnum):
    """Access modes"""
    private = 0
    protected = 1
    public = 2


PRIVATE_MODE = AccessMode.private
PROTECTED_MODE = AccessMode.protected
PUBLIC_MODE = AccessMode.public

ACCESS_MODE_IDS = [
    'private',
    'protected',
    'public'
]

ACCESS_MODE_LABELS = (
    _("Private"),
    _("Protected"),
    _("Public")
)


ACCESS_MODE_VOCABULARY = SimpleVocabulary([
    SimpleTerm(i, t, t) for i, t in enumerate(ACCESS_MODE_LABELS)
])


class IPropertiesField(IDict):
    """Properties schema field interface"""


@implementer(IPropertiesField)
class PropertiesField(Dict):
    """Properties schema field"""

    def __init__(self, *args, **kwargs):
        super().__init__(key_type=TextLine(),
                         value_type=TextLine(),
                         *args, **kwargs)


class IDocumentVersion(IWorkflowPublicationSupport):
    """Document version interface"""

    oid = TextLine(title="Document OID",
                   description=_("Document unique identifier"),
                   readonly=True)

    title = TextLine(title=_("Document title"),
                     description=_("User friendly name of the document"),
                     required=True)

    application_name = TextLine(title=_("Source application name"),
                                description=_("Name of the application which submitted "
                                              "the document"),
                                required=True)

    data = FileField(title=_("Document data"),
                     description=_("This is where document content is stored"),
                     required=True)

    hash = TextLine(title=_("Document data hash"),
                    description=_("This unique signature is built using SHA512 algorithm"),
                    required=True)

    access_mode = Choice(title=_("Access mode"),
                         description=_("Access mode on this document"),
                         required=True,
                         vocabulary=ACCESS_MODE_VOCABULARY,
                         default=PRIVATE_MODE)

    update_mode = Choice(title=_("Update mode"),
                         description=_("Update mode on this document"),
                         required=True,
                         vocabulary=ACCESS_MODE_VOCABULARY,
                         default=PRIVATE_MODE)

    properties = PropertiesField(title=_("Properties"),
                                 description=_("List of free additional properties which can be "
                                               "applied to the document; these properties can't "
                                               "be used for searching"),
                                 required=False)

    tags = List(title=_("Document tags"),
                description=_("List of free additional tags which can be applied to the "
                              "document; these tags can be used for searching"),
                value_type=TextLine(),
                required=False)

    updater = PrincipalField(title=_("Last document updater"),
                             description=_("Name of the last principal which updated the "
                                           "document"),
                             required=True)

    def update(self, data, properties, request=None):
        """Set document data and properties"""

    def update_status(self, properties, request=None):
        """Update document status"""

    def to_json(self, request=None):
        """Get document properties in JSON format"""


class IDocumentRoles(IContentRoles):
    """Document roles interface"""

    creator = PrincipalField(title=_("Document creator"),
                             description=_("Name of the principal which created the document"),
                             role_id=ZFILES_CREATOR_ROLE,
                             required=True)

    owner = PrincipalField(title=_("Document owner"),
                           description=_("Name of the principal which is owner of the document"),
                           role_id=ZFILES_OWNER_ROLE,
                           required=True)

    readers = PrincipalsSetField(title=_("Document readers"),
                                 description=_("Name of principals allowed to read the document"),
                                 role_id=ZFILES_READER_ROLE,
                                 required=False)

    managers = PrincipalsSetField(title=_("Document managers"),
                                  description=_("Name of principals allowed to update the "
                                                "document"),
                                  role_id=ZFILES_MANAGER_ROLE,
                                  required=False)


class IDocument(IWorkflowManagedContent):
    """Document interface"""

    containers('.IDocumentFolder')

    oid = TextLine(title="Document OID",
                   description=_("Document unique identifier"),
                   readonly=True)

    def get_oid(self):
        """Generate new unique ID"""


class IDocumentFolder(IBTreeContainer):
    """Document folder interface"""

    containers('.IDocumentContainer', '.IDocumentFolder')
    contains(IDocument, '.IDocumentFolder')


DOCUMENT_CONTAINER_NAME = 'ZFiles'
'''ZFiles documents container name'''


class IDocumentContainer(IBTreeContainer):
    """Document container utility interface"""

    contains(IDocumentFolder)

    oid_prefix = TextLine(title=_("Documents OID prefix"),
                          description=_("Prefix used to identify documents which were "
                                        "created locally (unlike documents which were created "
                                        "into another documents container and synchronized with "
                                        "this container)"),
                          required=False)

    def add_document(self, data, properties, request):
        """Add new document"""

    def import_document(self, oid, data, properties, request):
        """Import document from outer ZFiles database"""

    def find_documents(self, params, request=None):
        """Find documents matching given params"""

    def get_document(self, oid, version=None):
        """Retrieve existing document from it's OID

        If no version number is specified, the last version
        is returned.
        """

    # pylint: disable=too-many-arguments
    def update_document(self, oid, version=None, data=None, properties=None, request=None):
        """Update document data or properties"""

    def delete_document(self, oid):
        """Delete document or version"""


class IDocumentContainerRoles(IContentRoles):
    """Document container utility roles interface"""

    application_managers = PrincipalsSetField(title=_("Application managers"),
                                              description=_("These principals can only "
                                                            "manage application properties; "
                                                            "documents manager role is required "
                                                            "to manage documents!"),
                                              role_id=ZFILES_ADMIN_ROLE,
                                              required=False)

    documents_creators = PrincipalsSetField(title=_("Documents creators"),
                                            description=_("These principals will be allowed to "
                                                          "create or import new documents"),
                                            role_id=ZFILES_IMPORTER_ROLE,
                                            required=False)

    documents_managers = PrincipalsSetField(title=_("Documents managers"),
                                            description=_("These principals will be allowed to "
                                                          "manage any document properties"),
                                            role_id=ZFILES_MANAGER_ROLE,
                                            required=False)

    documents_readers = PrincipalsSetField(title=_("Documents readers"),
                                           description=_("These principals will be allowed to "
                                                         "read any document properties"),
                                           role_id=ZFILES_READER_ROLE,
                                           required=False)


class DocumentContainerError(Exception):
    """Base document container error"""


#
# Documents synchronizer interface
#

IMPORT_MODE = 'import'
DELETE_MODE = 'delete'


DOCUMENT_SYNCHRONIZER_KEY = 'pyams_zfiles.synchronizer'


class IDocumentSynchronizer(Interface):
    """Documents synchronizer interface"""

    target = TextLine(title=_("Remote XML-RPC endpoint"),
                      description=_("URL of the remote documents container XML-RPC endpoint "
                                    "used for synchronization"),
                      required=False)

    username = TextLine(title=_("User name"),
                        description=_("Name of the remote user used for synchronization"),
                        required=False)

    password = Password(title=_("Password"),
                        description=_("Password of the remote user used for synchronization"),
                        required=False)

    def synchronize(self, oid, mode=IMPORT_MODE, request=None):
        """Synchronize given OID to remote container"""
