Name:      dawawin
License:   Waqf
Group:     System Environment/Base
Version:   0.1.20
Release:   1
Summary:   Display and store poems.
URL:       http://sourceforge.net/projects/dawawin/
Source0:   http://garr.dl.sourceforge.net/project/dawawin/%{name}-%{version}.tar.gz
Source1:   dawawin.png
BuildRequires:  gstreamer-devel pygobject3-devel python2-devel ImageMagick
Requires:  gstreamer pygobject3 python2
BuildRoot: %{_tmppath}/%{name}-%{version}-build  
BuildArch: noarch

%description  
برنامج عرض وتخزين القصائد الشعرية.
Display and store poems.

%prep
%setup -q

%build
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot} --optimize=2 --record=INSTALLED_FILES
done;

%clean
rm -rf $RPM_BUILD_ROOT  

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc README LICENSE-en LICENSE-ar.txt TODO AUTHORS ChangeLog

%changelog
* Fri May 29 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.20-1
- update

* Fri May 24 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.19-1
- update

* Wed May 15 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.18-1
- update

* Sat May 11 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.17-1
- update

* Wed May 08 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.16-1
- update

* Sat May 04 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.15-1
- update

* Fri May 03 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.14-1
- update

* Wed May 01 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.12-1
- update

* Tue Apr 30 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.11-1
- update

* Sun Apr 28 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.10-1
- update

* Thu Apr 18 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.9-1
- update

* Tue Apr 16 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.7-1
- update

* Mon Apr 15 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.6-1
- update

* Sat Apr 13 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.5-1
- update

* Thu Apr 11 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1.3-1
- update

* Sat Apr 06 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 0.1-1
- Initial release
