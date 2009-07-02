#
# spec file for package bash (Version 4.0)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
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



Name:           bash
BuildRequires:  bison fdupes ncurses-devel
License:        GPL v2 or later
Group:          System/Shells
%define         bash_vers 4.0
%define         rl_vers   6.0
Recommends:     bash-doc = %bash_vers
Recommends:     bash-lang = %bash_vers
Suggests:       command-not-found
AutoReqProv:    on
Version:        4.0
Release:        12
Summary:        The GNU Bourne-Again Shell
Url:            http://www.gnu.org/software/bash/bash.html
Source0:        ftp://ftp.gnu.org/gnu/bash/bash-%{bash_vers}.tar.bz2
Source1:        ftp://ftp.gnu.org/gnu/readline/readline-%{rl_vers}.tar.bz2
Source2:        bash-%{bash_vers}-patches.tar.bz2
Source3:        readline-%{rl_vers}-patches.tar.bz2
Source4:        run-tests
Source5:        dot.bashrc
Source6:        dot.profile
Source7:        bash-rpmlintrc
Patch0:         bash-%{bash_vers}.dif
Patch1:         bash-2.03-manual.patch
Patch2:         bash-4.0-security.patch
Patch3:         bash-3.2-2.4.4.patch
Patch4:         bash-3.0-evalexp.patch
Patch5:         bash-3.0-warn-locale.patch
Patch6:         bash-3.0-nfs_redir.patch
Patch7:         bash-3.0-decl.patch
Patch9:         bash-4.0-extended_quote.patch
Patch10:        bash-3.2-printf.patch
Patch11:        bash-4.0-loadables.dif
Patch14:        bash-3.2-sigrestart.patch
Patch15:        bash-3.2-longjmp.dif
Patch16:        bash-4.0-setlocale.dif
Patch17:        bash-4.0-headers.dif
Patch20:        readline-%{rl_vers}.dif
Patch21:        readline-4.3-input.dif
Patch22:        readline-6.0-wrap.patch
Patch23:        readline-5.2-conf.patch
Patch30:        readline-6.0-destdir.patch
Patch40:        bash-4.0.10-typo.patch
Patch41:        bash-4.0.24-globstar-nulldir.patch
Patch42:        bash-4.0.24-acl.dif
Patch43:        bash-4.0.24-memleak-read.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%global         _sysconfdir /etc
%global         _incdir     %{_includedir}
%global         _ldldir     /%{_lib}/bash
%global         _minsh      0
%{expand:       %%global rl_major %(echo %{rl_vers} | sed -r 's/.[0-9]+//g')}

%description
Bash is an sh-compatible command interpreter that executes commands
read from standard input or from a file.  Bash incorporates useful
features from the Korn and C shells (ksh and csh).  Bash is intended to
be a conformant implementation of the IEEE Posix Shell and Tools
specification (IEEE Working Group 1003.2).



Authors:
--------
    Brian Fox <bfox@gnu.org>
    Chet Ramey <chet@ins.cwru.edu>

%package -n bash-doc
License:        GPL v2 or later
Summary:        Documentation how to Use the GNU Bourne-Again Shell
Group:          Documentation/Man
Provides:       bash:%{_infodir}/bash.info.gz
PreReq:         %install_info_prereq
Version:        4.0
Release:        12
AutoReqProv:    on

%description -n bash-doc
This package contains the documentation for using the bourne shell
interpreter Bash.



Authors:
--------
    Brian Fox <bfox@gnu.org>
    Chet Ramey <chet@ins.cwru.edu>

%lang_package(bash)
%package -n bash-devel
License:        GPL v2 or later
Summary:        Include Files mandatory for Development of bash loadable builtins
Group:          Development/Languages/C and C++
Version:        4.0
Release:        1
AutoReqProv:    on

%description -n bash-devel
This package contains the C header files for writing loadable new
builtins for the interpreter Bash. Use -I /usr/include/bash/<version>
on the compilers command line.



Authors:
--------
    Brian Fox <bfox@gnu.org>
    Chet Ramey <chet@ins.cwru.edu>

%package -n bash-loadables
License:        GPL v2 or later
Summary:        Loadable bash builtins
Group:          System/Shells
Version:        4.0
Release:        1
AutoReqProv:    on

%description -n bash-loadables
This package contains the examples for the ready-to-dynamic-load
builtins found in the source tar ball of the bash:

basename      Return non-directory portion of pathname.

cut	      cut(1) replacement.

dirname       Return directory portion of pathname.

finfo	      Print file info.

getconf       POSIX.2 getconf utility.

head	      Copy first part of files.

id	      POSIX.2 user identity.

ln	      Make links.

logname       Print login name of current user.

mkdir	      Make directories.

pathchk       Check pathnames for validity and portability.

print	      Loadable ksh-93 style print builtin.

printenv      Minimal builtin clone of BSD printenv(1).

push	      Anyone remember TOPS-20?

realpath      Canonicalize pathnames, resolving symlinks.

rmdir	      Remove directory.

sleep	      sleep for fractions of a second.

strftime      Loadable builtin interface to strftime(3).

sync	      Sync the disks by forcing pending filesystem writes to
complete.

tee	      Duplicate standard input.

tty	      Return terminal name.

uname	      Print system information.

unlink	      Remove a directory entry.

whoami	      Print out username of current user.



Authors:
--------
    Brian Fox <bfox@gnu.org>
    Chet Ramey <chet@ins.cwru.edu>

%package -n libreadline6
License:        GPL v2 or later
Summary:        The Readline Library
Group:          System/Libraries
Provides:       bash:/%{_lib}/libreadline.so.%{rl_major}
Version:        6.0
Release:        12
Recommends:     readline-doc = %{version}
# bug437293
%ifarch ppc64
Obsoletes:      readline-64bit
%endif
#
Provides:       readline =  6.0
Obsoletes:      readline <= 6.0
AutoReqProv:    on

%description -n libreadline6
The readline library is used by the Bourne Again Shell (bash, the
standard command interpreter) for easy editing of command lines.  This
includes history and search functionality.



Authors:
--------
    Brian Fox <bfox@gnu.org>
    Chet Ramey <chet@ins.cwru.edu>

%package -n readline-devel
License:        GPL v2 or later
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries/C and C++
Provides:       bash:%{_libdir}/libreadline.a
Version:        6.0
Release:        12
Requires:       libreadline6 = %{version}
Requires:       ncurses-devel
Recommends:     readline-doc = %{version}
AutoReqProv:    on
# bug437293
%ifarch ppc64
Obsoletes:      readline-devel-64bit
%endif
#

%description -n readline-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.



Authors:
--------
    Brian Fox <bfox@gnu.org>
    Chet Ramey <chet@ins.cwru.edu>

%package -n readline-doc
License:        GPL v2 or later
Summary:        Documentation how to Use and Program with the Readline Library
Group:          System/Libraries
Provides:       readline:%{_infodir}/readline.info.gz
PreReq:         %install_info_prereq
Version:        6.0
Release:        12
AutoReqProv:    on

%description -n readline-doc
This package contains the documentation for using the readline library
as well as programming with the interface of the readline library.



Authors:
--------
    Brian Fox <bfox@gnu.org>
    Chet Ramey <chet@ins.cwru.edu>

%prep
%setup -q -n bash-%{bash_vers} -b1 -b2 -b3
for p in ../bash-%{bash_vers}-patches/*; do
    test -e $p || break
    echo Patch $p
    patch -s -p0 < $p
done
unset p
%patch1  -p0 -b .manual
%patch2  -p0 -b .security
%patch3  -p0 -b .2.4.4
%patch4  -p0 -b .evalexp
%patch5  -p0 -b .warnlc
%patch6  -p0 -b .nfs_redir
%patch7  -p0 -b .decl
%patch9  -p0 -b .extended_quote
%patch10 -p0 -b .printf
%patch11 -p0 -b .plugins
%patch14 -p0 -b .sigrestart
%patch15 -p0 -b .longjmp
%patch16 -p0 -b .setlocale
%patch17 -p0 -b .headers
%patch21 -p0 -b .zerotty
%patch22 -p0 -b .wrap
%patch23 -p0 -b .conf
%patch40 -p0 -b .typo
%patch41 -p0 -b .globstar
%patch42 -p0 -b .acl
%patch43 -p0 -b .leak
%patch0  -p0
cd ../readline-%{rl_vers}
for p in ../readline-%{rl_vers}-patches/*; do
    test -e $p || break
    echo Patch $p
    patch -s -p0 < $p
done
%patch21 -p2 -b .zerotty
%patch22 -p2 -b .wrap
%patch23 -p2 -b .conf
%patch30 -p0 -b .destdir
%patch20 -p0

%build
  LANG=POSIX
  LC_ALL=$LANG
  unset LC_CTYPE
  CPU=$(uname -m 2> /dev/null)
  HOSTTYPE=${CPU}
  MACHTYPE=${CPU}-suse-linux
  export LANG LC_ALL HOSTTYPE MACHTYPE
cd ../readline-%{rl_vers}
%{?suse_update_config:%{suse_update_config -f support}}
  autoconf
  cflags ()
  {
      local flag=$1; shift
      case "${RPM_OPT_FLAGS}" in
      *${flag}*) return
      esac
      if test -n "$1" && gcc -Werror $flag -S -o /dev/null -xc   /dev/null > /dev/null 2>&1 ; then
	  local var=$1; shift
	  eval $var=\${$var:+\$$var\ }$flag
      fi
  }
  echo 'int main () { return !(sizeof(void*) >= 8); }' | gcc -x c -o test64 -
  if ./test64 ; then
      LARGEFILE=""
  else
      LARGEFILE="-D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
  fi
  rm -f ./test64
  CFLAGS="$RPM_OPT_FLAGS $LARGEFILE -D_GNU_SOURCE -DRECYCLES_PIDS -Wall -g"
  LDFLAGS=""
  cflags -std=gnu89              CFLAGS
  cflags -Wuninitialized         CFLAGS
  cflags -Wextra                 CFLAGS
  cflags -Wno-unprototyped-calls CFLAGS
  cflags -Wno-switch-enum        CFLAGS
  cflags -Wno-unused-variable    CFLAGS
  cflags -Wno-unused-parameter   CFLAGS
  cflags -ftree-loop-linear      CFLAGS
  cflags -pipe                   CFLAGS
  cflags -Wl,--as-needed         LDFLAGS
  cflags -Wl,-O2                 LDFLAGS
  cflags -Wl,--hash-size=16699   LDFLAGS
  cflags -Wl,-rpath,%{_ldldir}/%{bash_vers}   LDFLAGS
  CC=gcc
  CC_FOR_BUILD="$CC"
  CFLAGS_FOR_BUILD="$CFLAGS"
  LDFLAGS_FOR_BUILD="$LDFLAGS"
  export CC_FOR_BUILD CFLAGS_FOR_BUILD LDFLAGS_FOR_BUILD CFLAGS LDFLAGS CC
  ./configure --build=%{_target_cpu}-suse-linux	\
	--prefix=%{_prefix}			\
	--with-curses			\
	--mandir=%{_mandir}		\
	--infodir=%{_infodir}		\
	--libdir=%{_libdir}
  make
  make documentation
  ln -sf shlib/libreadline.so.%{rl_vers} libreadline.so
  ln -sf shlib/libreadline.so.%{rl_vers} libreadline.so.%{rl_major}
  ln -sf shlib/libhistory.so.%{rl_vers} libhistory.so
  ln -sf shlib/libhistory.so.%{rl_vers} libhistory.so.%{rl_major}
cd ../bash-%{bash_vers}
  # /proc is required for correct configuration
  test -d /dev/fd || { echo "/proc is not mounted!" >&2; exit 1; }
  ln -sf ../readline-%{rl_vers} readline
  export LD_LIBRARY_PATH=$PWD/../readline-%{rl_vers}
  CC="gcc -I$PWD -L$PWD/../readline-%{rl_vers}"
%if %_minsh
  cflags -Os CFLAGS
# cflags -U_FORTIFY_SOURCE CFLAGS
# cflags -funswitch-loops CFLAGS
# cflags -ftree-loop-im CFLAGS
# cflags -ftree-loop-ivcanon CFLAGS
# cflags -fprefetch-loop-arrays CFLAGS
# cflags -fno-stack-protector CFLAGS
# cflags -fno-unwind-tables CFLAGS
# cflags -fno-asynchronous-unwind-tables CFLAGS
%endif
  CC_FOR_BUILD="$CC"
  CFLAGS_FOR_BUILD="$CFLAGS"
  export CC_FOR_BUILD CFLAGS_FOR_BUILD CFLAGS LDFLAGS CC
%{?suse_update_config:%{suse_update_config -f support}}
  autoconf
  #
  # We have a malloc with our glibc
  #
  SYSMALLOC="
	--without-gnu-malloc
	--without-bash-malloc
  "
  #
  # System readline library (comment out it not to be used)
  #
  READLINE="
	--with-installed-readline
  "
  bash support/mkconffiles -v
%if %_minsh
  ./configure --build=%{_target_cpu}-suse-linux	\
	--prefix=%{_prefix}		\
	--mandir=%{_mandir}		\
	--infodir=%{_infodir}		\
	--libdir=%{_libdir}		\
	--with-curses			\
	--with-afs			\
	$SYSMALLOC			\
	--enable-minimal-config		\
	--enable-arith-for-command	\
	--enable-array-variables	\
	--enable-brace-expansion	\
	--enable-casemod-attributes	\
	--enable-casemod-expansion	\
	--enable-command-timing		\
	--enable-cond-command		\
	--enable-cond-regexp		\
	--enable-coprocesses		\
	--enable-directory-stack	\
	--enable-dparen-arithmetic	\
	--enable-extended-glob		\
	--enable-job-control		\
	--enable-net-redirections	\
	--enable-process-substitution	\
	--disable-strict-posix-default	\
	--enable-separate-helpfiles=%{_datadir}/bash/helpfiles \
	$READLINE
  make Program=sh sh
  make distclean
%endif
  ./configure --build=%{_target_cpu}-suse-linux	\
	--prefix=%{_prefix}		\
	--mandir=%{_mandir}		\
	--infodir=%{_infodir}		\
	--libdir=%{_libdir}		\
	--with-curses			\
	--with-afs			\
	$SYSMALLOC			\
	--enable-job-control		\
	--enable-alias			\
	--enable-readline		\
	--enable-history		\
	--enable-bang-history		\
	--enable-directory-stack	\
	--enable-process-substitution	\
	--enable-prompt-string-decoding	\
	--enable-select			\
	--enable-help-builtin		\
	--enable-array-variables	\
	--enable-brace-expansion	\
	--enable-command-timing		\
	--enable-disabled-builtins	\
	--disable-strict-posix-default	\
	--enable-separate-helpfiles=%{_datadir}/bash/helpfiles \
	$READLINE
  make %{?do_profiling:CFLAGS="$CFLAGS %cflags_profile_generate"} \
      all printenv recho zecho xcase
  env -i HOME=$PWD TERM=$TERM LD_LIBRARY_PATH=$LD_LIBRARY_PATH make TESTSCRIPT=%{SOURCE4} check
  make %{?do_profiling:CFLAGS="$CFLAGS %cflags_profile_feedback" clean} all
  make -C examples/loadables/
  make documentation

%install
cd ../readline-%{rl_vers}
  make install htmldir=%{_defaultdocdir}/readline \
	       installdir=%{_defaultdocdir}/readline/examples DESTDIR=%{buildroot}
  make install-shared libdir=/%{_lib} linkagedir=%{_libdir} DESTDIR=%{buildroot}
  rm -rf %{buildroot}%{_defaultdocdir}/bash
  mkdir -p %{buildroot}%{_defaultdocdir}/bash
  chmod 0755 %{buildroot}/%{_lib}/libhistory.so.%{rl_vers}
  chmod 0755 %{buildroot}/%{_lib}/libreadline.so.%{rl_vers}
  rm -vf %{buildroot}/%{_lib}/libhistory.so.%{rl_vers}*old
  rm -vf %{buildroot}/%{_lib}/libreadline.so.%{rl_vers}*old
  rm -vf %{buildroot}/%{_lib}/libhistory.so
  rm -vf %{buildroot}/%{_lib}/libreadline.so
  ln -sf /%{_lib}/libhistory.so.%{rl_vers}  %{buildroot}/%{_libdir}/libhistory.so
  ln -sf /%{_lib}/libreadline.so.%{rl_vers} %{buildroot}/%{_libdir}/libreadline.so
cd ../bash-%{bash_vers}
  make install DESTDIR=%{buildroot}
  make -C examples/loadables/ install-plugins DESTDIR=%{buildroot} libdir=/%{_lib}
  make -C examples/loadables/ install-headers DESTDIR=%{buildroot}
  mkdir -p %{buildroot}/bin
  mv %{buildroot}%{_bindir}/bash %{buildroot}/bin/
%if %_minsh
  install sh  %{buildroot}/bin/sh
  ln -sf ../../bin/sh   %{buildroot}%{_bindir}/sh
%else
  ln -sf bash %{buildroot}/bin/sh
  ln -sf ../../bin/bash %{buildroot}%{_bindir}/sh
%endif
  ln -sf ../../bin/bash %{buildroot}%{_bindir}/rbash
  install -m 644 COMPAT NEWS    %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 COPYING        %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 doc/FAQ        %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 doc/INTRO      %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 doc/*.html     %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 doc/builtins.1 %{buildroot}%{_mandir}/man1/bashbuiltins.1
  install -m 644 doc/rbash.1    %{buildroot}%{_mandir}/man1/rbash.1
  gzip -9f %{buildroot}%{_infodir}/*.inf*[^z] || true
  mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
  sed 's/^|//' > %{buildroot}%{_defaultdocdir}/bash/BUGS <<\EOF
Known problems
--------------
|
This version of bash/readline supports multi byte handling
that is e.g. wide character support for UTF-8.  This causes
problems in geting the current cursor position within the
readline runtime library:
|
bash-%{bash_vers}> LANG=ja_JP
bash-%{bash_vers}> echo -n "Hello"
bash-%{bash_vers}>
|
In other words the prompt overwrites the output of the
echo comand.  The boolean variable byte-oriented
set in %{_sysconfdir}/inputrc or $HOME/.inputrc avoids this
but disables multi byte handling.
EOF
  # remove unpackaged files
  rm -fv %{buildroot}%{_libdir}/libhistory.so.*
  rm -fv %{buildroot}%{_libdir}/libreadline.so.*
  rm -fv %{buildroot}%{_infodir}/rluserman.info.gz
  rm -fv %{buildroot}%{_mandir}/man3/history.3*
  mkdir -p %{buildroot}%{_sysconfdir}/skel
  install -m 644 %{S:5}    %{buildroot}%{_sysconfdir}/skel/.bashrc
  install -m 644 %{S:6}    %{buildroot}%{_sysconfdir}/skel/.profile
  touch -t 199605181720.50 %{buildroot}%{_sysconfdir}/skel/.bash_history
  chmod 600                %{buildroot}%{_sysconfdir}/skel/.bash_history
  %find_lang bash
  %fdupes -s %{buildroot}%{_datadir}/bash/helpfiles

%post -n bash-doc
%install_info --info-dir=%{_infodir} %{_infodir}/bash.info.gz

%postun -n bash-doc
%install_info_delete --info-dir=%{_infodir} %{_infodir}/bash.info.gz

%post -n libreadline6 -p /sbin/ldconfig

%postun -n libreadline6 -p /sbin/ldconfig

%post -n readline-doc
%install_info --info-dir=%{_infodir} %{_infodir}/history.info.gz
%install_info --info-dir=%{_infodir} %{_infodir}/readline.info.gz

%postun -n readline-doc
%install_info_delete --info-dir=%{_infodir} %{_infodir}/history.info.gz
%install_info_delete --info-dir=%{_infodir} %{_infodir}/readline.info.gz

%clean
ldd -u -r %{buildroot}/bin/bash || true
ldd -u -r %{buildroot}%{_libdir}/libreadline.so || true
%{?buildroot: %{__rm} -rf %{buildroot}}

%files
%defattr(-,root,root)
%config %attr(600,root,root) %{_sysconfdir}/skel/.bash_history
%config %attr(644,root,root) %{_sysconfdir}/skel/.bashrc
%config %attr(644,root,root) %{_sysconfdir}/skel/.profile
/bin/bash
/bin/sh
%dir %{_sysconfdir}/bash_completion.d
%{_bindir}/bashbug
%{_bindir}/rbash
%{_bindir}/sh
%dir %{_datadir}/bash
%dir %{_datadir}/bash/helpfiles
%{_datadir}/bash/helpfiles/*

%files -n bash-lang -f bash.lang
%defattr(-,root,root)

%files -n bash-doc
%defattr(-,root,root)
%doc %{_infodir}/bash.info.gz
%doc %{_mandir}/man1/bash.1.gz
%doc %{_mandir}/man1/bashbuiltins.1.gz
%doc %{_mandir}/man1/bashbug.1.gz
%doc %{_mandir}/man1/rbash.1.gz
%doc %{_defaultdocdir}/bash/

%files -n bash-devel
%defattr(-,root,root)
%dir /%{_includedir}/bash/
%dir /%{_includedir}/bash/%{bash_vers}/
%dir /%{_includedir}/bash/%{bash_vers}/builtins/
/%{_incdir}/bash/%{bash_vers}/*.h
/%{_incdir}/bash/%{bash_vers}/builtins/*.h

%files -n bash-loadables
%defattr(-,root,root)
%dir %{_ldldir}/
%dir %{_ldldir}/%{bash_vers}/
%{_ldldir}/%{bash_vers}/*

%files -n libreadline6
%defattr(-,root,root)
/%{_lib}/libhistory.so.%{rl_major}
/%{_lib}/libhistory.so.%{rl_vers}
/%{_lib}/libreadline.so.%{rl_major}
/%{_lib}/libreadline.so.%{rl_vers}

%files -n readline-devel
%defattr(-,root,root)
%{_incdir}/readline/
%{_libdir}/libhistory.a
%{_libdir}/libhistory.so
%{_libdir}/libreadline.a
%{_libdir}/libreadline.so
%doc %{_mandir}/man3/readline.3.gz

%files -n readline-doc
%defattr(-,root,root)
%doc %{_infodir}/history.info.gz
%doc %{_infodir}/readline.info.gz
%doc %{_defaultdocdir}/readline/

%changelog
* Tue Jun 09 2009 werner@suse.de
- Branch off some sub packages:
  * bash-lang to include localization
  * bash-loadables for installing the loadable runtime builtins
  * bash-devel to install headers for developing loadable builtins
* Wed Jun 03 2009 werner@suse.de
- Enforce the usage of euidaccess(3) instead of stat(2) for testing
  permissions for a file (bnc#509105)
* Mon May 25 2009 werner@suse.de
- Update to newest patch level 24:
  * include last few patches
- Add patches from mailing list for globstar expansion
* Mon May 11 2009 werne@suse.de
- Increase size of hash table for runtime linker a lot
* Mon Apr 27 2009 werne@suse.de
- Add patches from mailing list:
  * fix problem with invisible characters in prompt
  * make dir*/** work
* Tue Apr 21 2009 werne@suse.de
- Do not crash on forbidden subdirectories with globstar extension
* Wed Apr 15 2009 werne@suse.de
- Add fix to be able to clear to eol in readline library
* Tue Apr 14 2009 werne@suse.de
- Add fix for timing issue in readline SIGWINCH handling
* Wed Apr 08 2009 werne@suse.de
- Add patches from bug-bash@gnu.org to avoid eg. segmentation fault
* Mon Mar 16 2009 werner@suse.de
- Add patches from bug-bash@gnu.org to avoid eg. segmentation fault
* Thu Mar 12 2009 werner@suse.de
- Add patch from bug-bash@gnu.org to enable |& not only for
  builtins and shell functions but for all commands.
* Tue Mar 10 2009 werner@suse.de
- Switch to official patches, now we are on patch level 10
* Wed Mar 04 2009 werner@suse.de
- Use patches from bug-bash@gnu.org to make it work
* Wed Mar 04 2009 werner@suse.de
- Patch for bnc#481817 does not work in any case
* Wed Mar 04 2009 werner@suse.de
- My last patch for bnc#470548 send to bug-bash@gnu.org was not
  fully applied and this had caused a memory corruption on tab
  completion.
- Enable the parser to find closing parenthesis at the end of
  an argument of a command even if backslash is used (bnc#481817)
- Correct link of shared libraries of devel readline package
* Fri Feb 27 2009 werner@suse.de
- Update bash 4.0 to patch level 0
- Update readline 6.0 to patch level 0
* Wed Feb 18 2009 werner@suse.de
- Add readline patch 13
* Fri Jan 30 2009 werner@suse.de
- Restore state if shell function for completion is interrupted (bnc#470548)
* Tue Jan 13 2009 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)
* Fri Dec 19 2008 werner@suse.de
- Enable large file support (bnc#460560)
* Tue Dec 09 2008 schwab@suse.de
- Add bash patches 40-48.
* Tue Nov 25 2008 werner@suse.de
- Parse the return value of setlocale(LC_ALL) (bnc#447846)
* Thu Oct 16 2008 werner@suse.de
- Let's avoid not needed library dependencies (bnc#439051)
* Mon Sep 01 2008 prusnak@suse.cz
- bash should suggest command-not-found, not scout
* Thu Jul 24 2008 werner@suse.de
- Add command-not-found.patch for scout support (fate#303730)
* Tue Jun 17 2008 werner@suse.de
- Avoid underline the full paragraph in the man page (bnc#400767)
* Sat May 17 2008 coolo@suse.de
- fix rename of xxbit packages
* Tue May 06 2008 schwab@suse.de
- Add bash patches 34-39.
* Mon Apr 28 2008 matz@suse.de
- Fix last patch.
* Thu Apr 24 2008 werner@suse.de
- Add workaround for bnc#382214
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Wed Apr 02 2008 werner@suse.de
- Allow to (re)send signals within trap handlers (bnc#345441)
- Clear exit status if not sourcing system profile (bnc#372061)
* Thu Feb 28 2008 dmueller@suse.de
- remove invalid filerequires, the libreadline5 dependency is enough
* Mon Jan 28 2008 schwab@suse.de
- Add bash patches 26-33.
* Tue Jan 08 2008 werner@suse.de
- Restart the signal handler for SIGCHLD if not already done
  within the signal handler its self (may help for bug #345441)
* Mon Jan 07 2008 schwab@suse.de
- Fix memory leak in read builtin.
* Fri Dec 07 2007 werner@suse.de
- Add skel files .bashrc, bash_history, and .profile from aaa_skel
* Tue Dec 04 2007 werner@suse.de
- Extend fix for off-by-one error in libreadline (bug #274120)
- Enable ssh detection in the bash (bug #345570)
* Thu Sep 20 2007 werner@suse.de
- Remove error triggering path requirement (bug #326751)
* Mon Aug 27 2007 schwab@suse.de
- Add bash patches 18-25.
* Sat Aug 11 2007 schwab@suse.de
- Add bash patches 10-17.
* Sat Aug 04 2007 dmueller@suse.de
- fix devel requires
* Fri Aug 03 2007 schwab@suse.de
- Fix dependencies.
* Tue Jul 31 2007 werner@suse.de
- Branch off bash-doc and readline-doc (bug #260209)
- Rename readline to libreadline5 (bug #260209)
* Thu Apr 19 2007 schwab@suse.de
- Fix bug in readline redisplay.
* Thu Mar 29 2007 dmueller@suse.de
- add ncurses-devel requires to readline-devel
* Mon Mar 26 2007 rguenther@suse.de
- Add bison and ncurses-devel BuildRequires.
* Wed Mar 07 2007 rguenther@suse.de
- Fix order of changelog entries.  Remove duplicate entry.
* Wed Feb 28 2007 werner@suse.de
- Don't access buffer but resulting pointer for array element names
  to avoid the not initialized area of the buffer.  This also fixes
  an inherent wrong calculation of the string length of the array
  element names (bug #248717)
* Thu Dec 14 2006 werner@suse.de
- Update to bash 3.2 patch level 9
* Wed Dec 06 2006 schwab@suse.de
- Remove obsolete patches.
* Fri Nov 17 2006 werner@suse.de
- Remove /usr/bin/bash (#206000)
* Tue Nov 14 2006 werner@suse.de
- Update to bash 3.2 patch level 5
* Wed Sep 27 2006 werner@suse.de
- Use PIE to make a shared bash binary
- Make the bash modules build for testing
* Fri Sep 22 2006 werner@suse.de
- Remove rpath option for libraries use linker defaults instead
* Fri Sep 22 2006 werner@suse.de
- Add symbolic link for POSIX bourne shell to /usr/bin/ (#206000)
* Thu Sep 14 2006 werner@suse.de
- Add environment variable DEFAULT_BELL_STYLE to control the
  bell style of the readline library without using intputrc.
* Mon Aug 07 2006 werner@suse.de
- Let readline-devel requires libncurses.so (bug #188673)
* Thu Jul 27 2006 werner@suse.de
- Let printf builtin handle stdout errors correctly (bug #190349)
* Wed May 31 2006 werner@suse.de
- Fix crash in IFS multi byte handling (bug #180317)
* Tue May 23 2006 werner@suse.de
- Make the test suite run even on ppc emulated on ppc64
* Mon May 15 2006 werner@suse.de
- Update bash 3.1 to patch level 17
  * Allow array subscripts to be sourounded by double quotes
- Run test suite with nearly all scripts
* Mon Apr 03 2006 werner@suse.de
- Update bash 3.1 to patch level 16
  * Bash will dump core when attempting to perform globbing in
  directories with very large numbers of files
  * Solve problem with the extended globbing code prevented dots
  from matching filenames when used in some matching patterns
* Mon Mar 27 2006 werner@suse.de
- Use access(2) with temporary switched euid/ruid and egid/rgid
  instead of stat(2) to determine the access permissions of a
  file, this works even on RO mounted NFS file systems (#160513)
* Wed Mar 22 2006 werner@suse.de
- Be sure that ~/.inputrc is read even if INPUTRC is set to
  system wide /etc/inputrc (bug #160003)
- Make prefix-meta work even with new readline syntax but
  disable it by default (since bug #suse21096)
* Mon Mar 20 2006 werner@suse.de
- Update to bash 3.1 to patch level 14 and readline 5.1 to level 4
  * Do not terminate words prematurely if parentheses are involved
  * Readline sometimes reference freed memory
  * Fix double displayed prompt when using non-incremental searches
* Sun Mar 12 2006 schwab@suse.de
- Update bash31-010 patch, better fix for #151000.
* Thu Mar 02 2006 werner@suse.de
- Update bash 3.1 to patch level 11 and readline 5.1 to level 2
  * Includes fix for line-wrapping errors
  * Replacement for bug fix of bug #146075 with better
  reallocation and compaction of the job array list.
  * Do not let SIGINT from terminal reach background processes
  * Do not let asynchronous background jobs set the terminal
  process group incorrectly.
  * Replacement for bug fix of bug #151000
  * Do not strip quoting inside double-quoted command substitutions
* Wed Mar 01 2006 werner@suse.de
- Re-enable escaping newline within quotes in commands (#151000)
* Mon Jan 30 2006 werner@suse.de
- Do initialize the fresh members of the job array (bug #146075)
* Mon Jan 30 2006 schwab@suse.de
- Barf if /proc is missing.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 10 2006 werner@suse.de
- Update to newest patch level 5:
  + corrects several omissions in the bash documentation
  + local array variable declared at function scope shadowing
  a global variable should create a separate instance
  + When tilde expansion fails, do not skip rest of an expansion
- Expand dollar quotes even for the single quote case (bug #141394)
* Thu Dec 22 2005 werner@suse.de
- Switch to first patchlevel for the bash and the readline library.
  This should fix problems happen with local/eval/let builtins.
* Mon Dec 19 2005 werner@suse.de
- Remove dangling sym links
* Tue Dec 13 2005 schwab@suse.de
- Fix segfault in readline callback interface.
* Mon Dec 12 2005 schwab@suse.de
- Fix return of random data.
- Set CFLAGS_FOR_BUILD.
* Fri Dec 09 2005 werner@suse.de
- Update to bash version 3.1 and readline library version 5.1
* Thu Sep 29 2005 werner@suse.de
- More cookie for the compiler
* Mon Sep 19 2005 werner@suse.de
- Give the compiler its cookie
* Tue Apr 19 2005 postadal@suse.cz
- fixed crashing on read -e command and line wrapping (in readline code)
  (bug #76709)
* Fri Jan 28 2005 werner@suse.de
- Add workaround for NFS bug which does not check permissions
  on open of a file but close (bug #20244)
* Thu Nov 25 2004 werner@suse.de
- Remove local array patch because not needed anymore
- Fix a crash on internal arrays if unset during execution of
  functions and files (bug #48511)
* Sun Nov 21 2004 schwab@suse.de
- Add patches from <ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/> and
  <ftp://ftp.cwru.edu/pub/bash/readline-5.0-patches/>.
* Fri Nov 19 2004 werner@suse.de
- Fix the evalexp fix (bug #48253)
* Mon Oct 25 2004 werner@suse.de
- Be sure that the FN macro nroff macro is available in all
  sub manual pages (bug #47560)
* Tue Oct 12 2004 werner@suse.de
- Re-activate first part of prompt fix because it does not harm
  (bug #36919)
* Tue Oct 12 2004 ro@suse.de
- no macros in Version lines
* Mon Oct 11 2004 werner@suse.de
- Disable prompt patch for now because not needed and other
  problmes caused by this fix (bug #36919)
- Clear out last_made_pid on success (bug #42232)
* Thu Sep 30 2004 werner@suse.de
- Clear out prompt line of isearch for invisible chars (bug #36919)
* Wed Sep 29 2004 werner@suse.de
- Fix prompt problem with invisible characters (bug #36919)
* Fri Sep 17 2004 werner@suse.de
- Fix line wraping for newlines in prompt (bug #45519)
* Thu Sep 16 2004 schwab@suse.de
- Fix missing return value.
* Sat Sep 11 2004 kukuk@suse.de
- Disable use of WCONTINUED as long as bash does not check if
  it is supported.
* Mon Sep 06 2004 werner@suse.de
- Fix prefix strip for last added patch
* Fri Sep 03 2004 werner@suse.de
- Add warning about broken glibc locale before we get the SIGSEGV
  (bug #44658)
* Sun Aug 01 2004 schwab@suse.de
- Fix rl_maybe_save_line.
- Track LC_TIME.
* Fri Jul 30 2004 werner@suse.de
- Put version to bash 3.0 and readline 5.0
* Mon Jun 07 2004 werner@suse.de
- Add missed declaration of oldval for previous bugfix
* Fri Jun 04 2004 werner@suse.de
- Fix local array variable handling (bug #41649)
* Wed Jun 02 2004 werner@suse.de
- Fix evaluation none local return stack curruption (bug #41488)
* Wed Apr 07 2004 werner@suse.de
- In case of quotes position counter has to be advanced (#38599)
* Thu Apr 01 2004 werner@suse.de
- Add directoy check to distinguish none unique and unique
  executables  (bug #37329)
* Mon Mar 29 2004 werner@suse.de
- Make the directory patch working as it should (bug #37329)
* Thu Mar 25 2004 werner@suse.de
- Move forward to official bug fixes to catch UTF-8 bug #31451
  and bug #36919
* Thu Feb 12 2004 werner@suse.de
- Fix cut&paste error of fix for bug #34427
* Wed Feb 11 2004 werner@suse.de
- Fix SIGSEGV in using UTF-8 and pattern matching (bug #34427)
- Fix LC_NUMERIC handling of builtin printf (bug #34428)
* Mon Feb 02 2004 werner@suse.de
- Fix the fix and also bug #34242
* Thu Jan 29 2004 werner@suse.de
- Fix performance problem for pattern matching in UTF-8 locale
  (port back patch from Mitsuru Chinen <mchinen@yamato.ibm.com>)
* Tue Jan 13 2004 kukuk@suse.de
- Fix last changes
* Sat Jan 10 2004 adrian@suse.de
- add %%run_ldconfig
* Mon Jul 28 2003 werner@suse.de
- Add /etc/bash_completion.d directory
* Thu Jun 26 2003 kukuk@suse.de
- Fix specfile for lib64
* Wed Jun 04 2003 jh@suse.de
- Enable profile feedback
* Fri May 23 2003 ro@suse.de
- remove unpackaged files
* Thu May 22 2003 mfabian@suse.de
- improvement for bash-2.05b-locale.patch and
  bash-2.05b-readline-init.patch: this fixes the problem that
  the line editor in bash is not correctly initialized in the first
  bash after login via ssh or on the linux console. This is
  especially obvious in UTF-8 locales when editing non-ASCII
  characters on the command line. See also:
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=74701
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=74925
  The following bug remains fixed:
  http://bugzilla.suse.de/show_bug.cgi?id=16999
- bash-2.05b-complete.patch: (by Miloslav Trmac <mitr@volny.cz>)
  achieve correct alignment of file names containing non-ASCII
  characters when typing "ls " and pressing Tab twice to show
  the completions. See also:
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=90201
* Mon Mar 17 2003 werner@suse.de
- Do not execute command line if tty is closed (bug #25445)
* Thu Feb 13 2003 schwab@suse.de
- Fix prompt decoding with -noediting.
* Tue Feb 11 2003 kukuk@suse.de
- To avoid loop in PreRequires, don't install info pages. The info
  package contains a dir file which contains the bash entries
  already.
* Fri Feb 07 2003 ro@suse.de
- fixed specfile
* Fri Feb 07 2003 ro@suse.de
- added install_info macros
* Mon Jan 27 2003 schwab@suse.de
- Fix bugs #21096 and #21392 properly: don't recurse on
  do-lowercase-version for fallback entry.
* Tue Jan 21 2003 werner@suse.de
- Allow rbash as login shell (`-' problem, bug #22917)
* Wed Dec 18 2002 schwab@suse.de
- Use BuildRoot.
* Thu Dec 12 2002 mfabian@suse.de
- add bash-2.05b-display-mbspeed.patch received from
  Jiro SEKIBA <jir@yamato.ibm.com> to improve display speed in
  multibyte locales.
* Sat Nov 09 2002 ro@suse.de
- add bison to neededforbuild for now
  (till we're sure about bison again)
* Thu Oct 31 2002 werner@suse.de
- For bug #21096 and #21392: implement an oom protection.
* Mon Oct 21 2002 werner@suse.de
- More for bug#21096: Make prefix-meta work even if mapped onto
  longer escape sequences.
* Fri Oct 18 2002 werner@suse.de
- Fix bug#21096: sequences like `ESC ... CHARACTER' with CHARACTER
  mapped on functions will not cause an endless recursion anymore.
* Wed Sep 25 2002 ro@suse.de
- removed more bogus provides
* Wed Sep 11 2002 werner@suse.de
- Correct Provides (package should not provides its self)
* Fri Aug 30 2002 werner@suse.de
- Add version dependend require on readline (bug #18652)
* Fri Aug 30 2002 werner@suse.de
- Fix annoying display bug in wide character support (bug #18449)
* Wed Aug 28 2002 werner@suse.de
- Add comment about multi byte handling and echo builtin (#18449)
* Wed Aug 21 2002 mls@suse.de
- fix $RANDOM randomness in subshells
* Fri Aug 09 2002 kukuk@suse.de
- readline-devel should require readline
* Mon Jul 29 2002 werner@suse.de
- Expansion of `~user/<dir>' is like `/<dir>'
* Sat Jul 27 2002 kukuk@suse.de
- Remove not used tetex from neededforbuild
- Fix building of man2html (bash.html still broken)
* Fri Jul 19 2002 werner@suse.de
- Check value of LANG before LC_ALL will be unset for getting the
  _current_ default value of LC_ALL with setlocale(3) (bug #16999)
* Fri Jul 19 2002 werner@suse.de
- Fix NULL pointer handled by memset (readline:mbutil.c)
* Thu Jul 18 2002 werner@suse.de
- Update to new version bash 2.05b/readline 4.3
* Wed May 22 2002 schwab@suse.de
- Fix vi-change-char.
- Fix missing declaration.
* Wed Apr 17 2002 schwab@suse.de
- Fix last change.
* Thu Apr 11 2002 sf@suse.de
- using %%{_libdir} to put the shlibs into the correct directories
  (lib / lib64)
* Tue Mar 26 2002 werner@suse.de
- Fix possible endless loop if terminal will be disconneted during
  complete answer (bug report from bastian@kde.org, for more see
  http://bugs.kde.org/db/37/37999.html)
* Wed Mar 20 2002 ro@suse.de
- removed tetex from neededforbuild, it's not used here
* Wed Mar 06 2002 werner@suse.de
- Use improved bug fix for line wrapping problem, now line wrapping
  work for char and wide char environments
- Fix readline version number
* Wed Feb 27 2002 mfabian@suse.de
- add readline-4.2-i18n-0.3-display.patch from
  Jiro SEKIBA <jir@yamato.ibm.com> to fix a line wrapping
  problem.
* Mon Jan 21 2002 werner@suse.de
- Fix bug #12834: Update to bash-2.05-i18n-0.5.patch.gz and
  bash-2.05-readline-i18n-0.3.patch.gz
* Thu Oct 18 2001 werner@suse.de
- Allways include /etc/inputrc if INPUTRC isn't system file
* Mon Oct 08 2001 werner@suse.de
- Fix readline i18n patch: enable configure of multi byte handling,
  fix warnings and bug in histexpand.c
* Fri Oct 05 2001 werner@suse.de
- Add two patches for I18N support of bash and readline library
* Tue Sep 04 2001 werner@suse.de
- Add patch to avoid trouble with C++ header definitions
* Fri Aug 03 2001 werner@suse.de
- Fix fc crash (bug #9620)
* Mon Jul 02 2001 olh@suse.de
- dont apply bash-2.05-s390x-unwind.patch on ppc and sparc
* Thu Jun 14 2001 bk@suse.de
- fix 64-bit bigendian bug for s390x
* Wed Jun 06 2001 werner@suse.de
- Re-order configure.in to avoid trouble with new autoconf
* Tue May 08 2001 mfabian@suse.de
- bzip2 sources
* Sat May 05 2001 schwab@suse.de
- Fix process substitution when stdin is closed.
* Wed May 02 2001 werner@suse.de
- Make patch for 2.4.4 work within spec
* Wed May 02 2001 werner@suse.de
- Remove buggy patch in job control, add a workaround
* Mon Apr 30 2001 werner@suse.de
- Add patch to get job control into right order on a pipe
* Thu Apr 12 2001 werner@suse.de
- Provide cpp macro OLD_READLINE for backwards compatibility
  at compile time with old readline interface
* Thu Apr 12 2001 ro@suse.de
- added split-alias as provides (again)
* Wed Apr 11 2001 werner@suse.de
- Update to bash 2.05 and readline 4.2
- Port of our patches
* Thu Feb 22 2001 werner@suse.de
- Split package into bash/readline/readline-devel
- Depend libreadline on libncurses
* Thu Sep 14 2000 werner@suse.de
- Add some bug fixes
- Add missed ssh fix for none interactive shell
* Wed Jun 07 2000 werner@suse.de
- Fix some patches
- Add export patch for bash 2.04
- Fix `soname' of readline and history libraries
- Fix linkage of major readline and history libraries
* Mon Jun 05 2000 schwab@suse.de
- Fix unwind_protect_pointer on 64-bit systems.
* Wed May 31 2000 schwab@suse.de
- Comment out declaration of savestring in <readline.h> that conflicts
  with other people's declaration (eg. gdb).
* Mon May 29 2000 aj@suse.de
- Upgrade to bash 2.04 and readline 4.1.
* Sun May 21 2000 kukuk@suse.de
- Use docdir
* Sat Apr 01 2000 bk@suse.de
- remove obviosly unneeded link /usr/lib/libreadline.so on s390
* Tue Mar 14 2000 werner@suse.de
- Add locale patch to enable LC_NUMERIC handling
* Thu Feb 24 2000 werner@suse.de
- Use $VENDOR for several linux architectures
- Set check_window_size (shopt checkwinsize) to true, this will
  correct screen size even if it changes during a job.
* Tue Feb 15 2000 schwab@suse.de
- Update config.{guess,sub} to latest version.
- Fix spec file to create doc directory before installing into it.
* Sat Jan 29 2000 werner@suse.de
- Add mailstat patch (handles mail directories)
- Fix configuration (system is %%arch-suse-linux)
- Fix segfault (job handling)
- Fix manual (add rbash manual, add some missed options)
- Install rbash (symlink to bash)
- Fix readline (End, Del)
- Fix temporary file handling (do not write without check)
- Use system random interface not builtin
- Remove some compiler warnings
- Set --enable-disabled-builtins (useful)
- Install shared readline and history in /lib (bash needs that)
- Enable shared readline (version 4.0) and history library
- Try to use shared readline and history for bash (TEST)
* Fri Dec 03 1999 kasal@suse.de
- added command to make and install doc/bashref.html
* Fri Nov 26 1999 kukuk@suse.de
- Fix spec file
* Thu Nov 25 1999 kukuk@suse.de
- Merge Makefile.Linux with spec file, use RPM_OPT_FLAGS
- Remove --disable-dparen-arithmetic
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Tue Aug 24 1999 uli@suse.de
- fixed for PPC
* Mon Jul 19 1999 florian@suse.de
- update to bash 2.03, readline 4.0
* Wed Jan 13 1999 @suse.de
- disabled `Broken pipe' messages
* Sun Dec 13 1998 bs@suse.de
- removed notify message - bash 2.0 is standard for a long time now.
* Mon Dec 07 1998 florian@suse.de
- remove SSH_CLIENT-kludge as this cannot detect all correct cases
  where .bashrc should be loaded
- delete email-changes in bashbug script
- update readline to version 2.2.1
* Thu Nov 12 1998 bs@suse.de
- minor fix for new rpm
* Thu Oct 01 1998 ro@suse.de
- update to 2.02.1 / reintegrated werner's tmp-fix for bashbug
* Thu Jul 23 1998 werner@suse.de
- use mktemp
* Thu Jul 16 1998 werner@suse.de
- fix bashbug temp file handling
* Wed Jun 17 1998 ro@suse.de
- changed general.h: !defined (gid_t)
* Mon Oct 27 1997 florian@suse.de
- do not include old compatible-only safestring() in libreadline.a
* Thu Oct 09 1997 florian@suse.de
- update to version 2.01.1
- add several bugfixes
- fix missing things in spec-file
* Thu Aug 14 1997 florian@suse.de
- add several bug-fixes from gnu.bash.bug and fix memory management
  of LC_ALL
* Sat Jul 05 1997 florian@suse.de
- add another bugfix from gnu.utils.bugs
* Mon Jun 23 1997 florian@suse.de
- create the history file with 0600 perms
- add minor bugfix to check for new email
* Thu Jun 05 1997 florian@suse.de
- bash: check for NULL-pointer before calling "savestring()"
- add bashref.info and newer FAQ
* Tue Apr 22 1997 bs@suse.de
- added FAQ and bashref.html to /usr/doc/packages/bash
* Sun Apr 13 1997 florian@suse.de
- update to bash 2.0 with lots of patches from gnu.utils.bugs
  Mon Sep  2 02:48:35 MET DST 1996
  new version with security patches
* Thu Jan 02 1997 florian@suse.de
  security fix included (0xff was command separator)
