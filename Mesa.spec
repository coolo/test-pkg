#
# spec file for package Mesa
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


%define glamor 1
%ifnarch s390 s390x aarch64 m68k
# Requires non-empty --with-gallium-drivers
%define egl_gallium 1
%else
%define egl_gallium 0
%endif
%ifarch %ix86 x86_64
%define llvm_r600 1
%else
%define llvm_r600 0
%endif

%define _version 10.0.3
%define _name_archive MesaLib

Name:           Mesa
Version:        10.0.2
Release:        0
BuildRequires:  autoconf >= 2.60
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  gcc-c++
%if %llvm_r600
BuildRequires:  libelf-devel
%endif
BuildRequires:  libexpat-devel
BuildRequires:  libtalloc-devel
BuildRequires:  libtool
BuildRequires:  libxml2-python
BuildRequires:  pkgconfig
BuildRequires:  python-base
BuildRequires:  xorg-x11-util-devel
BuildRequires:  pkgconfig(libdrm) >= 2.4.24
BuildRequires:  pkgconfig(xshmfence)
%ifarch %arm
BuildRequires:  pkgconfig(libdrm_freedreno) >= 2.4.43
%endif
%ifarch x86_64 %ix86
BuildRequires:  pkgconfig(libdrm_intel) >= 2.4.38
%endif
BuildRequires:  pkgconfig(libdrm_nouveau) >= 2.4.41
BuildRequires:  pkgconfig(libdrm_radeon) >= 2.4.45
BuildRequires:  pkgconfig(libkms) >= 1.0.0
BuildRequires:  pkgconfig(libudev) > 150
%if 0%{?suse_version} >= 1320
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
%endif
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb-dri2)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-glx)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(zlib)
%ifarch %arm ppc64 ppc64le s390x %ix86 x86_64
BuildRequires:  llvm-devel
%endif
BuildRequires:  libXvMC-devel
BuildRequires:  libvdpau-devel

Url:            http://www.mesa3d.org
Provides:       Mesa7 = %{version}
Obsoletes:      Mesa7 < %{version}
Provides:       intel-i810-Mesa = %{version}
Obsoletes:      intel-i810-Mesa < %{version}
Provides:       Mesa-libIndirectGL1 = %{version}
Obsoletes:      Mesa-libIndirectGL1 < %{version}
Provides:       xorg-x11-Mesa = %{version}
Obsoletes:      Mesa-nouveau3d
Obsoletes:      xorg-x11-Mesa < %{version}
# bug437293
%ifarch ppc64
Obsoletes:      Mesa-64bit < %{version}
Obsoletes:      XFree86-Mesa-64bit < %{version}
Provides:       Mesa-64bit < %{version}
Provides:       XFree86-Mesa-64bit = %{version}
%endif
#
Summary:        System for rendering interactive 3-D graphics
License:        MIT
Group:          System/Libraries
Source:         %{_name_archive}-%{_version}.tar.bz2
Source2:        baselibs.conf
Source3:        README.updates
Source4:        manual-pages.tar.bz2
Source6:        %name-rpmlintrc
# to be upstreamed
Patch11:        u_Fix-crash-in-swrast-when-setting-a-texture-for-a-pix.patch
# Patch from Fedora, fix 16bpp in llvmpipe
Patch13:        u_mesa-8.0.1-fix-16bpp.patch
# Patch from Fedora, use shmget when available, under llvmpipe
Patch15:        u_mesa-8.0-llvmpipe-shmget.patch
# PATCH-FIX-UPSTREAM Mesa-bnc864943-9.2.0-swrast-copy-sub-buffer.patch bnc#864943 federico@suse.com - Fix software rendering for Clutter/Cogl
Patch16:        Mesa-bnc864943-10.0.3-swrast-copy-sub-buffer.patch
Patch17:        U_0001-glx-Fix-the-default-values-for-GLXFBConfig-attribute.patch
Patch18:        U_0002-glx-Fix-the-GLXFBConfig-attrib-sort-priorities.patch
Patch19:        mesa-ppc64le-novector.patch
Patch20:        mesa-overflow-fix.patch
Patch21:        Mesa-fix-llvm-link.patch
Patch22:        u_mesa-gallium-llvmpipe-fix-SIGFPE.patch

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
Requires:       Mesa-libglapi-devel = %version
Requires:       libOSMesa-devel = %version
Requires:       libgbm-devel
%if 0%{?suse_version} >= 1320
Requires:       libwayland-egl-devel
%endif
# bug437293
%ifarch ppc64
Obsoletes:      Mesa-devel-64bit < %{version}
Obsoletes:      XFree86-Mesa-devel-64bit < %{version}
Provides:       Mesa-devel-64bit = %{version}
Provides:       XFree86-Mesa-devel-64bit = %{version}
%endif
#
Provides:       Mesa-devel-static = %{version}
Provides:       xorg-x11-Mesa-devel = %{version}
Obsoletes:      Mesa-devel-static < %{version}
Obsoletes:      xorg-x11-Mesa-devel < %{version}
Provides:       Mesa-libIndirectGL-devel = %{version}
Obsoletes:      Mesa-libIndirectGL-devel < %{version}

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
Requires:       Mesa = %version

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
Summary:        Free implementation of the OpenGL|ES 1.x Common Profile API
Group:          System/Libraries

%description -n Mesa-libGLESv1_CM1
OpenGL|ES is a cross-platform API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

OpenGL|ES 1.x provides an API for fixed-function hardware.

%package -n Mesa-libGLESv1_CM-devel
Summary:        Development files for the OpenGL ES 1.x API
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
Summary:        Development files for the OpenGL ES 2.x API
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

%package -n Mesa-libGLESv3-devel
Summary:        Development files for the OpenGL ES 3.x API
Group:          Development/Libraries/C and C++
#Requires:       Mesa-libGLESv3-3 = %version
Requires:       pkgconfig(egl)

%description -n Mesa-libGLESv3-devel
OpenGL|ES is a cross-platform API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

This package provides a development environment for building
applications using the OpenGL|ES 3.x APIs.

%package -n libOSMesa9
Summary:        Mesa Off-screen rendering extension
Group:          System/Libraries

%description -n libOSMesa9
OSmesa is a Mesa extension that allows programs to render to an
off-screen buffer using the OpenGL API without having to create a
rendering context on an X Server. It uses a pure software renderer.

%package -n libOSMesa-devel
Summary:        Development files for the Mesa Offscreen Rendering extension
Group:          Development/Libraries/C and C++
Requires:       libOSMesa9 = %version

%description -n libOSMesa-devel
Development files for the OSmesa Mesa extension that allows programs to render to an
off-screen buffer using the OpenGL API without having to create a
rendering context on an X Server. It uses a pure software renderer.

%package -n Mesa-libglapi0
Summary:        Free implementation of the GL API
Group:          System/Libraries

%description -n Mesa-libglapi0
The Mesa GL API module is responsible for dispatching all the gl*
functions. It is intended to be mainly used by the Mesa-libGLES*
packages.

%package -n Mesa-libglapi-devel
Summary:        Development files for the free implementation of the GL API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libglapi0 = %version

%description -n Mesa-libglapi-devel
Development files for the Mesa GL API module which is responsible for
dispatching all the gl* functions. It is intended to be mainly used by
the Mesa-libGLES* packages.

%package -n libgbm1
Summary:        Generic buffer management API
Group:          System/Libraries

%description -n libgbm1
This package contains the GBM buffer management library. It provides
a mechanism for allocating buffers for graphics rendering tied to
Mesa.

GBM is intended to be used as a native platform for EGL on drm or
openwfd.

%package -n libgbm-devel
Summary:        Development files for the EGL API
Group:          Development/Libraries/C and C++
Requires:       libgbm1 = %version

%description -n libgbm-devel
This package contains the GBM buffer management library. It provides
a mechanism for allocating buffers for graphics rendering tied to
Mesa.

GBM is intended to be used as a native platform for EGL on drm or
openwfd.

This package provides the development environment for compiling
programs against the GBM library.

%if 0%{?suse_version} >= 1320

%package -n libwayland-egl1
Summary:        Additional egl functions for wayland
Group:          System/Libraries

%description -n libwayland-egl1
This package provides additional functions for egl-using programs
that run within the wayland framework. This allows for applications
that need not run full-screen and cooperate with a compositor.

%package -n libwayland-egl-devel
Summary:        Development files for libwayland-egl1
Group:          Development/Libraries/C and C++
Requires:       libwayland-egl1 = %version

%description -n libwayland-egl-devel
This package is required to link wayland client applications to the EGL
implementation of Mesa.
%endif

%package -n libxatracker2
Summary:        XA state tracker
Group:          System/Libraries
Version:        1.0.0
Release:        0

%description -n libxatracker2
This package contains the XA state tracker for gallium3D driver.
It superseeds the Xorg state tracker and provides an infrastructure
to accelerate Xorg 2D operations. It is currently used by vmwgfx
video driver.

%package -n libxatracker-devel
Summary:        Development files for the XA API
Group:          Development/Libraries/C and C++
Version:        1.0.0
Release:        0
Requires:       libxatracker2 = %version

%description -n libxatracker-devel
This package contains the XA state tracker for gallium3D driver.
It superseeds the Xorg state tracker and provides an infrastructure
to accelerate Xorg 2D operations. It is currently used by vmwgfx
video driver.

This package provides the development environment for compiling
programs against the XA state tracker.

%package -n libXvMC_nouveau
Summary:        XVMC state tracker for Nouveau
Group:          System/Libraries

%description -n libXvMC_nouveau
This package contains the XvMC state tracker for Nouveau. This is
still "work in progress", i.e. expect poor video quality, choppy
videos and artefacts all over.

%package -n libXvMC_r600
Summary:        XVMC state tracker for R600
Group:          System/Libraries

%description -n libXvMC_r600
This package contains the XvMC state tracker for R600. This is
still "work in progress", i.e. expect poor video quality, choppy
videos and artefacts all over.

%package -n libvdpau_nouveau
Summary:        XVMC state tracker for Nouveau
Group:          System/Libraries
Supplements:    xf86-video-nouveau

%description -n libvdpau_nouveau
This package contains the VDPAU state tracker for Nouveau. 

%package -n libvdpau_r600
Summary:        XVMC state tracker for R600
Group:          System/Libraries
Supplements:    xf86-video-ati

%description -n libvdpau_r600
This package contains the VDPAU state tracker for R600. 

%package -n libvdpau_radeonsi
Summary:        XVMC state tracker for radeonsi
Group:          System/Libraries
Supplements:    xf86-video-ati

%description -n libvdpau_radeonsi
This package contains the VDPAU state tracker for radeonsi. 

%prep
%setup -n %{name}-%{_version} -b4 -q
# remove some docs
rm -rf docs/README.{VMS,WIN32,OS2}
#%patch11 -p1
#%patch15 -p1
#%patch13 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1

%build
rm -f src/mesa/depend
export TALLOC_LIBS=-ltalloc
export TALLOC_CFLAGS="-I/usr/include"
%if 0%{?suse_version} >= 1320
egl_platforms=x11,drm,wayland
%else
egl_platforms=x11,drm
%endif
autoreconf -fi
###           --with-gallium-drivers=r300,r600,radeonsi,nouveau,swrast,svga \
###           --with-gallium-drivers=r300,r600,nouveau,swrast,svga \
###           --with-gallium-drivers=r300,nouveau,swrast,svga \
%configure --enable-gles1 \
           --enable-gles2 \
           --enable-dri \
           --with-egl-platforms=$egl_platforms \
           --enable-shared-glapi \
           --enable-texture-float \
           --enable-osmesa \
%if %glamor
           --enable-gbm \
           --enable-glx-tls \
%endif
%if %egl_gallium
           --enable-gallium-egl \
%endif
           --with-dri-searchpath=/usr/%{_lib}/dri/updates:/usr/%{_lib}/dri \
%ifarch %ix86 x86_64
           --enable-xa \
           --enable-gallium-llvm \
           --with-dri-drivers=i915,i965,nouveau,r200,radeon \
           --enable-opencl-icd \
%if %llvm_r600
           --with-llvm-shared-libs \
           --enable-r600-llvm-compiler \
           --with-gallium-drivers=r300,r600,radeonsi,nouveau,swrast,svga \
%else
           --with-gallium-drivers=r300,r600,nouveau,swrast,svga \
%endif
           --enable-vdpau \
           --enable-xvmc \
%endif
%ifarch %arm ppc64 ppc64le
           --enable-xa \
           --enable-gallium-llvm \
           --with-dri-drivers=nouveau \
%ifarch %arm
           --with-gallium-drivers=r300,r600,nouveau,swrast,svga,freedreno \
%else
           --with-gallium-drivers=r300,r600,nouveau,swrast,svga \
%endif
           --enable-vdpau \
           --enable-xvmc \
%endif
%ifarch ia64 ppc %sparc hppa
           --with-dri-drivers=nouveau,r200,radeon \
           --with-gallium-drivers=r300,r600,nouveau,swrast \
%endif
%ifarch s390 aarch64 m68k
           --with-dri-drivers=swrast \
           --with-gallium-drivers="" \
%endif
%ifarch s390x
        --enable-xa \
        --enable-gallium-llvm \
        --with-dri-drivers=swrast \
        --with-gallium-drivers=swrast,svga \
%endif
           CFLAGS="$RPM_OPT_FLAGS -DNDEBUG"
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;

# Make a symlink to libGL.so.1.2 for compatibility (bnc#809359, bnc#831306)
test -f $RPM_BUILD_ROOT%{_libdir}/libGL.so.1.2 || \
  ln -s `readlink $RPM_BUILD_ROOT%{_libdir}/libGL.so.1` $RPM_BUILD_ROOT%{_libdir}/libGL.so.1.2

for dir in ../xc/doc/man/{GL/gl,GL/glx}; do
 pushd $dir
   xmkmf -a
   make %{?_smp_mflags}
   make install.man DESTDIR=$RPM_BUILD_ROOT MANPATH=%{_mandir} LIBMANSUFFIX=3gl
 popd
done
#DRI driver update mechanism
mkdir -p $RPM_BUILD_ROOT/usr/%{_lib}/dri/updates
install -m 644 $RPM_SOURCE_DIR/README.updates \
  $RPM_BUILD_ROOT/usr/%{_lib}/dri/updates

%fdupes -s $RPM_BUILD_ROOT/%_mandir
### disabled for now on request of Coolo
### "please take out this libs things from Cristian for 12.3 - I have no interest in debugging
###  broken build dependencies at this point"
#sed -i -e '/^Libs.private/d' -e '/^Requires.private/d' %{buildroot}%{_libdir}/pkgconfig/*.pc

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

%post   -n libOSMesa9 -p /sbin/ldconfig

%postun -n libOSMesa9 -p /sbin/ldconfig

%post   -n libgbm1 -p /sbin/ldconfig

%postun -n libgbm1 -p /sbin/ldconfig

%ifnarch s390 aarch64 m68k

%post   -n libxatracker2 -p /sbin/ldconfig

%postun -n libxatracker2 -p /sbin/ldconfig

%post   -n libXvMC_nouveau
%postun -n libXvMC_nouveau

%endif
%ifnarch s390 s390x aarch64 m68k

%post   -n libXvMC_r600

%postun -n libXvMC_r600

%post   -n libvdpau_r600
%postun -n libvdpau_r600

%if %llvm_r600
%post   -n libvdpau_radeonsi
%postun -n libvdpau_radeonsi
%endif
%endif

%post   -n Mesa-libglapi0 -p /sbin/ldconfig

%postun -n Mesa-libglapi0 -p /sbin/ldconfig

%if 0%{?suse_version} >= 1320
%post   -n libwayland-egl1 -p /sbin/ldconfig

%postun -n libwayland-egl1 -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc docs/README* docs/COPYING
%config /etc/drirc
%{_libdir}/dri/
%if %egl_gallium
%dir %_libdir/egl/
%_libdir/egl/egl_gallium.so
%dir %_libdir/gallium-pipe/
%_libdir/gallium-pipe/pipe_*.so
%endif

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
%exclude %_includedir/GL/osmesa.h
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

%files -n Mesa-libGLESv3-devel
%defattr(-,root,root)
%_includedir/GLES3
#%_libdir/libGLESv3.so
#%_libdir/pkgconfig/glesv3.pc

%files -n libOSMesa9
%defattr(-,root,root)
%_libdir/libOSMesa.so.8.0.0
%_libdir/libOSMesa.so.8

%files -n libOSMesa-devel
%defattr(-,root,root)
%_includedir/GL/osmesa.h
%_libdir/libOSMesa.so
%_libdir/pkgconfig/osmesa.pc

%if 0%{?suse_version} >= 1320
%files -n libwayland-egl1
%defattr(-,root,root)
%_libdir/libwayland-egl.so.1*

%files -n libwayland-egl-devel
%defattr(-,root,root)
%_libdir/libwayland-egl.so
%_libdir/pkgconfig/wayland-egl.pc

%endif

%files -n libgbm1
%defattr(-,root,root)
%_libdir/libgbm.so.1*
%if %egl_gallium
%dir %_libdir/gbm/
%_libdir/gbm/gbm_gallium_drm.so
%endif

%files -n libgbm-devel
%defattr(-,root,root)
%_includedir/gbm.h
%_libdir/libgbm.so
%_libdir/pkgconfig/gbm.pc

%ifnarch s390 ppc aarch64 m68k

%files -n libxatracker2
%defattr(-,root,root)
%_libdir/libxatracker.so.2*

%files -n libxatracker-devel
%defattr(-,root,root)
%_includedir/xa_*.h
%_libdir/libxatracker.so
%_libdir/pkgconfig/xatracker.pc

%endif

%ifnarch s390 s390x aarch64 m68k

%files -n libXvMC_nouveau
%defattr(-,root,root)
%_libdir/libXvMCnouveau.so
%_libdir/libXvMCnouveau.so.1
%_libdir/libXvMCnouveau.so.1.0.0

%files -n libvdpau_nouveau
%defattr(-,root,root)
%_libdir/vdpau/libvdpau_nouveau.so
%_libdir/vdpau/libvdpau_nouveau.so.1
%_libdir/vdpau/libvdpau_nouveau.so.1.0.0

%endif
%ifnarch s390 s390x aarch64 m68k

%files -n libXvMC_r600
%defattr(-,root,root)
%_libdir/libXvMCr600.so
%_libdir/libXvMCr600.so.1
%_libdir/libXvMCr600.so.1.0.0

%files -n libvdpau_r600
%defattr(-,root,root)
%_libdir/vdpau/libvdpau_r600.so
%_libdir/vdpau/libvdpau_r600.so.1
%_libdir/vdpau/libvdpau_r600.so.1.0.0

%endif

%if %llvm_r600
%files -n libvdpau_radeonsi
%defattr(-,root,root)
%_libdir/vdpau/libvdpau_radeonsi.so
%_libdir/vdpau/libvdpau_radeonsi.so.1
%_libdir/vdpau/libvdpau_radeonsi.so.1.0.0
%endif

%files -n Mesa-libglapi0
%defattr(-,root,root)
%_libdir/libglapi.so.0*

%files -n Mesa-libglapi-devel
%defattr(-,root,root)
%_libdir/libglapi.so

%files devel
%defattr(-,root,root)
%doc docs/*.html
%_includedir/GL/internal
%_libdir/pkgconfig/dri.pc

%changelog
