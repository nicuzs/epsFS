EpsFS Extended Permisions Set File System
=========================================

##This are just a bunch of side notes - not a doc 


* Mounting the fs

run:
``$groups <usename>``

if you don't see fuse there, add it using:

``$sudo addgroup <username> fuse``

To remove a user from a group use:

``sudo deluser tim fuse``

restart your session ``$ cinnamon-session-exit``

* Dont forget to show off how secure the mount operation is:

not even the root user can access the filesystem mounted by my user even
though the root has files inside my filesystem on which he has permissions
(ubeer cool, right ?!?! )
i.e. any other user trying to access my mount point will see the following
permission set:
``d????????? ? ?    ?       ?            ?``

If you want other users to acces the filesystem, make sure you edit the fuse config in ``/etc`` 

* Connecting to my custom ssh server:

    ``ssh user@127.0.0.1 -p 8022 #localhost - not really cool``

    ``ssh user@192.168.1.x -p 8022 #cooler but you have to setup port fwd on the router``
I guess I should get back to finish implementing this thing


* USER MANAGEMENT - posix standard way
``sudo useradd <uname>``

``sudo passwd <uname>``


each user should consider /epsfs/home as their homedir; update that in /etc/passwd when creatin' a new user


use ``awk`` to get the available sys users and uids
``awk -F":" '{ print $1 ";" $3 }' /etc/passwd``

* if your system ever crashes, unmount the mountpoint using:
    ``fusermount -u <mount_dir>``

* i linked the bash_history file to /dev/null just to make user's history more secure
    ``ln /dev/null .bash_history -sf``

* This is a naive way used to figure out which users are connected via ssh (The best way would be to make that custom ssh server work and filter all the requests ...)

``netstat -atpn|grep ssh``

REMEMBER: the fs uses this utility so the user mounting the file_system must have the ability to run sudo commands whithout being required to enter a password  (use ``sudo visudo`` to make the user a demi-god-root user :) )
