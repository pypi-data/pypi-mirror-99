from __future__ import absolute_import

import os
import time
import functools

from oslo_log import log
import pandas
import podman as podmanlib
import docker as dockerlib

import tobiko
from tobiko import podman
from tobiko import docker
from tobiko.openstack import topology
from tobiko.shell import sh
from tobiko.shell import ssh
from tobiko.tripleo import overcloud
from tobiko.tripleo import topology as tripleo_topology


LOG = log.getLogger(__name__)


def get_container_runtime_module():
    """check what container runtime is running
    and return a handle to it"""
    # TODO THIS LOCKS SSH CLIENT TO CONTROLLER
    ssh_client = topology.list_openstack_nodes(group='controller')[
        0].ssh_client
    if docker.is_docker_running(ssh_client=ssh_client):
        return docker
    else:
        return podman


def get_container_runtime_name():
    return container_runtime_module.__name__.rsplit('.', 1)[1]


if overcloud.has_overcloud():
    container_runtime_module = get_container_runtime_module()
    container_runtime_name = get_container_runtime_name()


@functools.lru_cache()
def list_node_containers(ssh_client):
    """returns a list of containers and their run state"""
    client = get_container_client(ssh_client=ssh_client)
    if container_runtime_module == podman:
        return container_runtime_module.list_podman_containers(client=client)

    elif container_runtime_module == docker:
        return container_runtime_module.list_docker_containers(client=client)


def get_container_client(ssh_client=None):
    """returns a list of containers and their run state"""

    for attempt in tobiko.retry(
            timeout=60.0,
            interval=5.0):
        try:
            if container_runtime_module == podman:
                return container_runtime_module.get_podman_client(
                    ssh_client=ssh_client).connect()
            elif container_runtime_module == docker:
                return container_runtime_module.get_docker_client(
                    ssh_client=ssh_client).connect()
        except dockerlib.errors.DockerException:
            LOG.debug('Unable to connect to docker API')
            attempt.check_limits()
            ssh.reset_default_ssh_port_forward_manager()
    # no successful connection to docker/podman API has been performed
    raise RuntimeError('Unable to connect to container mgmt tool')


def list_containers_df(group=None):
    actual_containers_list = list_containers(group)
    return pandas.DataFrame(
        get_container_states_list(actual_containers_list),
        columns=['container_host', 'container_name', 'container_state'])


def list_containers(group=None):
    """get list of containers in running state
    from specified node group
    returns : a list of overcloud_node's running containers"""

    # moved here from topology
    # reason : Workaround for :
    # AttributeError: module 'tobiko.openstack.topology' has no
    # attribute 'container_runtime'

    containers_list = tobiko.Selection()
    if group:
        openstack_nodes = topology.list_openstack_nodes(group=group)
    else:
        openstack_nodes = topology.list_openstack_nodes(group='overcloud')

    for node in openstack_nodes:
        node_containers_list = list_node_containers(ssh_client=node.ssh_client)
        containers_list.extend(node_containers_list)
    return containers_list


expected_containers_file = '/home/stack/expected_containers_list_df.csv'


def save_containers_state_to_file(expected_containers_list,):
    expected_containers_list_df = pandas.DataFrame(
        get_container_states_list(expected_containers_list),
        columns=['container_host', 'container_name', 'container_state'])
    expected_containers_list_df.to_csv(
        expected_containers_file)
    return expected_containers_file


def assert_containers_running(group, expected_containers, full_name=True):

    """assert that all containers specified in the list are running
    on the specified openstack group(controller or compute etc..)"""

    failures = []

    openstack_nodes = topology.list_openstack_nodes(group=group)
    for node in openstack_nodes:
        node_containers = list_node_containers(ssh_client=node.ssh_client)
        containers_list_df = pandas.DataFrame(
            get_container_states_list(node_containers),
            columns=['container_host', 'container_name', 'container_state'])
        # check that the containers are present
        LOG.info('node: {} containers list : {}'.format(
            node.name, containers_list_df.to_string(index=False)))
        for container in expected_containers:
            # get container attrs dataframe
            if full_name:
                container_attrs = containers_list_df.query(
                    'container_name == "{}"'.format(container))
            else:
                container_attrs = containers_list_df[
                    containers_list_df['container_name'].
                    str.contains(container)]
            # check if the container exists
            LOG.info('checking container: {}'.format(container))
            if container_attrs.empty:
                failures.append(
                    'expected container {} not found on node {} ! : \n\n'.
                    format(container, node.name))
            # if container exists, check it is running
            else:
                # only one running container is expected
                container_running_attrs = container_attrs.query(
                    'container_state=="running"')
                if container_running_attrs.empty:
                    failures.append(
                        'expected container {} is not running on node {} , '
                        'its state is {}! : \n\n'.format(
                            container, node.name,
                            container_attrs.container_state.values.item()))
                elif len(container_running_attrs) > 1:
                    failures.append(
                        'only one running container {} was expected on '
                        'node {}, but got {}! : \n\n'.format(
                            container, node.name,
                            len(container_running_attrs)))

    if failures:
        tobiko.fail('container states mismatched:\n{!s}', '\n'.join(failures))

    else:
        LOG.info('All tripleo common containers are in running state! ')


def assert_all_tripleo_containers_running():
    """check that all common tripleo containers are running
    param: group controller or compute , check containers
    sets in computes or controllers"""

    common_controller_tripleo_containers = ['cinder_api', 'cinder_api_cron',
                                            'cinder_scheduler',
                                            'glance_api', 'heat_api',
                                            'heat_api_cfn',
                                            'heat_api_cron', 'heat_engine',
                                            'horizon', 'iscsid', 'keystone',
                                            'logrotate_crond', 'memcached',
                                            'neutron_api', 'nova_api',
                                            'nova_api_cron', 'nova_conductor',
                                            'nova_metadata', 'nova_scheduler',
                                            'nova_vnc_proxy',
                                            'swift_account_auditor',
                                            'swift_account_reaper',
                                            'swift_account_replicator',
                                            'swift_account_server',
                                            'swift_container_auditor',
                                            'swift_container_replicator',
                                            'swift_container_server',
                                            'swift_container_updater',
                                            'swift_object_auditor',
                                            'swift_object_expirer',
                                            'swift_object_replicator',
                                            'swift_object_server',
                                            'swift_object_updater',
                                            'swift_proxy', 'swift_rsync']

    common_compute_tripleo_containers = ['iscsid', 'logrotate_crond',
                                         'nova_compute', 'nova_libvirt',
                                         'nova_migration_target',
                                         'nova_virtlogd']

    for group, group_containers in [('controller',
                                     common_controller_tripleo_containers),
                                    ('compute',
                                     common_compute_tripleo_containers)]:
        assert_containers_running(group, group_containers)
    # TODO: need to address OSP-version specific containers here.
    # optional ovn containers checks
    assert_ovn_containers_running()


@functools.lru_cache()
def ovn_used_on_overcloud():
    return list_containers_df()['container_name'].\
            str.contains('ovn').any(axis=None)


def assert_ovn_containers_running():
    # specific OVN verifications
    if ovn_used_on_overcloud():
        ovn_controller_containers = ['ovn_controller',
                                     'ovn-dbs-bundle-{}-'.
                                     format(container_runtime_name)]
        ovn_compute_containers = ['ovn_metadata_agent',
                                  'ovn_controller']
        group_containers_list = [('controller', ovn_controller_containers),
                                 ('compute', ovn_compute_containers)]
        if 'networker' in topology.list_openstack_node_groups():
            ovn_networker_containers = ['ovn_controller']
            group_containers_list.append(('networker',
                                          ovn_networker_containers))
        for group, group_containers in group_containers_list:
            assert_containers_running(group, group_containers, full_name=False)
        LOG.info("Networking OVN containers verified in running state")
    else:
        LOG.info("Networking OVN not configured")


def run_container_config_validations():
    """check containers configuration in different scenarios
    """

    # TODO add here any generic configuration validation
    config_checkings = []

    if ovn_used_on_overcloud():
        ovn_config_checkings = \
            [{'node_group': 'controller',
              'container_name': 'neutron_api',
              'config_file': '/etc/neutron/plugins/ml2/ml2_conf.ini',
              'param_validations': [{'section': 'ml2',
                                     'param': 'mechanism_drivers',
                                     'expected_value': 'ovn'},
                                    {'section': 'ml2',
                                     'param': 'type_drivers',
                                     'expected_value': 'geneve'},
                                    {'section': 'ovn',
                                     'param': 'ovn_l3_mode',
                                     'expected_value': 'True'},
                                    {'section': 'ovn',
                                     'param': 'ovn_metadata_enabled',
                                     'expected_value': 'True'}]}]
        config_checkings += ovn_config_checkings
    else:
        ovs_config_checkings = \
            [{'node_group': 'controller',
              'container_name': 'neutron_api',
              'config_file': '/etc/neutron/plugins/ml2/ml2_conf.ini',
              'param_validations': [{'section': 'ml2',
                                     'param': 'mechanism_drivers',
                                     'expected_value': 'openvswitch'}]}]
        config_checkings += ovs_config_checkings

    for config_check in config_checkings:
        for node in topology.list_openstack_nodes(
                group=config_check['node_group']):
            for param_check in config_check['param_validations']:
                obtained_param = sh.execute(
                    f"{container_runtime_name} exec -uroot "
                    f"{config_check['container_name']} crudini "
                    f"--get {config_check['config_file']} "
                    f"{param_check['section']} {param_check['param']}",
                    ssh_client=node.ssh_client, sudo=True).stdout.strip()
                if param_check['expected_value'] not in obtained_param:
                    tobiko.fail(f"Expected {param_check['param']} value: "
                                f"{param_check['expected_value']}\n"
                                f"Obtained {param_check['param']} value: "
                                f"{obtained_param}")
        LOG.info("Configuration verified:\n"
                 f"node group: {config_check['node_group']}\n"
                 f"container: {config_check['container_name']}\n"
                 f"config file: {config_check['config_file']}")


def comparable_container_keys(container, include_container_objects=False):
    """returns the tuple : 'container_host','container_name',
    'container_state, container object if specified'
     """
    if container_runtime_module == podman and include_container_objects:
        return (tripleo_topology.ip_to_hostname(
            container._client._context.hostname),  # pylint: disable=W0212
                container.data['names'], container.data['status'],
                container)
    elif container_runtime_module == podman:
        return (tripleo_topology.ip_to_hostname(
            container._client._context.hostname),  # pylint: disable=W0212
                container.data['names'], container.data['status'])

    elif container_runtime_module == docker and include_container_objects:
        return (container.attrs['Config']['Hostname'],
                container.attrs['Name'].strip('/'),
                container.attrs['State']['Status'],
                container)
    elif container_runtime_module == docker:
        return (container.attrs['Config']['Hostname'],
                container.attrs['Name'].strip('/'),
                container.attrs['State']['Status'])


@functools.lru_cache()
def list_containers_objects_df():
    containers_list = list_containers()
    containers_objects_list_df = pandas.DataFrame(
        get_container_states_list(
            containers_list, include_container_objects=True),
        columns=['container_host', 'container_name',
                 'container_state', 'container_object'])
    return containers_objects_list_df


def get_overcloud_container(container_name=None, container_host=None,
                            partial_container_name=None):
    """gets an container object by name on specified host
    container"""
    con_obj_df = list_containers_objects_df()
    if partial_container_name and container_host:
        con_obj_df = con_obj_df[con_obj_df['container_name'].str.contains(
            partial_container_name)]
        contaniner_obj = con_obj_df.query(
            'container_host == "{container_host}"'.format(
                container_host=container_host))['container_object']
    elif container_host:
        contaniner_obj = con_obj_df.query(
            'container_name == "{container_name}"'
            ' and container_host == "{container_host}"'.
            format(container_host=container_host,
                   container_name=container_name))['container_object']
    else:
        contaniner_obj = con_obj_df.query(
            'container_name == "{container_name}"'.
            format(container_name=container_name))['container_object']
    if not contaniner_obj.empty:
        return contaniner_obj.values[0]
    else:
        tobiko.fail('container {} not found!'.format(container_name))


def action_on_container(action,
                        container_name=None, container_host=None,
                        partial_container_name=None):
    """take a container snd preform an action on it
    actions are as defined in : podman/libs/containers.py:14/164"""
    container = get_overcloud_container(
        container_name=container_name,
        container_host=container_host,
        partial_container_name=partial_container_name)
    # we get the specified action as function from podman lib
    if container_runtime_module == podman:
        container_function = getattr(
            podmanlib.libs.containers.Container, '{}'.format(action))
    else:
        container_function = getattr(
            dockerlib.models.containers.Container, '{}'.format(action))
    LOG.info('action_on_container: executing : {} on {}'.format(action,
                                                                container))
    return container_function(container)


def get_container_states_list(containers_list,
                              include_container_objects=False):
    container_states_list = tobiko.Selection()
    container_states_list.extend([comparable_container_keys(
        container, include_container_objects=include_container_objects) for
                                  container in containers_list])
    return container_states_list


pcs_resource_list = ['haproxy', 'galera', 'redis', 'ovn-dbs', 'cinder',
                     'rabbitmq']


def remove_containers_if_pacemaker_resources(comparable_containers_df):
    """remove any containers in
    param: comparable_containers_df that are pacemaker resources
    i.e if they contain tha names of resources defined in
    pcs_resources_list"""

    for row in comparable_containers_df.iterrows():
        for pcs_resource in pcs_resource_list:
            if pcs_resource in str(row):
                LOG.info(f'pcs resource {pcs_resource} has changed state, '
                         f'but that\'s ok since pcs resources can change '
                         f'state/host: {str(row)}')
                # if a pcs resource is found , we drop that row
                comparable_containers_df.drop(row[0], inplace=True)
    return comparable_containers_df


def dataframe_difference(df1, df2, which=None):
    """Find rows which are different between two DataFrames."""
    comparison_df = df1.merge(df2,
                              indicator='same_state',
                              how='outer')
    # return only non identical rows
    if which is None:
        diff_df = comparison_df[comparison_df['same_state'] != 'both']

    else:
        diff_df = comparison_df[comparison_df['same_state'] == which]

    # if the list of diffrent state container are pacemaker resources ignore
    # the error since we are checking pacemaker also.

    remove_containers_if_pacemaker_resources(diff_df)

    return diff_df


def assert_equal_containers_state(expected_containers_list=None,
                                  timeout=120, interval=2,
                                  recreate_expected=False):

    """compare all overcloud container states with using two lists:
    one is current , the other some past list
    first time this method runs it creates a file holding overcloud
    containers' states: /home/stack/expected_containers_list_df.csv'
    second time it creates a current containers states list and
    compares them, they must be identical"""

    # if we have a file or an explicit variable use that , otherwise  create
    # and return
    if recreate_expected or (not expected_containers_list and
                             not os.path.exists(expected_containers_file)):
        save_containers_state_to_file(list_containers())
        return

    elif expected_containers_list:
        expected_containers_list_df = pandas.DataFrame(
            get_container_states_list(expected_containers_list),
            columns=['container_host', 'container_name', 'container_state'])

    elif os.path.exists(expected_containers_file):
        expected_containers_list_df = pandas.read_csv(
            expected_containers_file)

    failures = []
    start = time.time()
    error_info = 'Output explanation: left_only is the original state, ' \
                 'right_only is the new state'

    while time.time() - start < timeout:

        failures = []
        actual_containers_list_df = list_containers_df()

        LOG.info('expected_containers_list_df: {} '.format(
            expected_containers_list_df.to_string(index=False)))
        LOG.info('actual_containers_list_df: {} '.format(
            actual_containers_list_df.to_string(index=False)))

        # execute a `dataframe` diff between the expected and actual containers
        expected_containers_state_changed = \
            dataframe_difference(expected_containers_list_df,
                                 actual_containers_list_df)
        # check for changed state containerstopology
        if not expected_containers_state_changed.empty:
            failures.append('expected containers changed state ! : '
                            '\n\n{}\n{}'.format(
                             expected_containers_state_changed.
                             to_string(index=False), error_info))
            LOG.info('container states mismatched:\n{}\n'.format(failures))
            time.sleep(interval)
            # clear cache to obtain new data
            list_node_containers.cache_clear()
        else:
            LOG.info("assert_equal_containers_state :"
                     " OK, all containers are on the same state")
            return
    if failures:
        tobiko.fail('container states mismatched:\n{!s}', '\n'.join(
            failures))
