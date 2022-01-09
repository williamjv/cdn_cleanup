## Server IP Audit

This script will go through Akamai netstorage and erase all files so that the netstorage property can be removed. The script utilizes SFTP to accomplish this.

The problem I intended to solve is by having a client that will continually erase files until they are gone and reconnect if necessary.  It has been my experience a normal client will randomly disconnect due to various reasons and at some point I will have to restart the process again.

---
### Configuration:

* config.yml 

Change the information that best fit each individual needs.  The `root_dir` do not include any slashes.

```
database:
  username: sshacs
  port_num: 22
  hostname: HOST.ssh.upload.akamai.com
  root_dir: 123456
  priv_key: /home/NAME/.ssh/id_rsa
```

---

### Example of use:

As always I encourage using python virtual environment.  Here is some good documentation if you are not familiar.

* https://realpython.com/python-virtual-environments-a-primer/

Once config.yml is updated then run the below command.

```
python3 storage.py
```

* It will first gather a list of files.
* Then it will begin erasing those files and outputting what it is deleting.
