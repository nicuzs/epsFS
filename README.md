FUSE fun
========
##Kid of docs


* Mounting the fs

run:
``$groups <usename>``

if you don't see fuse there, add it using:

``$sudo addgroup <username> fuse``

restart your session ``$ cinnamon-session-exit``

* Dont forget to show off how secure the mount operation is:

not even the root user can access the filesystem mounted by my user even
though the root has files inside my filesystem on which he has permissions
(ubeer cool, right ?!?! )
i.e. any other user trying to access my mount point will see the following
permission set:
``d????????? ? ?    ?       ?            ?``



* Connecting to my custom ssh server:
    ``ssh user@127.0.0.1 -p 8022 #localhost - not really cool``
    ``ssh user@192.168.1.x -p 8022 #cooler but you have to setup port fwd on the router``

* When generatin' ssh keys use ``-b 1024`` argument
