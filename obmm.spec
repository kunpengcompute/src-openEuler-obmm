Name:          libobmm
Version:       1.0
Release:       1
Summary:       Runtime libobmm for Huawei OBMM driver
License:       GPLv2

Source0: %{name}.tar.gz
ExclusiveArch: aarch64
BuildRequires: kernel-headers
BuildRequires: make
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: cmake-filesystem

%global debug_package %{nil}

%package devel
Summary:        Development files Huawei OBMM driver
Requires:       %{name} = %{version}-%{release}

%description
This package contains the OBMM library.

%description devel
This package contains the development files Huawei OBMM driver

%prep
%setup -c -n obmm

%build
cd src/libobmm
cmake -DCMAKE_INSTALL_PREFIX:PATH=build .
make
make install

%install
rm -rf %{buildroot}
mkdir -p -m755 %{buildroot}%{_libdir}
mkdir -p -m755 %{buildroot}%{_includedir}

install -m 0755 src/libobmm/build/lib/libobmm.so.1.0.1 %{buildroot}%{_libdir}/libobmm.so.1.0.1
install -m 0644 src/libobmm/libobmm.h %{buildroot}%{_includedir}/
ln -sf libobmm.so.1 %{buildroot}%{_libdir}/libobmm.so
ln -sf libobmm.so.1.0.1 %{buildroot}%{_libdir}/libobmm.so.1

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_libdir}/libobmm.so.1
%{_libdir}/libobmm.so.1.0.1

%files devel
%defattr(-,root,root,-)
%{_includedir}/libobmm.h
%{_libdir}/libobmm.so

%changelog
* Tue Nov 18 2025 Wang Xin <wangxin667@h-partners.com> - 1.0-1
- init libobmm