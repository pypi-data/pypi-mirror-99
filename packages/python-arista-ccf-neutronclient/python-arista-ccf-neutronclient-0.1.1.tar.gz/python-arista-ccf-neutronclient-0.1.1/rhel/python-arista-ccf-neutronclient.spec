%global pypi_name python-arista-ccf-neutronclient
%global pypi_name_underscore python_arista_ccf_neutronclient
%global rpm_prefix openstackclient-arista-ccf

Name:           %{pypi_name}
Version:        0.1.1
Release:        1%{?dist}
Epoch:          1
Summary:        Python bindings for Arista Networks Converged Cloud Fabric Neutron API
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:       python3-pbr >= 5.1.0
Requires:       python3-neutronclient >= 6.14.0

%description
This package contains Arista Networks Converged Cloud Fabric
python client for Openstack CLI.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%files
%license LICENSE
%{python3_sitelib}/%{pypi_name_underscore}
%{python3_sitelib}/*.egg-info


%post

%preun

%postun

%changelog
* Tue Jun 6 2021 Weifan Fu <weifan.fu@arista.com> - 0.1.1
- Bump Version for Pypi release, minor pep8 fix, rhel requirement fix
* Tue Jun 6 2021 Weifan Fu <weifan.fu@arista.com> - 0.1.0
- OSP-300: Rename to Arista CCF Neutron CLI and use python3 as default
* Tue Jun 6 2019 Weifan Fu <weifan.fu@bigswitch.com> - 0.0.7
- OSP-278: Transition from Neutron CLI to OpenStack CLi
* Tue Nov 20 2018 Weifan Fu <weifan.fu@bigswitch.com> - 0.0.6
- OSP-252: update tox for py3
* Mon Oct 08 2018 Aditya Vaja <wolverine.av@gmail.com> - 0.0.5
- OSP-241: fix entry point extension name and import error
* Tue Aug 21 2018 Aditya Vaja <wolverine.av@gmail.com> - 0.0.4
- OSP-165: add force sync command for topo_sync and build changes
