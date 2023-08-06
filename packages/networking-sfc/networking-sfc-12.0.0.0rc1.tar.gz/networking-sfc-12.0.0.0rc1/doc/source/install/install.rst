..
      Copyright 2015 Futurewei. All rights reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.


      Convention for heading levels in Neutron devref:
      =======  Heading 0 (reserved for the title in a document)
      -------  Heading 1
      ~~~~~~~  Heading 2
      +++++++  Heading 3
      '''''''  Heading 4
      (Avoid deeper levels because they do not render well.)


Installation
============

If possible, you should rely on packages provided by your Linux and/or
OpenStack distribution:

* For Fedora or CentOS, you can install the ``python-networking-sfc`` RPM
  package provided by the RDO project.

If you use ``pip``, follow these steps to install networking-sfc:

* `identify the version of the networking-sfc package
  <https://opendev.org/openstack/releases/raw/branch/master/deliverables/_independent/networking-sfc.yaml>`_
  that matches your OpenStack version:

  * Ocata: latest 4.0.x version
  * Newton: latest 3.0.x version
  * Mitaka: latest 2.0.x version

* indicate pip to (a) install precisely this version and (b) take into
  account OpenStack upper constraints on package versions for dependencies
  (example for Ocata):

  .. code-block:: console

     pip install -c https://opendev.org/openstack/requirements/raw/branch/master/upper-constraints.txt?h=stable/ocata networking-sfc==4.0.0
