from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive.helpers import data_changed


class HttpRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:http}-relation-{joined,changed,departed,broken}')
    def changed(self):
        services = self.services()
        if services:
            self.set_state('{relation_name}.available')
        else:
            self.remove_state('{relation_name}.available')
        if data_changed(self.relation_name, services):
            self.set_state('{relation_name}.changed')

    def services(self):
        """
        Returns a list of available HTTP services and their associated hosts
        and ports.

        The return value is a list of dicts of the following form::

            [
                {
                    'service_name': name_of_service,
                    'hosts': [
                        {
                            'hostname': address_of_host,
                            'port': port_for_host,
                        },
                        # ...
                    ],
                },
                # ...
            ]
        """
        services = {}
        for conv in self.conversations():
            service_name = conv.scope.split('/')[0]
            service = services.setdefault(service_name, {
                'service_name': service_name,
                'hosts': [],
            })
            host = conv.get_remote('hostname') or conv.get_remove('private-address')
            port = conv.get_remote('port')
            if host and port:
                service['hosts'].append({
                    'hostname': host,
                    'port': port,
                })
        return [s for s in services.values() if s['hosts']]
