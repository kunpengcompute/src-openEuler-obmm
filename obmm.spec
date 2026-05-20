Name:          obmm
Version:       1.0.1
Release:       2
Summary:       Runtime library for Huawei OBMM driver
License:       Mulan PSL v2

Source0: %{name}-%{version}.tar.gz
ExclusiveArch: aarch64
BuildRequires: kernel-headers
BuildRequires: make
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: cmake-filesystem

Obsoletes:      libobmm < %{version}-%{release}
Provides:       libobmm = %{version}-%{release}

%global debug_package %{nil}

%global soversion 1

%package devel
Summary:        Development files for Huawei OBMM driver
Requires:       %{name} = %{version}-%{release}
Obsoletes:      libobmm-devel < %{version}-%{release}
Provides:       libobmm-devel = %{version}-%{release}

%description
This package contains the OBMM library.

%description devel
This package contains the development files for Huawei OBMM driver

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
	-DCMAKE_INSTALL_PREFIX=%{_prefix}
%make_build

%install
cd build
%make_install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/libobmm.so.%{version}
%{_libdir}/libobmm.so.%{soversion}

%files devel
%defattr(-,root,root,-)
%{_includedir}/libobmm.h
%{_libdir}/libobmm.so

%changelog
* Wed May 20 2026 Yuhao Zhang <yuhao.zhang@huawei.com> - 1.0.1-2
- Rename package from libobmm to obmm
- Add Obsoletes and Provides for backward compatibility

* Thu Mar 26 2026 Yuhao Zhang <yuhao.zhang@huawei.com> - 1.0.1-1
- Update to v1.0.1 from upstream
- add syslog

* Tue Nov 18 2025 Wang Xin <wangxin667@h-partners.com> - 1.0-1
- init libobmm
