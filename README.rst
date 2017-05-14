.. image:: https://img.shields.io/pypi/v/pytestautomation.svg
   :target: https://pypi.python.org/pypi/pytestautomation/

.. image:: https://img.shields.io/pypi/dm/pytestautomation.svg
   :target: https://pypi.python.org/pypi/pytestautomation/

.. image:: https://travis-ci.org/crazy-canux/pytestautomation.svg?branch=master
   :target: https://travis-ci.org/crazy-canux/pytestautomation

.. image:: https://coveralls.io/repos/github/crazy-canux/pytestautomation/badge.svg?branch=master
   :target: https://coveralls.io/github/crazy-canux/pytestautomation?branch=master


===================
pytestautomation
===================

pytestautomation is pure python code.

It's a API packge for monitoring plugins, like Nagios, Icinga, Naemon, Shinken, Centreon, Opsview and Sensu.

`[awesome-monitoring] <https://github.com/crazy-canux/awesome-monitoring>`_.

--------------
How to install
--------------

Use pip to install::

    pip install pytestautomation

----------
How to use
----------

Just import what protocol you need::

    from pytestautomation.ftp_ftplib import Ftp
    from pytestautomation.http_requests import Http
    from pytestautomation.mssql_pymssql import Mssql
    from pytestautomation.mysql_pymysql import Mysql
    from pytestautomation.ssh_paramiko import Ssh
    from pytestautomation.winrm_pywinrm import WinRM
    from pytestautomation.wmi_sh import Wmi
    from pytestautomation.wmi_subprocess import Wmi

Then write your own function monitoring class::

    class YourClass(Ftp/Mssql/Ssh/WinRM/Wmi/Http/Snmp/...):
        def __init__(self):
            super(YourClass, self).__init__()
            self.logger.debug("Init YourClass.")

        def define_sub_options(self):
            super(YourClass, self).define_sub_options()
            self.your_parser = self.subparsers.add_parser(...)
            self.your_parser.add_argument(...)
            ...

        def your_handle(self):
            """Put your function monitoring code here."""
            # Default status is ok.
            status = self.ok

            # Call the API and get the monitoring data.
            # Read the document or check the API on python/ipython Interactive console.
            # help(Ftp/...)
            # dir(Ftp/...)
            ...

            #  Compare with the warning and critical value and change the status.
            ...

            self.shortoutput = "..."
            self.longoutput.append(...)
            self.perfdata.append(...)

            self.logger.debug("Return status and output.")
            status(self.output())

If you put more than one function monitoring class in one file(Not recommend)::

    class Register(YourClass1, YourClass2, ...):
        def __init__(self):
            super(Register, self).__init__()

Last step::

    def main():
        # For multiple inherit
        # plugin = Register()
        plugin = YourClass()
        arguments = sys.argv[1:]
        if 'your' in arguments:
            plugin.your_handle()
        elif 'your2' in arguments:
            plugin.your2_handle()
        else:
            plugin.unknown("Unknown actions.")

    if __name__ == "__main__":
        main()

--------------
How to extends
--------------

Check the TODO list, you can give test examples or documents.

Also you can pull request for your code.

-----
TODO
-----

* Distribute 1.3.0 to pypi.
* Write unit test in tests/
* Compatible with Python3(2.0.0)
* vSphere monitoring(1.6.0)
* LDAP monitoring(1.5.0)
* SNMP monitoring(1.4.0)

=============
Documentation
=============

`[Documentation] <http://pytestautomation.readthedocs.io/en/latest/>`_

============
Contribution
============

`[Contribution] <https://github.com/crazy-canux/pytestautomation/blob/master/CONTRIBUTING.rst>`_

=======
Authors
=======

`[Authors] <https://github.com/crazy-canux/pytestautomation/blob/master/AUTHORS.rst>`_

=======
License
=======

`[License] <https://github.com/crazy-canux/pytestautomation/blob/master/LICENSE>`_
