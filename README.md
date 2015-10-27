# Overview

This interface layer implements the basic form of the `http` interface protocol,
which is used for things such as reverse-proxies, load-balanced servers, REST
service discovery, et cetera.

# Usage

## Provides

By providing the `http` interface, your charm is providing an HTTP server that
can be load-balanced, reverse-proxied, used as a REST endpoint, etc.

Your charm need only provide the port on which it is serving its content, as
soon as the `{relation_name}.available` state is set:

```python
@when('website.available')
def configure_website(website):
    website.configure(port=hookenv.config('port'))
```

## Requires

By requiring the `http` interface, your charm is consuming one or more HTTP
servers, as a REST endpoint, to load-balance a set of servers, etc.

Your charm can respond to either (or both of) the `{relation_name}.available`
and `{relation_name}.changed` states, with the former indicating that there is
at least one HTTP server connected, and the latter indicating that there is at
least one HTTP server connected and that the connection info has changed.  (The
changed state should be removed after being handled.)

The `services()` method returns a list of available HTTP services and their
associated hosts and ports.

The return value is a list of dicts of the following form:

```python
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
```

A trivial example of handling this interface would be:

```python
@when('reverseproxy.changed')
def update_reverse_proxy_config(reverseproxy):
    for service in reverseproxy.services():
        for host in service['hosts']:
            hookenv.log('{} has a unit {}:{}'.format(
                services['service_name'],
                host['hostname'],
                host['port']))
    remove_state('reverseproxy.changed')
```
