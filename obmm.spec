Name:          libobmm
Version:       1.0.1
Release:       1
Summary:       Runtime libobmm for Huawei OBMM driver
License:       GPLv2

Source0: %{name}-%{version}.tar.gz
ExclusiveArch: aarch64
BuildRequires: kernel-headers
BuildRequires: make
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: cmake-filesystem

%global debug_package %{nil}

%global soversion 1

%package devel
Summary:        Development files Huawei OBMM driver
Requires:       %{name} = %{version}-%{release}

%description
This package contains the OBMM library.

%description devel
This package contains the development files Huawei OBMM driver

%prep
%setup -n %{name}-%{version}

# Verify version consistency between spec and source code
SOURCE_VERSION=$(cat VERSION 2>/dev/null || echo "VERSION file not found")
if [ "$SOURCE_VERSION" != "%{version}" ]; then
    echo "ERROR: Version mismatch!"
    echo "  Spec Version: %{version}"
    echo "  Source VERSION file: $SOURCE_VERSION"
    echo "  Please update spec Version to match source code VERSION file."
    exit 1
fi
echo "Version check passed: %{version}"

%build
mkdir -p build
cd build

cmake ../src/libobmm \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir} \

make

%install
rm -rf %{buildroot}

cd build
make install DESTDIR=%{buildroot}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_libdir}/libobmm.so.%{version}
%{_libdir}/libobmm.so.%{soversion}

%files devel
%defattr(-,root,root,-)
%{_includedir}/libobmm.h
%{_libdir}/libobmm.so

%changelog
* Thu Mar 26 2026 Yuhao Zhang <yuhao.zhang@huawei.com> - 1.0.1-1
- Update to v1.0.1 from upstream
- add syslog

* Tue Nov 18 2025 Wang Xin <wangxin667@h-partners.com> - 1.0-1
- init libobmm
