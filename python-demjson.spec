%if 0%{?fedora}
%global with_python3}
%endif

%global srcname demjson

Name:           python-%{srcname}
Version:        2.2.4
Release:        3%{?dist}
Summary:        Python JSON module and lint checker
Group:          Development/Languages
License:        LGPLv3+
URL:            http://deron.meranda.us/python/%{srcname}/
Source0:        http://deron.meranda.us/python/%{srcname}/dist/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%global base_description The demjson package is a comprehensive Python language library to read\
and write JSON; the popular language-independent data format standard.\
\
It includes a command tool, jsonlint, that allows you to easily check\
and validate any JSON document, and spot any potential data\
portability issues. It can also reformat and re-indent a JSON document\
to make it easier to read.

%description
%{base_description}


%package -n python2-%{srcname}
Summary:        Python JSON module and lint checker
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description -n python2-%{srcname}
%{base_description}

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Python JSON module and lint checker
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# needed for 2to3
BuildRequires:  python-tools

%description -n python3-%{srcname}
%{base_description}
%endif


%prep
%autosetup -c -n %{srcname}-%{version}
mv %{srcname}-%{version} python2
%if 0%{?with_python3}
cp -a python2 python3
%endif


%build
pushd python2
%py2_build
popd

%if 0%{?with_python3}
pushd python3
%py3_build
popd
%endif


%install
pushd python2
%py2_install
mv %{buildroot}%{_bindir}/jsonlint %{buildroot}%{_bindir}/jsonlint-%{python2_version}
ln -s jsonlint-%{python2_version} %{buildroot}%{_bindir}/jsonlint-2
popd

%if 0%{?with_python3}
pushd python3
%py3_install
mv %{buildroot}%{_bindir}/jsonlint %{buildroot}%{_bindir}/jsonlint-%{python3_version}
ln -s jsonlint-%{python3_version} %{buildroot}%{_bindir}/jsonlint-3
popd
%endif

# fix shebang lines
find %{buildroot}%{python2_sitelib} \
%if 0%{?with_python3}
     %{buildroot}%{python3_sitelib} \
%endif
     -name '*.py' -exec \
     sed -i "1{/^#!/d}" {} \;

find %{buildroot}%{_bindir} -ls

# 2.X binary is called by default for now
ln -s jsonlint-%{python2_version} %{buildroot}%{_bindir}/jsonlint


%check
pushd python2/test
PYTHONPATH=%{buildroot}%{python2_sitelib} \
%{__python2} test_demjson.py
popd

%if 0%{?with_python3}
pushd python3/test
2to3 -w --no-diffs test_demjson.py
PYTHONPATH=%{buildroot}%{python3_sitelib} \
%{__python3} test_demjson.py
popd
%endif


%files -n python2-%{srcname}
%doc python2/README.txt
%doc python2/README.md
%doc python2/docs
%license python2/LICENSE.txt
%{python2_sitelib}/*
%{_bindir}/jsonlint
%{_bindir}/jsonlint-2
%{_bindir}/jsonlint-%{python2_version}


%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc python3/README.txt
%doc python3/README.md
%doc python3/docs
%license python3/LICENSE.txt
%{python3_sitelib}/*
%{_bindir}/jsonlint-3
%{_bindir}/jsonlint-%{python3_version}
%endif


%changelog
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 23 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.4-1
- Update to 2.2.4.
- Follow updated Python packaging guidelines.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jun 19 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.3-1
- Update to 2.2.3.
- Apply updated Python packaging guidelines.
- Mark LICENSE.txt with %%license.

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
