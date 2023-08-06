.. image:: https://raw.githubusercontent.com/senaite/senaite.impress/master/static/logo_pypi.png
   :target: https://github.com/senaite/senaite.impress#readme
   :alt: senaite.impress
   :height: 128

*Publication of HTML/PDF Reports in SENAITE*
============================================

.. image:: https://img.shields.io/pypi/v/senaite.impress.svg?style=flat-square
   :target: https://pypi.python.org/pypi/senaite.impress

.. image:: https://img.shields.io/github/issues-pr/senaite/senaite.impress.svg?style=flat-square
   :target: https://github.com/senaite/senaite.impress/pulls

.. image:: https://img.shields.io/github/issues/senaite/senaite.impress.svg?style=flat-square
   :target: https://github.com/senaite/senaite.impress/issues

.. image:: https://img.shields.io/badge/README-GitHub-blue.svg?style=flat-square
   :target: https://github.com/senaite/senaite.impress#readme

.. image:: https://img.shields.io/badge/Built%20with-%E2%9D%A4-red.svg
   :target: https://github.com/senaite/senaite.impress

.. image:: https://img.shields.io/badge/Made%20for%20SENAITE-%E2%AC%A1-lightgrey.svg
   :target: https://www.senaite.com


About
=====

SENAITE IMPRESS is basically a rendering engine for HTML documents to PDF. It
supports any kind of international paperformat with their corresponding paper
dimensions, portrait and landscape orientation and merging of multiple PDFs to
one document.


Installation
============

Please follow the installations instructions for `Plone 4`_ and
`senaite.lims`_.

To install SENAITE IMPRESS, you have to add `senaite.impress` into the
`eggs` list inside the `[buildout]` section of your
`buildout.cfg`::

   [buildout]
   parts =
       instance
   extends =
       http://dist.plone.org/release/4.3.19/versions.cfg
   find-links =
       http://dist.plone.org/release/4.3.19
       http://dist.plone.org/thirdparty
   eggs =
       Plone
       Pillow
       senaite.lims
       senaite.impress
   zcml =

   [instance]
   recipe = plone.recipe.zope2instance
   user = admin:admin
   http-address = 127.0.0.1:8080
   eggs =
       ${buildout:eggs}
   zcml =
       ${buildout:zcml}

   [versions]
   setuptools =
   zc.buildout =


**Note**

The above example works for the buildout created by the unified
installer. If you however have a custom buildout you might need to add
the egg to the `eggs` list in the `[instance]` section rather than
adding it in the `[buildout]` section.

Also see this section of the Plone documentation for further details:
https://docs.plone.org/4/en/manage/installing/installing_addons.html

**Important**

For the changes to take effect you need to re-run buildout from your
console::

   bin/buildout


Installation Requirements
-------------------------

The following versions are required for SENAITE IMPRESS:

-  Plone 4.3.19
-  senaite.lims >= 1.3.0


.. _Plone 4: https://docs.plone.org/4/en/manage/installing/index.html
.. _senaite.lims: https://github.com/senaite/senaite.lims#installation


Changelog
=========

1.2.4 (2020-08-05)
------------------

- #96 Remove call to getObjectWorkflowStates (in `is_provisional` func)
- #91 Fix infinite recursion when calling print/publish view w/o items parameter
- #89 PDF Print View
- #88 Support context aware report controller views


1.2.3 (2020-03-01)
------------------

- #86 Allow request parameter overrides for template, orientation and paperformat


1.2.2 (2019-10-26)
------------------

- #83: Handle `None` values in decorator more gracefully
- #82: Fix Date Published is empty on MultiDefault report
- #81: Rebuild JavaScript bundle with new versions
- #80: Update Bootstrap CSS to version 4.3.1
- #79: Use senaite.core.api instead of senaite.api
- #78: Fix template error on missing lab address data


1.2.1 (2019-07-01)
------------------

- #75: Conflict safe concurrent report creation
- #71: Implemented storage adapter
- #73: Extend README wrt 'Reports in external packages'
- #66: Fix Publication Preference Traceback with Default template
- #68: Fix empty Date Published on Default report


1.2.0 (2019-03-30)
------------------

- #64: Fix Rejected AS are shown in the PDF Report
- #62: Better error message handling
- #57: SENAITE CORE integration
- #52: Use the most recent AR as the primary storage
- #48: Fix PDF storage in primary AR when "Store Multi-Report PDFs Individually" option is turned off


1.1.0 (2018-10-04)
------------------

- #44: Changed field ChildAnalysisRequest -> Retest
- #42: Combine Attachments coming from Request and Analysis together for unified grouping/sorting
- #41: Default reports update
- #40: Customizable report options
- #37: Added hyphenize and get_transition_date helper methods
- #36: Allow JS injection and custom report scripts
- #34: Pass through the calculated dimensions to the template
- #33: Include D3JS and support for Range Graphs
- #32: Added language selector
- #31: Fix sort order of uniquified items
- #30: Keep order of grouped items
- #29: Added report developer mode
- #28: Fixed i18n domain for time localization
- #27: Refactored Report Adapters to Multi Adapters
- #25: Added controlpanel descriptions
- #24: Control individual report generation for multi-report PDFs
- #23: Fixed multi client report handling
- #21: Improved email template
- #19: Allow additional attachments in publication email
- #18: Fixed barcode rendering in multi-colum report
- #17: Fix alert section overlapping of the header section
- #16: Fix unicode error in sort method
- #15: Handle commas in recipient email name better
- #13: Fix bootstrap columns CSS for WeasyPrint
- #12: Added upgrade-step machinery
- #11: Refactored to ReportModel -> SuperModel


1.0.2 (2018-07-10)
------------------

- #8: Better Print CSS
- #7: Correct margin calculation
- #6: Updated default report templates


1.0.1 (2018-06-23)
------------------

- Pinned `senaite.api>=1.2.0`
- Updated PyPI page


1.0.0 (2018-06-23)
------------------

- Initial Release


