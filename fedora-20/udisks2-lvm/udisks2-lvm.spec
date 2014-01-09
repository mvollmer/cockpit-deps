Summary: Disk Manager, LVM addon
Name: udisks2-lvm
Version: 1.99.0
Release: 1%{?dist}
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
/
