from misttests.api.helpers import *


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_networks_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_networks(api_token=owner_api_token,
                                       cloud_id='dummy').get()
    assert_response_not_found(response)
    print "Success!!!"


def test_list_networks_wrong_api_token(pretty_print, mist_core):
    response = mist_core.list_networks(api_token='dummy',
                                       cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_networks_no_api_token(pretty_print, mist_core):
    response = mist_core.list_networks(api_token='',
                                       cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_subnets_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_subnets(api_token=owner_api_token,
                                      cloud_id='dummy', network_id='dummy').get()
    assert_response_not_found(response)
    print "Success!!!"


def test_list_subnets_wrong_api_token(pretty_print, mist_core):
    response = mist_core.list_subnets(api_token='dummy', network_id='dummy',
                                      cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_subnets_no_api_token(pretty_print, mist_core):
    response = mist_core.list_networks(api_token='',
                                       cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_network_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_network(api_token=owner_api_token,
                                        cloud_id='dummy').post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_create_network_wrong_api_token(pretty_print, mist_core):
    response = mist_core.create_network(api_token='dummy',
                                        cloud_id='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


# def test_create_network_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.create_network(api_token=owner_api_token, network_params={'network': {}},
#                                         cloud_id='dummy').post()
#     assert_response_not_found(response)
#     print "Success!!!"


def test_create_network_no_api_token(pretty_print, mist_core):
    response = mist_core.create_network(api_token='', cloud_id='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_create_subnet_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_subnet(api_token=owner_api_token,
                                       cloud_id='dummy', network_id='dummy').post()
    assert_response_not_found(response)
    print "Success!!!"


def test_create_subnet_wrong_api_token(pretty_print, mist_core):
    response = mist_core.create_subnet(api_token='dummy', network_id='dummy',
                                       cloud_id='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_subnet_no_api_token(pretty_print, mist_core):
    response = mist_core.create_subnet(api_token='', network_id='dummy',
                                       cloud_id='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_network_no_api_token(pretty_print, mist_core):
    response = mist_core.delete_network(api_token='', network_id='dummy',
                                        cloud_id='dummy').delete()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_network_wrong_api_token(pretty_print, mist_core):
    response = mist_core.delete_network(api_token='dummy', network_id='dummy',
                                        cloud_id='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_network_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_network(api_token=owner_api_token,
                                       cloud_id='dummy', network_id='dummy').delete()
    assert_response_not_found(response)
    print "Success!!!"


def test_delete_subnet_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_subnet(api_token='dummy', network_id='dummy',
                                       cloud_id='dummy', subnet_id='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


# check - it should get forbidden?
def test_delete_subnet_no_api_token(pretty_print, mist_core):
    response = mist_core.delete_subnet(api_token='dummy', network_id='dummy',
                                       cloud_id='dummy', subnet_id='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_subnet_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_subnet(api_token=owner_api_token, network_id='dummy',
                                       cloud_id='dummy', subnet_id='dummy').delete()
    assert_response_not_found(response)
    print "Success!!!"


############################################################################
#                          Functional Testing                              #
############################################################################

# @pytest.mark.incremental
# class TestNetworksFunctionality:
#     def test_create_network_openstack(self, mist_core, cache, owner_api_token):
#         response = mist_core.add_cloud(provider='openstack', title='Openstack', api_token=owner_api_token,
#                                        username=config.CREDENTIALS['OPENSTACK']['username'],
#                                        tenant=config.CREDENTIALS['OPENSTACK']['tenant'],
#                                        password=config.CREDENTIALS['OPENSTACK']['password'],
#                                        auth_url=config.CREDENTIALS['OPENSTACK']['auth_url']
#                                        ).post()
#         assert_response_ok(response)
#         cache.set('cloud_ids/openstack', response.json()['id'])
#
#         network_params = {'network':{'name':'openstack_net%d' % random.randint(1,200),
#                                      'admin_state_up': True}}
#
#         response = mist_core.create_network(api_token=owner_api_token, network_params= network_params,
#                                             cloud_id=cache.get('cloud_ids/openstack', '')).post()
#         assert_response_ok(response)
#
#         cache.set('network_ids/openstack', response.json()['id'])
#
#         response = mist_core.list_networks(api_token=owner_api_token,
#                                            cloud_id=cache.get('cloud_ids/openstack', '')).get()
#         assert_response_ok(response)
#         print "Success!!!"

    # def test_create_network_ec2(self, mist_core, cache, owner_api_token):
    #     response = mist_core.add_cloud(provider='ec2', title='AWS', api_token=owner_api_token,
    #                                    api_key=config.CREDENTIALS['AWS']['api_key'],
    #                                    api_secret=config.CREDENTIALS['AWS']['api_secret'],
    #                                    region='ap-northeast-1'
    #                                    ).post()
    #     assert_response_ok(response)
    #     cache.set('cloud_ids/ec2', response.json()['id'])
    #     response = mist_core.create_network(api_token=owner_api_token,
    #                                         network_params={'network': {'name': 'ec2_api_test_network',
    #                                         'cidr': '10.1.0.0/16'}}, cloud_id=cache.get('cloud_ids/ec2', '')).post()
    #     assert_response_ok(response)
    #
    #     cache.set('network_ids/ec2', response.json()['network_id'])
    #
    #     response = mist_core.list_networks(api_token=owner_api_token,
    #                                        cloud_id=cache.get('cloud_ids/ec2', '')).get()
    #     assert_response_ok(response)
    #     print "Success!!!"

# remove resources
