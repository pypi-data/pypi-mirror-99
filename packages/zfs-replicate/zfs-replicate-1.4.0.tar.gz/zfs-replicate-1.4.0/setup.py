# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zfs',
 'zfs.replicate',
 'zfs.replicate.cli',
 'zfs.replicate.compress',
 'zfs.replicate.filesystem',
 'zfs.replicate.snapshot',
 'zfs.replicate.ssh',
 'zfs.replicate.task']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'stringcase>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['zfs-replicate = zfs.replicate.cli.main:main']}

setup_kwargs = {
    'name': 'zfs-replicate',
    'version': '1.4.0',
    'description': 'ZFS Snapshot Replicator',
    'long_description': "Description\n-----------\n\nZFS_ Replicate Utility\n\nA small command line utility to handle remote replication of ZFS_ snapshots\nusing SSH_.\n\nThis project is directly based on the autorepl.py_ script used by FreeNAS_.\n\nI am providing code in the repository to you under an open source license.\nBecause this is my personal repository, the license you receive to my code is\nfrom me and not my employer (Facebook).\n\nGetting Started\n---------------\n\nUsage is pretty straight-forward and documented in the command's help output.\nFor more information on ZFS_ snapshots, see:\n`Working With Oracle Solaris ZFS Snapshots and Clones`_\n\nRemote Configuration\n--------------------\n\nIf you're replicating using the root user's credentials, you should really\nreconsider, but this script should just work.\n\nOtherwise, you'll not only need to ensure the user you're using has SSH_ access\nto the remote host, but also can mount filesystems (if this is desirable) and\nhas ZFS_ permissions configured correctly.\n\nAllow user to mount (FreeBSD_)::\n\n    sysctl -w vfs.usermount=1\n\nZFS_ Permissions::\n\n    zfs allow ${USER} create,destroy,snapshot,rollback,clone,promote,rename,mount,send,receive,readonly,quota,reservation,hold ${BACKUP_DATASET}\n\nMore information about this configuration can be found at the following\nsources:\n\n* `ZFS REMOTE REPLICATION SCRIPT WITH REPORTING`_\n* `ZFS replication without using Root user`_\n\nCompared to Other Tools\n-----------------------\n\nThis tool is only for replication of snapshots.  It assumes that another system\nis creating them on a regular basis.  It also doesn't require installation of\nany special tools (other than the standard shell scripts) on the remote host.\n\nOther tools fill other niches:\n\n`sanoid`_\n  A full snapshot management system.  Its companion application, syncoid,\n  handles replication with many available options.\n\n`zfs-replicate (BASH)`_\n  A very similar project.  The major differences are configuration style (our\n  project uses parameters whereas this project uses a BASH script), and the\n  system expectations (e.g., logging controls).\n\n`znapzend`_\n  Another scheduling and replicating system.\n\n`zrep`_\n  A SH script with several control commands for snapshot replication.\n\nMore information has been captured in `this survey`_.\n\nReporting Issues\n----------------\n\nAny issues discovered should be recorded on Github_.  If you believe you've\nfound an error or have a suggestion for a new feature, please ensure that it is\nreported.\n\nIf you would like to contribute a fix or new feature, please submit a pull\nrequest.  This project follows `git flow`_ and utilizes travis_ to\nautomatically check pull requests before a manual review.\n\n.. _autorepl.py: https://github.com/freenas/freenas/blob/master/gui/tools/autorepl.py\n.. _FreeBSD: https://www.freebsd.org/\n.. _FreeNAS: http://www.freenas.org/\n.. _git flow: http://nvie.com/posts/a-successful-git-branching-model/\n.. _Github: https://github.com/alunduil/zfs-replicate\n.. _sanoid: https://github.com/jimsalterjrs/sanoid\n.. _SSH: https://www.openssh.com/\n.. _this survey: https://www.reddit.com/r/zfs/comments/7fqu1y/a_small_survey_of_zfs_remote_replication_tools://www.reddit.com/r/zfs/comments/7fqu1y/a_small_survey_of_zfs_remote_replication_tools/\n.. _travis: https://travis-ci.org/aunduil/zfs-replicate\n.. _Working With Oracle Solaris ZFS Snapshots and Clones: https://docs.oracle.com/cd/E26505_01/html/E37384/gavvx.html#scrolltoc\n.. _ZFS: http://open-zfs.org/wiki/System_Administration\n.. _ZFS REMOTE REPLICATION SCRIPT WITH REPORTING: https://techblog.jeppson.org/2014/10/zfs-remote-replication-script-with-reporting/\n.. _zfs-replicate (BASH): https://github.com/leprechau/zfs-replicate\n.. _ZFS replication without using Root user: https://forums.freenas.org/index.php?threads/zfs-replication-without-using-root-user.21731/\n.. _znapzend: http://www.znapzend.org/\n.. _zrep: http://www.bolthole.com/solaris/zrep/\n",
    'author': 'Alex Brandt',
    'author_email': 'alunduil@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alunduil/zfs-replicate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
