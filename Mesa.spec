#
# spec file for package Mesa
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
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
%define _name_archive mesa
%define _version 11.1.0
%define with_opencl 0
%ifarch %ix86 x86_64 %arm ppc ppc64 ppc64le s390x
%define gallium_loader 1
%else
%define gallium_loader 0
%endif
%ifarch %ix86 x86_64 %arm ppc ppc64 ppc64le
%define xvmc_support 1
%define vdpau_nouveau 1
%define vdpau_radeon 1
%else
%define xvmc_support 0
%define vdpau_nouveau 0
%define vdpau_radeon 0
%endif
%ifarch %ix86 x86_64
%define with_nine 1
%if 0%{gallium_loader} && 0%{?suse_version} > 1310
# llvm >= 3.7 not provided for <= 13.1
%define with_opencl 1
%endif
%endif
Name:           Mesa
Version:        11.1.0
Release:        0
Summary:        System for rendering interactive 3-D graphics
License:        MIT
Group:          System/Libraries
Url:            http://www.mesa3d.org
Source:         ftp://ftp.freedesktop.org/pub/mesa/%{_version}/%{_name_archive}-%{_version}.tar.xz
Source1:        ftp://ftp.freedesktop.org/pub/mesa/%{_version}/%{_name_archive}-%{_version}.tar.xz.sig
Source2:        baselibs.conf
Source3:        README.updates
Source4:        manual-pages.tar.bz2
Source6:        %{name}-rpmlintrc
Source7:        Mesa.keyring
# required for building against wayland of openSUSE 13.1
Patch0:         n_Fixed-build-against-wayland-1.2.1.patch
# to be upstreamed
Patch11:        u_Fix-crash-in-swrast-when-setting-a-texture-for-a-pix.patch
# Patch from Fedora, fix 16bpp in llvmpipe
Patch13:        u_mesa-8.0.1-fix-16bpp.patch
# Patch from Fedora, use shmget when available, under llvmpipe
Patch15:        u_mesa-8.0-llvmpipe-shmget.patch
BuildRequires:  autoconf >= 2.60
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  imake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  python-base
BuildRequires:  python-mako
BuildRequires:  python-xml
BuildRequires:  pkgconfig(dri2proto)
BuildRequires:  pkgconfig(dri3proto)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(glproto)
BuildRequires:  pkgconfig(libdrm) >= 2.4.60
BuildRequires:  pkgconfig(libdrm_amdgpu) >= 2.4.63
BuildRequires:  pkgconfig(libdrm_nouveau) >= 2.4.62
BuildRequires:  pkgconfig(libdrm_radeon) >= 2.4.56
BuildRequires:  pkgconfig(libkms) >= 1.0.0
BuildRequires:  pkgconfig(libudev) > 151
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(presentproto)
BuildRequires:  pkgconfig(vdpau) >= 0.4.1
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb-dri2)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-glx)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xshmfence)
BuildRequires:  pkgconfig(xvmc)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(zlib)
Provides:       Mesa7 = %{version}
Obsoletes:      Mesa7 < %{version}
Provides:       intel-i810-Mesa = %{version}
Obsoletes:      intel-i810-Mesa < %{version}
Provides:       Mesa-libIndirectGL1 = %{version}
Obsoletes:      Mesa-libIndirectGL1 < %{version}
Provides:       Mesa-nouveau3d = %{version}
Provides:       xorg-x11-Mesa = %{version}
Obsoletes:      Mesa-nouveau3d < %{version}
Obsoletes:      xorg-x11-Mesa < %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%ifarch %arm
BuildRequires:  pkgconfig(libdrm_freedreno) >= 2.4.65
%endif
%ifarch x86_64 %ix86
BuildRequires:  libelf-devel
BuildRequires:  pkgconfig(libdrm_intel) >= 2.4.61
%endif
%if 0%{?suse_version} >= 1310
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
%endif
%ifarch %arm ppc64 ppc64le s390x %ix86 x86_64
BuildRequires:  llvm-devel
BuildRequires:  ncurses-devel
%endif
#!BuildIgnore:  python

%if 0%{with_opencl}
BuildRequires:  libclc
BuildRequires:  llvm-clang-devel
%endif

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
Requires:       Mesa = %{version}
Requires:       Mesa-dri-devel = %{version}
Requires:       Mesa-libEGL-devel = %{version}
Requires:       Mesa-libGL-devel = %{version}
Requires:       Mesa-libGLESv1_CM-devel = %{version}
Requires:       Mesa-libGLESv2-devel = %{version}
Requires:       Mesa-libglapi-devel = %{version}
Requires:       libOSMesa-devel = %{version}
Requires:       libgbm-devel
Provides:       Mesa-devel-static = %{version}
Provides:       xorg-x11-Mesa-devel = %{version}
Obsoletes:      Mesa-devel-static < %{version}
Obsoletes:      xorg-x11-Mesa-devel < %{version}
Provides:       Mesa-libIndirectGL-devel = %{version}
Obsoletes:      Mesa-libIndirectGL-devel < %{version}
%if 0%{?suse_version} >= 1310
Requires:       libwayland-egl-devel
%endif

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
Requires:       Mesa-libEGL1 = %{version}
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
Requires:       Mesa = %{version}

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
Requires:       Mesa-libGL1 = %{version}

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
Requires:       Mesa-libGLESv1_CM1 = %{version}
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

The libGLESv2.so.2 library provides symbols for all OpenGL ES 2 and
ES 3 entry points.

%package -n Mesa-libGLESv2-devel
Summary:        Development files for the OpenGL ES 2.x API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libGLESv2-2 = %{version}
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
Requires:       Mesa-libGLESv2-2 = %{version}
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
Requires:       libOSMesa9 = %{version}

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
Requires:       Mesa-libglapi0 = %{version}

%description -n Mesa-libglapi-devel
Development files for the Mesa GL API module which is responsible for
dispatching all the gl* functions. It is intended to be mainly used by
the Mesa-libGLES* packages.

%package -n Mesa-dri-devel
Summary:        Development files for the DRI API
Group:          Development/Libraries/C and C++
Requires:       Mesa = %{version}

%description -n Mesa-dri-devel
This package contains the development environment required for
compiling programs and libraries using the DRI API.

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
Requires:       libgbm1 = %{version}

%description -n libgbm-devel
This package contains the GBM buffer management library. It provides
a mechanism for allocating buffers for graphics rendering tied to
Mesa.

GBM is intended to be used as a native platform for EGL on drm or
openwfd.

This package provides the development environment for compiling
programs against the GBM library.

%if 0%{?suse_version} >= 1310
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
Requires:       libwayland-egl1 = %{version}

%description -n libwayland-egl-devel
This package is required to link wayland client applications to the EGL
implementation of Mesa.
%endif

%if 0%{?with_nine}
%package libd3d
Summary:        Mesa Direct3D9 state tracker
Group:          System/Libraries
# Manually provide d3d library (bnc#918294)
%ifarch x86_64 s390x ppc64le aarch64
Provides:       d3dadapter9.so.1()(64bit)
%else
Provides:       d3dadapter9.so.1
%endif

%description libd3d
Mesa Direct3D9 state tracker

%package libd3d-devel
Summary:        Mesa Direct3D9 state tracker development package
Group:          System/Libraries
Requires:       %{name}-libd3d = %{version}

%description libd3d-devel
Mesa Direct3D9 state tracker development package
%endif

%package -n libxatracker2
Version:        1.0.0
Release:        0
Summary:        XA state tracker
Group:          System/Libraries

%description -n libxatracker2
This package contains the XA state tracker for gallium3D driver.
It superseeds the Xorg state tracker and provides an infrastructure
to accelerate Xorg 2D operations. It is currently used by vmwgfx
video driver.

%package -n libxatracker-devel
Version:        1.0.0
Release:        0
Summary:        Development files for the XA API
Group:          Development/Libraries/C and C++
Requires:       libxatracker2 = %{version}

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

%package -n libvdpau_r300
Summary:        XVMC state tracker for R300
Group:          System/Libraries
Supplements:    xf86-video-ati

%description -n libvdpau_r300
This package contains the VDPAU state tracker for R300.

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

%if 0%{with_opencl}
%package libOpenCL
Summary:        Mesa OpenCL implementation
Group:          System/Libraries

%description libOpenCL
This package contains the Mesa OpenCL implementation or GalliumCompute.
%endif

%package libva
Summary:        Mesa VA-API implementation
Group:          System/Libraries
Supplements:    Mesa

%description libva
This package contains the Mesa VA-API implementation provided through gallium.

%prep
%setup -q -n %{_name_archive}-%{_version} -b4
# remove some docs
rm -rf docs/README.{VMS,WIN32,OS2}
%if 0%{?suse_version} < 1320
# required for building against wayland of openSUSE 13.1
%patch0 -p1
%endif
### disabled, but not dropped yet; these still need investigation in
### order to figure out whether the issue is still reproducable and
### hence a fix is required
#%patch11 -p1
#%patch15 -p1
#%patch13 -p1

%build
%if 0%{?suse_version} >= 1310
egl_platforms=x11,drm,wayland
%else
egl_platforms=x11,drm
%endif
autoreconf -fvi
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
           --enable-dri3 \
           --enable-shader-cache \
           %{?with_nine:--enable-nine} \
%if %{glamor}
           --enable-gbm \
           --enable-glx-tls \
%endif
%if 0%{?suse_version} < 1315
           --with-dri-searchpath=%{_libdir}/dri/updates:%{_libdir}/dri \
%else
           --with-dri-searchpath=%{_libdir}/dri \
%endif
%ifarch %ix86 x86_64
           --enable-xa \
           --enable-gallium-llvm \
           --with-dri-drivers=i915,i965,nouveau,r200,radeon \
%if 0%{with_opencl}
           --enable-opencl \
           --enable-opencl-icd \
%endif
           --enable-llvm-shared-libs \
           --enable-r600-llvm-compiler \
           --with-gallium-drivers=r300,r600,radeonsi,nouveau,swrast,svga \
           --enable-vdpau \
           --enable-va \
           --enable-xvmc \
%endif
%ifarch %arm ppc64 ppc64le
           --enable-xa \
           --enable-gallium-llvm \
           --with-dri-drivers=nouveau \
%ifarch %arm
           --with-gallium-drivers=r300,r600,nouveau,swrast,svga,freedreno,vc4 \
%else
           --with-gallium-drivers=r300,r600,nouveau,swrast,svga \
%endif
           --enable-vdpau \
           --enable-xvmc \
%endif
%ifarch ia64 ppc hppa
           --with-dri-drivers=nouveau,r200,radeon \
           --with-gallium-drivers=r300,r600,nouveau,swrast \
%endif
%ifarch s390 aarch64
           --with-dri-drivers=swrast \
           --with-gallium-drivers="" \
%endif
%ifarch s390x
        --enable-xa \
        --enable-gallium-llvm \
        --with-dri-drivers=swrast \
        --with-gallium-drivers=swrast,svga \
%endif
        CFLAGS="%{optflags} -DNDEBUG"
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -type f -name "*.la" -delete -print

# Make a symlink to libGL.so.1.2 for compatibility (bnc#809359, bnc#831306)
test -f %{buildroot}%{_libdir}/libGL.so.1.2 || \
  ln -s `readlink %{buildroot}%{_libdir}/libGL.so.1` %{buildroot}%{_libdir}/libGL.so.1.2

for dir in ../xc/doc/man/{GL/gl,GL/glx}; do
 pushd $dir
   xmkmf -a
   make %{?_smp_mflags}
   make install.man DESTDIR=%{buildroot} MANPATH=%{_mandir} LIBMANSUFFIX=3gl
 popd
done
%if 0%{?suse_version} < 1315
#DRI driver update mechanism
mkdir -p %{buildroot}%{_libdir}/dri/updates
install -m 644 $RPM_SOURCE_DIR/README.updates \
  %{buildroot}%{_libdir}/dri/updates
%endif

%fdupes -s %{buildroot}/%{_mandir}

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

%ifarch %ix86 x86_64 %arm ppc64 ppc64le s390x
%post   -n libxatracker2 -p /sbin/ldconfig

%postun -n libxatracker2 -p /sbin/ldconfig
%endif

%if %{xvmc_support}
%post   -n libXvMC_nouveau -p /sbin/ldconfig

%postun -n libXvMC_nouveau -p /sbin/ldconfig

%post   -n libXvMC_r600 -p /sbin/ldconfig

%postun -n libXvMC_r600 -p /sbin/ldconfig
%endif

%if %{vdpau_radeon}
%post   -n libvdpau_r300 -p /sbin/ldconfig

%postun -n libvdpau_r300 -p /sbin/ldconfig

%post   -n libvdpau_r600 -p /sbin/ldconfig

%postun -n libvdpau_r600 -p /sbin/ldconfig
%endif

%ifarch %ix86 x86_64
%post   -n libvdpau_radeonsi -p /sbin/ldconfig

%postun -n libvdpau_radeonsi -p /sbin/ldconfig
%endif

%post   -n Mesa-libglapi0 -p /sbin/ldconfig

%postun -n Mesa-libglapi0 -p /sbin/ldconfig

%if 0%{?suse_version} >= 1310
%post   -n libwayland-egl1 -p /sbin/ldconfig

%postun -n libwayland-egl1 -p /sbin/ldconfig
%endif

%if 0%{?with_nine}
%post libd3d -p /sbin/ldconfig

%postun libd3d -p /sbin/ldconfig
%endif

%if 0%{with_opencl}
%post   libOpenCL -p /sbin/ldconfig

%postun libOpenCL -p /sbin/ldconfig
%endif

%post libva -p /sbin/ldconfig

%postun libva -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs/README* docs/COPYING
%config %{_sysconfdir}/drirc
%dir %{_libdir}/dri
%if 0%{?suse_version} < 1315
%{_libdir}/dri/updates
%endif
%{_libdir}/dri/*_dri.so
%if 0%{with_opencl}
# only built with opencl
%dir %{_libdir}/gallium-pipe/
%{_libdir}/gallium-pipe/pipe_*.so
%endif

%files -n Mesa-libEGL1
%defattr(-,root,root)
%{_libdir}/libEGL.so.1*

%files -n Mesa-libEGL-devel
%defattr(-,root,root)
%{_includedir}/EGL
%{_includedir}/KHR
%{_libdir}/libEGL.so
%{_libdir}/pkgconfig/egl.pc

%files -n Mesa-libGL1
%defattr(-,root,root)
%{_libdir}/libGL.so.1*

%files -n Mesa-libGL-devel
%defattr(-,root,root)
%dir %{_includedir}/GL
%{_includedir}/GL/*.h
%exclude %{_includedir}/GL/osmesa.h
%{_libdir}/libGL.so
%{_libdir}/pkgconfig/gl.pc
%{_mandir}/man3/gl[A-Z]*

%files -n Mesa-libGLESv1_CM1
%defattr(-,root,root)
%{_libdir}/libGLESv1_CM.so.1*

%files -n Mesa-libGLESv1_CM-devel
%defattr(-,root,root)
%{_includedir}/GLES
%{_libdir}/libGLESv1_CM.so
%{_libdir}/pkgconfig/glesv1_cm.pc

%files -n Mesa-libGLESv2-2
%defattr(-,root,root)
%{_libdir}/libGLESv2.so.2*

%files -n Mesa-libGLESv2-devel
%defattr(-,root,root)
%{_includedir}/GLES2
%{_libdir}/libGLESv2.so
%{_libdir}/pkgconfig/glesv2.pc

%files -n Mesa-libGLESv3-devel
%defattr(-,root,root)
%{_includedir}/GLES3
#%_libdir/libGLESv3.so
#%_libdir/pkgconfig/glesv3.pc

%files -n libOSMesa9
%defattr(-,root,root)
%{_libdir}/libOSMesa.so.8.0.0
%{_libdir}/libOSMesa.so.8

%files -n libOSMesa-devel
%defattr(-,root,root)
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%if 0%{?suse_version} >= 1310
%files -n libwayland-egl1
%defattr(-,root,root)
%{_libdir}/libwayland-egl.so.1*

%files -n libwayland-egl-devel
%defattr(-,root,root)
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc
%endif

%files -n libgbm1
%defattr(-,root,root)
%{_libdir}/libgbm.so.1*

%files -n libgbm-devel
%defattr(-,root,root)
%{_includedir}/gbm.h
%{_libdir}/libgbm.so
%{_libdir}/pkgconfig/gbm.pc

%ifarch %ix86 x86_64 %arm ppc64 ppc64le s390x
%files -n libxatracker2
%defattr(-,root,root)
%{_libdir}/libxatracker.so.2*

%files -n libxatracker-devel
%defattr(-,root,root)
%{_includedir}/xa_*.h
%{_libdir}/libxatracker.so
%{_libdir}/pkgconfig/xatracker.pc
%endif

%if %{xvmc_support}
%files -n libXvMC_nouveau
%defattr(-,root,root)
%{_libdir}/libXvMCnouveau.so
%{_libdir}/libXvMCnouveau.so.1
%{_libdir}/libXvMCnouveau.so.1.0
%{_libdir}/libXvMCnouveau.so.1.0.0

%files -n libXvMC_r600
%defattr(-,root,root)
%{_libdir}/libXvMCr600.so
%{_libdir}/libXvMCr600.so.1
%{_libdir}/libXvMCr600.so.1.0
%{_libdir}/libXvMCr600.so.1.0.0
%endif

%if %{vdpau_nouveau}
%files -n libvdpau_nouveau
%defattr(-,root,root)
%{_libdir}/vdpau/libvdpau_nouveau.so
%{_libdir}/vdpau/libvdpau_nouveau.so.1
%{_libdir}/vdpau/libvdpau_nouveau.so.1.0
%{_libdir}/vdpau/libvdpau_nouveau.so.1.0.0
%endif

%if %{vdpau_radeon}
%files -n libvdpau_r300
%defattr(-,root,root)
%{_libdir}/vdpau/libvdpau_r300.so
%{_libdir}/vdpau/libvdpau_r300.so.1
%{_libdir}/vdpau/libvdpau_r300.so.1.0
%{_libdir}/vdpau/libvdpau_r300.so.1.0.0

%files -n libvdpau_r600
%defattr(-,root,root)
%{_libdir}/vdpau/libvdpau_r600.so
%{_libdir}/vdpau/libvdpau_r600.so.1
%{_libdir}/vdpau/libvdpau_r600.so.1.0
%{_libdir}/vdpau/libvdpau_r600.so.1.0.0
%endif

%ifarch %ix86 x86_64
%files -n libvdpau_radeonsi
%defattr(-,root,root)
%{_libdir}/vdpau/libvdpau_radeonsi.so
%{_libdir}/vdpau/libvdpau_radeonsi.so.1
%{_libdir}/vdpau/libvdpau_radeonsi.so.1.0
%{_libdir}/vdpau/libvdpau_radeonsi.so.1.0.0
%endif

%files -n Mesa-libglapi0
%defattr(-,root,root)
%{_libdir}/libglapi.so.0*

%files -n Mesa-libglapi-devel
%defattr(-,root,root)
%{_libdir}/libglapi.so

%files -n Mesa-dri-devel
%defattr(-,root,root)
%{_includedir}/GL/internal
%{_libdir}/pkgconfig/dri.pc

%files devel
%defattr(-,root,root)
%doc docs/*.html

%if 0%{?with_nine}
%files libd3d
%defattr(-,root,root)
%dir %{_libdir}/d3d/
%{_libdir}/d3d/*.so.*
#%{_sysconfdir}/OpenCL/vendors/mesa.icd

%files libd3d-devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/d3d.pc
%{_includedir}/d3dadapter/
%{_libdir}/d3d/*.so
%endif

%if 0%{with_opencl}
%files libOpenCL
%defattr(-,root,root)
%dir %{_sysconfdir}/OpenCL
%dir %{_sysconfdir}/OpenCL/vendors
%{_sysconfdir}/OpenCL/vendors/mesa.icd
%{_libdir}/libMesaOpenCL.so*
%endif

%files libva
%defattr(-,root,root)
%dir %{_libdir}/dri
%{_libdir}/dri/gallium_drv_video.so

%changelog
