#!/usr/bin/python

try:
    import time
    import os
    import paramiko
    import stat
    import yaml
    from paramiko.client import AutoAddPolicy
except (ModuleNotFoundError, ImportError) as module:
    quit(f'The following module needs to be installed:\n {module}\n Use "pip install $MODULE" then try again.\n')


def deltree(sftp, remotepath, level=0):
    """Recursively deletes files"""
    try:
        for f in sftp.listdir_attr(remotepath):
            rpath = os.path.join(remotepath, f.filename)
            if stat.S_ISDIR(f.st_mode):
                deltree(sftp, rpath, level=(level + 1))
            else:
                rpath = os.path.join(remotepath, f.filename)
                print(f'removing\t {rpath}')
                sftp.remove(rpath)
        print(f'removing\t {remotepath}')
        sftp.rmdir(remotepath)
    except (FileNotFoundError, OSError):
        deltree(sftp, remotepath)


def main():
    """Pull data from config.yml and make SSH connection."""

    f = open(os.path.join(__location__, 'config.yml'))
    config = yaml.load(f, Loader=yaml.BaseLoader)
    host = config['database']['hostname']
    port = config['database']['port_num']
    user = config['database']['username']
    remote_dir = config['database']['root_dir']
    p_key = config['database']['priv_key']

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(host, port, user, key_filename=p_key)
    sftp = ssh.open_sftp()

    try:
        deltree(sftp, remote_dir)
    except KeyboardInterrupt:
        """Closes SSH session when script is interrupted."""
        ssh.close()
        quit('Gracefully closed SSH session.')

    # Close to end
    ssh.close()


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quit('')
