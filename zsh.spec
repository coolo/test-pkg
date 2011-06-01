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



Name:           zsh
Version:        4.3.12
Release:        1
License:        BSD
Summary:        Shell with comprehensive completion
Url:            http://www.zsh.org
Group:          System/Shells
Source0:        %{name}-%{version}.tar.bz2
Source1:        zshrc
Source2:        zshenv
Source3:        zprofile
Patch1:         %{name}-%{version}-disable-c02cond-test.patch
BuildRequires:  fdupes
BuildRequires:  libcap-devel
BuildRequires:  ncurses-devel
BuildRequires:  yodl
PreReq:         %{install_info_prereq}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Zsh is a UNIX command interpreter (shell) that resembles the Korn shell
(ksh). It is not completely compatible. It includes many enhancements,
notably in the command-line editor, options for customizing its
behavior, file name globbing, features to make C-shell (csh) users feel
at home, and extra features drawn from tcsh (another `custom' shell).
Zsh is well known for its command line completion.

%prep
%setup -q
%patch1

# Fix bindir path in some files
perl -p -i -e 's|/usr/local/bin|%{_bindir}|' \
    Doc/intro.ms Misc/globtests.ksh Misc/globtests \
    Misc/lete2ctl Util/check_exports Util/helpfiles \
    Util/reporter

%build
# readd the site-* dir.
%configure \
    --enable-site-scriptdir=%{_datadir}/%{name}/site/scripts/ \
    --enable-site-fndir=%{_datadir}/%{name}/site/scripts/ \
    --enable-maildir-support \
    --with-tcsetpgrp \
    --enable-cap \
    --enable-multibyte

make

# make html documentation
make -C Doc all zsh.info zsh_toc.html

# make help text files
mkdir -p Help
pushd Help/
troff -Tlatin1 -t -mandoc ../Doc/zshbuiltins.1 | \
	grotty -cbou | \
	sed -e 's/±/{+|-}/' | \
	../Util/helpfiles
popd

# generate intro.ps
groff -Tps -ms Doc/intro.ms > intro.ps

# better name for html documentation
mkdir Doc/htmldoc/
mv Doc/*.html Doc/htmldoc

# remove some unwanted files in Etc/
rm -f Etc/Makefile* Etc/*.yo

%install
%makeinstall install.info

# install SUSE configuration
install -m 0755 -Dd  %{buildroot}/{etc,bin}
install -m 0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{buildroot}/etc

# install help files
install -m 0755 -Dd    %{buildroot}%{_datadir}/%{name}/%{version}/help
install -m 0644 Help/* %{buildroot}%{_datadir}/%{name}/%{version}/help/

# link zsh binary
mv %{buildroot}%{_bindir}/zsh %{buildroot}/bin/zsh
ln -s -f ../../bin/zsh %{buildroot}%{_bindir}/zsh

# Remove versioned zsh binary
rm -f %{buildroot}%{_bindir}/zsh-*

%fdupes %{buildroot}

%check
make check

%clean
rm -rf %{buildroot}

%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%files
%defattr(-,root,root)
%doc Etc/* intro.ps Misc/compctl-examples Doc/htmldoc
%config(noreplace) %{_sysconfdir}/zshrc
%config(noreplace) %{_sysconfdir}/zshenv
%config(noreplace) %{_sysconfdir}/zprofile
%{_bindir}/zsh
/bin/zsh
%{_libdir}/zsh/
%{_datadir}/zsh/
%{_infodir}/zsh.info*.gz
%{_mandir}/man1/zsh*.1.gz

%changelog
