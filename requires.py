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
        services_data = {}
        for conv in self.conversations():
            unit = conv.scope
            service = unit.split('/')[0]
            host = conv.get_remote('hostname') or conv.get_remove('private-address')
            port = conv.get_remote('port')
            if host and port:
                services_data.setdefault(service, []).append((host, port))
        return services_data
