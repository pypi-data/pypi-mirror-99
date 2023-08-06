===========
Maestro CLI
===========

Launch Maestro JobRequest with ease.


Exemple :

::

   >>> from maestro_cli import Maestro
   >>>
   >>> maestro = Maestro()
   >>> maestro.launch_jobrequest(82, {'A': 1, 'B': 3, 'C': 2})
   <JobRequest #1877>

::

   >>> maestro = Maestro('http://localhost:8003', '9354a3fe-e1ec-499d-9402-bbef0d700487', 'BeHive')
   >>> request = maestro.get_jobrequest(414)
   >>> request.progress
   45.0
   >>> request.status_label
   En cours
   >>> request.cancel()
   >>> 200
