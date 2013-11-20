# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

# Filter the _speedups.so provides that otherwise comes into the provides
%global __provides_exclude_from ^(%{python_sitearch}/.*\\.so)$

Name:           python-scss
Version:        1.2.0
Release:        2%{?dist}
Summary:        A Scss compiler for Python

License:        MIT
URL:            https://github.com/Kronuz/pyScss
Source0:        https://github.com/Kronuz/pyScss/archive/v%{version}.tar.gz
# Review request for this is filed: https://github.com/Kronuz/pyScss/pull/241
Patch0:         python-scss-remove-shebangs.patch

BuildRequires:  python-devel
BuildRequires:  python-six
BuildRequires:  python-sphinx
Requires:       python-six
Requires:       python-setuptools

%description
A Scss compiler for Python

%prep
%setup -q -n pyScss-%{version}
%patch0 -p0


%build
CFLAGS="%{optflags}" %{__python} setup.py build
cd docs
make SPHINXBUILD=sphinx-build man


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
chmod +x %{buildroot}%{python_sitearch}/scss/tool.py
mkdir -p %{buildroot}%{_mandir}/man1/
cp -r docs/_build/man/pyscss.1 %{buildroot}%{_mandir}/man1/pyscss.1


%files
%doc DESCRIPTION LICENSE README.rst
%{python_sitearch}/*
%{_bindir}/pyscss
%{_mandir}/man1/pyscss.1.gz



%changelog
* Thu Oct 17 2013 Patrick Uiterwijk <puiterwijk@gmail.com> - 1.2.0-1
- Initial packaging
