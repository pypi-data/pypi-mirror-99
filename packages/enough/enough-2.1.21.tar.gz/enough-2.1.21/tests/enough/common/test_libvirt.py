import pytest
import sh

from enough.common import libvirt
from enough.common.openstack import OpenStack


@pytest.mark.libvirt_integration
def test_libvirt_network_all(dotenough_libvirt_fixture):
    lv = libvirt.Libvirt(dotenough_libvirt_fixture.config_dir, '.')
    prefix = '10.2.3'
    name = dotenough_libvirt_fixture.prefix
    network = lv.network_create(name, prefix)
    assert network.name() == name
    assert network.name() == lv.network_create(name, prefix).name()
    n = '10'
    ip = f'{prefix}.{n}'
    mac = f'52:54:00:00:00:{n}'
    host = 'sample-host'
    assert lv.network_host_set(name, host, mac, ip) is True
    assert lv.network_host_set(name, host, mac, ip) is False
    assert lv.network_host_unset(name, host, mac, ip) is True
    assert lv.network_host_unset(name, host, mac, ip) is False
    assert lv.network_destroy(name) is True
    assert lv.network_destroy(name) is False


@pytest.mark.libvirt_integration
def test_libvirt_create_or_udpate(dotenough_libvirt_fixture):
    lv = libvirt.Libvirt(dotenough_libvirt_fixture.config_dir, '.',
                         domain=dotenough_libvirt_fixture.domain)
    info = lv.create_or_update([dotenough_libvirt_fixture.prefix])
    assert info[dotenough_libvirt_fixture.prefix]['port'] == '22'


@pytest.mark.libvirt_integration
def test_libvirt_networks_create(dotenough_libvirt_fixture):
    lv = libvirt.Libvirt(dotenough_libvirt_fixture.config_dir, '.')
    networks = lv.networks_create()
    for network in networks:
        assert network.name().startswith(dotenough_libvirt_fixture.prefix)
    assert 'bind-host' in networks[0].XMLDesc()
    for (_, network) in lv.networks_definitions_get().items():
        assert network['name'] in lv.lv.listNetworks()
    lv.networks_destroy()
    for (_, network) in lv.networks_definitions_get().items():
        assert network['name'] not in lv.lv.listNetworks()


@pytest.mark.libvirt_integration
def test_libvirt_image_builder(dotenough_libvirt_fixture):
    lv = libvirt.Libvirt(dotenough_libvirt_fixture.config_dir, '.',
                         domain=dotenough_libvirt_fixture.domain)
    assert lv.image_builder() is False


@pytest.mark.openstack_integration
@pytest.mark.libvirt_integration
def test_libvirt_backup(mocker, dotenough_libvirt_fixture, openstack_name, dot_openstack):
    lv = libvirt.Libvirt(dotenough_libvirt_fixture.config_dir, '.',
                         domain=dotenough_libvirt_fixture.domain)
    host = 'fake-host'
    mocker.patch('enough.common.libvirt.Libvirt.pets_get', return_value=[host])
    sh.qemu_img('create', '-f', 'qcow2', lv.host_image_name(host), '1M')
    o = OpenStack(dot_openstack.config_dir)

    lv.backup_create(o)
    backup = o.backup_name_create(host)
    assert [backup] == o.image_list()

    lv.args['days'] = 0
    lv.backup_prune(o)
    assert [] == o.image_list()
