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
        for relation in self.relations:
            relation.to_publish.update({
                'hostname': hostname,
                'private-address': private_address,
                'port': port,
            })
