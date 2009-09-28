#
# spec file for package Mesa (Version 7.5.2)
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

# norootforbuild


Name:           Mesa
BuildRequires:  gcc-c++ libdrm-devel libexpat-devel pkgconfig xorg-x11-devel
Url:            http://www.mesa3d.org
License:        MIT License (or similar)
Group:          System/Libraries
Provides:       xorg-x11-Mesa intel-i810-Mesa Mesa7
Obsoletes:      xorg-x11-Mesa intel-i810-Mesa Mesa7
AutoReqProv:    on
# bug437293
%ifarch ppc64
Obsoletes:      XFree86-Mesa-64bit
Obsoletes:      Mesa-64bit
%endif
#
Version:        7.5.2
Release:        1
Summary:        Mesa is a 3-D graphics library with an API which is very similar to that of OpenGL
Source:         MesaLib-%{version}.tar.bz2
Source1:        MesaDemos-%{version}.tar.bz2
Source3:        README.updates
Source4:        manual-pages.tar.bz2
Source5:        drirc
Patch1:         dri_driver_dir.diff
Patch6:         link-shared.diff
Patch7:         disable_gem_warning.diff
Patch15:        Mesa_indirect_old_xserver_compatibility.diff
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
Group:          System/Libraries
# bug437293
%ifarch ppc64
Obsoletes:      XFree86-Mesa-devel-64bit
Obsoletes:      Mesa-devel-64bit
%endif
#
Provides:       xorg-x11-Mesa-devel Mesa-devel-static
Obsoletes:      xorg-x11-Mesa-devel Mesa-devel-static

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
%setup -n %{name}-%{version} -b1 -b4
# make legal department happy (Bug #204110)
test -f src/mesa/drivers/directfb/idirectfbgl_mesa.c && exit 1
test -f progs/ggi/asc-view.c && exit 1
# no need to build (GLUT-)Demos
rm -rf src/glut progs/{demos,redbook,samples,xdemos,glsl}
# we use freeglut
rm -f include/GL/{glut.h,uglglutshapes.h,glutf90.h}
%patch1
sed -i 's/REPLACE/%_lib/g' src/glx/x11/Makefile
### FIXME
#%patch6
%patch7 -p1
%patch15 -p1

%build

%install
rm src/mesa/depend
autoreconf -fi
### libGL (disable savage/mga, bnc #402132/#403071)
%configure --disable-glw \
           --with-driver=dri \
%ifarch %ix86 x86_64
           --with-dri-drivers=i810,i915,i965,mach64,r128,r200,r300,radeon,s3v,sis,tdfx,trident,unichrome,ffb,swrast \
           --enable-gallium-nouveau \
%endif
%ifarch ppc
           --with-dri-drivers=i810,i915,i965,mach64,r128,r200,r300,radeon,s3v,tdfx,trident,unichrome,ffb,swrast \
%endif
%ifarch s390 s390x
           --with-dri-drivers=swrast \
%endif
%ifarch %arm
           --with-dri-drivers=swrast \
%endif
           --disable-glut
make -C src/gallium/state_trackers/dri
gmake
make install DESTDIR=$RPM_BUILD_ROOT
# build and install Indirect Rendering only libGL
make realclean
%configure --with-driver=xlib \
           --disable-glu \
           --disable-glw \
           --disable-glut \
           --disable-gallium
sed -i 's/GL_LIB = .*/GL_LIB = IndirectGL/g' configs/autoconf
gmake 
cp -a %{_lib}/libIndirectGL.so.* %{_lib}/libOSMesa.so* \
  $RPM_BUILD_ROOT/usr/%{_lib}
for dir in ../xc/doc/man/{GL/gl,GL/glx,GLU}; do
pushd $dir
  xmkmf -a
  make
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

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs/README* docs/COPYING
%config /etc/drirc
/usr/include/GL/gl.h
/usr/include/GL/glext.h
/usr/include/GL/glx.h
/usr/include/GL/glxext.h
/usr/%{_lib}/libGL.so
/usr/%{_lib}/lib*.so.*
/usr/%{_lib}/dri/

%files devel
%defattr(-,root,root)
%doc docs/*.html docs/*.spec
/usr/include/GL/dmesa.h
/usr/include/GL/ggimesa.h
/usr/include/GL/gl_mangle.h
/usr/include/GL/glfbdev.h
/usr/include/GL/glu.h
/usr/include/GL/glu_mangle.h
/usr/include/GL/glx_mangle.h
/usr/include/GL/mesa_wgl.h
/usr/include/GL/mglmesa.h
/usr/include/GL/osmesa.h
/usr/include/GL/svgamesa.h
/usr/include/GL/vms_x_fix.h
/usr/include/GL/wmesa.h
/usr/include/GL/internal/dri_interface.h
/usr/include/GL/wglext.h
%exclude /usr/include/GL/glew.h
%exclude /usr/include/GL/glxew.h
%exclude /usr/include/GL/wglew.h
/usr/%{_lib}/libGLU.so
/usr/%{_lib}/libOSMesa.so
/usr/%{_lib}/libEGL.so
/usr/%{_lib}/pkgconfig/dri.pc
/usr/%{_lib}/pkgconfig/gl.pc
/usr/%{_lib}/pkgconfig/glu.pc
%{_mandir}/man3/*

%changelog
