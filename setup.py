#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Fourth Paradigm Development, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
from setuptools import setup, find_packages, findall


setup(
    name = "openstack_dashboard_fileupload",
    version = "1.0",
    url = "https://launchpad.net/django-openstack/",
    license = "Apache 2.0",
    description = "OpenStack Fileupload Plugin.",
    author = "Devin Carlen et al.",
    author_email = "devin.carlen@gmail.com",
    py_modules = ["openstack_dashboard.plugins.projadmin.fileupload"],
    packages = ["openstack_dashboard.plugins.fileupload"],
    package_data = {"openstack_dashboard.plugins.fileupload":
                        ["../../../" + s for s in
                        findall("openstack_dashboard/templates") +
                        findall("openstack_dashboard/static")],
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ]
)

