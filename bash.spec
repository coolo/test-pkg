#
# spec file for package bash
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



Name:           bash
BuildRequires:  bison ncurses-devel
%if %suse_version > 1020
BuildRequires:  fdupes
%endif
License:        GPLv2+
Group:          System/Shells
%define         bash_vers 4.2
%define         rl_vers   6.2
%define         extend    ""
%if %suse_version > 1020
Recommends:     bash-lang = %bash_vers
# The package bash-completion is a source of
# bugs which will hit at most this package
#Recommends:	bash-completion
Suggests:       command-not-found
Recommends:     bash-doc = %bash_vers
%endif
Version:        4.2
Release:        5
Summary:        The GNU Bourne-Again Shell
Url:            http://www.gnu.org/software/bash/bash.html
Source0:        ftp://ftp.gnu.org/gnu/bash/bash-%{bash_vers}.tar.gz
Source1:        ftp://ftp.gnu.org/gnu/readline/readline-%{rl_vers}.tar.gz
Source2:        bash-%{bash_vers}-patches.tar.bz2
Source3:        readline-%{rl_vers}-patches.tar.bz2
Source4:        run-tests
Source5:        dot.bashrc
Source6:        dot.profile
Source7:        bash-rpmlintrc
Source8:        baselibs.conf
# Remember unsafe method, compare with
# http://lists.gnu.org/archive/html/bug-bash/2011-03/msg00070.html
# http://lists.gnu.org/archive/html/bug-bash/2011-03/msg00071.html
# http://lists.gnu.org/archive/html/bug-bash/2011-03/msg00073.html
Source9:        bash-4.2-history-myown.dif.bz2
Patch0:         bash-%{bash_vers}.dif
Patch1:         bash-2.03-manual.patch
Patch2:         bash-4.0-security.patch
Patch3:         bash-4.2-2.4.4.patch
Patch4:         bash-3.0-evalexp.patch
Patch5:         bash-3.0-warn-locale.patch
Patch6:         bash-4.2-endpw.dif
Patch7:         bash-3.0-decl.patch
Patch8:         bash-4.0-async-bnc523667.dif
Patch9:         bash-4.0-extended_quote.patch
Patch10:        bash-3.2-printf.patch
Patch11:        bash-4.0-loadables.dif
Patch12:        bash-4.1-completion.dif
Patch13:        bash-4.2-nscdunmap.dif
Patch14:        bash-4.2-sigrestart.patch
Patch15:        bash-3.2-longjmp.dif
Patch16:        bash-4.0-setlocale.dif
Patch17:        bash-4.0-headers.dif
Patch20:        readline-%{rl_vers}.dif
Patch21:        readline-4.3-input.dif
Patch22:        readline-6.1-wrap.patch
Patch23:        readline-5.2-conf.patch
Patch24:        readline-6.2-metamode.patch
Patch25:        readline-6.2-endpw.dif
Patch30:        readline-6.2-destdir.patch
Patch40:        bash-4.1-bash.bashrc.dif
Patch46:        man2html-no-timestamp.patch
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

%package -n bash-doc
License:        GPLv2+
Summary:        Documentation how to Use the GNU Bourne-Again Shell
Group:          Documentation/Man
Provides:       bash:%{_infodir}/bash.info.gz
PreReq:         %install_info_prereq
Version:        4.2
Release:        5
%if %suse_version > 1120
BuildArch:      noarch
%endif

%description -n bash-doc
This package contains the documentation for using the bourne shell
interpreter Bash.

%if %{defined lang_package}
%lang_package(bash)
%else

%package -n bash-lang
License:        GPLv2+
Summary:        Languages for package bash
Group:          System/Localization
Provides:       bash-lang = %{version}
Requires:       bash = %{version}

%description -n bash-lang
Provides translations to the package bash
%endif

%package -n bash-devel
License:        GPLv2+
Summary:        Include Files mandatory for Development of bash loadable builtins
Group:          Development/Languages/C and C++
Version:        4.2
Release:        5

%description -n bash-devel
This package contains the C header files for writing loadable new
builtins for the interpreter Bash. Use -I /usr/include/bash/<version>
on the compilers command line.

%package -n bash-loadables
License:        GPLv2+
Summary:        Loadable bash builtins
Group:          System/Shells
Version:        4.2
Release:        5

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


%package -n libreadline6
License:        GPLv2+
Summary:        The Readline Library
Group:          System/Libraries
Provides:       bash:/%{_lib}/libreadline.so.%{rl_major}
Version:        6.2
Release:        5
%if %suse_version > 1020
Recommends:     readline-doc = %{version}
%endif
# bug437293
%ifarch ppc64
Obsoletes:      readline-64bit
%endif
#
Provides:       readline =  6.2
Obsoletes:      readline <= 6.1

%description -n libreadline6
The readline library is used by the Bourne Again Shell (bash, the
standard command interpreter) for easy editing of command lines.  This
includes history and search functionality.

%package -n readline-devel
License:        GPLv2+
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries/C and C++
Provides:       bash:%{_libdir}/libreadline.a
Version:        6.2
Release:        5
Requires:       libreadline6 = %{version}
Requires:       ncurses-devel
%if %suse_version > 1020
Recommends:     readline-doc = %{version}
%endif
# bug437293
%ifarch ppc64
Obsoletes:      readline-devel-64bit
%endif
#

%description -n readline-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%package -n readline-doc
License:        GPLv2+
Summary:        Documentation how to Use and Program with the Readline Library
Group:          System/Libraries
Provides:       readline:%{_infodir}/readline.info.gz
PreReq:         %install_info_prereq
Version:        6.2
Release:        5
%if %suse_version > 1120
BuildArch:      noarch
%endif

%description -n readline-doc
This package contains the documentation for using the readline library
as well as programming with the interface of the readline library.

%prep
%setup -q -n bash-%{bash_vers}%{extend} -b1 -b2 -b3
for p in ../bash-%{bash_vers}-patches/*; do
    test -e $p || break
    test "${p##*/}" = "bash-4.2-pwd.patch" && continue
    echo Patch $p
    patch -s -p0 < $p
done
unset p
%patch1  -p0 -b .manual
%patch2  -p0 -b .security
%patch3  -p0 -b .2.4.4
%patch4  -p0 -b .evalexp
%patch5  -p0 -b .warnlc
%patch6  -p0 -b .endpw
%patch7  -p0 -b .decl
%patch8  -p0 -b .async
%patch9  -p0 -b .extended_quote
%patch10 -p0 -b .printf
%patch11 -p0 -b .plugins
%patch12 -p0 -b .completion
%patch13 -p0 -b .nscdunmap
%patch14 -p0 -b .sigrestart
%patch15 -p0 -b .longjmp
%patch16 -p0 -b .setlocale
%patch17 -p0 -b .headers
%patch21 -p0 -b .zerotty
%patch22 -p0 -b .wrap
%patch23 -p0 -b .conf
%patch24 -p0 -b .metamode
%patch25 -p0 -b .endpw
%patch40 -p0 -b .bashrc
%patch46 -p0 -b .notimestamp
%patch0  -p0 -b .0
pushd ../readline-%{rl_vers}%{extend}
for p in ../readline-%{rl_vers}-patches/*; do
    test -e $p || break
    echo Patch $p
    patch -s -p0 < $p
done
%patch21 -p2 -b .zerotty
%patch22 -p2 -b .wrap
%patch23 -p2 -b .conf
%patch24 -p2 -b .metamode
%patch25 -p2 -b .endpw
%patch30 -p0 -b .destdir
%patch20 -p0 -b .0

%build
  LANG=POSIX
  LC_ALL=$LANG
  unset LC_CTYPE
  CPU=$(uname -m 2> /dev/null)
  HOSTTYPE=${CPU}
  MACHTYPE=${CPU}-suse-linux
  export LANG LC_ALL HOSTTYPE MACHTYPE
pushd ../readline-%{rl_vers}%{extend}
%{?suse_update_config:%{suse_update_config -f support}}
  autoconf
  cflags ()
  {
      local flag=$1; shift
      local var=$1; shift
      test -n "${flag}" -a -n "${var}" || return
      case "${!var}" in
      *${flag}*) return
      esac
      case "$flag" in
      -Wl,*)
	  set -o noclobber
	  echo 'int main () { return 0; }' > ldtest.c
	  if ${CC:-gcc} -Werror $flag -o /dev/null -xc ldtest.c > /dev/null 2>&1 ; then
	      eval $var=\${$var:+\$$var\ }$flag
	  fi
	  set +o noclobber
	  rm -f ldtest.c
	  ;;
      *)
	  if ${CC:-gcc} -Werror $flag -S -o /dev/null -xc /dev/null > /dev/null 2>&1 ; then
	      eval $var=\${$var:+\$$var\ }$flag
	  fi
	  if ${CXX:-g++} -Werror $flag -S -o /dev/null -xc++ /dev/null > /dev/null 2>&1 ; then
	      eval $var=\${$var:+\$$var\ }$flag
	  fi
      esac
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
  ./configure --disable-static --build=%{_target_cpu}-suse-linux	\
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
popd
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
  TMPDIR=$(mktemp -d /tmp/bash.XXXXXXXXXX) || exit 1
  env -i HOME=$PWD TERM=$TERM LD_LIBRARY_PATH=$LD_LIBRARY_PATH TMPDIR=$TMPDIR make TESTSCRIPT=%{SOURCE4} check
  make %{?do_profiling:CFLAGS="$CFLAGS %cflags_profile_feedback" clean} all
  make -C examples/loadables/
  make documentation

%install
pushd ../readline-%{rl_vers}%{extend}
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
popd
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
%if %suse_version > 1020
  %fdupes -s %{buildroot}%{_datadir}/bash/helpfiles
%endif

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
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%doc %{_mandir}/man3/readline.3.gz

%files -n readline-doc
%defattr(-,root,root)
%doc %{_infodir}/history.info.gz
%doc %{_infodir}/readline.info.gz
%doc %{_defaultdocdir}/readline/

%changelog
