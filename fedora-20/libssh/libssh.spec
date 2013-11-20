Name:           libssh-rc-devel
Version:        0.6.0rc1
Release:        1%{?dist}
Summary:        A library implementing the SSH2 protocol (0xbadc0de version)
License:        LGPLv2+
URL:            http://www.libssh.org/
Group:          System Environment/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        https://red.libssh.org/attachments/download/52/libssh-0.6.0rc1.tar.gz

BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  krb5-devel

%description
The ssh library was designed to be used by programmers needing a working SSH
implementation by the mean of a library. The complete control of the client is
made by the programmer. With libssh, you can remotely execute programs, transfer
files, use a secure and transparent tunnel for your remote programs. With its
Secure FTP implementation, you can play with remote files easily, without
third-party programs others than libcrypto (from openssl).

This package contains the release candidate built as a static library.

%prep
%setup -q -n libssh-%{version}
# Remove examples, they are not packaged and do not build on EPEL 5
sed -i -e 's|add_subdirectory(examples)||g' CMakeLists.txt
rm -fr examples

%build
if test ! -e "obj"; then
  mkdir obj
fi
pushd obj

%cmake \
    %{_builddir}/libssh-%{version} -DWITH_GSSAPI=ON -DWITH_ZLIB=ON -DWITH_STATIC_LIB=ON -DWITH_EXAMPLES=OFF
make %{?_smp_mflags} VERBOSE=1
make doc

popd

%install
pushd obj
make DESTDIR=%{buildroot} install
pushd %{buildroot}
rm .%{_libdir}/libssh.so*
rm .%{_libdir}/libssh_threads.so*
mv .%{_libdir}/libssh.a .%{_libdir}/libssh_rc.a
mv .%{_libdir}/libssh_threads.a .%{_libdir}/libssh_threads_rc.a
mkdir -p .%{_includedir}/libssh_rc
mv .%{_includedir}/libssh .%{_includedir}/libssh_rc/libssh
sed -e 's|libssh|libssh_rc|' \
	-e 's|-I/usr/include|-I/usr/include/libssh_rc -DLIBSSH_STATIC=1|' \
	-e 's|-lssh|-lz -lcrypto -lkrb5 -lgssapi_krb5 %{_libdir}/libssh_rc.a|' \
	.%{_libdir}/pkgconfig/libssh.pc > .%{_libdir}/pkgconfig/libssh_rc.pc
rm .%{_libdir}/pkgconfig/libssh.pc
sed  -e 's|libssh_threads|libssh_threads_rc|' \
	-e 's|-I/usr/include||' \
	-e 's|-lssh_threads|%{_libdir}/libssh_threads_rc.a|' \
	-e '$ a\Requires: libssh_rc' \
	.%{_libdir}/pkgconfig/libssh_threads.pc > .%{_libdir}/pkgconfig/libssh_threads_rc.pc
rm .%{_libdir}/pkgconfig/libssh_threads.pc
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%doc AUTHORS BSD ChangeLog COPYING README
%{_libdir}/libssh_rc.a
%{_libdir}/libssh_threads_rc.a
%{_includedir}/libssh_rc/libssh/callbacks.h
%{_includedir}/libssh_rc/libssh/legacy.h
%{_includedir}/libssh_rc/libssh/libssh.h
%{_includedir}/libssh_rc/libssh/server.h
%{_includedir}/libssh_rc/libssh/sftp.h
%{_includedir}/libssh_rc/libssh/ssh2.h
%{_libdir}/pkgconfig/libssh_rc.pc
%{_libdir}/pkgconfig/libssh_threads_rc.pc
%{_libdir}/cmake/libssh-config-version.cmake
%{_libdir}/cmake/libssh-config.cmake

%changelog
* Fri Oct 18 2013 - Stef Walter <stefw@redhat.com> - 0.6-rc1.1
- Forked to be a static rc devel library

* Fri Jul 26 2013 - Andreas Schneider <asn@redhat.com> - 0.5.5-1
- Update to 0.5.5.
- Clenup the spec file.

* Thu Jul 18 2013 Simone Caronni <negativo17@gmail.com> - 0.5.4-5
- Add EPEL 5 support.
- Add Debian patches to enable Doxygen documentation.

* Tue Jul 16 2013 Simone Caronni <negativo17@gmail.com> - 0.5.4-4
- Add patch for #982685.

* Mon Jun 10 2013 Simone Caronni <negativo17@gmail.com> - 0.5.4-3
- Clean up SPEC file and fix rpmlint complaints.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Petr Lautrbach <plautrba@redhat.com> 0.5.4-1
- update to security 0.5.4 release
- CVE-2013-0176 (#894407)

* Tue Nov 20 2012 Petr Lautrbach <plautrba@redhat.com> 0.5.3-1
- update to security 0.5.3 release (#878465)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Petr Lautrbach <plautrba@redhat.com> 0.5.2-1
- update to 0.5.2 version (#730270)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun  1 2011 Jan F. Chadima <jchadima@redhat.com> - 0.5.0-1
- bounce versionn to 0.5.0 (#709785)
- the support for protocol v1 is disabled

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Jan F. Chadima <jchadima@redhat.com> - 0.4.8-1
- bounce versionn to 0.4.8 (#670456)

* Mon Sep  6 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.6-1
- bounce versionn to 0.4.6 (#630602)

* Thu Jun  3 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.4-1
- bounce versionn to 0.4.4 (#598592)

* Wed May 19 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.3-1
- bounce versionn to 0.4.3 (#593288)

* Tue Mar 16 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.2-1
- bounce versionn to 0.4.2 (#573972)

* Tue Feb 16 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.1-1
- bounce versionn to 0.4.1 (#565870)

* Fri Dec 11 2009 Jan F. Chadima <jchadima@redhat.com> - 0.4.0-1
- bounce versionn to 0.4.0 (#541010)

* Thu Nov 26 2009 Jan F. Chadima <jchadima@redhat.com> - 0.3.92-2
- typo in spec file

* Thu Nov 26 2009 Jan F. Chadima <jchadima@redhat.com> - 0.3.92-1
- bounce versionn to 0.3.92 (0.4 beta2) (#541010)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.2-4
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Jan F. Chadima <jchadima@redhat.com> - 0.2-2
- Small changes during review

* Mon Jun 01 2009 Jan F. Chadima <jchadima@redhat.com> - 0.2-1
- Initial build

