===========================
Documenten API CMIS adapter
===========================

:Version: 1.2.3
:Source: https://github.com/open-zaak/cmis-adapter
:Keywords: CMIS, Documenten API, VNG, Common Ground
:PythonVersion: 3.7

|build-status| |coverage| |linting| |black| |python-versions| |django-versions| |pypi-version|

A CMIS backend-connector for the `Documenten API`_.

Developed by `Maykin Media B.V.`_ commissioned by the municipality of Utrecht
with support of the municipality of Súdwest-Fryslân and the Open Zaak project
team.


Introduction
============

The Documenten API CMIS adapter allows Django implementations of the Documenten
API to easily connect to a CMIS-compatible Document Management System (DMS).
Most notably it's used by `Open Zaak`_ to use a DMS as backend for the
Documenten API rather then using its own backend.

.. _`Open Zaak`: https://github.com/open-zaak/open-zaak/

Features
--------

Both `CMIS 1.0`_ and `CMIS 1.1`_ are supported but not for all bindings. Below
is a list of supported bindings for each CMIS version.

.. _`CMIS 1.0`: https://docs.oasis-open.org/cmis/CMIS/v1.0/cmis-spec-v1.0.html
.. _`CMIS 1.1`: https://docs.oasis-open.org/cmis/CMIS/v1.1/CMIS-v1.1.html

+----------------------+-----------+-----------+
|                      |  CMIS 1.0 |  CMIS 1.1 |
+======================+===========+===========+
| Web Services binding | Supported |  Untested |
+----------------------+-----------+-----------+
| AtomPub binding      |  Untested |  Untested |
+----------------------+-----------+-----------+
| Browser binding      |    N/A    | Supported |
+----------------------+-----------+-----------+

For the supported bindings, the following features are implemented:

* Retrieve from and store documents in a CMIS-compatible DMS.
* Supports reading and writing of documents.
* Supports checking out/in of documents.
* Supports custom data-model for storing additional meta data.

Tested against:

* `Corsa platform`_ using CMIS 1.0 Web Services binding (Thanks to `BCT`_)
* `Alfresco`_ Enterprise 5.2.3 using CMIS 1.1 Browser binding (Thanks to
  `Contezza`_)
* `Alfresco CE 6.1.2-ga`_ (Used for CI)

.. _`Corsa platform`: https://www.bctsoftware.com/corsa/
.. _`BCT`: https://www.bctsoftware.com/
.. _`Contezza`: https://contezza.nl/
.. _`Alfresco CE 6.1.2-ga`: https://hub.docker.com/layers/alfresco/alfresco-content-repository-community/6.1.2-ga/images/sha256-6edaf25aded1b16991f06be7754a7030c9d67429353e39ce1da3fd307a5f2e6f?context=explore


Installation
============

**NOTE: If you are using Open Zaak 1.3.1 or above, the CMIS-adapter is already
included and does not require separate installation.**

Requirements
------------

* Python 3.7 or above
* setuptools 30.3.0 or above
* Django 2.2 or newer

Install
-------

1. Install the library in your Django project:

.. code-block:: bash

    $ pip install drc-cmis

2. Add to ``INSTALLED_APPS`` in your Django ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        "drc_cmis",
        ...
    ]

3. Create a mapping file to match Documenten API attributes to custom
   properties in your DMS model. See `Mapping configuration`_.

4. In your ``settings.py``, add these settings to enable it:

.. code-block:: python

    # Enables the CMIS-backend and the Django admin interface for configuring
    # the DMS settings.
    CMIS_ENABLED = True

    # Absolute path to the mapping of Documenten API attributes to (custom)
    # properties in your DMS content model.
    CMIS_MAPPER_FILE = /path/to/cmis_mapper.json

5. Login to the Django admin as superuser and configure the CMIS backend.

Mapping configuration
=====================

There are 2 important concepts:

* Content model - The DMS configuration to store (custom) properties on folders
  and documents. These properties are called CMIS properties.
* CMIS-mapper - a JSON-file containing the translation from Documenten API
  attributes to CMIS properties.

Mapping the Documenten API attributes to (custom) CMIS properties in the DMS
content model should be done with great care. When the DMS stores these
properties, the Documenten API relies on their existance to create proper responses.

Below is a snippet of the CMIS-mapper:

.. code-block:: json

    {
      "DOCUMENT_MAP": {
        "titel": "drc:document__titel"
      }
    }

The ``DOCUMENT_MAP`` describes the mapping for the
``EnkelvoudigInformatieObject`` resource in the Documenten API. In this
snippet, only the ``EnkelvoudigInformatieObject.titel`` attribute is mapped to
a custom CMIS property called ``drc:document_titel``.

Communication between the Documenten API using the CMIS-adapter, is done via
CMIS. Therefore, when creating a document via the Documenten API, the
attributes are translated to CMIS properties as shown below (note that this is
a stripped down request example).

.. code-block:: xml

    <?xml version="1.0"?>
    <soapenv:Envelope xmlmsg:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlmsg:msg="http://docs.oasis-open.org/ns/cmis/messaging/200908/" xmlmsg:core="http://docs.oasis-open.org/ns/cmis/core/200908/">
    <soapenv:Header />
    <soapenv:Body>
      <msg:createDocument>
        <msg:repositoryId>d6a10501-ef36-41e1-9aae-547154f57838</msg:repositoryId>
        <msg:properties>
          <core:propertyString propertyDefinitionId="drc:document__titel">
          <core:value>example.txt</core:value>
        </msg:properties>
        <msg:folderId>workspace://SpacesStore/7c6c7c86-fd63-4eec-bcf8-ffb59f6f6b90</msg:folderId>
      </msg:createDocument>
    </soapenv:Body>
    </soapenv:Envelope>

An example of the mapping configuration, with all possible Documenten API
resources and attributes is shown in ``test_app/cmis_mapper.json``
(`cmis_mapper.json`_). The related DMS content model, that has the definitions
for all these CMIS properties, for `Alfresco`_ (an open source DMS) is in
``/alfresco/extension/alfreso-zsdms-model.xml`` (`alfreso-zsdms-model.xml`_).
Both the mapping and the model should be aligned.

.. _`cmis_mapper.json`: https://github.com/open-zaak/cmis-adapter/blob/master/test_app/cmis_mapper.json
.. _`alfreso-zsdms-model.xml`: https://github.com/open-zaak/cmis-adapter/blob/master/alfresco/extension/alfreso-zsdms-model.xml

Mappings
--------

The content model and the CMIS-mapper configurations need to be aligned. For
each object, the API resource, the CMIS objecttype, CMIS basetype and the
(configuratble) CMIS-mapper object is described.

**Document**

The document itself, its content and meta data.

+-------------------------+---------------------------------+
| Documenten API resource | ``EnkelvoudigInformatieObject`` |
+-------------------------+---------------------------------+
| CMIS objecttype \*      | ``drc:document``                |
+-------------------------+---------------------------------+
| CMIS basetype           | ``cmis:document``               |
+-------------------------+---------------------------------+
| CMIS-mapper object      | ``DOCUMENT_MAP``                |
+-------------------------+---------------------------------+

The mapping between API-attributes and CMIS properties can be found in the `cmis_mapper.json`_.

**Gebruiksrechten**

Usage rights. These rights don't need to be enforced by the DMS but are stored
for use outside the DMS.

+-------------------------+---------------------------------+
| Documenten API resource | ``Gebruiksrechten``             |
+-------------------------+---------------------------------+
| CMIS objecttype \*      | ``drc:gebruiksrechten``         |
+-------------------------+---------------------------------+
| CMIS basetype           | ``cmis:document``               |
+-------------------------+---------------------------------+
| CMIS-mapper object      | ``GEBRUIKSRECHTEN_MAP``         |
+-------------------------+---------------------------------+

The mapping between API-attributes and CMIS properties can be found in the `cmis_mapper.json`_.

**ObjectInformatieObject**

Relation between a document and another object, like a Zaak, Besluit or
something else.

+-------------------------+---------------------------------+
| Documenten API resource | ``ObjectInformatieObject``      |
+-------------------------+---------------------------------+
| CMIS objecttype \*      | ``drc:oio``                     |
+-------------------------+---------------------------------+
| CMIS basetype           | ``cmis:document``               |
+-------------------------+---------------------------------+
| CMIS-mapper object      | ``OBJECTINFORMATIEOBJECT_MAP``  |
+-------------------------+---------------------------------+

The mapping between API-attributes and CMIS properties can be found in the `cmis_mapper.json`_.

**Zaaktype folder**

Contains all Zaken from this Zaaktype and has itself some meta data about the
Zaaktype. API-attributes are from the `Catalogi API`_ ``Zaaktype``-resource.

.. _`Catalogi API`: https://vng-realisatie.github.io/gemma-zaken/standaard/catalogi/index

+-------------------------+---------------------------------+
| Catalogi API resource   | ``Zaaktype``                    |
+-------------------------+---------------------------------+
| CMIS objecttype \*      | ``drc:zaaktypefolder``          |
+-------------------------+---------------------------------+
| CMIS basetype           | ``cmis:folder``                 |
+-------------------------+---------------------------------+
| CMIS-mapper object      | ``ZAAKTYPE_MAP``                |
+-------------------------+---------------------------------+

The mapping between API-attributes and CMIS properties can be found in the `cmis_mapper.json`_.

**Zaak folder**

Contains all Zaak-related documents and has itself some meta data about the
Zaak. API-attributes are from the `Zaken API`_ ``Zaak``-resource.

.. _`Zaken API`: https://vng-realisatie.github.io/gemma-zaken/standaard/zaken/index

+-------------------------+---------------------------------+
| Zaken API resource      | ``Zaak``                        |
+-------------------------+---------------------------------+
| CMIS objecttype \*      | ``drc:zaakfolder``              |
+-------------------------+---------------------------------+
| CMIS basetype           | ``cmis:folder``                 |
+-------------------------+---------------------------------+
| CMIS-mapper object      | ``ZAAK_MAP``                    |
+-------------------------+---------------------------------+

The mapping between API-attributes and CMIS properties can be found in the `cmis_mapper.json`_.

\* CMIS objecttype: ``cmis:objectTypeId``

DMS Content model configuration
-------------------------------

The CMIS mapper configuration must match the content model in the DMS. Each
property, like ``drc:document__titel`` in the example above, must be defined
in the content model.

The example shown in ``/alfresco/extension/alfreso-zsdms-model.xml``
indicates all attributes, types and whether the property is indexed (queryable)
or not. If these attributes are incorrectly configured, the Documenten API
might not work correctly.

DMS folder structure
--------------------

Open Zaak uses a folder structure in the DMS similar to the
`Zaak- en Documentservices 1.2`_. However, due to way the Documenten API works
there are differences.

.. _`Zaak- en Documentservices 1.2`: https://www.gemmaonline.nl/index.php/Zaak-_en_Documentservices

**Creating a document**

When a document is created via the Documenten API, the document is placed in a
temporary folder. By default this is:

.. code-block::

    CMIS Root
    +-- DRC (cmis:folder)
        +-- [year] (cmis:folder)
            +-- [month] (cmis:folder)
                +-- [day] (cmis:folder)
                    +-- [filename] (drc:document)

For example:

.. code-block::

    CMIS Root > DRC > 2020 > 12 > 31 > document.txt

If nothing else happens, this document will remain here.

**Creating gebruiksrechten**

A document can have Gebruiksrechten. These are stored as a separate document
(``gebruiksrechten``) in a folder called ``Related data``. This folder is
always in the same folder as the document itself and is of type ``cmis:folder``.

The Gebruiksrechten will always be moved or copied along with the document.

For example:

.. code-block::

    CMIS Root > DRC > 2020 > 12 > 31 > document.txt
    CMIS Root > DRC > 2020 > 12 > 31 > Related data > document.txt-gebruiksrechten

**Relating a document to a Zaak**

Relating a document to a Zaak (by creating an ``ObjectInformatieObject``
instance in the Documenten API) will cause the document and its Gebruiksrechten
if it exists, to be **moved** or **copied** to the zaak folder.

.. code-block::

    CMIS Root
    +-- DRC (cmis:folder)
        +-- [zaaktype-folder] (drc:zaaktypefolder)
            +-- [year] (cmis:folder)
                +-- [month] (cmis:folder)
                    +-- [day] (cmis:folder)
                        +-- [zaak-folder] (drc:zaakfolder)
                            +-- [filename] (drc:document)
                            +-- Related data (cmis:folder)
                                +-- [filename]-gebruiksrechten (drc:gebruiksrechten)
                                +-- [filename]-oio (drc:oio)

A document is **moved** when the document was **not related** to a Zaak before
(and thus it was in the temporary folder). The document is **copied** to the
new zaak folder when the document was **already related** to a Zaak.

The relation of a document to a Zaak is implicitly described by its path. In
addition however, this relation is stored as a separate document (``oio``) in
the ``Related data`` folder.

For example:

.. code-block::

    CMIS Root > DRC > Melding Openbare Ruimte > 2020 > 12 > 31 > ZAAK-0000001 > document.txt
    CMIS Root > DRC > Melding Openbare Ruimte > 2020 > 12 > 31 > ZAAK-0000001 > Related data > document.txt-gebruiksrechten
    CMIS Root > DRC > Melding Openbare Ruimte > 2020 > 12 > 31 > ZAAK-0000001 > Related data > document.txt-oio

**Relating a document to a Besluit**

When a document is related to a Besluit, there's a few different scenario's:

1. The Besluit is **related** to a Zaak and...

   1. The document is **not related** to a Zaak (and thus the document is in
      the temporary folder): The document is **moved** to the Zaak folder of
      the Zaak that is related to the Besluit.
   2. The document is **already related** to a Zaak: The document is **copied**
      to the new Zaak folder.

2. The Besluit is **not related** to a Zaak and...

   1. The document is **not related** to a Zaak: The document **stays** in its
      temporary folder.
   2. The document is **related** to a Zaak: The document is **copied** to the
      temporary folder.

In all cases, the relation of a document to a Besluit is stored as a separate
document (``oio``) in the ``Related data`` folder, relative to wherever the new
document is stored.

**Relating a document to another object**

When a document is related to any other object, the document is not moved or
copied and stays in its temporary folder.

DMS folder structure overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can configure the folders used by the CMIS adapter via the admin interface.
Some folders are templated (indicated with ``{{ }}``) which means their value
depends on the current date or the related Zaak.

A complete overview of all default folders and documents are shown below:

**Zaak folder path**

Storage location for documents related to a Zaak.

Default: ``/DRC/{{ zaaktype }}/{{ year }}/{{ month }}/{{ day }}/{{ zaak }}/``

.. code-block::

    CMIS Root
    +-- DRC (cmis:folder)
        +-- [zaaktype-folder] (drc:zaaktypefolder)
            +-- [year] (cmis:folder)
                +-- [month] (cmis:folder)
                    +-- [day] (cmis:folder)
                        +-- [zaak-folder] (drc:zaakfolder)
                            +-- [filename] (drc:document)
                            +-- Related data (cmis:folder)
                                +-- [filename]-gebruiksrechten (drc:gebruiksrechten)
                                +-- [filename]-oio (drc:oio)

You can for example change this to: ``/DRC/{{ zaaktype }}/{{ zaak }}/`` to
remove the year/month/day folder structure entirely.

**Other folder path**

Storage location for documents not (yet) related to a Zaak.

Default: ``/DRC/{{ year }}/{{ month }}/{{ day }}/``

.. code-block::

    CMIS Root
    +-- DRC (cmis:folder)
        +-- [year] (cmis:folder)
            +-- [month] (cmis:folder)
                +-- [day] (cmis:folder)
                    +-- [filename] (drc:document)
                    +-- Related data (cmis:folder)
                        +-- [filename]-gebruiksrechten (drc:gebruiksrechten)
                        +-- [filename]-oio (drc:oio)


References
==========

* `Issues <https://github.com/open-zaak/open-zaak/issues>`_
* `Code <https://github.com/open-zaak/cmis-adapter>`_


License
=======

Copyright © Dimpact 2019 - 2020

Licensed under the EUPL_

.. _EUPL: LICENCE.md

.. _`Maykin Media B.V.`: https://www.maykinmedia.nl

.. _`Alfresco`: https://www.alfresco.com/ecm-software/alfresco-community-editions

.. |build-status| image:: https://github.com/open-zaak/cmis-adapter/workflows/Run%20CI/badge.svg
    :target: https://github.com/open-zaak/cmis-adapter/actions?query=workflow%3A%22Run+CI%22
    :alt: Run CI

.. |linting| image:: https://github.com/open-zaak/cmis-adapter/workflows/Code%20quality%20checks/badge.svg
    :target: https://github.com/open-zaak/cmis-adapter/actions?query=workflow%3A%22Code+quality+checks%22
    :alt: Code linting

.. |coverage| image:: https://codecov.io/gh/open-zaak/cmis-adapter/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/open-zaak/cmis-adapter
    :alt: Coverage status

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/drc-cmis.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/drc-cmis.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/drc-cmis.svg
    :target: https://pypi.org/project/drc-cmis/

.. _Documenten API: https://vng-realisatie.github.io/gemma-zaken/standaard/documenten/index
