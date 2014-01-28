Name:           storaged
Version:        0.2.0
Release:        2%{?dist}
Summary:        Extended storage management DBus service

# The daemon and tools are licensed under the GPLv2 (or later) and libraries are
# licensed under LGPLv2 (or later).
License:        GPLv2+ and LGPLv2+
URL:            https://github.com/cockpit-project/storaged
Source0:        https://github.com/cockpit-project/%{name}/archive/%{version}.tar.gz

BuildRequires:  libudisks2-devel
BuildRequires:  libxslt
BuildRequires:  gobject-introspection-devel
BuildRequires:  libgudev1-devel
BuildRequires:  lvm2-devel
BuildRequires:  glib2-devel
BuildRequires:  polkit-devel
BuildRequires:  intltool
BuildRequires:  systemd
BuildRequires:  docbook-style-xsl

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
This is a DBus service that provides management of extended
storage options, currently only LVM.

This is an extension to udisks2.


%prep
%setup -q
# NOCONFIGURE=1 because otherwise autogen also runs ./configure
NOCONFIGURE=1 ./autogen.sh


%build
%configure
make %{?_smp_mflags}


%install
%make_install


%files
%doc AUTHORS COPYING HACKING README
%doc %{_mandir}/man8/storaged.8.gz
%{_unitdir}/storaged.service
%{_libdir}/%{name}
%{_sysconfdir}/dbus-1/system.d/com.redhat.lvm2.conf
%{_datadir}/dbus-1/interfaces/com.redhat.lvm2.xml
%{_datadir}/dbus-1/system-services/com.redhat.lvm2.service
%{_datadir}/polkit-1/actions/com.redhat.lvm2.policy


%post
%systemd_post com.redhat.lvm2.service

%preun
%systemd_preun com.redhat.lvm2.service

%postun
%systemd_postun_with_restart com.redhat.lvm2.service


%changelog
* Thu Jan 16 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.1.0-2
- Removed double systemd BuildRequire
- Rewritten summary and description

* Sun Jan 12 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.1.0-1
- Rename from udisks2-lvm
