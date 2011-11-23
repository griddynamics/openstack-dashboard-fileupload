#
# spec file for package openstack-dashboard-fileupload
#
# Copyright 2011 Grid Dynamics Consulting Services, Inc.  All rights reserved.
#
#    This software is provided to Cisco Systems, Inc. as "Supplier Materials"
#    under the license terms governing Cisco's use of such Supplier Materials described
#    in the Master Services Agreement between Grid Dynamics Consulting Services, Inc. and Cisco Systems, Inc.,
#    as amended by Amendment #1.  If the parties are unable to agree upon the terms
#    of the Amendment #1 by July 31, 2011, this license shall automatically terminate and
#    all rights in the Supplier Materials shall revert to Grid Dynamics, unless Grid Dynamics specifically
#    and otherwise agrees in writing.

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           openstack-dashboard-fileupload
Version:        1.0
Release:        0.20110916.1739%{?dist}
Epoch:          1
Url:            http://www.openstack.org
License:        Apache 2.0
Group:          Development/Languages/Python
Source0:        http://openstack-dashboard-fileupload.openstack.org/tarballs/%{name}-%{version}.tar.gz  
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel python-setuptools
BuildArch:      noarch
Summary:        Fileupload plugin for OpenStack Dashboard

Requires:       openstack-dashboard

%description
An images file uploading plugin for Openstack Dashboard

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/openstack_dashboard/plugins/fileupload/*
%{python_sitelib}/openstack_dashboard/plugins/projadmin/fileupload.py*
%{python_sitelib}/openstack_dashboard/templates/fileupload/*
%{python_sitelib}/openstack_dashboard_fileupload-*.egg-info

%changelog
