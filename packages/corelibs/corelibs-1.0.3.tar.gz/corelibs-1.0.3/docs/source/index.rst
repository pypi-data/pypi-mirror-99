.. corelibs documentation master file, created by
   sphinx-quickstart on Mon Sep 28 20:26:34 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Package **corelibs**
====================
.. note:: Bienvenue dans la documentation de :magenta:`corelibs`.

    L'objectif de corelibs est d'agréger dans différents modules, toutes les fonctionnalités utiles pour
    simplifier nos travaux sans devoir tout réécrire à chaque fois...

.. toctree::
   :maxdepth: 3
   :numbered:
   :caption: Contents:

.. _reference-label-config:

Installation & Mise à jour
==========================
.. note::

   | :magenta:`corelibs` est orienté Anaconda, sur les autres environnements, :magenta:`corelibs` reste fonctionnel, sauf toutes les spécificités propre à l'environnement Anaconda qui resteront sans réponse.

.. warning::

   | :magenta:`corelibs` gère toutes les dépendances lors de la phase installation/mise à jour.

   | Malgré tout, certains packages peuvent ne plus être accessibles (changement de dépôt/adresse...) il faudrait alors faire l'installation manuellement, comme c'est le cas pour le package :magenta:`mkl-service` (au moment de la rédaction de ce présent document)

.. topic:: Description générale **Installation**

   Étapes pour installer le package :magenta:`corelibs`:

   #. lancer le terminal Anaconda ayant pour titre :green:`Anaconda Prompt (Anaconda3)`

      .. code-block:: bash

         (base) C:\Users\kim>

   #. dans :green:`Anaconda Prompt (Anaconda3)` :

      #. si besoin, lister les environnements existant

         .. code-block:: bash

            (base) C:\Users\kim>conda env list

      #. activer l'environnement sur lequel est souhaité l'installation du package :magenta:`corelibs`

         .. code-block:: bash

            (base) C:\Users\kim>conda activate nom_environnement

      #. installer le package :magenta:`mkl-service` récalcitrant, via le dépôt conda, canal conda-forge.

         .. code-block:: bash

            (nom_environnement) C:\Users\kim>conda install -c conda-forge mkl-service

      #. installer le package :magenta:`corelibs`

         .. code-block:: bash

            (nom_environnement) C:\Users\kim>pip install corelibs

.. topic:: Description générale **Mise à jour**

   Étapes pour mettre à jour le package :magenta:`corelibs`:

   #. lancer le terminal Anaconda et dans :green:`Anaconda Prompt (Anaconda3)`

   #. activer l'environnement sur lequel est installé le package :magenta:`corelibs`

      .. code-block:: bash

         (base) C:\Users\kim>conda activate nom_environnement

   #. mettre à jour :magenta:`corelibs`

      .. code-block:: bash

         (nom_environnement) C:\Users\kim>pip install corelibs -U


Interface Utilisateur
=====================

.. topic:: Description générale

   :magenta:`corelibs` a une interface utilisateur pour accéder plus rapidement à la documentation et certaines fonctionnalités, pour cela :

   #. lancer le terminal Anaconda et dans :green:`Anaconda Prompt (Anaconda3)`

   #. activer l'environnement sur lequel est installé le package :magenta:`corelibs`

      .. code-block:: bash

         (base) C:\Users\kim>conda activate nom_environnement

   #. lancer l'interface :magenta:`corelibs` avec la commande

      .. code-block:: bash

         (nom_environnement) C:\Users\kim>corelibs

   qui affichera l'interface suivante

   .. image:: ..\\ss\\corelibs_gui.png


Configurations
==============
.. topic:: Description générale

    Ci-dessous sont listés l'ensemble des constantes définies et utilisées dans le package :magenta:`corelibs`.

    Ces constantes peuvent être utilisées telles que définies ou écrasées à discrétion :
        * soit de manière globale, via le fichier **user_config.py**
        * soit localement, dans les programmes python appelants.

    L'ordre de recherche d'une constante est donc :
        #. **localement**
        #. **user_config.py**
        #. **config.py** (le fichier de configuration de :magenta:`corelibs`)

    Dans le cas d'une constante simple, par exemple ``DEFAULT_LOGS_EXTENSION = ".log"``, corelibs utilisera la
    version écrasée telle que redéfinie.

    Dans le cas d'une constante plus complexe, de type dictionnaire, par exemple

    | ``DEFAULT_FIELD_STYLES = {``
    | ``"asctime": {"color": 242, "bright": True},``
    | ``"hostname": {"color": "magenta"},``
    | ``"username": {"color": "yellow"},``
    | ``"levelname": {"color": 242, "bright": True},``
    | ``"name": {"color": "blue"},``
    | ``"programname": {"color": "cyan"}``
    | ``}``

    corelibs ne remplacera que les clés/valeurs redéfinies (i.e. les autres clés/valeurs seront gardées inchangées)

    .. literalinclude:: ..\\..\\tests\\global_user_config.py
        :language: python

    .. note::

        | Le fichier **user_config.py** se trouve à l'emplacement :red:`%HOMEPATH%/.corelibs` (pour les utilisateurs Windows)
            et :red:`~/.corelibs` (pour les utilisateurs Linux/Unix) - cf. :func:`corelibs.lazy.open_explorer()`

        | Ce fichier est automatiquement inclut à l'exécution, ainsi que son dossier parent. De ce fait, il est donc
            possible d'y définir des constantes utilisateurs et/ou d'ajouter dans le répertoire parent des programmes
            python devant être inclus et exécuté globalement.

        | La configuration fonctionne également sur **Jupyter**

        .. image:: ..\\ss\\jupyter_user_config.png

    .. warning::

        | Les écrasements sont contrôlés par des schémas de validation. Si le fichier est corrompu, il est possible de supprimer le fichier **user_config.py**.
            :magenta:`corelibs` le regénèrera automatiquement.

        | Pour plus de détails sur les valeurs possibles, suivre la documentation officielle des packages tiers (cf. :ref:`reference-label-liens-utiles` et :ref:`reference-label-dependances`).

.. literalinclude:: ..\\..\\corelibs\\.corelibs\\user_config.py
    :language: python

Module **log**
==============
.. automodule:: corelibs.log
   :members:

Module **lazy**
===============
.. automodule:: corelibs.lazy
   :members:

Module **cleanse**
==================
.. automodule:: corelibs.cleanse
   :members:

Module **data**
===============
.. automodule:: corelibs.data
   :members:

Module **tools**
================
.. automodule:: corelibs.tools
   :members:
.. autoclass:: corelibs.tools.Archive
   :members:

.. _reference-label-dependances:

Dépendances
===========
.. topic:: Description générale

   Les dépendances sont installées automatiquement lors de l'installation/MAJ du package :magenta:`corelibs`.

   Dans le cas d'une création manuelle d'un nouvel environnement virtuel, selon le contexte de création, il est
   peut-être nécessaire de réinstaller manuellement les dépendances ci-dessous dans le-dit nouvel environnement.

.. note::

   Pour mémoire, l'installation d'un package se fait avec cette commande

   .. code-block:: bash

      $ pip install nom_package

   Et la mise à jour d'un package se fait avec cette commande

   .. code-block:: bash

      $ pip install nom_package -U


* |coloredlogs_url|
* |colorama_url|
* |schema_url|
* |ipython_url|
* |blessed_url|
* |enlighten_url|
* |click_url|
* |numpy_url|
* |numba_url|
* |PyYAML_url|
* |yamale_url|
* |stackprinter_url|
* |PySimpleGUI_url|
* |PyScaffold_url|
* |pandas_url|
* |dtale_url|

.. |coloredlogs_url| raw:: html

   <a href="https://coloredlogs.readthedocs.io/en/latest/" target="_blank">coloredlogs</a>
   <span class="magenta">>=14.0</span>

.. |colorama_url| raw:: html

   <a href="https://pypi.org/project/colorama/" target="_blank">colorama</a>
   <span class="magenta">>=0.4.3</span>

.. |schema_url| raw:: html

   <a href="https://pypi.org/project/schema/" target="_blank">schema</a>
   <span class="magenta">>=0.7.2</span>

.. |ipython_url| raw:: html

   <a href="https://pypi.org/project/ipython/" target="_blank">ipython</a>
   <span class="magenta">>=7.19.0</span>

.. |blessed_url| raw:: html

   <a href="https://pypi.org/project/blessed/" target="_blank">blessed</a>
   <span class="magenta">>=1.17.11</span> (>1.17.6 non compatible avec inquirer==2.7.0)

.. |enlighten_url| raw:: html

   <a href="https://pypi.org/project/enlighten/" target="_blank">enlighten</a>
   <span class="magenta">>=1.6.2</span>

.. |click_url| raw:: html

   <a href="https://pypi.org/project/click/" target="_blank">click</a>
   <span class="magenta">>=7.1.2</span>

.. |numpy_url| raw:: html

   <a href="https://pypi.org/project/numpy/" target="_blank">numpy</a>
   <span class="magenta">==1.19.3</span> (>=1.19.4 => numba crash!)

.. |numba_url| raw:: html

   <a href="https://pypi.org/project/numba/" target="_blank">numba</a>
   <span class="magenta">==0.51.2</span> (>0.51.2 non compatible avec numpy>1.19.3)

.. |prompt-toolkit_url| raw:: html

   <a href="https://pypi.org/project/prompt-toolkit/" target="_blank">prompt-toolkit</a>
   <span class="magenta">>=3.0.8</span>

.. |PyYAML_url| raw:: html

   <a href="https://pypi.org/project/PyYAML/" target="_blank">PyYAML</a>
   <span class="magenta">>=5.3.1</span>

.. |yamale_url| raw:: html

   <a href="https://pypi.org/project/yamale/" target="_blank">yamale</a>
   <span class="magenta">>=3.0.4</span>

.. |stackprinter_url| raw:: html

   <a href="https://pypi.org/project/stackprinter/" target="_blank">stackprinter</a>
   <span class="magenta">>=0.2.5</span>

.. |PySimpleGUI_url| raw:: html

   <a href="https://pypi.org/project/PySimpleGUI/" target="_blank">PySimpleGUI</a>
   <span class="magenta">>=4.33.0</span>

.. |PyScaffold_url| raw:: html

   <a href="https://pypi.org/project/PyScaffold/" target="_blank">PyScaffold</a>
   <span class="magenta">>=3.3</span>

.. |pandas_url| raw:: html

   <a href="https://pypi.org/project/pandas/" target="_blank">pandas</a>
   <span class="magenta">>=1.2.0</span>

.. |dtale_url| raw:: html

   <a href="https://pypi.org/project/dtale/" target="_blank">dtale</a>
   <span class="magenta">>=1.30.0</span>

.. |punnycode_url| raw:: html

   <a href="https://www.rfc-editor.org/rfc/rfc3492.txt" target="_blank">Punnycode</a>

.. _reference-label-liens-utiles:

Liens utiles
============
.. topic:: Description générale

   Tous les liens utiles sont listés ici, à jeter un oeil (voire même les 2 =þ)

* :magenta:`Python 3.*` :
   * |python_3_time_format_code_url|
   * |python_3_log_lvl_url|
   * |python_3_log_record_attributes_url|
   * |python_3_lib_regex_url|
* :magenta:`Normes/Spec/Documentations` :
   * |terminal_color_escape_url|
   * |sevenzip_commands_spec_url|
   * |unicode_category_url|
   * |unicode_table_url|
   * |PyScaffold_doc_url|
   * |Sphinx_doc_url|
   * |pandas_doc_url|

.. |python_3_time_format_code_url| raw:: html

   <a href="https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes" target="_blank">Liste des codes pour le formatage des timestamps</a>

.. |python_3_log_lvl_url| raw:: html

   <a href="https://docs.python.org/3/library/logging.html?highlight=logging%20format#logging-levels" target="_blank">Définitions niveaux d'alertes</a>

.. |python_3_log_record_attributes_url| raw:: html

   <a href="https://docs.python.org/3/library/logging.html?highlight=logging%20format#logrecord-attributes" target="_blank">Définitions des attributs <b>LogRecord</b></a>

.. |python_3_lib_regex_url| raw:: html

   <a href="https://docs.python.org/3/library/re.html" target="_blank">Librairie regex</a>

.. |terminal_color_escape_url| raw:: html

   <a href="https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html" target="_blank">Définition des caractères d'échappement ANSI pour les sorties Terminal</a>

.. |sevenzip_commands_spec_url| raw:: html

   <a href="https://sevenzip.osdn.jp/chm/cmdline/switches/method.htm" target="_blank">Documentation commandes 7zip</a>

.. |unicode_category_url| raw:: html

   <a href="http://www.unicode.org/reports/tr44/#General_Category_Values" target="_blank">Classification des caractères Unicodes</a>

.. |unicode_table_url| raw:: html

   <a href="https://www.compart.com/en/unicode/" target="_blank">Jeux de caractères Unicodes</a>

.. |PyScaffold_doc_url| raw:: html

   <a href="https://readthedocs.org/projects/pyscaffold/downloads/pdf/latest/" target="_blank">Documentation PyScaffold</a>

.. |Sphinx_doc_url| raw:: html

   <a href="https://www.sphinx-doc.org/_/downloads/en/master/pdf/" target="_blank">Documentation Sphinx</a>

.. |character_encoding_url| raw:: html

   <a href="https://en.wikipedia.org/wiki/Character_encoding#:~:text=Simple%20character%20encoding%20schemes%20include,number%20of%20bytes%20used%20per" target="_blank">Character encoding</a>

.. |pandas_doc_url| raw:: html

   <a href="https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html" target="_blank">Documentation Pandas</a>

Index & Tables des matières
===========================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
