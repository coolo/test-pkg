#
# spec file for package Mesa (Version 7.9)
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

%define enable_nouveau 1

%define _version 7.9

Version:        7.9
Release:        2

Name:           Mesa
BuildRequires:  gcc-c++ libdrm-devel libexpat-devel pkgconfig python-base xorg-x11-devel
BuildRequires:  bison flex libtalloc-devel libxml2-python
%if 0%{?suse_version} > 1020
BuildRequires:  fdupes
%endif
Url:            http://www.mesa3d.org
License:        MIT License (or similar)
Group:          System/Libraries
Provides:       xorg-x11-Mesa = %{version} intel-i810-Mesa = %{version} Mesa7 = %{version}
Obsoletes:      xorg-x11-Mesa < %{version} intel-i810-Mesa < %{version} Mesa7 < %{version}
AutoReqProv:    on
# bug437293
%ifarch ppc64
Obsoletes:      XFree86-Mesa-64bit < %{version} Mesa-64bit < %{version}
Provides:       XFree86-Mesa-64bit = %{version} Mesa-64bit < %{version}
%endif
#
Summary:        System for rendering interactive 3-D graphics
Source:         MesaLib-%{_version}-rc2.tar.bz2
Source1:        MesaDemos-7.8.2.tar.bz2
Source2:        baselibs.conf
Source3:        README.updates
Source4:        manual-pages.tar.bz2
Source5:        drirc
# add update path for dri drivers
Patch1:         dri_driver_dir.diff
# to be upstreamed
Patch8:         egl-buildfix.diff
Patch9:         Mesa_indirect_old_xserver_compatibility.diff
# already upstream
Patch10:        commit-73dab75.diff
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
Requires:       Mesa = %version xorg-x11-devel libdrm-devel
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

%package nouveau3d
License:        MIT License (or similar)
Requires:       Mesa = %version xorg-x11-driver-video-nouveau
Summary:        Experimental 3D driver for nouveau driver
Group:          System/Libraries

%description nouveau3d
This is the 3D driver for open source nouveau driver. It uses Gallium3d architecture within Mesa.

Note:
This driver is in a very experimental state. So it is not recommend that you use it.
Bug reports using this driver are not supported by developers.

Authors:
--------
    Brian Paul
    Pekka Paalanen
    Ben Skeggs
    Francisco Jerez

%prep
%setup -n %{name}-%{_version}-rc2 -a1 -b4 -q
# no need to build (GLUT-)Demos
rm -rf src/glut progs/{demos,redbook,samples,xdemos,glsl}
# we use freeglut
rm -f include/GL/{glut.h,uglglutshapes.h,glutf90.h}
# remove some docs
rm -rf docs/README.{VMS,WIN32,OS2}
%patch1
sed -i 's/REPLACE/%_lib/g' src/glx/Makefile
sed -i 's/REPLACE/%_lib/g' src/egl/drivers/dri2/Makefile
%patch8
%patch9 -p0
%patch10 -p1

%build

%install
rm -f src/mesa/depend
export TALLOC_LIBS=-ltalloc
export TALLOC_CFLAGS="-I/usr/include"
autoreconf -fi
### libGL (disable savage/mga, bnc #402132/#403071; reenable mga, bnc #466635)
%configure --disable-glw \
           --with-driver=dri \
%ifarch %ix86 x86_64
%if 0%{?suse_version} >= 1130
           --with-dri-drivers=i810,i915,i965,mach64,r128,r200,r300,r600,radeon,sis,tdfx,unichrome,swrast,nouveau,mga \
%else
           --with-dri-drivers=i810,i915,i965,mach64,r128,r200,r300,r600,radeon,sis,tdfx,unichrome,swrast \
%endif
%if %enable_nouveau
           --enable-gallium-nouveau \
%endif
%endif
%ifarch ppc %sparc hppa
%if 0%{?suse_version} >= 1130
           --with-dri-drivers=i810,i915,i965,mach64,r128,r200,r300,r600,radeon,tdfx,unichrome,swrast,nouveau \
%else
           --with-dri-drivers=i810,i915,i965,mach64,r128,r200,r300,r600,radeon,tdfx,unichrome,swrast \
%endif
%endif
%ifarch s390 s390x
           --with-dri-drivers=swrast \
%endif
%ifarch %arm
           --with-dri-drivers=swrast \
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
           --disable-gallium \
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
%if 0%{?suse_version} > 1020
%fdupes -s $RPM_BUILD_ROOT/%_mandir
%endif 

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
%{_libdir}/egl/
%exclude %{_libdir}/dri/nouveau_dri.so
%if 0%{?suse_version} >= 1130
%exclude %{_libdir}/dri/nouveau_vieux_dri.so
%endif

%files devel
%defattr(-,root,root)
%doc docs/*.html docs/*.spec
%{_includedir}/GL
%{_includedir}/EGL
%{_includedir}/KHR
%exclude %{_includedir}/GL/glew.h
%exclude %{_includedir}/GL/glxew.h
%exclude %{_includedir}/GL/wglew.h
%{_libdir}/libGL.so
%{_libdir}/libGLU.so
%{_libdir}/libOSMesa.so
%{_libdir}/libEGL.so
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/pkgconfig/gl.pc
%{_libdir}/pkgconfig/glu.pc
%{_mandir}/man3/*

%files nouveau3d
%defattr(-,root,root)
%{_libdir}/dri/nouveau_dri.so
%if 0%{?suse_version} >= 1130
%{_libdir}/dri/nouveau_vieux_dri.so
%endif

%changelog
