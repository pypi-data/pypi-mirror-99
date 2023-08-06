ckanext-dcor_depot
==================

|PyPI Version| |Build Status| |Coverage Status|

This plugin manages how data are stored in DCOR. There are two types of
files in DCOR:

1. Resources uploaded by users, imported from figshare, or
   imported from a data archive
2. Ancillary files that are generated upon resource creation, such as
   condensed DC data, preview images (see
   `ckanext-dc_view <https://github.com/DCOR-dev/ckanext-dc_view>`_).

This plugin implements:

- Data storage management. All resources uploaded by a user are moved
  to ``/data/users-HOSTNAME/USERNAME-ORGNAME/PK/ID/PKGNAME_RESID_RESNAME``
  and symlinks are created in ``/data/ckan-HOSTNAME/resources/RES/OUR/CEID``.
  CKAN itself will not notice this. The idea is to have a filesystem overview
  about the datasets of each user.
- Import datasets from figshare. Existing datasets from figshare are
  downloaded to the ``/data/depots/figshare`` directory and, upon resource
  creation, symlinked there from  ``/data/ckan-HOSTNAME/resources/RES/OUR/CEID``
  (Note that this is an exemption of the data storage management described
  above). When running the following command, the "figshare-import" organization
  is created and the datasets listed in ``figshare_dois.txt`` are added to CKAN:

  ::

     ckan -c /etc/ckan/default/ckan.ini import-figshare


- Populate an internal depot from RT-DC data stored in tar archives. This
  is part of an effort to have automated imports of RT-DC data from other
  sources. The idea is to move experimental data to the DCOR server in
  tar archives and DCOR can then populate the internal depot with it.
  The location of the internal depot is ``/data/depots/internal/``
  and it follows a very specific directory structure
  ``201X/2019-08/20/2019-08-20_1126_c083de*`` where the path is generated
  from the acquisition date, time, and part of the hash (``c083de``) of
  the original data file. According to this scheme, all files with the
  same path stem belong to one dataset:

  - ``2019-08-20_1126_c083de.sha256sums`` a file containing SHA256 sums
  - ``2019-08-20_1126_c083de_v1.rtdc`` the actual measurement
  - ``2019-08-20_1126_c083de_v1_condensed.rtdc`` the condensed dataset
  - ``2019-08-20_1126_c083de_ad1_m001_bg.png`` an ancillary image
  - ``2019-08-20_1126_c083de_ad2_m002_bg.png`` another ancillary image
  - ...

  ::

     ckan -c /etc/ckan/default/ckan.ini depotize-archive


- Import datasets from the internal depot. The previous command
  ``depotize-archive`` just populates the depot directory structure.
  To make the datasets available in CKAN, this step must be performed:

  ::

     ckan -c /etc/ckan/default/ckan.ini import-internal


Please make sure that the necessary file permissions are given in ``/data``. 


Installation
------------

::

    pip install ckanext-dcor_depot


Add this extension to the plugins and defaul_views in ckan.ini:

::

    ckan.plugins = [...] dcor_depot
    ckan.storage_path=/data/ckan-HOSTNAME
    ckanext.dcor_depot.depots_path=/data/depots
    ckanext.dcor_depot.users_depot_name=users-HOSTNAME

This plugin stores resources to `/data`:

::

    mkdir -p /data/depots/users-$(hostname)
    chown -R www-data /data/depots/users-$(hostname)


Testing
-------
If CKAN/DCOR is installed and setup for testing, this extension can
be tested with pytest:

::

    pytest ckanext

Testing can also be done via vagrant in a virtualmachine using the
`dcor-test <https://app.vagrantup.com/paulmueller/boxes/dcor-test/>` image.
Make sure that `vagrant` and `virtualbox` are installed and run the
following commands in the root of this repository:

::

    # Setup virtual machine using `Vagrantfile`
    vagrant up
    # Run the tests
    vagrant ssh -- sudo bash /testing/vagrant-run-tests.sh


.. |PyPI Version| image:: https://img.shields.io/pypi/v/ckanext.dcor_depot.svg
   :target: https://pypi.python.org/pypi/ckanext.dcor_depot
.. |Build Status| image:: https://img.shields.io/github/workflow/status/DCOR-dev/ckanext-dcor_depot/Checks
   :target: https://github.com/DCOR-dev/ckanext-dcor_depot/actions?query=workflow%3AChecks
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/DCOR-dev/ckanext-dcor_depot
   :target: https://codecov.io/gh/DCOR-dev/ckanext-dcor_depot
