# Originally from https://raw.github.com/seveas/go.rpm/master/go.spec

# tweaked to work with go 1.5.3

# To build:
#
# sudo yum -y install rpmdevtools ed bison mercurial && rpmdev-setuptree
#
# wget https://raw.github.com/jhsimpson/archivematica-specs/master/go.spec -O ~/rpmbuild/SPECS/go.spec
# wget https://go.googlecode.com/files/go1.5.3.src.tar.gz -O ~/rpmbuild/SOURCES/go1.5.3.src.tar.gz
#
# rpmbuild -bb ~/rpmbuild/SPECS/go.spec

Name:          go
Version:       1.5.3
Release:       1%{?dist}
Summary:       Go compiler and tools
Group:         Development/Languages
License:       BSD
URL:           http://golang.org/
Source0:       https://storage.googleapis.com/golang/go1.5.3.src.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ed
BuildRequires: bison
BuildRequires: mercurial
Provides:      golang


%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global debug_package %{nil}
%global __spec_install_post /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot  \
  /usr/lib/rpm/brp-compress

%ifarch %ix86
    %global GOARCH 386
%endif
%ifarch    x86_64
    %global GOARCH amd64
%endif

%description
Go is a systems programming language that aims to be both fast and convenient.

%prep
%setup -q -n go

%build
GOSRC="$(pwd)"
GOROOT="$(pwd)"
GOROOT_FINAL=%{_libdir}/go
GOOS=linux
GOBIN="$GOROOT/bin"
GOARCH="%{GOARCH}"
export GOARCH GOROOT GOOS GOBIN GOROOT_FINAL
export MAKE=%{__make}

mkdir -p "$GOBIN"
cd src

LC_ALL=C PATH="$PATH:$GOBIN" ./make.bash

%install
rm -rf %{buildroot}

GOROOT_FINAL=%{_libdir}/go
GOROOT="%{buildroot}%{_libdir}/go"
GOOS=linux
GOBIN="$GOROOT/bin"
GOARCH="%{GOARCH}"
export GOARCH GOROOT GOOS GOBIN GOROOT_FINAL

mkdir -p $GOROOT/{misc,lib,src}
mkdir -p %{buildroot}%{_bindir}/

cp -ar pkg lib bin $GOROOT
cp -ar src/cmd $GOROOT/src
cp -ar misc/cgo $GOROOT/misc

ln -sf %{_libdir}/go/bin/go %{buildroot}%{_bindir}/go
ln -sf %{_libdir}/go/bin/godoc %{buildroot}%{_bindir}/godoc
ln -sf %{_libdir}/go/bin/gofmt %{buildroot}%{_bindir}/gofmt

ln -sf %{_libdir}/go/pkg/tool/linux_%{GOARCH}/cgo %{buildroot}%{_bindir}/cgo
ln -sf %{_libdir}/go/pkg/tool/linux_%{GOARCH}/ebnflint %{buildroot}%{_bindir}/ebnflint

%ifarch %ix86
for tool in 8a 8c 8g 8l; do
%else
for tool in 6a 6c 6g 6l; do
%endif
ln -sf %{_libdir}/go/pkg/tool/linux_%{GOARCH}/$tool %{buildroot}%{_bindir}/$tool
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS CONTRIBUTORS LICENSE doc/*
%{_libdir}/go
%ifarch %ix86
%{_bindir}/8*
%else
%{_bindir}/6*
%endif
%{_bindir}/cgo
%{_bindir}/ebnflint
%{_bindir}/go*

%changelog
* Mon Feb 15 2016 Justin Simpson <jsimpson@artefactual.com> - 1.5.3
- First attempt at 1.5.3 rpm
* Tue Aug 13 2013 Nathan Milford <nathan@milford.io> - 1.2
- Bumped to 1.2.
