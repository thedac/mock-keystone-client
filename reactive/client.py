from charmhelpers.core.hookenv import status_set, log, config
from charmhelpers.core.templating import render
from charms.reactive import when, when_not
from charms.reactive import set_state, remove_state


@when('identity-credentials.connected')
@when_not('identity-credentials.available.auth')
def join_credentials_relation(keystone_credentials):
    keystone_credentials.request_credentials(
        username='mock-client',
        project=config('project'),
        requested_roles=config('requested_roles'),
        requested_grants=config('requested_roles'),
        domain=config('domain'))
    remove_state('credentials-ready')
    status_set('waiting', 'Waiting for identity credentials relation data')


@when('identity-credentials.available.auth')
def credentials_ready(keystone_credentials):
    log('Rendering novarc')
    render(source='novarc',
           target='/home/ubuntu/novarc',
           owner='ubuntu',
           perms=0o600,
           context={
               'id': keystone_credentials,
           })
    set_state('credentials-ready')
    status_set('active', 'Credentials Related')
