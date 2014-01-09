Summary: Disk Manager, LVM addon
Name: udisks2-lvm
Version: 1.99.0
Release: 2%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: XXX
Source0: udisks-lvm-%{version}.tar.bz2

BuildRequires: glib2-devel
BuildRequires: gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires: polkit-devel >= %{polkit_version}
BuildRequires: intltool
BuildRequires: libgudev1-devel >= %{systemd_version}
BuildRequires: gtk-doc
BuildRequires: systemd-devel
BuildRequires: lvm2-devel
BuildRequires: libudisks2-devel
BuildRequires: libxslt

BuildRequires: automake autoconf
BuildRequires: gnome-common

%description
XXX

%prep
%setup -q -n udisks-lvm-%{version}
autoreconf

%build
%configure
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%files
%doc README AUTHORS COPYING HACKING
/etc/dbus-1/system.d/com.redhat.lvm2.conf
/usr/lib/systemd/system/udisks-lvm.service
/usr/lib/udisks2/udisks-lvm-helper
/usr/lib/udisks2/udisksd-lvm
/usr/share/dbus-1/interfaces/com.redhat.lvm2.xml
/usr/share/dbus-1/system-services/com.redhat.lvm2.service
/usr/share/man/man8/udisksd-lvm.8.gz
/usr/share/polkit-1/actions/com.redhat.lvm2.policy
