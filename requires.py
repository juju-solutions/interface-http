from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class HttpRequires(RelationBase):
    scope = scopes.SERVICE
    auto_accessors = ['host', 'port']

    @hook('{requires:http}-relation-{joined,changed}')
    def changed(self):
        data = {
            'host': self.host(),
            'port': self.port()
        }
        if all(data.values()):
            self.set_state('{relation_name}.available')

    @hook('{requires:http}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.available')
