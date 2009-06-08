from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.membrane.interfaces.user import IMembraneUserObject
from Products.membrane.interfaces.plugin_markers import IUserAuthProvider
from Products.membrane.relations import UserRelatedRelation

class UserRelated(object):
    """
    Default implementation for extracting a user id from a piece of
    content.  Could be used to adapt from IReferenceable to IMembraneUserObject,
    but is really just used as a mix-in for more specific adapters.
    """
    security = ClassSecurityInfo()

    implements(IMembraneUserObject)
        
    def __init__(self, context):
        self.context = context

    #
    #   IMembraneUserObject implementation
    #
    security.declarePublic('getUserId')
    def getUserId(self):
        """
        Return the user id 
        """
        relationship = UserRelatedRelation.relationship
        user_providers = self.context.getBRefs(relationship=relationship)
        if user_providers:
            assert len(user_providers) == 1
            user_provider = IUserAuthProvider(user_providers[0])
            return IMembraneUserObject(user_provider).getUserId()
        else:
            try:
                user_provider = IUserAuthProvider(self.context)
                return IMembraneUserObject(user_provider).getUserId()
            except TypeError:
                return None
