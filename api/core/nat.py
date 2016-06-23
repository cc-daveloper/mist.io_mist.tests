from tests.api.helpers import *
from tests.api.utils import *

from tests.helpers.setup import setup_user_if_not_exists

from tests import config


def test_nat(pretty_print, mist_core, cache, valid_api_token):
    sanitized_url = config.VPN_URL.replace('http://', '').split(':')[0]
    # setting up user
    user = setup_user_if_not_exists(config.EMAIL, config.PASSWORD1)

    print '\n>>> POSTing in /tunnels for a new VPN Tunnel'
    # request a dummy tunnel
    tunnel_data = {
        'client_addr': '',
        'cidrs': ['10.10.10.0/24'],
        'name': 'DummyTestTunnel',
        'description': 'Testing DNAT'
    }
    response = mist_core.add_vpn_tunnel(api_token=valid_api_token,
                                        **tunnel_data).post()
    assert_response_ok(response)

    print '\n>>> GETing forwarding (addr, port) tuples from the OpenVPN server'
    from mist.core.vpn.methods import destination_nat
    # scenarios providing an (addr, port) tuple to be translated
    addr, port = destination_nat(user, '10.10.10.5', 80)
    print '(%s, %s) -> (%s, %s)' % ('10.10.10.5', 80, addr, port)
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'
    addr, port = destination_nat(user, '10.10.10.5', 22)
    print '(%s, %s) -> (%s, %s)' % ('10.10.10.5', 22, addr, port)
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'
    # providing only a single URI string to be translated
    # and returned in the same exact format
    addr = destination_nat(user, '10.10.10.5')
    print '%s -> %s' % ('10.10.10.5', addr)
    addr, port = addr.split(':')[0], addr.split(':')[1]
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'
    addr = destination_nat(user, 'https://10.10.10.5')
    print '%s -> %s' % ('https://10.10.10.5', addr)
    assert addr.startswith('https://'), 'Prefix missing!'
    addr = addr.replace('https://', '')
    addr, port = addr.split(':')[0], addr.split(':')[1]
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'
    addr = destination_nat(user, '10.10.10.5:5000')
    print '%s -> %s' % ('10.10.10.5:5000', addr)
    addr, port = addr.split(':')[0], addr.split(':')[1]
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'
    addr = destination_nat(user, 'http://10.10.10.5:5000/api/v1')
    print '%s -> %s' % ('http://10.10.10.5:5000/api/v1', addr)
    assert addr.startswith('http://'), 'Prefix missing!'
    assert addr.endswith('/api/v1'), 'Suffix missing!'
    addr = addr.replace('http://', '')
    addr = addr.replace('/api/v1', '')
    addr, port = addr.split(':')[0], addr.split(':')[1]
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'

    print "\n>>> GETing /tunnels"
    response = mist_core.list_vpn_tunnels(api_token=valid_api_token).get()
    assert_response_ok(response)

    tunnels = json.loads(response.content)
    assert_list_not_empty(tunnels)
    for tunnel in tunnels:
        if tunnel['name'] == 'DummyTestTunnel':
            _id = tunnel['_id']

    print "\n>>> DELETEing VPN Tunnel"
    response = mist_core.del_vpn_tunnel(api_token=valid_api_token,
                                        tunnel_id=_id).delete()
    assert_response_ok(response)

    print "Success!!!!"
