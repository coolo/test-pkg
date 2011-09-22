#
# spec file for package Mesa
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

%define _version 7.11

Version:        7.11
Release:        5

Name:           Mesa
BuildRequires:  gcc-c++ libdrm-devel libexpat-devel pkgconfig python-base xorg-x11-devel
BuildRequires:  bison fdupes flex libtalloc-devel libudev-devel libxml2-python
%ifarch %ix86 x86_64
BuildRequires:  llvm-devel
%endif
Url:            http://www.mesa3d.org
License:        MIT License (or similar)
Group:          System/Libraries
Provides:       xorg-x11-Mesa = %{version} intel-i810-Mesa = %{version} Mesa7 = %{version}
Obsoletes:      xorg-x11-Mesa < %{version} intel-i810-Mesa < %{version} Mesa7 < %{version}
Obsoletes:      Mesa-nouveau3d
AutoReqProv:    on
# bug437293
%ifarch ppc64
Obsoletes:      XFree86-Mesa-64bit < %{version} Mesa-64bit < %{version}
Provides:       XFree86-Mesa-64bit = %{version} Mesa-64bit < %{version}
%endif
#
Summary:        System for rendering interactive 3-D graphics
Source:         MesaLib-%{_version}.tar.bz2
Source2:        baselibs.conf
Source3:        README.updates
Source4:        manual-pages.tar.bz2
Source5:        drirc
# to be upstreamed
Patch9:         u_GLX-SWrast-Make-GLX-with-SWrast-enabled-work-on-olde.patch
Patch11:        u_Fix-crash-in-swrast-when-setting-a-texture-for-a-pix.patch
# already upstream
Patch13:        U_Mesa-7.11-llvm3.patch
Patch14:        U_glx-ignore-BadRequest-errors-from-DRI2Connect.diff
Patch15:        Mesa-llvm-3.0.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL.* To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc.(SGI). However, the author does not possess an
OpenGL license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI. Those who
want a licensed implementation of OpenGL should contact a licensed
vendor.

Please do not refer to the library as MesaGL (for legal reasons). It's
just Mesa or The Mesa 3-D graphics library.

* OpenGL is a trademark of Silicon Graphics Incorporated.



Authors:
--------
    Brian Paul

%package devel
License:        MIT License (or similar)
Requires:       Mesa = %version xorg-x11-devel libdrm-devel libudev-devel
Summary:        Libraries, includes and more to develop Mesa applications
Group:          Development/Libraries/X11
# bug437293
%ifarch ppc64
Obsoletes:      XFree86-Mesa-devel-64bit < %{version} Mesa-devel-64bit < %{version}
Provides:       XFree86-Mesa-devel-64bit = %{version} Mesa-devel-64bit = %{version}
%endif
#
Provides:       xorg-x11-Mesa-devel = %{version} Mesa-devel-static = %{version}
Obsoletes:      xorg-x11-Mesa-devel < %{version} Mesa-devel-static < %{version}

%description devel
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL.* To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc.(SGI). However, the author does not possess an
OpenGL license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI. Those who
want a licensed implementation of OpenGL should contact a licensed
vendor.

Please do not refer to the library as MesaGL (for legal reasons). It's
just Mesa or The Mesa 3-D graphics library.

* OpenGL is a trademark of Silicon Graphics Incorporated.



Authors:
--------
    Brian Paul

%prep
%setup -n %{name}-%{_version} -b4 -q
# no need to build (GLUT-)Demos
rm -rf src/glut progs/{demos,redbook,samples,xdemos,glsl}
# we use freeglut
rm -f include/GL/{glut.h,uglglutshapes.h,glutf90.h}
# remove some docs
rm -rf docs/README.{VMS,WIN32,OS2}
%patch9 -p1
%patch11 -p1
%patch13 -p0
%patch14 -p1
%patch15 -p1

%build

%install
rm -f src/mesa/depend
export TALLOC_LIBS=-ltalloc
export TALLOC_CFLAGS="-I/usr/include"
autoreconf -fi
### libGL (disable savage/mga, bnc #402132/#403071; reenable mga, bnc #466635)
%configure --disable-glw \
           --enable-gles1 \
           --enable-gles2 \
           --with-driver=dri \
           --with-egl-platforms=x11,drm \
           --enable-shared-glapi \
           --with-dri-searchpath=/usr/%{_lib}/dri/updates:/usr/%{_lib}/dri \
%ifarch %ix86 x86_64
           --with-dri-drivers=i810,i915,i965,mach64,r128,r200,radeon,sis,tdfx,unichrome,swrast,mga \
%if 0%{?suse_version} >= 1130
           --with-gallium-drivers=r300,r600,nouveau \
%else
           --with-gallium-drivers=r300,r600 \
%endif
%endif
%ifarch ppc ppc64 %sparc hppa
           --with-dri-drivers=i810,i915,i965,mach64,r128,r200,radeon,tdfx,unichrome,swrast \
%if 0%{?suse_version} >= 1130
           --with-gallium-drivers=r300,r600,nouveau \
%else
           --with-gallium-drivers=r300,r600 \
%endif
%endif
%ifarch s390 s390x %arm
           --with-dri-drivers=swrast \
           --with-gallium-drivers="" \
%endif
           --disable-glut \
           CFLAGS="$RPM_OPT_FLAGS -DNDEBUG"
make %{?jobs:-j%jobs}
make install DESTDIR=$RPM_BUILD_ROOT
# build and install Indirect Rendering only libGL
make realclean
%configure --with-driver=xlib \
           --disable-glu \
           --disable-glw \
           --disable-glut \
           --with-gallium-drivers="" \
           CFLAGS="$RPM_OPT_FLAGS -DNDEBUG"
sed -i 's/GL_LIB = .*/GL_LIB = IndirectGL/g' configs/autoconf
make %{?jobs:-j%jobs}
cp -a %{_lib}/libIndirectGL.so.* %{_lib}/libOSMesa.so* \
  $RPM_BUILD_ROOT/usr/%{_lib}
for dir in ../xc/doc/man/{GL/gl,GL/glx,GLU}; do
pushd $dir
  xmkmf -a
  make %{?jobs:-j%jobs};
  make install.man DESTDIR=$RPM_BUILD_ROOT MANPATH=%{_mandir} LIBMANSUFFIX=3gl
popd
done
# DRI driver update mechanism
mkdir -p $RPM_BUILD_ROOT/usr/%{_lib}/dri/updates
install -m 644 $RPM_SOURCE_DIR/README.updates \
  $RPM_BUILD_ROOT/usr/%{_lib}/dri/updates
# global drirc file
mkdir -p $RPM_BUILD_ROOT/etc
install -m 644 $RPM_SOURCE_DIR/drirc $RPM_BUILD_ROOT/etc
%fdupes -s $RPM_BUILD_ROOT/%_mandir

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs/README* docs/COPYING
%config /etc/drirc
%{_libdir}/lib*.so.*
%{_libdir}/dri/
#%{_libdir}/egl/

%files devel
%defattr(-,root,root)
%doc docs/*.html docs/*.spec
%{_includedir}/GL
%{_includedir}/GLES
%{_includedir}/GLES2
%{_includedir}/EGL
%{_includedir}/KHR
%{_includedir}/gbm.h
%{_libdir}/libGL.so
%{_libdir}/libGLU.so
%{_libdir}/libOSMesa.so
%{_libdir}/libEGL.so
%{_libdir}/libGLESv1_CM.so
%{_libdir}/libGLESv2.so
%{_libdir}/libglapi.so
%{_libdir}/libgbm.so
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/pkgconfig/gl.pc
%{_libdir}/pkgconfig/glu.pc
%{_libdir}/pkgconfig/glesv1_cm.pc
%{_libdir}/pkgconfig/glesv2.pc
%{_libdir}/pkgconfig/gbm.pc
%{_mandir}/man3/*

%changelog
