#
# spec file for package zsh
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           zsh
Version:        4.3.11
Release:        1
License:        Other uncritical OpenSource License
Group:          System/Shells
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  ncurses-devel
BuildRequires:  libcap-devel
BuildRequires:  yodl
BuildRequires:  fdupes
PreReq:         %{install_info_prereq}
Url:            http://www.zsh.org
Source0:        %{name}-%{version}.tar.bz2
Source1:        zshrc
Source2:        zshenv
Source3:        _yast2
Source4:        _SuSEconfig
Source5:        _hwinfo
Source6:        _make
Source7:        zprofile
Source8:        _osc
Source9:        _zypper
# unused atm. we build the docs with yodl on our own.
Source20:       %{name}-%{version}-doc.tar.bz2
Patch0:         %{name}-%{version}-doc_makefile.patch
Patch1:         %{name}-%{version}-doc_intro_paths.patch
Patch2:         %{name}-%{version}-run-help_pager.patch
Patch3:         zsh-cleanup.patch
Patch4:         subst-crash.patch
Summary:        Shell with comprehensive completion
%define do_profiling 0

%description
Zsh is a UNIX command interpreter (shell) that resembles the Korn shell
(ksh). It is not completely compatible. It includes many enhancements,
notably in the command-line editor, options for customizing its
behavior, file name globbing, features to make C-shell (csh) users feel
at home, and extra features drawn from tcsh (another `custom' shell).
Zsh is well known for its command line completion.

Authors:
--------
    Paul Falstad

%prep
%setup -q
%patch0
%patch1
%patch2
%patch3
%patch4 -p1
# Fix bindir path in some files
perl -p -i -e 's|/usr/local/bin|%{_bindir}|' \
    Functions/Misc/zcalc Functions/Example/cat \
    Functions/Misc/checkmail Functions/Misc/run-help Misc/globtests \
    Misc/globtests.ksh Test/ztst.zsh Util/reporter Misc/lete2ctl \
    Util/check_exports Util/helpfiles 
# Get rid of /usr/princeton examples
perl -p -i -e 's|/usr/princeton|%{_bindir}|' \
    Doc/intro.ms

%build
export CC="gcc" CFLAGS="%{optflags} -pipe -fno-strict-aliasing"
# readd the site-* dir.
%configure \
    --enable-site-scriptdir=%{_datadir}/%{name}/site/scripts/ \
    --enable-site-fndir=%{_datadir}/%{name}/site/scripts/ \
    --enable-maildir-support \
    --with-tcsetpgrp \
    --enable-zsh-debug \
    --enable-cap \
    --enable-multibyte
# compiling with profiling data is default.
%if %do_profiling
# compile with profiling data writing enabled
make VERSION="%{version}" CFLAGS="$CFLAGS "%cflags_profile_generate \
     DLCFLAGS="-fPIC -fno-profile-arcs" LDFLAGS="-fprofile-arcs"
# this is needed to create the profiling data files *.gcda
make check
make clean
# compile with profiling data reading enabled and writing disabled
make VERSION="%{version}" CFLAGS="$CFLAGS "%cflags_profile_feedback \
     DLCFLAGS="-fPIC -fno-branch-probabilities" LDFLAGS="-fprofile-arcs"
make check
make clean
%else
make VERSION="%{version}"
%endif
# make html documentation
make -C Doc all zsh.info zsh_toc.html VERSION="%{version}"
# make help text files
mkdir -p Help
pushd Help/
troff -Tlatin1 -t -mandoc ../Doc/zshbuiltins.1 | \
	grotty -cbou | \
	sed -e 's/±/{+|-}/' | \
	../Util/helpfiles
popd
# generate intro.txt
groff Doc/intro.ms > intro.txt
# better name for html documentation
%{__mkdir} Doc/htmldoc/
%{__mv} Doc/*.html Doc/htmldoc
# remove some unwanted files in Etc/
%{__rm} -f Etc/Makefile* Etc/*.yo

%install
%makeinstall install.info VERSION="%{version}"
# install SUSE configuration
%{__install} -m 0755 -Dd  %{buildroot}/{etc,bin}
%{__install} -m 0644 %{S:1} %{S:2} %{S:7} %{buildroot}/etc
%{__install} -m 0644 %{S:3} %{S:4} %{S:5} %{S:6} %{S:8} %{S:9} %{buildroot}%{_datadir}/%{name}/%version/functions
# install help files
%{__install} -m 0755 -Dd    %{buildroot}%{_datadir}/%{name}/%{version}/help
%{__install} -m 0644 Help/* %{buildroot}%{_datadir}/%{name}/%{version}/help/
# link zsh binary
%{__mv} %{buildroot}%{_bindir}/zsh %{buildroot}/bin/zsh
%{__ln_s} -f ../../bin/zsh %{buildroot}/usr/bin/zsh
%fdupes $RPM_BUILD_ROOT

%clean
%{__rm} -rf %{buildroot}

%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%files
%defattr(-,root,root)
%doc Etc/* intro.txt Misc/compctl-examples Doc/htmldoc
%config(noreplace) /etc/zshrc
%config(noreplace) /etc/zshenv
%config(noreplace) /etc/zprofile
%{_bindir}/zsh
/bin/zsh
%{_libdir}/zsh/
%{_datadir}/zsh/
%{_infodir}/zsh.info*.gz
%{_mandir}/man1/zsh*.1.gz

%changelog
