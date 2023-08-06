import os
import socket
from pprint import pprint

import six

from fabric.api import (
    env,
    require,
    runs_once,
)

from burlap import common
from burlap import constants as c
from burlap.decorators import task_or_dryrun

try:
    import boto
    import boto.ec2
except ImportError:
    boto = None

EC2 = 'ec2'
KVM = 'kvm'

if 'vm_name_tag' not in env:

    env.vm_name_tag = 'Name'
    env.vm_group_tag = 'Group'
    env.vm_release_tag = 'Release'

    env.vm_type = None

    # If a name is not given, one will be auto-generated based on this pattern.
    env.vm_name_template = 'web{index}'

    # A release tag given to the instance when created to distinquish it from
    # future upgrades to the same instance name.
    env.vm_release = None

    env.vm_ec2_account_id = None
    # https://help.ubuntu.com/community/EC2StartersGuide#Official_Ubuntu_Cloud_Guest_Amazon_Machine_Images_.28AMIs.29
    env.vm_ec2_ami = None # e.g. 'ami-a29943cb'
    env.vm_ec2_instance_type = None # e.g. 'm1.small'
    env.vm_ec2_ebs = None
    env.vm_ec2_region = None # e.g. 'us-east-1'
    env.vm_ec2_zone = None # e.g. 'us-east-1b'
    env.vm_ec2_available_security_groups = {} # {(name,desc):[(protocol, port, port, ip_range)]
    env.vm_ec2_selected_security_groups = []
    env.vm_ec2_aws_access_key_id = None
    env.vm_ec2_aws_secret_access_key = None
    env.vm_ec2_volume = '/dev/sdh1'
    env.vm_ec2_keypair_name = None
    env.vm_ec2_use_elastic_ip = False
    env.vm_ec2_subnet_id = None
    env.vm_ec2_allocate_address_domain = None

    # If true, we will attempt to add or delete group rules.
    env.vm_ec2_security_group_owner = False

    # Stores dynamically allocated EIP for each host, {hostname: ip}.
    # Usually stored in a shelf file.
    env.vm_elastic_ip_mappings = None

def retrieve_ec2_hosts(extended=0, site=None):
    verbose = common.get_verbose()
    extended = int(extended)
    if verbose:
        print('site:', site)
    for host_name, data in list_instances(show=0, verbose=verbose).items():
        if verbose:
            print('host_name:', host_name)
            pprint(data, indent=4)

        # Ignore hosts that are disabled for the given site.
        if site not in (None, c.ALL) and env.available_sites_by_host and host_name in env.available_sites_by_host:
            if site not in env.available_sites_by_host[host_name]:
                if verbose:
                    print('skipping because site %s is not set for this host' % site)
                continue

        if extended:
            yield (host_name, data)
        elif data.public_dns_name:
            yield data.public_dns_name
        else:
            yield data.ip

env.hosts_retrievers[EC2] = retrieve_ec2_hosts

def translate_ec2_hostname(hostname):
    verbose = common.get_verbose()
    for name, data in list_instances(show=0, verbose=verbose).items():
        if name == hostname:
            return data.public_dns_name

env.hostname_translators[EC2] = translate_ec2_hostname

def get_ec2_connection():
    conn = boto.ec2.connect_to_region(
        #env.vm_ec2_zone,
        env.vm_ec2_region,
        aws_access_key_id=env.vm_ec2_aws_access_key_id,
        aws_secret_access_key=env.vm_ec2_aws_secret_access_key,
    )
    assert conn, 'Unable to create EC2 connection with region %s and access key %s.' % (env.vm_ec2_region, env.vm_ec2_aws_access_key_id)
    return conn

def get_all_ec2_instances(instance_ids=None):
    conn = get_ec2_connection()
    #return sum(map(lambda r: r.instances, conn.get_all_instances(instance_ids=instance_ids)), [])
    return sum([r.instances for r in conn.get_all_instances(instance_ids=instance_ids)], [])

def get_all_running_ec2_instances():
    #instances = filter(lambda i: i.state == 'running', get_all_ec2_instances())
    instances = [i for i in get_all_ec2_instances() if i.state == 'running']
    instances.reverse()
    return instances



@task_or_dryrun
#@runs_once #breaks get_or_create()
def list_instances(show=1, name=None, group=None, release=None, except_release=None):
    """
    Retrieves all virtual machines instances in the current environment.
    """
    from burlap.common import shelf, OrderedDict, get_verbose

    verbose = get_verbose()
    require('vm_type', 'vm_group')
    assert env.vm_type, 'No VM type specified.'
    env.vm_type = (env.vm_type or '').lower()
    _name = name
    _group = group
    _release = release
    if verbose:
        print('name=%s, group=%s, release=%s' % (_name, _group, _release))

    env.vm_elastic_ip_mappings = shelf.get('vm_elastic_ip_mappings')

    data = type(env)()
    if env.vm_type == EC2:
        if verbose:
            print('Checking EC2...')
        for instance in get_all_running_ec2_instances():
            name = instance.tags.get(env.vm_name_tag)
            group = instance.tags.get(env.vm_group_tag)
            release = instance.tags.get(env.vm_release_tag)
            if env.vm_group and env.vm_group != group:
                if verbose:
                    print(('Skipping instance %s because its group "%s" '
                        'does not match env.vm_group "%s".') \
                            % (instance.public_dns_name, group, env.vm_group))
                continue
            if _group and group != _group:
                if verbose:
                    print(('Skipping instance %s because its group "%s" '
                        'does not match local group "%s".') \
                            % (instance.public_dns_name, group, _group))
                continue
            if _name and name != _name:
                if verbose:
                    print(('Skipping instance %s because its name "%s" '
                        'does not match name "%s".') \
                            % (instance.public_dns_name, name, _name))
                continue
            if _release and release != _release:
                if verbose:
                    print(('Skipping instance %s because its release "%s" '
                        'does not match release "%s".') \
                            % (instance.public_dns_name, release, _release))
                continue
            if except_release and release == except_release:
                continue
            if verbose:
                print('Adding instance %s (%s).' % (name, instance.public_dns_name or instance.ip_address))
            data.setdefault(name, type(env)())
            data[name]['id'] = instance.id
            data[name]['public_dns_name'] = instance.public_dns_name or instance.ip_address
            if verbose:
                print('Public DNS: %s' % instance.public_dns_name)

            if env.vm_elastic_ip_mappings and name in env.vm_elastic_ip_mappings:
                data[name]['ip'] = env.vm_elastic_ip_mappings[name]
            else:
                data[name]['ip'] = socket.gethostbyname(instance.public_dns_name)

        if int(show):
            pprint(data, indent=4)
        return data
    if env.vm_type == KVM:
        #virsh list
        pass
    else:
        raise NotImplementedError

#@task_or_dryrun
#@runs_once
#def list(*args, **kwargs):
#    #execute(list_instances, *args, **kwargs)
#    list_instances(*args, **kwargs)


def set_ec2_security_group_id(name, id): # pylint: disable=redefined-builtin
    from burlap.common import shelf, OrderedDict
    v = shelf.get('vm_ec2_security_group_ids', OrderedDict())
    v[name] = str(id)
    shelf.set('vm_ec2_security_group_ids', v)


@task_or_dryrun
def get_ec2_security_group_id(name=None, verbose=0):
    from burlap.common import shelf, OrderedDict

    verbose = int(verbose)

    group_id = None
    conn = get_ec2_connection()
    groups = conn.get_all_security_groups()
    for group in groups:
        if verbose:
            print('group:', group.name, group.id)
        if group.name == name:
            group_id = group.id

    # Otherwise try the local cache.
    if not group_id:
        v = shelf.get('vm_ec2_security_group_ids', OrderedDict())
        group_id = v.get(name)

    if verbose:
        print(group_id)
    return group_id


@task_or_dryrun
def get_or_create_ec2_security_groups(names=None, verbose=1):
    """
    Creates a security group opening 22, 80 and 443
    """
    verbose = int(verbose)

    if verbose:
        print('Creating EC2 security groups...')

    conn = get_ec2_connection()

    if isinstance(names, six.string_types):
        names = names.split(',')
    names = names or env.vm_ec2_selected_security_groups
    if verbose:
        print('Group names:', names)

    ret = []
    for name in names:
        try:
            group_id = get_ec2_security_group_id(name)
            if verbose:
                print('group_id:', group_id)
            #group = conn.get_all_security_groups(groupnames=[name])[0]
            # Note, groups in a VPC can't be referred to by name?
            group = conn.get_all_security_groups(group_ids=[group_id])[0]
        except boto.exception.EC2ResponseError as e:
            if verbose:
                print(e)
            group = get_ec2_connection().create_security_group(
                name,
                name,
                vpc_id=env.vm_ec2_vpc_id,
            )
            print('group_id:', group.id)
            set_ec2_security_group_id(name, group.id)
        ret.append(group)

        # Find existing rules.
        actual_sets = set()
        for rule in list(group.rules):
            ip_protocol = rule.ip_protocol
            from_port = rule.from_port
            to_port = rule.to_port
            for cidr_ip in rule.grants:
                #print('Revoking:', ip_protocol, from_port, to_port, cidr_ip)
                #group.revoke(ip_protocol, from_port, to_port, cidr_ip)
                rule_groups = ((rule.groups and rule.groups.split(',')) or [None])
                for src_group in rule_groups:
                    src_group = (src_group or '').strip()
                    if src_group:
                        actual_sets.add((ip_protocol, from_port, to_port, str(cidr_ip), src_group))
                    else:
                        actual_sets.add((ip_protocol, from_port, to_port, str(cidr_ip)))

        # Find actual rules.
        expected_sets = set()
        for authorization in env.vm_ec2_available_security_groups.get(name, []):
            if verbose:
                print('authorization:', authorization)
            if len(authorization) == 4 or (len(authorization) == 5 and not (authorization[-1] or '').strip()):
                src_group = None
                ip_protocol, from_port, to_port, cidr_ip = authorization[:4]
                if cidr_ip:
                    expected_sets.add((ip_protocol, str(from_port), str(to_port), cidr_ip))
            else:
                ip_protocol, from_port, to_port, cidr_ip, src_group = authorization
                if cidr_ip:
                    expected_sets.add((ip_protocol, str(from_port), str(to_port), cidr_ip, src_group))

        # Calculate differences and update rules if we own the group.
        if env.vm_ec2_security_group_owner:
            if verbose:
                print('expected_sets:')
                print(expected_sets)
                print('actual_sets:')
                print(actual_sets)
            del_sets = actual_sets.difference(expected_sets)
            if verbose:
                print('del_sets:')
                print(del_sets)
            add_sets = expected_sets.difference(actual_sets)
            if verbose:
                print('add_sets:')
                print(add_sets)

            # Revoke deleted.
            for auth in del_sets:
                print(len(auth))
                print('revoking:', auth)
                group.revoke(*auth)

            # Create fresh rules.
            for auth in add_sets:
                print('authorizing:', auth)
                group.authorize(*auth)

    return ret

@task_or_dryrun
def get_or_create_ec2_key_pair(name=None, verbose=1):
    """
    Creates and saves an EC2 key pair to a local PEM file.
    """
    verbose = int(verbose)
    name = name or env.vm_ec2_keypair_name
    pem_path = 'roles/%s/%s.pem' % (env.ROLE, name)
    conn = get_ec2_connection()
    kp = conn.get_key_pair(name)
    if kp:
        print('Key pair %s already exists.' % name)
    else:
        # Note, we only get the private key during creation.
        # If we don't save it here, it's lost forever.
        kp = conn.create_key_pair(name)
        open(pem_path, 'wb').write(kp.material)
        os.system('chmod 600 %s' % pem_path)
        print('Key pair %s created.' % name)
    #return kp
    return pem_path

@task_or_dryrun
def list_security_groups():
    conn = get_ec2_connection()
    sgs = conn.get_all_security_groups()
    print('Id,Name,Number of Instances')
    for sg in sorted(sgs, key=lambda o: o.name):
        print('%s,%s,%s' % (sg.id, sg.name, len(sg.instances())))

@task_or_dryrun
def exists(name=None, group=None, release=None, except_release=None, verbose=1):
    """
    Determines if a virtual machine instance exists.
    """
    verbose = int(verbose)
    instances = list_instances(
        name=name,
        group=group,
        release=release,
        except_release=except_release,
        verbose=verbose,
        show=verbose)
    ret = bool(instances)
    if verbose:
        print('\ninstance %s exist' % ('DOES' if ret else 'does NOT'))
    #return ret
    return instances

@task_or_dryrun
def get_name():
    """
    Retrieves the instance name associated with the current host string.
    """
    if env.vm_type == EC2:
        for instance in get_all_running_ec2_instances():
            if env.host_string == instance.public_dns_name:
                name = instance.tags.get(env.vm_name_tag)
                return name
    else:
        raise NotImplementedError

@task_or_dryrun
def shutdown(force=False):
    #virsh shutdown <name>
    #virsh destroy <name> #to force
    raise NotImplementedError

@task_or_dryrun
def reboot():
    #virsh reboot <name>
    raise NotImplementedError

@task_or_dryrun
@runs_once
def list_ips():
    data = list_instances(show=0, verbose=0)
    for key, attrs in data.items():
        print(attrs.get('ip'), key)
