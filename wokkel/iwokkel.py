# Copyright (c) 2003-2007 Ralph Meijer
# See LICENSE for details.

"""
Wokkel interfaces.
"""

from zope.interface import Attribute, Interface

class IXMPPHandler(Interface):
    """
    Interface for XMPP protocol handlers.

    Objects that provide this interface can be added to a stream manager to
    handle of (part of) an XMPP extension protocol.
    """

    manager = Attribute("""XML stream manager""")
    xmlstream = Attribute("""The managed XML stream""")

    def makeConnection(xs):
        """
        A connection over the underlying transport of the XML stream has been
        established.

        At this point, no traffic has been exchanged over the XML stream
        given in C{xs}.

        This should setup C{self.xmlstream} and call L{connectionMade}.

        @type xs: L{XmlStream<twisted.words.protocols.jabber.XmlStream>}
        """

    def connectionMade(self):
        """
        Called after a connection has been established.

        This method can be used to change properties of the XML Stream, its
        authenticator or the stream manager prior to stream initialization
        (including authentication).
        """

    def connectionInitialized():
        """
        The XML stream has been initialized.

        At this point, authentication was successful, and XML stanzas can be
        exchanged over the XML stream C{self.xmlstream}. This method can be
        used to setup observers for incoming stanzas.
        """

    def connectionLost(reason):
        """
        The XML stream has been closed.

        Subsequent use of C{self.parent.send} will result in data being queued
        until a new connection has been established.

        @type reason: L{twisted.python.failure.Failure}
        """


class IDisco(Interface):
    """
    Interface for XMPP service discovery.
    """

    def getDiscoInfo(target, requestor, nodeIdentifier=None):
        """
        Get identity and features from this entity, node.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The optional identifier of the node at this
                               entity to retrieve the identify and features of.
                               The default is C{None}, meaning the root node.
        @type nodeIdentifier: C{unicode}
        """

    def getDiscoItems(target, requestor, nodeIdentifier=None):
        """
        Get contained items for this entity, node.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The optional identifier of the node at this
                               entity to retrieve the identify and features of.
                               The default is C{None}, meaning the root node.
        @type nodeIdentifier: C{unicode}
        """

class IPubSubService(Interface):
    """
    Interface for an XMPP Publish Subscribe Service.

    All methods that are called as the result of an XMPP request are to
    return a deferred that fires when the requested action has been performed.
    Alternatively, exceptions maybe raised directly or by calling C{errback}
    on the returned deferred.
    """

    def notifyPublish(entity, nodeIdentifier, notifications):
        """
        Send out notifications for a publish event.

        @param entity: The entity the notifications will originate from.
        @type entity: L{jid.JID}
        @param nodeIdentifier: The identifier of the node that was published
                               to.
        @type nodeIdentifier: C{unicode}
        @param notifications: The notifications as tuples of subscriber and
                              the list of items to be notified.
        @type notifications: C{list} of (L{jid.JID}, C{list} of
                             L{domish.Element})
        """

    def publish(requestor, nodeIdentifier, items):
        """
        Called when a publish request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The identifier of the node to publish to.
        @type nodeIdentifier: C{unicode}
        @param items: The items to be published as L{domish} elements.
        @type items: C{list} of C{domish.Element}
        @return: deferred that fires on success.
        @rtype: L{defer.Deferred}
        """

    def subscribe(requestor, nodeIdentifier, subscriber):
        """
        Called when a subscribe request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The identifier of the node to subscribe to.
        @type nodeIdentifier: C{unicode}
        @param subscriber: The entity to be subscribed.
        @type subscriber: L{jid.JID}
        @return: A deferred that fires with a C{str} representing the
                 subscription state, C{'subscribed'} or C{'pending'}.
        @rtype: L{defer.Deferred}
        """

    def unsubscribe(requestor, nodeIdentifier, subscriber):
        """
        Called when a subscribe request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The identifier of the node to unsubscribe from.
        @type nodeIdentifier: C{unicode}
        @param subscriber: The entity to be unsubscribed.
        @type subscriber: L{jid.JID}
        @return: A deferred that fires with C{None} when unsubscription has
                 succeeded.
        @rtype: L{defer.Deferred}
        """

    def subscriptions(requestor):
        """
        Called when a subscriptions retrieval request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @return: A deferred that fires with a C{list} of suscriptions as
                 C{tuple}s of (node identifier as C{unicode}, subscriber as
                 L{jid.JID}, subscription state as C{str}). The subscription
                 state can be C{'subscribed'} or C{'pending'}.
        @rtype: L{defer.Deferred}
        """

    def affiliations(requestor):
        """
        Called when a affiliations retrieval request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @return: A deferred that fires with a C{list} of affiliations as
                 C{tuple}s of (node identifier as C{unicode}, affiliation state
                 as C{str}). The affiliation can be C{'owner'}, C{'publisher'},
                 or C{'outcast'}.
        @rtype: L{defer.Deferred}
        """

    def create(requestor, nodeIdentifier):
        """
        Called when a node creation request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The suggestion for the identifier of the node to
                               be created. If the request did not include a
                               suggestion for the node identifier, the value
                               is C{None}.
        @type nodeIdentifier: C{unicode} or C{NoneType}
        @return: A deferred that fires with a C{unicode} that represents
                 the identifier of the new node.
        @rtype: L{defer.Deferred}
        """

    def getDefaultConfiguration(requestor):
        """
        Called when a default node configuration request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @return: A deferred that fires with a C{dict} representing the default
                 node configuration. Keys are C{str}s that represent the
                 field name. Values can be of types C{unicode}, C{int} or
                 C{bool}.
        @rtype: L{defer.Deferred}
        """

    def getConfiguration(requestor, nodeIdentifier):
        """
        Called when a node configuration retrieval request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The identifier of the node to retrieve the
                               configuration from.
        @type nodeIdentifier: C{unicode}
        @return: A deferred that fires with a C{dict} representing the node
                 configuration. Keys are C{str}s that represent the field name.
                 Values can be of types C{unicode}, C{int} or C{bool}.
        @rtype: L{defer.Deferred}
        """

    def setConfiguration(requestor, nodeIdentifier, options):
        """
        Called when a node configuration change request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The identifier of the node to change the
                               configuration of.
        @type nodeIdentifier: C{unicode}
        @return: A deferred that fires with C{None} when the node's
                 configuration has been changed.
        @rtype: L{defer.Deferred}
        """

    def items(requestor, nodeIdentifier, maxItems, itemIdentifiers):
        """
        Called when a items retrieval request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The identifier of the node to retrieve items
                               from.
        @type nodeIdentifier: C{unicode}
        """

    def retract(requestor, nodeIdentifier, itemIdentifiers):
        """
        Called when a item retraction request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The identifier of the node to retract items
                               from.
        @type nodeIdentifier: C{unicode}
        """

    def purge(requestor, nodeIdentifier):
        """
        Called when a node purge request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The identifier of the node to be purged.
        @type nodeIdentifier: C{unicode}
        """

    def delete(requestor, nodeIdentifier):
        """
        Called when a node deletion request has been received.

        @param requestor: The entity the request originated from.
        @type requestor: L{jid.JID}
        @param nodeIdentifier: The identifier of the node to be delete.
        @type nodeIdentifier: C{unicode}
        """

