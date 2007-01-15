#
# spec file for package zsh (Version 4.3.2)
#
# Copyright (c) 2006 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           zsh
Version:        4.3.2
Release:        1
License:        Other License(s), see package
Group:          System/Shells
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if %suse_version > 1000
BuildRequires:  libcap-devel
%else
BuildRequires:  libcap
%endif
BuildRequires:  yodl
PreReq:         %{install_info_prereq}
URL:            http://www.zsh.org
Source0:        %{name}-%{version}.tar.bz2
Source1:        zshrc
Source2:        zshenv
Source3:        _yast2
Source4:        _SuSEconfig
Source5:        _hwinfo
Source6:        _make
# unused atm. we build the docs with yodl on our own.
Source20:       %{name}-%{version}-doc.tar.bz2
Patch0:         %{name}-4.3.1.diff
Patch1:         %{name}-4.2.5-tailsyntax.diff
Patch2:         %{name}-4.3.1-91.diff
Summary:        Shell with comprehensive completion

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
%setup
%patch0
%patch1
%patch2

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
%{__ln_s} zsh.html Doc/htmldoc/index.html
# remove some unwanted files in Etc/
%{__rm} -f Etc/Makefile* Etc/*.yo

%install

%makeinstall install.info VERSION="%{version}"
# install SUSE configuration
%{__install} -m 0755 -Dd  %{buildroot}/{etc,bin}
%{__install} -m 0644 %{S:1} %{S:2} %{buildroot}/etc
%{__install} -m 0644 %{S:3} %{S:4} %{S:5} %{S:6} %{buildroot}%{_datadir}/%{name}/%version/functions
# install help files
%{__install} -m 0755 -Dd    %{buildroot}%{_datadir}/%{name}/help
%{__install} -m 0644 Help/* %{buildroot}%{_datadir}/%{name}/help/
# link zsh binary
%{__mv} %{buildroot}%{_bindir}/zsh %{buildroot}/bin/zsh
%{__ln_s} -f ../../bin/zsh %{buildroot}/usr/bin/zsh

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
%{_bindir}/zsh
/bin/zsh
%{_libdir}/zsh/
%{_datadir}/zsh/
%{_infodir}/zsh.info*.gz
%{_mandir}/man1/zsh*.1.gz

%changelog -n zsh
* Fri Jul 14 2006 - mskibbe@suse.de
- merged in patches from poeml (mruecker@suse.de)
- rediffed patches for -p0 (mruecker@suse.de)
- update to version 4.3.2 which (mruecker@suse.de)
  o fix two minor build problems
  o contains initial support for multibyte characters in the shell's line editor
- only require libcap for build on 10.0 and older (mruecker@suse.de)
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Sat Jan 14 2006 - schwab@suse.de
- Don't strip binaries.
* Mon Dec 05 2005 - hvogel@suse.de
- clean up specfile
- document profiling builds
* Mon Dec 05 2005 - mmj@suse.de
- Fix typo
* Mon Dec 05 2005 - mmj@suse.de
- Update to 4.2.6
* Wed Apr 06 2005 - mmj@suse.de
- Update to 4.2.5
* Tue Mar 15 2005 - mmj@suse.de
- Fix Makefile completion by using the _make from an older zsh
  version [#72875]
* Thu Feb 17 2005 - poeml@suse.de
- update yast2 completion to also complete *.ycp files
* Thu Feb 03 2005 - mmj@suse.de
- Update to 4.2.4
* Mon Jan 31 2005 - ro@suse.de
- adapt to texi2html changes
* Wed Jan 26 2005 - uli@suse.de
- run configure with --with-tcsetpgrp as suggested by the fail log
  (fixes s390*)
* Sat Jan 15 2005 - mmj@suse.de
- Update to zsh-4.2.3 which is a bugfix release not really affecting
  us, but better keep up to date
* Wed Jan 12 2005 - mmj@suse.de
- Update to zsh-4.2.2
* Mon Dec 20 2004 - poeml@suse.de
- fix yast2 completion to work without /sbin in PATH [#49374]
- fix yast2 and SuSEconfig completion to not show files from
  working directory
- update hwinfo completion
* Fri Aug 13 2004 - mmj@suse.de
- Update to zsh-4.2.1
* Wed Jul 28 2004 - ro@suse.de
- fix build of helpfiles after groff update
* Fri Mar 19 2004 - mmj@suse.de
- Update to zsh-4.2.0 final release
* Mon Mar 08 2004 - mmj@suse.de
- Update to zsh-4.2.0-pre-3
* Thu Feb 26 2004 - mmj@suse.de
- Update to zsh-4.2.0-pre-1
* Fri Jan 16 2004 - mmj@suse.de
- Use -fprofile-arcs when linking and -fno-strict-aliasing for
  compiling.
- Fix tail syntax
* Sat Oct 18 2003 - mmj@suse.de
- Fix neededforbuild
* Thu Oct 16 2003 - mmj@suse.de
- Don't build as root
- Cleanup specfile
* Tue Oct 14 2003 - jh@suse.de
- Fix profiling lockup.  (we can not profile dl_closed modules yet)
* Thu Jun 19 2003 - mmj@suse.de
- Update to 4.1.1
- Enable profiling
* Thu May 08 2003 - mmj@suse.de
- And do it even better, thanks Andreas Schwab.
* Thu May 08 2003 - mmj@suse.de
- Use a better way of unaliasing 'which'. Thanks Ingo Lameter.
* Thu Apr 24 2003 - ro@suse.de
- fix install_info --delete call and move from preun to postun
* Mon Apr 07 2003 - mmj@suse.de
- Only delete info entries when removing last version.
* Fri Feb 07 2003 - mmj@suse.de
- Use %%install_info macro
- Clean up build root
* Thu Jan 09 2003 - mmj@suse.de
- Set the important option 'nopromptcr' to not screw output.
* Mon Sep 16 2002 - mmj@suse.de
- Use BuildRoot
* Fri Aug 16 2002 - mmj@suse.de
- Move zsh binary to /bin [#17758]
- Use proper libdir
* Thu Aug 15 2002 - poeml@suse.de
- update completion for _yast{,2} and add one for _hwinfo
* Wed Aug 14 2002 - mmj@suse.de
- Update to 4.0.6 which was released this fast b/c a termcap /
  terminfo fix was forgotten together with a fix for _mount.
* Mon Aug 12 2002 - mmj@suse.de
- Update to 4.0.5 which includes a lot more completion, modules and
  bugfixes.
* Tue Jun 04 2002 - mmj@suse.de
- Added the html documentation from the ZSH team.
* Tue Apr 16 2002 - mmj@suse.de
- Fix to own %%{_defaultdocdir}/zsh
* Mon Mar 11 2002 - mmj@suse.de
- Comment out a completion that a lot of people find broken
* Fri Feb 22 2002 - mmj@suse.de
- Added yast2 and SuSEconfig completion from poeml@
* Wed Feb 13 2002 - stepan@suse.de
- remove .orig and .rej files from patch set.
* Wed Jan 30 2002 - mmj@suse.de
- Moved /etc/zshrc and /etc/zshenv to this package. This is ok b/c
  it is only specific zsh options.
* Thu Dec 13 2001 - mmj@suse.de
- Fix broken symlink from help/man1 -> ../Doc
* Sat Oct 27 2001 - mmj@suse.de
- Update to 4.0.4
* Thu Oct 25 2001 - mmj@suse.de
- Update to 4.0.3
* Tue Jun 26 2001 - mmj@suse.de
- Update to the newly released 4.0.2
* Sat Jun 02 2001 - mmj@suse.de
- Updated to the new stable release, zsh-4.0.1
- Fixed build prob on beta-i386 and beta-ia64
* Tue May 08 2001 - mfabian@suse.de
- bzip2 sources
* Sun Apr 15 2001 - schwab@suse.de
- Fix missing declarations.
* Fri Apr 13 2001 - mmj@suse.de
- Updated to 4.0.1-pre-3
* Wed Mar 14 2001 - mmj@suse.de
- Updated to 4.0.1-pre-2
* Sun Feb 18 2001 - mmj@suse.de
- Updated to 4.0.1-pre-1
* Fri Dec 15 2000 - werner@suse.de
- Update to 3.1.9-dev-8
* Fri Oct 06 2000 - kukuk@suse.de
- Change group tag
* Fri May 12 2000 - schwab@suse.de
- Update config files.
- Move docs to %%{_defaultdocdir}.
* Thu Jan 27 2000 - werner@suse.de
- New zsh version 3.1.6-dev-16
- Install html and info documentation
- Enable run-help help library
- Fix paths of perl and zsh scripts
- Enable command line history
- Enable command line complementation/correction
* Mon Dec 06 1999 - schwab@suse.de
- Fix errors from makeinfo
* Mon Sep 13 1999 - bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Tue Nov 17 1998 - bs@suse.de
- removed symlink /etc/zshrc -> profile (aaa_base contains a real zshrc now)
* Fri Oct 10 1997 - florian@suse.de
- update to version 3.0.5
* Mon Jun 23 1997 - florian@suse.de
- update to version 3.0.4
* Wed Jan 22 1997 - florian@suse.de
- update to version 3.0.2
* Thu Jan 02 1997 - florian@suse.de
- update to version 3.0.1
- added more documentation in binary package
* Thu Jan 02 1997 - florian@suse.de
  new version 3.0.0
