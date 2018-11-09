from charmhelpers.core import hookenv
from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class HttpProvides(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def joined(self):
        set_flag(self.expand_name('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('{endpoint_name}.available'))

    def get_ingress_address(self, rel_id=None):
        # If no rel_id is provided, we fallback to the first one
        if rel_id is None:
            rel_id = self.relations[0].relation_id
        return hookenv.ingress_address(rel_id, hookenv.local_unit())

    def configure(self, port, private_address=None, hostname=None):
        for relation in self.relations:
            ingress_address = self.get_ingress_address(relation.relation_id)
            relation.to_publish_raw.update({
                'hostname': hostname or ingress_address,
                'private-address': private_address or ingress_address,
                'port': port,
            })

    def set_remote(self, **kwargs):
        # NB: This method provides backwards compatibility for charms that
        # called RelationBase.set_remote. Most commonly, this was done by
        # charms that needed to pass reverse proxy stanzas to http proxies.
        # This type of interaction with base relation classes is discouraged,
        # and should be handled with logic encapsulated in appropriate
        # interfaces. Eventually, this method will be deprecated in favor of
        # that behavior.
        for relation in self.relations:
            relation.to_publish_raw.update(kwargs)
