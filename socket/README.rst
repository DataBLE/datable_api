.. 

Socket service
======================

Client
----------
Run :code:`twistd -noy client.py` on the mote so that it will connect to the cloud
and start receiving commands.  Make sure that the :code:`HOST` is set to the 
appropriate server, either :code:`localhost` or a valid, publicly accessible IP
or hostname.  Make sure to run this within an X session so that the video
player works correctly.


Server
-------
Run :code:`twistd -noy server.py` on the cloud server that the motes will be connecting
to.


Testing on localhost
----------------------
To test both services on :code:`localhost`, make sure to add :code:`--pidfile=client.pid`
and :code:`--pidfile=server.pid` to the client and server services :code:`twistd` command
argument so that they pid files don't clash.


Daemonize
-----------
Running :code:`twistd` without the :code:`-no` argument will daemonize the processes.
