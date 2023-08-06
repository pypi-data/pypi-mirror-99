"""
System settings
===============
"""
from fabric.api import hide, run, settings

from burlap.files import file # pylint: disable=redefined-builtin
from burlap.utils import read_lines, run_as_root
from burlap.constants import *

is_file = file.is_file

class UnsupportedFamily(Exception):
    """
    Operation not supported on this system family.

    ::

        from burlap.system import UnsupportedFamily, distrib_family

        family = distrib_family()
        if family == 'debian':
            do_some_stuff()
        elif family == 'redhat':
            do_other_stuff()
        else:
            raise UnsupportedFamily(supported=['debian', 'redhat'])

    """

    def __init__(self, supported):
        self.supported = supported
        self.distrib = distrib_id()
        self.family = distrib_family()
        msg = "Unsupported family %s (%s). Supported families: %s" % (self.family, self.distrib, ', '.join(supported))
        super().__init__(msg)


def distrib_id():
    """
    Get the OS distribution ID.

    Example::

        from burlap.system import distrib_id

        if distrib_id() != 'Debian':
            abort(u"Distribution is not supported")

    """

    with settings(hide('running', 'stdout')):
        kernel = (run('uname -s') or '').strip().lower()
        if kernel == LINUX:
            # lsb_release works on Ubuntu and Debian >= 6.0
            # but is not always included in other distros
            if is_file('/usr/bin/lsb_release'):
                id_ = run('lsb_release --id --short').strip().lower()
                if id in ['arch', 'archlinux']:  # old IDs used before lsb-release 1.4-14
                    id_ = ARCH
                return id_
            if is_file('/etc/debian_version'):
                return DEBIAN
            if is_file('/etc/fedora-release'):
                return FEDORA
            if is_file('/etc/arch-release'):
                return ARCH
            if is_file('/etc/redhat-release'):
                release = run('cat /etc/redhat-release')
                if release.startswith('Red Hat Enterprise Linux'):
                    return REDHAT
                if release.startswith('CentOS'):
                    return CENTOS
                if release.startswith('Scientific Linux'):
                    return SLES
            if is_file('/etc/gentoo-release'):
                return GENTOO
        elif kernel == SUNOS:
            return SUNOS


def distrib_release():
    """
    Get the release number of the distribution.

    Example::

        from burlap.system import distrib_id, distrib_release

        if distrib_id() == 'CentOS' and distrib_release() == '6.1':
            print(u"CentOS 6.2 has been released. Please upgrade.")

    """
    with settings(hide('running', 'stdout')):
        kernel = (run('uname -s') or '').strip().lower()
        if kernel == LINUX:
            return run('lsb_release -r --short')
        if kernel == SUNOS:
            return run('uname -v')


def distrib_codename():
    """
    Get the codename of the Linux distribution.

    Example::

        from burlap.deb import distrib_codename

        if distrib_codename() == 'precise':
            print(u"Ubuntu 12.04 LTS detected")

    """
    with settings(hide('running', 'stdout')):
        return run('lsb_release --codename --short')


def distrib_desc():
    """
    Get the description of the Linux distribution.

    For example: ``Debian GNU/Linux 6.0.7 (squeeze)``.
    """
    with settings(hide('running', 'stdout')):
        if not is_file('/etc/redhat-release'):
            return run('lsb_release --desc --short')
        return run('cat /etc/redhat-release')


def distrib_family():
    """
    Get the distribution family.

    Returns one of ``debian``, ``redhat``, ``arch``, ``gentoo``,
    ``sun``, ``other``.
    """
    distrib = (distrib_id() or '').lower()
    if distrib in ['debian', 'ubuntu', 'linuxmint', 'elementary os']:
        return DEBIAN
    if distrib in ['redhat', 'rhel', 'centos', 'sles', 'fedora']:
        return REDHAT
    if distrib in ['sunos']:
        return SUN
    if distrib in ['gentoo']:
        return GENTOO
    if distrib in ['arch', 'manjarolinux']:
        return ARCH
    return 'other'


def get_hostname():
    """
    Get the fully qualified hostname.
    """
    with settings(hide('running', 'stdout')):
        return run('hostname --fqdn')


def set_hostname(hostname, persist=True):
    """
    Set the hostname.
    """
    run_as_root('hostname %s' % hostname)
    if persist:
        run_as_root('echo %s >/etc/hostname' % hostname)


def get_sysctl(key):
    """
    Get a kernel parameter.

    Example::

        from burlap.system import get_sysctl

        print("Max number of open files:", get_sysctl('fs.file-max')

    """
    with settings(hide('running', 'stdout')):
        return run_as_root('/sbin/sysctl -n -e %(key)s' % locals())


def set_sysctl(key, value):
    """
    Set a kernel parameter.

    Example::

        import burlap

        # Protect from SYN flooding attack
        burlap.system.set_sysctl('net.ipv4.tcp_syncookies', 1)

    """
    run_as_root('/sbin/sysctl -n -e -w %(key)s=%(value)s' % locals())


def supported_locales():
    """
    Gets the list of supported locales.

    Each locale is returned as a ``(locale, charset)`` tuple.
    """
    family = distrib_family()
    if family == 'debian':
        return _parse_locales('/usr/share/i18n/SUPPORTED')
    if family == 'arch':
        return _parse_locales('/etc/locale.gen')
    if family == 'redhat':
        return _supported_locales_redhat()
    raise UnsupportedFamily(supported=['debian', 'arch', 'redhat'])


def _parse_locales(path):
    lines = read_lines(path)
    return list(_split_on_spaces(_strip(_remove_comments(lines))))


def _split_on_spaces(lines):
    return (line.split(' ') for line in lines)


def _strip(lines):
    return (line.strip() for line in lines)


def _remove_comments(lines):
    return (line for line in lines if not line.startswith('#'))


def _supported_locales_redhat():
    res = run('/usr/bin/locale -a')
    return [(locale, None) for locale in res.splitlines()]


def get_arch():
    """
    Get the CPU architecture.

    Example::

        from burlap.system import get_arch

        if get_arch() == 'x86_64':
            print(u"Running on a 64-bit Intel/AMD system")

    """
    with settings(hide('running', 'stdout')):
        arch = run('uname -m')
        return arch


def cpus():
    """
    Get the number of CPU cores.

    Example::

        from burlap.system import cpus

        nb_workers = 2 * cpus() + 1

    """
    with settings(hide('running', 'stdout')):
        res = run('python -c "import multiprocessing; '
                  'print(multiprocessing.cpu_count())"')
        return int(res)


def using_systemd():
    """
    Return True if using systemd

    Example::

        from burlap.system import use_systemd

        if using_systemd():
            # do stuff with burlap.systemd ...
            pass

    """
    return run('which systemctl', quiet=True).succeeded


def time():
    """
    Return the current time in seconds since the Epoch.

    Same as :py:func:`time.time()`

    """

    with settings(hide('running', 'stdout')):
        return int(run('date +%s'))
