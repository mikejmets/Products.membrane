from Acquisition import aq_chain, aq_inner
from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces import IMembraneUserGroups
from Products.membrane.interfaces import IGroup
from userrelated import UserRelated


class Groups(UserRelated):
    """
    Adapts from IGroupsProvider to IMembraneUserGroups, gets groups
    from acquisition and backrefs
    """
    security = ClassSecurityInfo()

    implements(IMembraneUserGroups)

    def __init__(self, context):
        self.context = context

    #
    #   IGroupsPlugin implementation
    #
    security.declarePrivate('getGroupsForPrincipal')
    def getGroupsForPrincipal(self, principal, request=None):
        groups = {}
        # Get all BRefs that implement IGroup - slightly expensive
        for obj in self.context.getBRefs():
            if IGroup.providedBy(obj):
                groups[obj.getGroupId()] = 1
        for parent in aq_chain(aq_inner(self.context)):
            if IGroup.providedBy(parent):
                groups[parent.getGroupId()] = 1
        return tuple(groups.keys())


class SelectedGroups(UserRelated):
    """
    Adapts from ISelectedGroupsProvider to IMembraneUserGroups; gets groups
    from acquisition and backrefs w/ a specific relationship.
    """
    security = ClassSecurityInfo()

    implements(IMembraneUserGroups)

    def __init__(self, context):
        self.context = context

    #
    #   IGroupsPlugin implementation
    #
    security.declarePrivate('getGroupsForPrincipal')
    def getGroupsForPrincipal(self, principal, request=None):
        groups = {}
        for relationship in self.context.getGroupRelationships():
            groups.update(dict.fromkeys([g.getUserId() for g in
                                         self.context.getBRefs(relationship)]))
        for parent in aq_chain(aq_inner(self.context)):
            if IGroup.providedBy(parent):
                groups[parent.getGroupId()] = 1
        return tuple(groups.keys())
