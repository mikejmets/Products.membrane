""" 
User interface
"""
from zope.interface import Interface

from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin

from Products.Archetypes.interfaces import IReferenceable
    
class IUserRelated(Interface):
    """
    Needs to be implemented by anything user-related so we can easily
    determine the unique user that the object is related to.
    """
    def getUserId():
        """
        Return the unique identifier for the user that this piece of content
        relates to.
        """

class IMembraneUserAuth(IUserRelated, IAuthenticationPlugin):
    """
    Used for objects that can handle user authentication.
    """

class IMembraneUserProperties(IUserRelated, IPropertiesPlugin):
    """
    Used for objects that can provide user properties.
    """

class IMembraneUserGroups(IUserRelated, IGroupsPlugin):
    """
    Used for objects that can provide user groups.
    """

class IMembraneUserRoles(IUserRelated, IRolesPlugin):
    """
    Used for objects that can provide user roles.
    """