import pkg_resources
from satella.files import write_to_file, read_in_file
from .parse_config import parse_etc_socatlord
import subprocess
import os
import argparse
import sys


verbose = False


def kill_all_socats():
    global verbose
    for socat in os.listdir('/var/run/socatlord'):
        path = os.path.join('/var/run/socatlord', socat)
        pid = int(read_in_file(path, 'utf-8'))
        try:
            if verbose:
                print('Killing %s' % (pid, ))
            os.kill(pid, 9)
            if verbose:
                print('Killed %s OK' % (pid, ))
        except PermissionError:
            print('Failed to kill %s with EPERM' % (pid, ))
        except OSError:
            print('Failed to kill %s' % (pid, ))
        os.unlink(path)


def run():
    global verbose
    parser = argparse.ArgumentParser(prog='socatlord', usage='''Call with a single argument
    *install* will install and enable socatlord to work as a systemd service (socatlord.service)
    *run* will shut down all socats that it previously spawned (free-range socats won't be touched) and restart them
    *stop* will terminate socats''')
    parser.add_argument('-v', action='store_true', help='Display what commands are ran and pipe socats to stdout')
    parser.add_argument('--config', default='/etc/socatlord', help='Location of config file (default is /etc/socatlord)')
    parser.add_argument('operation', choices=['install', 'run', 'stop'], help='Operation to do')

    args = parser.parse_args()

    verbose = args.v

    if not os.path.exists(args.config):
        write_to_file(args.config, b'''# Put your redirections here
# eg. 
# 443 -> 192.168.1.1:443
# will redirect all TCP traffic that comes to this host (0.0.0.0) to specified host and port
# to redirect UDP traffic just prefix your config with udp, eg.
# udp 443 -> 192.168.1.1:443
# You can additionally specify explicit interfaces to listen on eg.
# 192.168.1.2:443 -> 192.168.1.1:443
''')
        if verbose:
            print('%s created' % (args.config, ))

    if len(sys.argv) > 1:
        if args.operation == 'install':
            filename = pkg_resources.resource_filename(__name__, 'systemd/socatlord.service')
            contents = read_in_file(filename, 'utf-8')
            write_to_file('/lib/systemd/system/socatlord.service', contents, 'utf-8')
            os.system('systemctl daemon-reload')
            os.system('systemctl enable socatlord.service')
        elif args.operation == 'stop':
            kill_all_socats()
        elif args.operation == 'run':

            if not os.path.exists('/var/run/socatlord'):
                os.mkdir('/var/run/socatlord')
            os.chmod(0o600, '/var/run/socatlord')

            kill_all_socats()

            for i, row in enumerate(parse_etc_socatlord(args.config)):
                proto, host1, port1, host2, port2 = row
                command = ['socat', '%s-listen:%s,bind=%s,reuseaddr,fork' % (proto, port1, host1),
                           '%s:%s:%s' % (proto, host2, port2)]
                kwargs = {'stdin': subprocess.DEVNULL, 'stdout': subprocess.DEVNULL,
                        'stderr': subprocess.DEVNULL}
                if verbose:
                    print('Calling %s' % (command, ))
                    kwargs = {}
                proc = subprocess.Popen(command, **kwargs)
                write_to_file(os.path.join('/var/run/socatlord', str(i)), str(proc.pid), 'utf-8')


if __name__ == '__main__':
    run()
