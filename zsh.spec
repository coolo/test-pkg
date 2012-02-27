#
# spec file for package zsh
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
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
Version:        4.3.17
Release:        0
Summary:        Shell with comprehensive completion
License:        MIT
Group:          System/Shells
Url:            http://www.zsh.org
Source0:        ftp://ftp.zsh.org/pub/zsh-%{version}.tar.bz2
Source1:        zshrc
Source2:        zshenv
Source3:        zprofile
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora_version}
Source11:       zlogin.rhs
Source12:       zlogout.rhs
Source13:       zprofile.rhs
Source14:       zshrc.rhs
Source15:       zshenv.rhs
Source16:       dotzshrc.rh
Source17:       zshprompt.pl
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version}
Requires(pre):  %{install_info_prereq}
%if 0%{?suse_version} >= 1110
BuildRequires:  fdupes
BuildRequires:  yodl
%endif
%else
Requires(pre):  /sbin/install-info
Requires(pre):  fileutils
Requires(pre):  grep
%endif

BuildRequires:  libcap-devel
BuildRequires:  ncurses-devel
BuildRequires:  pcre-devel
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora_version}
BuildRequires:  libtermcap-devel
BuildRequires:  tetex
BuildRequires:  texi2html
BuildRequires:  texinfo
%endif

%description
Zsh is a UNIX command interpreter (shell) that resembles the Korn shell
(ksh). It is not completely compatible. It includes many enhancements,
notably in the command-line editor, options for customizing its
behavior, file name globbing, features to make C-shell (csh) users feel
at home, and extra features drawn from tcsh (another `custom' shell).
Zsh is well known for its command line completion.

%package htmldoc

Summary:        Zsh shell manual in html format
Group:          System/Shells
Provides:       %{name}-html = %{version}
Obsoletes:      %{name}-html < %{version}

%description htmldoc
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

This package contains the Zsh manual in html format.

%prep
%setup -q -n %{name}-%{version}

# Remove executable bit
chmod 0644 Etc/changelog2html.pl

%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora_version}
  cp -p %{SOURCE17} .
%endif

# Fix bindir path in some files
perl -p -i -e 's|/usr/local/bin|%{_bindir}|' \
    Doc/intro.ms Misc/globtests.ksh Misc/globtests \
    Misc/lete2ctl Util/check_exports Util/helpfiles \
    Util/reporter

%build
%configure \
    --enable-site-scriptdir=%{_datadir}/%{name}/site/scripts/ \
    --enable-site-fndir=%{_datadir}/%{name}/site/scripts/ \
    --enable-maildir-support \
    --with-tcsetpgrp \
    --enable-cap \
    --enable-multibyte \
    --enable-pcre \
%if 0%{?suse_version} >= 1220
    --with-term-lib="ncursesw tinfo" \
%else
    --with-term-lib="ncursesw" \
%endif
    --enable-cflags="%{optflags} %(ncursesw6-config --cflags)" \
    --enable-ldflags="%(ncursesw6-config --libs)"

make all info html

# make help text files
install -d Help
pushd Help/
troff -Tlatin1 -t -mandoc ../Doc/zshbuiltins.1 | \
	grotty -cbou | \
	sed -e 's/±/{+|-}/' | \
	../Util/helpfiles
popd

# generate intro.ps
groff -Tps -ms Doc/intro.ms > intro.ps

# better name for html documentation
install -d -m 0755 Doc/htmldoc/
mv Doc/*.html Doc/htmldoc

# remove some unwanted files in Etc/
rm -f Etc/Makefile* Etc/*.yo

%install
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora_version}
    rm -rf %{buildroot}
%endif

%if 0%{?suse_version}
%makeinstall install.info
%else
  make DESTDIR=%{buildroot} install install.info
%endif

install -m 0755 -Dd  %{buildroot}/{etc,bin}

%if 0%{?suse_version}
# install SUSE configuration
install -m 0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{buildroot}%{_sysconfdir}

# Create custom completion directory
mkdir %{buildroot}%{_sysconfdir}/zsh_completion.d
%endif

%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora_version}
# install RHEL || CentOS || Fedora configuration
for i in zlogin zlogout zprofile zshrc zshenv; do
  install -m 0644 $RPM_SOURCE_DIR/${i}.rhs %{buildroot}%{_sysconfdir}/$i
  install -D -m 0644 %{SOURCE16} %{buildroot}%{_sysconfdir}/skel/.zshrc
done
%endif

# install help files
install -m 0755 -Dd    %{buildroot}%{_datadir}/%{name}/%{version}/help
install -m 0644 Help/* %{buildroot}%{_datadir}/%{name}/%{version}/help/

# link zsh binary
ln -sf %{_bindir}/zsh %{buildroot}/bin/zsh

# Remove versioned zsh binary
rm -f %{buildroot}%{_bindir}/zsh-*

%if 0%{?suse_version} >= 1110
%fdupes %{buildroot}
%endif

%check
%if 0%{?suse_version}
make check
%else
# FixMe: sometimes failing Test
#+ fn:echo:2: write error: broken pipe
#+ fn:2: write error: inappropriate ioctl for device
mv Test/E01options.ztst Test/E01options.ztst.mvd
%ifarch s390 s390x ppc ppc64
  ( cd Test
    mkdir skipped
    mv Y*.ztst skipped )
%endif
  ZTST_verbose=0 make test
%endif

%preun
%if 0%{?suse_version}
  :
%else
  if [ "$1" = 0 ] ; then
    /sbin/install-info --delete %{_infodir}/zsh.info.gz %{_infodir}/dir \
      --entry="* zsh: (zsh).                  An enhanced bourne shell."
  fi
%endif

%post
%if 0%{?suse_version}
  %install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz
%else
if [ ! -f %{_sysconfdir}/shells ]; then
  echo "%{_bindir}/zsh" > %{_sysconfdir}/shells
else
  grep -q "^%{_bindir}/zsh$" %{_sysconfdir}/shells || echo "%{_bindir}/zsh" >> %{_sysconfdir}/shells
fi

/sbin/install-info %{_infodir}/zsh.info.gz %{_infodir}/dir \
  --entry="* zsh: (zsh).                  An enhanced bourne shell."
%endif

%postun
%if 0%{?suse_version}
  %install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz
%else
  if [ "$1" = 0 ] ; then
    if [ -f %{_sysconfdir}/shells ] ; then
      TmpFile=`%{_bindir}/mktemp /tmp/.zshrpmXXXXXX`
      grep -v '^%{_bindir}/zsh$' %{_sysconfdir}/shells > $TmpFile
      cp -f $TmpFile %{_sysconfdir}/shells
      rm -f $TmpFile
      chmod 644 %{_sysconfdir}/shells
    fi
  fi
%endif

%files
%defattr(-,root,root)
%doc ChangeLog FEATURES LICENCE MACHINES META-FAQ NEWS README
%doc Etc/* intro.ps Misc/compctl-examples

%config(noreplace) %{_sysconfdir}/zshrc
%config(noreplace) %{_sysconfdir}/zshenv
%config(noreplace) %{_sysconfdir}/zprofile
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora_version}
%config(noreplace) %{_sysconfdir}/zlogin
%config(noreplace) %{_sysconfdir}/zlogout
%config(noreplace) %{_sysconfdir}/skel/.zshrc
%endif

%if 0%{?suse_version}
%dir %{_sysconfdir}/zsh_completion.d
%endif

%{_bindir}/zsh
/bin/zsh
%{_libdir}/zsh/
%{_datadir}/zsh/
%{_infodir}/zsh.info*.gz
%{_mandir}/man1/zsh*.1.gz

%files htmldoc
%defattr(-,root,root)
%doc Doc/htmldoc/*

%changelog
