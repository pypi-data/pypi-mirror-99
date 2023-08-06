|
|
|
|
|
|

Upgrading PyPlanet
==================

Upgrading an existing installation isn't difficult at all. The only thing you really need to be careful about is the
breaking changes.

Before upgrading, please check your existing version, and check the :doc:`Change Log Document </changelog>`.

Since 0.6.0 you have two methods of upgrading. The in-game method and the manual PIP method.
**We strongly advice you to use the manual PIP method because the in-game upgrade can be unstable with big releases!**

.. note::

  We assume you installed PyPlanet with PyPi and initiated your project folder with ``init_project``.
  If you installed directly from Git, this document may not be suited for you.

.. warning::

  When using the executable method (downloaded from the GitHub releases page) you will have to redownload and replace the
  binary file instead of these steps! (Executable currently not released anymore).


In-game upgrade method
~~~~~~~~~~~~~~~~~~~~~~

To use this method your current version needs to be 0.6.0 or higher. You can use the following command to execute the upgrade.
You can also select a specific version (for example beta or rc) with the command.

.. code-block:: text

  //upgrade
  -- or --
  //upgrade 0.6.0-rc1

PyPlanet will reboot when the installation is complete. You might want to edit the apps.py to activate the new apps.
On the :doc:`configuration page </intro/configuration>` you can always find the latest apps entries.

.. warning::

  This method can be unstable. It's hard to fully adjust to your installation method and environment.
  We recommend making a backup of your installation, or have the knowledge of restoring or recreating
  the virtualenv or installation!


Manual PIP method
~~~~~~~~~~~~~~~~~

1. Check requirements.txt
`````````````````````````

In your project root you will find a file called ``requirements.txt``. This file is the input of the ``pip`` manager in the
next commands. So it needs to be well maintained.

By default you will see something like this:

.. code-block:: text

  pyplanet>=0.0.1,<1.0.0

This will tell ``pip`` to install a PyPlanet version above 0.0.1, but under 1.0.0. This way you will prevent sudden breaking
changes that may occur in big new releases, or breaking changes that were introduced to a major Maniaplanet update.

If you want to upgrade to a newer major version, for example 1.2.0 to 2.0.0. you have to change these numbers here. If not, continue
to the next step

2. Activate env
```````````````

If you use ``virtualenv`` or ``pyenv`` it's now time to activate your virtual environment. Do so with the commands.

.. code-block:: bash

  # Linux
  source env/bin/activate

  # PyEnv
  pyenv activate pyplanet

  # Windows
  env\Scripts\Activate.bat

3. Upgrade PyPlanet core
````````````````````````

Now you can run the ``pip`` command that will upgrade your installation.

.. code-block:: bash

  pip install -r requirements.txt --upgrade

.. warning::

  You may find errors during installation, make sure you have ``openssl, gcc, python development`` installed on your os!
  See the installation manual on how to install this.


4. Upgrade settings
```````````````````

See the changelog for new or updated settings and apply the changes now.


5. Upgrade apps setting
```````````````````````

It can be possible that we introduced new apps in the update. You will find this in the changelog, and all newest apps
will always be provided in the documentation.

On the :doc:`configuration page </intro/configuration>` you will always find the latest apps settings entries.


6. Start PyPlanet
`````````````````

At the next start it will apply any database migrations automatically.
