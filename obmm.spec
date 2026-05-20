Name:          obmm
Version:       1.0
Release:       3
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

# mainline patches 6000
Patch6001: backport-fix-remove-unused-parameter-warnings-in-vendor_adapt.patch
Patch6002: backport-feat-add-syslog-logging-for-OBMM-operations.patch
Patch6003: backport-refactor-improve-logging-placement-and-eliminate-mag.patch
Patch6004: backport-fix-address-code-quality-issues-in-logging-module.patch
Patch6005: backport-feat-assign-versions-in-the-spec.patch
Patch6006: backport-fix-update-documentation-and-unify-logging.patch
Patch6007: backport-fix-normalize-return-values-and-errno-handling.patch
Patch6008: backport-refactor-implement-automatic-version-management-for-.patch
Patch6009: backport-refactor-remove-unused-includes-and-deduplicate-CNA-.patch

# extra patches 9000
%global debug_package %{nil}

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
%setup -c -n %{name}-%{version}
# Fix CRLF line endings in source files before applying patches
find . -type f \( -name "*.c" -o -name "*.h" -o -name "*.txt" \) | xargs -r sed -i 's/\r$//'
%autopatch -p1

%build
cd src/libobmm
cmake -DCMAKE_INSTALL_PREFIX:PATH=build .
%make_build
make install

%install
rm -rf %{buildroot}
mkdir -p -m755 %{buildroot}%{_libdir}
mkdir -p -m755 %{buildroot}%{_includedir}

# This release version keeps the SO name hardcoded, it will be fixed in the next release version.
install -m 0755 src/libobmm/build/lib64/libobmm.so.1.0.1 %{buildroot}%{_libdir}/libobmm.so.1.0.1
install -m 0644 src/libobmm/libobmm.h %{buildroot}%{_includedir}/
ln -sf libobmm.so.1 %{buildroot}%{_libdir}/libobmm.so
ln -sf libobmm.so.1.0.1 %{buildroot}%{_libdir}/libobmm.so.1

%files
%defattr(-,root,root,-)
%{_libdir}/libobmm.so.1
%{_libdir}/libobmm.so.1.0.1

%files devel
%defattr(-,root,root,-)
%{_includedir}/libobmm.h
%{_libdir}/libobmm.so

%changelog
* Wed May 20 2026 Yuhao Zhang <yuhao.zhang@huawei.com> - 1.0-3
- Rename package from libobmm to obmm
- Fix License from GPLv2 to Mulan PSL v2
- Use %make_build macro
- Remove redundant %clean section
- Add Obsoletes and Provides for backward compatibility

* Thu Mar 12 2026 Yuhao Zhang <yuhao.zhang@huawei.com> - 1.0-2
- add syslog logging for OBMM operations.
- reassign obmm package version.
- minor fixes for the code format.
- normalize return values.

* Tue Nov 18 2025 Wang Xin <wangxin667@h-partners.com> - 1.0-1
- init libobmm
