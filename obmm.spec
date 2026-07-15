Name:          obmm
Version:       1.0
Release:       3%{?dist}
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

Patch0001: backport-fix-remove-unused-parameter-warnings-in-vendor_adapt.patch
Patch0002: backport-feat-add-syslog-logging-for-OBMM-operations.patch
Patch0003: backport-refactor-improve-logging-placement-and-eliminate-mag.patch
Patch0004: backport-fix-address-code-quality-issues-in-logging-module.patch
Patch0005: backport-feat-assign-versions-in-the-spec.patch
Patch0006: backport-fix-update-documentation-and-unify-logging.patch
Patch0007: backport-fix-normalize-return-values-and-errno-handling.patch
Patch0008: backport-refactor-implement-automatic-version-management-for-.patch
Patch0009: backport-refactor-remove-unused-includes-and-deduplicate-CNA-.patch

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
* Wed Jul 15 2026 zhaolichang <943677312@qq.com> - 1.0-3
- [Type] sync
- [Desc] Package init
