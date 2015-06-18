%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%if 0%{?fedora}
%global with_python3 1
%{!?python3_version: %global python3_version %(%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])")}
%endif

Name:           python-demjson
Version:        2.2.2
Release:        2%{?dist}
Summary:        Python JSON module and lint checker
Group:          Development/Languages
License:        LGPLv3+
URL:            http://deron.meranda.us/python/demjson/
Source0:        http://deron.meranda.us/python/demjson/dist/demjson-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# needed for 2to3
BuildRequires:  python-tools
%endif # with_python3

%description 
The demjson package is a comprehensive Python language library to read
and write JSON; the popular language-independent data format standard.

It includes a command tool, jsonlint, that allows you to easily check
and validate any JSON document, and spot any potential data
portability issues. It can also reformat and re-indent a JSON document
to make it easier to read.


%if 0%{?with_python3}
%package -n python3-demjson
Summary:        Python JSON module and lint checker
Group:          Development/Languages

%description -n python3-demjson
The demjson package is a comprehensive Python language library to read
and write JSON; the popular language-independent data format standard.

It includes a command tool, jsonlint, that allows you to easily check
and validate any JSON document, and spot any potential data
portability issues. It can also reformat and re-indent a JSON document
to make it easier to read.
%endif # with_python3


%prep
%setup -q -n demjson-%{version}

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# fix shebang lines
find %{buildroot}%{python_sitelib} -name '*.py' -exec \
     sed -i "1{/^#!/d}" {} \;

# rename binary
mv %{buildroot}%{_bindir}/jsonlint{,-%{python_version}}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# fix shebang lines
find %{buildroot}%{python3_sitelib} -name '*.py' -exec \
     sed -i "1{/^#!/d}" {} \;

# rename binary
mv %{buildroot}%{_bindir}/jsonlint{,-%{python3_version}}
popd
%endif # with_python3

# 2.X binary is called by default for now
ln -s jsonlint-%{python_version} %{buildroot}%{_bindir}/jsonlint


%check
cd test
PYTHONPATH=%{buildroot}%{python_sitelib} \
%{__python} test_demjson.py

%if 0%{?with_python3}
pushd %{py3dir}
cd test
2to3 -w --no-diffs test_demjson.py
PYTHONPATH=%{buildroot}%{python3_sitelib} \
%{__python3} test_demjson.py
popd
%endif # with_python3


%files
%doc README.txt README.md LICENSE.txt
%doc docs
%{python_sitelib}/*
%{_bindir}/jsonlint
%{_bindir}/jsonlint-%{python_version}


%if 0%{?with_python3}
%files -n python3-demjson
%doc README.txt README.md LICENSE.txt
%doc docs
%{python3_sitelib}/*
%{_bindir}/jsonlint-%{python3_version}
%endif # with_python3


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 25 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.2-1
- Update to 2.2.2.
- Provide python3 subpackage.
- Modernize spec file.
- Update %%description.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Apr  4 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6-1
- Update to 1.6.
- Injecting setuptools is only needed for EPEL5.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5-1
- Update to 1.5.
- Remove patch no longer needed.

* Wed Oct 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.4-1
- Update to 1.4. Upstream changed license to LGPLv3+.
- Apply a one-liner patch provided upstream.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3-3
- Rebuild for Python 2.6

* Mon Mar 31 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.3-2
- Cleanup BuildRequires.
- Don't pack INSTALL.txt.

* Thu Mar 27 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.3-1
- New package.
