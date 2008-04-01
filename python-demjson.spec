%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-demjson
Version:        1.3
Release:        2%{?dist}
Summary:        Python JSON module and lint checker

Group:          Development/Languages
License:        GPLv3+
URL:            http://deron.meranda.us/python/demjson/
Source0:        http://deron.meranda.us/python/demjson/dist/demjson-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel


%description 
This module provides classes and functions for encoding or decoding
data represented in the language-neutral JSON format (which is often
used as a simpler substitute for XML in Ajax web applications).  This
implementation tries to be as compliant to the JSON specification (RFC
4627) as possible, while still providing many optional extensions to
allow less restrictive JavaScript syntax.  It includes complete
Unicode support, including UTF-32, BOM, and surrogate pair processing.
It can also support JavaScript's NaN and Infinity numeric types as
well as it's 'undefined' type.

It also includes a lint-like JSON syntax validator which tests JSON
text for strict compliance to the standard.


%prep
%setup -q -n demjson-%{version}


%build
%if 0%{?fedora} > 8
%{__python} setup.py build
%else
%{__python} -c 'import setuptools; execfile("setup.py")' build
%endif


%install
rm -rf %{buildroot}
%if 0%{?fedora} > 8
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%else
%{__python} -c 'import setuptools; execfile("setup.py")' install -O1 --skip-build --root %{buildroot}
%endif
%{__install} -m 0755 -D -p jsonlint %{buildroot}%{_bindir}/jsonlint

# fix shebang lines
%{__sed} -i "1c#! /usr/bin/python" %{buildroot}%{_bindir}/jsonlint
find %{buildroot}%{python_sitelib} -name '*.py' -exec \
     %{__sed} -i "1{/^#!/d}" {} \;


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc docs/demjson.html docs/jsonlint.txt
%doc AUTHORS.txt CHANGES.txt LICENSE.txt
%doc NEWS.txt README.txt THANKS.txt
%{python_sitelib}/*
%{_bindir}/jsonlint


%changelog
* Mon Mar 31 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.3-2
- Cleanup BuildRequires.
- Don't pack INSTALL.txt.

* Thu Mar 27 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.3-1
- New package.
