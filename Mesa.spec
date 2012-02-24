#
# spec file for package Mesa
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


#
%define _version 8.0.1

Name:           Mesa
Version:        8.0.1
Release:        0
BuildRequires:  autoconf >= 2.59
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  libexpat-devel
BuildRequires:  libtalloc-devel
BuildRequires:  libtool
BuildRequires:  libxml2-python
BuildRequires:  pkgconfig
BuildRequires:  python-base
BuildRequires:  xorg-x11-util-devel
BuildRequires:  pkgconfig(dri2proto) >= 2.1
BuildRequires:  pkgconfig(glproto) >= 1.4.11
BuildRequires:  pkgconfig(libdrm) >= 2.4.24
%ifarch x86_64 %ix86
BuildRequires:  pkgconfig(libdrm_intel) >= 2.4.24
%endif
BuildRequires:  pkgconfig(libdrm_nouveau) >= 0.6
BuildRequires:  pkgconfig(libdrm_radeon) >= 2.4.24
BuildRequires:  pkgconfig(libudev) > 150
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb-dri2)
BuildRequires:  pkgconfig(xcb-glx)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
%ifarch %ix86 x86_64
BuildRequires:  llvm-devel
%endif
BuildRequires:  vim
Url:            http://www.mesa3d.org
Provides:       Mesa7 = %{version}
Obsoletes:      Mesa7 < %{version}
Provides:       intel-i810-Mesa = %{version}
Obsoletes:      intel-i810-Mesa < %{version}
Provides:       xorg-x11-Mesa = %{version}
Obsoletes:      xorg-x11-Mesa < %{version} 
Obsoletes:      Mesa-nouveau3d
# bug437293
%ifarch ppc64
Obsoletes:      XFree86-Mesa-64bit < %{version} Mesa-64bit < %{version}
Provides:       Mesa-64bit < %{version}
Provides:       XFree86-Mesa-64bit = %{version}
%endif
#
Summary:        System for rendering interactive 3-D graphics
License:        MIT
Group:          System/Libraries
Source:         MesaLib-%{_version}.tar.bz2
Source2:        baselibs.conf
Source3:        README.updates
Source4:        manual-pages.tar.bz2
Source5:        drirc
Source6:        %name-rpmlintrc
# to be upstreamed
Patch11:        u_Fix-crash-in-swrast-when-setting-a-texture-for-a-pix.patch
# already upstream
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

%package devel
Summary:        Libraries, includes and more to develop Mesa applications
Group:          Development/Libraries/X11
Requires:       Mesa = %version
Requires:       Mesa-libEGL-devel = %version
Requires:       Mesa-libGL-devel = %version
Requires:       Mesa-libGLESv1_CM-devel = %version
Requires:       Mesa-libGLESv2-devel = %version
Requires:       Mesa-libGLU-devel = %version
Requires:       Mesa-libIndirectGL1 = %version
Requires:       libOSMesa8 = %version
Requires:       Mesa-libglapi0 = %version
Requires:       libgbm-devel
# bug437293
%ifarch ppc64
Obsoletes:      XFree86-Mesa-devel-64bit < %{version} Mesa-devel-64bit < %{version}
Provides:       Mesa-devel-64bit = %{version}
Provides:       XFree86-Mesa-devel-64bit = %{version}
%endif
#
Provides:       Mesa-devel-static = %{version}
Provides:       xorg-x11-Mesa-devel = %{version}
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

%package -n Mesa-libEGL1
# Kudos to Debian for the descriptions
Summary:        Free implementation of the EGL API
Group:          System/Libraries

%description -n Mesa-libEGL1
This package contains the EGL native platform graphics interface
library. EGL provides a platform-agnostic mechanism for creating
rendering surfaces for use with other graphics libraries, such as
OpenGL|ES and OpenVG.

This package contains modules to interface with the existing system
GLX or DRI2 drivers to provide OpenGL via EGL. The Mesa main package
provides drivers to provide hardware-accelerated OpenGL|ES and OpenVG
support.

%package -n Mesa-libEGL-devel
Summary:        Development files for the EGL API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libEGL1 = %version
# Other requires taken care of by pkgconfig already

%description -n Mesa-libEGL-devel
This package contains the development environment required for
compiling programs against EGL native platform graphics interface
library. EGL provides a platform-agnostic mechanism for creating
rendering surfaces for use with other graphics libraries, such as
OpenGL|ES and OpenVG.

This package provides the development environment for compiling
programs against the EGL library.

%package -n Mesa-libGL1
Summary:        The GL/GLX runtime of the Mesa 3D graphics library
Group:          System/Libraries

%description -n Mesa-libGL1
Mesa is a software library for 3D computer graphics that provides a
generic OpenGL implementation for rendering three-dimensional
graphics.

GLX ("OpenGL Extension to the X Window System") provides the
interface connecting OpenGL and the X Window System: it enables
programs wishing to use OpenGL to do so within a window provided by
the X Window System.

%package -n Mesa-libGL-devel
Summary:        GL/GLX development files of the OpenGL API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libGL1 = %version

%description -n Mesa-libGL-devel
Mesa is a software library for 3D computer graphics that provides a
generic OpenGL implementation for rendering three-dimensional
graphics.

This package includes headers and static libraries for compiling
programs with Mesa.

%package -n Mesa-libGLESv1_CM1
Summary:        Free implementation of the OpenGL|ES 1.x API
Group:          System/Libraries

%description -n Mesa-libGLESv1_CM1
OpenGL|ES is a cross-platform API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

OpenGL|ES 1.x provides an API for fixed-function hardware.

%package -n Mesa-libGLESv1_CM-devel
Summary:        Development files for the EGL API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libGLESv1_CM1 = %version
Requires:       pkgconfig(egl)

%description -n Mesa-libGLESv1_CM-devel
OpenGL|ES is a cross-platform API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

OpenGL|ES 1.x provides an API for fixed-function hardware.

This package provides a development environment for building programs
using the OpenGL|ES 1.x APIs.

%package -n Mesa-libGLESv2-2
Summary:        Free implementation of the OpenGL|ES 2.x API
Group:          System/Libraries

%description -n Mesa-libGLESv2-2
OpenGL|ES is a cross-platform API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

OpenGL|ES 2.x provides an API for programmable hardware including
vertex and fragment shaders.

%package -n Mesa-libGLESv2-devel
Summary:        Development files for the EGL API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libGLESv2-2 = %version
Requires:       pkgconfig(egl)

%description -n Mesa-libGLESv2-devel
OpenGL|ES is a cross-platform API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

OpenGL|ES 2.x provides an API for programmable hardware including
vertex and fragment shaders.

This package provides a development environment for building
applications using the OpenGL|ES 2.x APIs.

%package -n Mesa-libGLU1
Summary:        Mesa OpenGL utility library
Group:          System/Libraries

%description -n Mesa-libGLU1
GLU offers simple interfaces for building mipmaps; checking for the
presence of extensions in the OpenGL (or other libraries which follow
the same conventions for advertising extensions); drawing
piecewise-linear curves, NURBS, quadrics and other primitives
(including, but not limited to, teapots); tesselating surfaces;
setting up projection matrices and unprojecting screen coordinates to
world coordinates.

This package provides the SGI implementation of GLU shipped with the
Mesa package.

%package -n Mesa-libGLU-devel
Summary:        Development files for the EGL API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libGLU1 = %version

%description -n Mesa-libGLU-devel
GLU offers simple interfaces for building mipmaps; checking for the
presence of extensions in the OpenGL (or other libraries which follow
the same conventions for advertising extensions); drawing
piecewise-linear curves, NURBS, quadrics and other primitives
(including, but not limited to, teapots); tesselating surfaces;
setting up projection matrices and unprojecting screen coordinates to
world coordinates.

This package contains includes headers and static libraries for
compiling programs with GLU.

%package -n Mesa-libIndirectGL1
# This is the equivalent to Debian's libgl1-mesa-swx11
Summary:        Free implementation of the OpenGL API
Group:          System/Libraries

%description -n Mesa-libIndirectGL1
This library provides a pure software rasterizer; it does not provide
a direct rendering capable library, or one which uses GLX. For that,
please see Mesa-libGL1.

%package -n libOSMesa8
Summary:        Mesa Off-screen rendering extension
Group:          System/Libraries

%description -n libOSMesa8
OSmesa is a Mesa extension that allows programs to render to an
off-screen buffer using the OpenGL API without having to create a
rendering context on an X Server. It uses a pure software renderer.

%package -n libgbm1
Summary:        Generic buffer management API
Group:          System/Libraries
# as per gbm.pc
Version:        0.0.0
Release:        0

%description -n libgbm1
This package contains the GBM buffer management library. It provides
a mechanism for allocating buffers for graphics rendering tied to
Mesa.

GBM is intended to be used as a native platform for EGL on drm or
openwfd.

%package -n libgbm-devel
Summary:        Development files for the EGL API
Group:          Development/Libraries/C and C++
Version:        0.0.0
Release:        0
Requires:       libgbm1 = %version

%description -n libgbm-devel
This package contains the GBM buffer management library. It provides
a mechanism for allocating buffers for graphics rendering tied to
Mesa.

GBM is intended to be used as a native platform for EGL on drm or
openwfd.

This package provides the development environment for compiling
programs against the GBM library.

%package -n Mesa-libglapi0
Summary:        Free implementation of the GL API
Group:          System/Libraries

%description -n Mesa-libglapi0
The Mesa GL API module is responsible for dispatching all the gl*
functions. It is intended to be mainly used by the Mesa-libGLES*
packages.

%prep
%setup -n %{name}-%{_version} -b4 -q
# no need to build (GLUT-)Demos
rm -rf src/glut progs/{demos,redbook,samples,xdemos,glsl}
# we use freeglut
rm -f include/GL/{glut.h,uglglutshapes.h,glutf90.h}
# remove some docs
rm -rf docs/README.{VMS,WIN32,OS2}
#%patch11 -p1

%build

%install
rm -f src/mesa/depend
export TALLOC_LIBS=-ltalloc
export TALLOC_CFLAGS="-I/usr/include"
autoreconf -fi
%configure --disable-glw \
           --enable-gles1 \
           --enable-gles2 \
           --with-driver=dri \
           --with-egl-platforms=x11,drm \
           --enable-shared-glapi \
           --enable-shared-dricore \
           --with-dri-searchpath=/usr/%{_lib}/dri/updates:/usr/%{_lib}/dri \
%ifarch %ix86 x86_64
           --with-dri-drivers=i915,i965,nouveau,r200,radeon \
           --with-gallium-drivers=r300,r600,nouveau,swrast \
%endif
%ifarch ppc ppc64 %sparc hppa
           --with-dri-drivers=nouveau,r200,radeon \
           --with-gallium-drivers=r300,r600,nouveau,swrast \
%endif
%ifarch s390 s390x %arm
           --with-dri-drivers=swrast \
           --with-gallium-drivers="" \
%endif
           --disable-glut \
           CFLAGS="$RPM_OPT_FLAGS -DNDEBUG"
make %{?_smp_mflags}
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
make %{?_smp_mflags}
cp -a %{_lib}/libIndirectGL.so.* %{_lib}/libOSMesa.so* \
  $RPM_BUILD_ROOT/usr/%{_lib}
for dir in ../xc/doc/man/{GL/gl,GL/glx,GLU}; do
pushd $dir
  xmkmf -a
  make %{?_smp_mflags}
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

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post   -n Mesa-libEGL1 -p /sbin/ldconfig

%postun -n Mesa-libEGL1 -p /sbin/ldconfig

%post   -n Mesa-libGL1 -p /sbin/ldconfig

%postun -n Mesa-libGL1 -p /sbin/ldconfig

%post   -n Mesa-libGLESv1_CM1 -p /sbin/ldconfig

%postun -n Mesa-libGLESv1_CM1 -p /sbin/ldconfig

%post   -n Mesa-libGLESv2-2 -p /sbin/ldconfig

%postun -n Mesa-libGLESv2-2 -p /sbin/ldconfig

%post   -n Mesa-libGLU1 -p /sbin/ldconfig

%postun -n Mesa-libGLU1 -p /sbin/ldconfig

%post   -n Mesa-libIndirectGL1 -p /sbin/ldconfig

%postun -n Mesa-libIndirectGL1 -p /sbin/ldconfig

%post   -n libOSMesa8 -p /sbin/ldconfig

%postun -n libOSMesa8 -p /sbin/ldconfig

%post   -n libgbm1 -p /sbin/ldconfig

%postun -n libgbm1 -p /sbin/ldconfig

%post   -n Mesa-libglapi0 -p /sbin/ldconfig

%postun -n Mesa-libglapi0 -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs/README* docs/COPYING
%config /etc/drirc
%{_libdir}/dri/
#%{_libdir}/egl/

%files -n Mesa-libEGL1
%defattr(-,root,root)
%_libdir/libEGL.so.1*

%files -n Mesa-libEGL-devel
%defattr(-,root,root)
%_includedir/EGL
%_includedir/KHR
%_libdir/libEGL.so
%_libdir/pkgconfig/egl.pc

%files -n Mesa-libGL1
%defattr(-,root,root)
%_libdir/libGL.so.1*

%files -n Mesa-libGL-devel
%defattr(-,root,root)
%dir %_includedir/GL
%_includedir/GL/*.h
%exclude %_includedir/GL/glu*.h
%_libdir/libGL.so
%_libdir/pkgconfig/gl.pc
%_mandir/man3/gl[A-Z]*

%files -n Mesa-libGLESv1_CM1
%defattr(-,root,root)
%_libdir/libGLESv1_CM.so.1*

%files -n Mesa-libGLESv1_CM-devel
%defattr(-,root,root)
%_includedir/GLES
%_libdir/libGLESv1_CM.so
%_libdir/pkgconfig/glesv1_cm.pc

%files -n Mesa-libGLESv2-2
%defattr(-,root,root)
%_libdir/libGLESv2.so.2*

%files -n Mesa-libGLESv2-devel
%defattr(-,root,root)
%_includedir/GLES2
%_libdir/libGLESv2.so
%_libdir/pkgconfig/glesv2.pc

%files -n Mesa-libGLU1
%defattr(-,root,root)
%_libdir/libGLU.so.1*

%files -n Mesa-libGLU-devel
%defattr(-,root,root)
%dir %_includedir/GL
%_includedir/GL/glu*.h
%_libdir/libGLU.so
%_libdir/pkgconfig/glu.pc
%_mandir/man3/glu*

%files -n Mesa-libIndirectGL1
%defattr(-,root,root)
%_libdir/libIndirectGL.so.1*

%files -n libOSMesa8
%defattr(-,root,root)
%_libdir/libOSMesa.so.8*

%files -n libgbm1
%defattr(-,root,root)
%_libdir/libgbm.so.1*

%files -n libgbm-devel
%defattr(-,root,root)
%_includedir/gbm.h
%_libdir/libgbm.so
%_libdir/pkgconfig/gbm.pc

%files -n Mesa-libglapi0
%defattr(-,root,root)
%_libdir/libglapi.so.0*

%files devel
%defattr(-,root,root)
%doc docs/*.html docs/*.spec
%_includedir/GL/internal
%_libdir/libOSMesa.so
%_libdir/libglapi.so
%_libdir/pkgconfig/dri.pc

%changelog
