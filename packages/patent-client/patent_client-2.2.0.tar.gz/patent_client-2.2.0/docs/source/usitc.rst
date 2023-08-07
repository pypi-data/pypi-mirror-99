USITC EDIS
^^^^^^^^^^
API URL: https://www.usitc.gov/docket_services/documents/EDIS3WebServiceGuide.pdf

.. note::
    Only publicly accessible documents are available. Any document that is marked confidential is not accessible.

.. warning::
    The document download feature is currently inoperative.

Patent Client provides an interface to the USITC EDIS API. Note that this is a very restricted subset
of the overall EDIS system, and does not permit searching - only direct lookups. The data is structured
in three tiers. An Investigation has many Documents, and each Document has many Attachments. The actual
filed documents are in the Attachments. if the Document is a single item (e.g. a brief of some kind),
the original file is the first-named attachment.

.. code-block:: python

    >>> from patent_client import ITCInvestigation
    >>> inv = ITCInvestigation.objects.get('337-TA-971')
    >>> inv.documents[5].title
    'Commission Opinion'

Models
======

.. automodule:: patent_client.usitc.model
    :members:
    :undoc-members:
