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
though the root has files inside my filesystem on which he has permisiions
(ubeer cool, right ?!?! )
i.e. any other user trying to access my mount point will see the following
permission set:
``d????????? ? ?    ?       ?            ?``
