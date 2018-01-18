from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class HttpProvides(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:http}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.available')

    @hook('{provides:http}-relation-departed')
    def departed(self):
        if len(self.conversation().units) == 1:
            # this is the last departing unit
            self.remove_state('{relation_name}.available')

    def get_ingress_address(self):
        try:
            network_info = hookenv.network_get(self.relation_name)
        except NotImplementedError:
            network_info = []

        if network_info and 'ingress-addresses' in network_info:
            # just grab the first one for now, maybe be more robust here?
            return network_info['ingress-addresses'][0]
        else:
            # if they don't have ingress-addresses they are running a juju that
            # doesn't support spaces, so just return the private address
            return hookenv.unit_get('private-address')

    def configure(self, port, private_address=None, hostname=None):
        if not hostname:
            hostname = self.get_ingress_address()
        if not private_address:
            private_address = self.get_ingress_address()
        relation_info = {
            'hostname': hostname,
            'private-address': private_address,
            'port': port,
        }
        self.set_remote(**relation_info)
