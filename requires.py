from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class HttpRequires(Endpoint):

    @when('endpoint.{endpoint_name}.changed')
    def changed(self):
        if any(unit.received_raw['port'] for unit in self.all_joined_units):
            set_flag(self.expand_name('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('{endpoint_name}.available'))

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
                            'private-address': private_address_of_host,
                            'port': port_for_host,
                        },
                        # ...
                    ],
                },
                # ...
            ]
        """
        services = {}
        for relation in self.relations:
            service_name = relation.application_name
            service = services.setdefault(service_name, {
                'service_name': service_name,
                'hosts': [],
            })
            for unit in relation.joined_units:
                data = unit.received_raw
                private_address = data['private-address']
                host = data['hostname'] or private_address
                port = data['port']
                if host and port:
                    service['hosts'].append({
                        'hostname': host,
                        'private-address': private_address,
                        'port': port,
                    })
        return [s for s in services.values() if s['hosts']]
