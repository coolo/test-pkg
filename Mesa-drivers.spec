#
# spec file for package Mesa-drivers
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
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


# Following define and the Name attribute are the only difference between
# Mesa.spec and Mesa-drivers.spec. Mesa-drivers.spec is generated from
# Mesa.spec using the pre_checkin.sh script.
#
# Mesa.spec builds everything that is hardware independent and does not
# require llvm. Most importantly it builds all OpenGL (ES) libraries.
#
# Mesa-drivers.spec builds hardware specific drivers and parts that require
# llvm.
#
# The purpose of this split is to be able to build most Mesa-* packages fast
# without waiting for llvm. This helps speed up whole distribution build in
# OBS. (https://bugzilla.suse.com/show_bug.cgi?id=1071297)
# Note that if you actually need to render something, you need the packages
# from Mesa-driver.

##### WARNING: please do not edit this auto generated spec file. Use the Mesa.spec! #####
%define drivers 1

%define libglvnd 0

%if 0%{?suse_version} >= 1330
  %define libglvnd 1
%endif

%define glamor 1
%define _name_archive mesa
%define _version 18.0.0-rc4
%define with_opencl 0
%define with_vulkan 0
%define with_llvm 0

%ifarch %ix86 x86_64 %arm aarch64 ppc ppc64 ppc64le s390x
  %define gallium_loader 1
%else
  %define gallium_loader 0
%endif

%define xvmc_support 0
%define vdpau_nouveau 0
%define vdpau_radeon 0

%ifarch %ix86 x86_64 aarch64 %arm ppc64 ppc64le
  %define xvmc_support 1
  %define vdpau_nouveau 1
  %define vdpau_radeon 1
%endif

%ifarch %ix86 x86_64
  %define with_nine 1
%endif

%if 0%{gallium_loader} && 0%{?suse_version} >= 1330
# llvm >= 3.9 not provided for <= 1330
  %ifnarch ppc
    %define with_opencl 1
  %endif
  %ifarch %ix86 x86_64
    %define with_vulkan 1
  %endif
%endif

%ifarch aarch64 %arm ppc64 ppc64le s390x %ix86 x86_64
  %define with_llvm 1
%endif

%if %{drivers}
  %define glamor 0
%else
  # No llvm dependencies
  %define with_llvm 0

  # OpenCL requires clang (LLVM)
  %define with_opencl 0

  # nine requires at least one non-swrast gallium driver
  %define with_nine 0

  # Not built because radeon driver is not built.
  %define vdpau_radeon 0

  # Not built because nouveau driver is not built.
  %define vdpau_nouveau 0

  # Not built. (Why?)
  %define xvmc_support 0

  # Vulkan includes radv driver which requires llvm
  %define with_vulkan 0
%endif

Name:           Mesa-drivers
Version:        18.0.0
Release:        0
Summary:        System for rendering 3-D graphics
License:        MIT
Group:          System/Libraries
Url:            http://www.mesa3d.org
#Git-Clone:     git://anongit.freedesktop.org/mesa/mesa
# For now directory structure of Mesa's ftp changed
# Source:         ftp://ftp.freedesktop.org/pub/mesa/%%{version}/%%{_name_archive}-%%{_version}.tar.xz
Source:         ftp://ftp.freedesktop.org/pub/mesa/%{_name_archive}-%{_version}.tar.xz
# Source1:        ftp://ftp.freedesktop.org/pub/mesa/%%{version}/%%{_name_archive}-%%{_version}.tar.xz.sig
Source1:        ftp://ftp.freedesktop.org/pub/mesa/%{_name_archive}-%{_version}.tar.xz.sig
Source2:        baselibs.conf
Source3:        README.updates
Source4:        manual-pages.tar.bz2
Source6:        %{name}-rpmlintrc
Source7:        Mesa.keyring
# to be upstreamed
Patch11:        u_Fix-crash-in-swrast-when-setting-a-texture-for-a-pix.patch
Patch12:        u_add_llvm_codegen_dependencies.patch
# Patch from Fedora, fix 16bpp in llvmpipe
Patch13:        u_mesa-8.0.1-fix-16bpp.patch
# Patch from Fedora, use shmget when available, under llvmpipe
Patch15:        u_mesa-8.0-llvmpipe-shmget.patch
# never to be upstreamed
Patch18:        n_VDPAU-XVMC-libs-Replace-hardlinks-with-copies.patch
# never to be upstreamed
Patch21:        n_Define-GLAPIVAR-separate-from-GLAPI.patch
# currently needed for libglvnd support
Patch31:        archlinux_0001-Fix-linkage-against-shared-glapi.patch
Patch32:        archlinux_glvnd-fix-gl-dot-pc.patch
# Upstream
Patch43:        u_mesa-python3-only.patch
Patch45:        n_Disable-AMDGPU-GFX9-Vega-on-LLVM-lessthan-6.0.0.patch
Patch46:        u_glsl-linker-error.patch

BuildRequires:  autoconf >= 2.60
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  imake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  python3-base
BuildRequires:  python3-mako
BuildRequires:  python3-xml
BuildRequires:  pkgconfig(dri2proto)
BuildRequires:  pkgconfig(dri3proto)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(glproto)
BuildRequires:  pkgconfig(libdrm) >= 2.4.75
BuildRequires:  pkgconfig(libdrm_amdgpu) >= 2.4.79
BuildRequires:  pkgconfig(libdrm_nouveau) >= 2.4.66
BuildRequires:  pkgconfig(libdrm_radeon) >= 2.4.71
%if 0%{?libglvnd}
BuildRequires:  pkgconfig(libglvnd) >= 0.1.0
%endif
BuildRequires:  pkgconfig(libkms) >= 1.0.0
BuildRequires:  pkgconfig(libudev) > 151
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(presentproto)
BuildRequires:  pkgconfig(vdpau) >= 1.1
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
Provides:       s2tc = %{version}
Obsoletes:      s2tc < %{version}
Provides:       libtxc_dxtn = %{version}
Obsoletes:      libtxc_dxtn < %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%ifarch %arm
BuildRequires:  pkgconfig(libdrm_freedreno) >= 2.4.74
BuildRequires:  pkgconfig(libelf)
%endif
%ifarch x86_64 %ix86
BuildRequires:  libelf-devel
BuildRequires:  pkgconfig(libdrm_intel) >= 2.4.75
%else
%if 0%{with_opencl}
BuildRequires:  libelf-devel
%endif
%endif
# Requirements for wayland bumped up from 17.0
%if 0%{?suse_version} > 1320 || (0%{?sle_version} >= 120300 && 0%{?is_opensuse})
BuildRequires:  pkgconfig(wayland-client) >= 1.11
BuildRequires:  pkgconfig(wayland-protocols) >= 1.8
BuildRequires:  pkgconfig(wayland-server) >= 1.11
%endif
%if 0%{with_llvm}
BuildRequires:  llvm-devel >= 3.9.0
%endif
%ifarch aarch64 %arm ppc64 ppc64le s390x %ix86 x86_64
BuildRequires:  ncurses-devel
%endif

%if 0%{with_opencl}
BuildRequires:  clang-devel
BuildRequires:  libclc
%endif

%if 0%{?libglvnd}
Requires:       Mesa-libEGL1  = %{version}
Requires:       Mesa-libGL1  = %{version}
Requires:       libglvnd >= 0.1.0
%endif

# This dependency on Mesa-dri and Mesa-gallium is here to make sure users that
# do not install recommends on their system still get working Mesa. It is
# ignored in obs when Mesa is installed as build dependency.
Requires:       Mesa-dri = %{version}
Requires:       Mesa-gallium = %{version}

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
Provides:       s2tc-devel = %{version}
Obsoletes:      s2tc-devel < %{version}
Provides:       libtxc_dxtn-devel = %{version}
Obsoletes:      libtxc_dxtn-devel < %{version}
%if 0%{?suse_version} > 1320 || (0%{?sle_version} >= 120300 && 0%{?is_opensuse})
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

%package libEGL1
# Kudos to Debian for the descriptions
Summary:        EGL API implementation
Group:          System/Libraries
%if 0%{?libglvnd}
Requires:       libglvnd >= 0.1.0
%endif

%description libEGL1
This package contains the EGL native platform graphics interface
library. EGL provides a platform-agnostic mechanism for creating
rendering surfaces for use with other graphics libraries, such as
OpenGL|ES and OpenVG.

This package contains modules to interface with the existing system
GLX or DRI2 drivers to provide OpenGL via EGL. The Mesa main package
provides drivers to provide hardware-accelerated OpenGL|ES and OpenVG
support.

%package libEGL-devel
Summary:        Development files for the EGL API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libEGL1 = %{version}
%if 0%{?libglvnd}
Requires:       libglvnd-devel >= 0.1.0
%endif
# Other requires taken care of by pkgconfig already

%description libEGL-devel
This package contains the development environment required for
compiling programs against EGL native platform graphics interface
library. EGL provides a platform-agnostic mechanism for creating
rendering surfaces for use with other graphics libraries, such as
OpenGL|ES and OpenVG.

This package provides the development environment for compiling
programs against the EGL library.

%package libGL1
Summary:        The GL/GLX runtime of the Mesa 3D graphics library
Group:          System/Libraries
Requires:       Mesa = %{version}
%if 0%{?libglvnd}
Requires:       libglvnd >= 0.1.0
%endif

%description libGL1
Mesa is a software library for 3D computer graphics that provides a
generic OpenGL implementation for rendering three-dimensional
graphics.

GLX ("OpenGL Extension to the X Window System") provides the
interface connecting OpenGL and the X Window System: it enables
programs wishing to use OpenGL to do so within a window provided by
the X Window System.

%package libGL-devel
Summary:        GL/GLX development files of the OpenGL API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libGL1 = %{version}
%if 0%{?libglvnd}
Requires:       libglvnd-devel >= 0.1.0
%endif

%description libGL-devel
Mesa is a software library for 3D computer graphics that provides a
generic OpenGL implementation for rendering three-dimensional
graphics.

This package includes headers and static libraries for compiling
programs with Mesa.

%package libGLESv1_CM1
Summary:        OpenGL|ES 1.x Common Profile API implementation
Group:          System/Libraries
%if 0%{?libglvnd}
Requires:       libglvnd >= 0.1.0
%endif

%description libGLESv1_CM1
OpenGL|ES is an API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

OpenGL|ES 1.x provides an API for fixed-function hardware.

%package libGLESv1_CM-devel
Summary:        Development files for the OpenGL ES 1.x API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libGLESv1_CM1 = %{version}
%if 0%{?libglvnd}
Requires:       libglvnd-devel >= 0.1.0
%endif
Requires:       pkgconfig(egl)

%description libGLESv1_CM-devel
OpenGL|ES is an API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

OpenGL|ES 1.x provides an API for fixed-function hardware.

This package provides a development environment for building programs
using the OpenGL|ES 1.x APIs.

%package libGLESv2-2
Summary:        OpenGL|ES 2.x API implementation
Group:          System/Libraries
%if 0%{?libglvnd}
Requires:       libglvnd >= 0.1.0
%endif

%description libGLESv2-2
OpenGL|ES is an API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

OpenGL|ES 2.x provides an API for programmable hardware including
vertex and fragment shaders.

The libGLESv2.so.2 library provides symbols for all OpenGL ES 2 and
ES 3 entry points.

%package libGLESv2-devel
Summary:        Development files for the OpenGL ES 2.x API
Group:          Development/Libraries/C and C++
Requires:       Mesa-libGLESv2-2 = %{version}
%if 0%{?libglvnd}
Requires:       libglvnd-devel >= 0.1.0
%endif
Requires:       pkgconfig(egl)

%description libGLESv2-devel
OpenGL|ES is an API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

OpenGL|ES 2.x provides an API for programmable hardware including
vertex and fragment shaders.

This package provides a development environment for building
applications using the OpenGL|ES 2.x APIs.

%package libGLESv3-devel
Summary:        Development files for the OpenGL ES 3.x API
Group:          Development/Libraries/C and C++
%if 0%{?libglvnd} == 0
Requires:       Mesa-libGLESv2-2 = %{version}
%endif
Requires:       pkgconfig(egl)

%description libGLESv3-devel
OpenGL|ES is an API for full-function 2D and 3D
graphics on embedded systems - including consoles, phones, appliances
and vehicles. It contains a subset of OpenGL plus a number of
extensions for the special needs of embedded systems.

This package provides a development environment for building
applications using the OpenGL|ES 3.x APIs.

%package -n libOSMesa8
Summary:        Mesa Off-screen rendering extension
# Wrongly named package shipped .so.8
Group:          System/Libraries
Obsoletes:      libOSMesa9 < %{version}
Provides:       libOSMesa9 = %{version}

%description -n libOSMesa8
OSmesa is a Mesa extension that allows programs to render to an
off-screen buffer using the OpenGL API without having to create a
rendering context on an X Server. It uses a pure software renderer.

%package -n libOSMesa-devel
Summary:        Development files for the Mesa Offscreen Rendering extension
Group:          Development/Libraries/C and C++
Requires:       libOSMesa8 = %{version}

%description -n libOSMesa-devel
Development files for the OSmesa Mesa extension that allows programs to render to an
off-screen buffer using the OpenGL API without having to create a
rendering context on an X Server. It uses a pure software renderer.

%package libglapi0
Summary:        Free implementation of the GL API
Group:          System/Libraries

%description libglapi0
The Mesa GL API module is responsible for dispatching all the gl*
functions. It is intended to be mainly used by the Mesa-libGLES*
packages.

%package libglapi-devel
Summary:        Development files for the Mesa GL API implementation
Group:          Development/Libraries/C and C++
Requires:       Mesa-libglapi0 = %{version}

%description libglapi-devel
Development files for the Mesa GL API module which is responsible for
dispatching all the gl* functions. It is intended to be mainly used by
the Mesa-libGLES* packages.

%package -n Mesa-dri
Summary:        DRI plug-ins for 3D acceleration
Group:          System/Libraries
Requires:       Mesa = %{version}
Supplements:    Mesa

%description -n Mesa-dri
This package contains Mesa DRI drivers for 3D acceleration.

%package dri-devel
Summary:        Development files for the DRI API
Group:          Development/Libraries/C and C++
Requires:       Mesa = %{version}

%description dri-devel
This package contains the development environment required for
compiling programs and libraries using the DRI API.

%package -n Mesa-dri-nouveau
Summary:        Mesa DRI plug-in for 3D acceleration via Nouveau
Group:          System/Libraries
Requires:       Mesa = %{version}
Supplements:    xf86-video-nouveau

%description -n Mesa-dri-nouveau
This package contains nouveau_dri.so, which is necessary for
Nouveau's 3D acceleration to work. It is packaged separately
since it is still experimental.

%package -n Mesa-gallium
Summary:        Mesa Gallium GPU drivers
Group:          System/Libraries
Requires:       Mesa = %{version}
Supplements:    Mesa

%description -n Mesa-gallium
This package contains Mesa Gallium drivers for 3D acceleration.

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

%package -n Mesa-libd3d
Summary:        Mesa Direct3D9 state tracker
# Manually provide d3d library (bnc#918294)
Group:          System/Libraries
%ifarch x86_64 s390x ppc64le aarch64
Provides:       d3dadapter9.so.1()(64bit)
%else
Provides:       d3dadapter9.so.1
%endif

%description -n Mesa-libd3d
Mesa Direct3D9 state tracker

%package -n Mesa-libd3d-devel
Summary:        Mesa Direct3D9 state tracker development package
Group:          Development/Libraries/C and C++
Requires:       Mesa-libd3d = %{version}

%description -n Mesa-libd3d-devel
Mesa Direct3D9 state tracker development package

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

%package -n Mesa-libOpenCL
Summary:        Mesa OpenCL implementation
Group:          System/Libraries
Requires:       libclc

%description -n Mesa-libOpenCL
This package contains the Mesa OpenCL implementation or GalliumCompute.

%package -n Mesa-libva
Summary:        Mesa VA-API implementation
Group:          System/Libraries
Supplements:    Mesa

%description -n Mesa-libva
This package contains the Mesa VA-API implementation provided through gallium.

%package -n libvulkan_intel
Summary:        Mesa vulkan driver for Intel GPU
Group:          System/Libraries
Supplements:    xf86-video-intel

%description -n libvulkan_intel
This package contains the Vulkan parts for Mesa.

%package -n libvulkan_radeon
Summary:        Mesa vulkan driver for AMD GPU
Group:          System/Libraries
Supplements:    xf86-video-ati
Supplements:    xf86-video-amdgpu

%description -n libvulkan_radeon
This package contains the Vulkan parts for Mesa.

%package -n Mesa-libVulkan-devel
Summary:        Mesa's Vulkan development files
Group:          Development/Libraries/C and C++
Requires:       libvulkan_intel = %{version}
Requires:       libvulkan_radeon = %{version}
Conflicts:      vulkan-devel

%description -n Mesa-libVulkan-devel
This package contains the development files for Mesa's Vulkan implementation.

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

%prep
%setup -q -n %{_name_archive}-%{_version} -b4
# remove some docs
rm -rf docs/README.{VMS,WIN32,OS2}
### disabled, but not dropped yet; these still need investigation in
### order to figure out whether the issue is still reproducable and
### hence a fix is required
#%patch11 -p1
#%patch15 -p1
#%patch13 -p1
%patch12 -p1
%patch18 -p1
%patch21 -p1

%if 0%{?libglvnd}
%patch31 -p1
%patch32 -p1
%endif

%patch43 -p1
%patch45 -p1
%patch46 -p1

# Remove requires to libglvnd/libglvnd-devel from baselibs.conf when
# disabling libglvnd build; ugly ...
%if 0%{?libglvnd} == 0
grep -v libglvnd "%{_sourcedir}/baselibs.conf" >"%{_sourcedir}/temp" && \
  mv "%{_sourcedir}/temp" "%{_sourcedir}/baselibs.conf"
%endif

# Remove requires to vulkan libs from baselibs.conf on platforms
# where vulkan build is disabled; ugly ...
%if 0%{?with_vulkan} == 0
grep -v -i vulkan "%{_sourcedir}/baselibs.conf" >"%{_sourcedir}/temp" && \
  mv "%{_sourcedir}/temp" "%{_sourcedir}/baselibs.conf"
%endif

%build
%if 0%{?suse_version} > 1320 || (0%{?sle_version} >= 120300 && 0%{?is_opensuse})
egl_platforms=x11,drm,wayland
%else
egl_platforms=x11,drm
%endif
autoreconf -fvi

export PYTHON2=/usr/bin/python3
%configure \
%if %{drivers}
           --disable-gles1 \
           --disable-gles2 \
           --disable-egl \
           --disable-glx \
           --disable-osmesa \
%else
%if 0%{?libglvnd}
           --enable-libglvnd \
%endif
           --enable-gles1 \
           --enable-gles2 \
           --enable-egl \
           --enable-osmesa \
%endif
           --with-platforms=$egl_platforms \
           --enable-dri \
           --enable-texture-float \
           --enable-dri3 \
           --enable-shared-glapi \
%if 0%{?with_nine}
           --enable-nine \
%endif
%if %{glamor}
           --enable-gbm \
           --enable-glx-tls \
%endif
%if 0%{with_opencl}
           --enable-opencl \
           --enable-opencl-icd \
%endif
           --with-dri-searchpath=%{_libdir}/dri \
%if 0%{with_llvm}
           --enable-llvm \
           --enable-llvm-shared-libs \
%endif
           --enable-vdpau \
           --enable-va \
           --enable-xvmc \
%if 0%{with_vulkan}
           --with-vulkan-drivers=intel,radeon \
%endif
%if %{drivers}
  %ifarch %ix86 x86_64
           --enable-xa \
           --with-dri-drivers=i915,i965,nouveau,r200,radeon \
           --with-gallium-drivers=r300,r600,radeonsi,nouveau,swrast,svga,virgl \
  %endif
  %ifarch %arm aarch64
           --enable-xa \
           --with-dri-drivers=nouveau \
           --with-gallium-drivers=r300,r600,nouveau,swrast,freedreno,vc4 \
  %endif
  %ifarch ppc64 ppc64le
           --enable-xa \
           --with-dri-drivers=nouveau \
           --with-gallium-drivers=r300,r600,nouveau,swrast \
  %endif
  %ifarch ia64 ppc hppa s390 s390x
           --with-dri-drivers=swrast \
           --with-gallium-drivers=swrast \
  %endif
%else
           --with-dri-drivers= \
           --with-gallium-drivers= \
%endif
        CFLAGS="%{optflags} -DNDEBUG"
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -type f -name "*.la" -delete -print

%if %{drivers}
# Delete things that we do not package in the Mesa-drivers variant, but can
# not disable from buildling and installing.

# in Mesa
rm %{buildroot}/%{_sysconfdir}/drirc

# in Mesa-libGL-devel
rm -rf %{buildroot}/%{_includedir}/GL

# in Mesa-libglapi0
rm %{buildroot}/%{_libdir}/libglapi.so*

# in libwayland-egl1
rm %{buildroot}/%{_libdir}/libwayland-egl.so*
rm %{buildroot}/%{_libdir}/pkgconfig/wayland-egl.pc

# in Mesa-dri-devel
rm %{buildroot}/%{_libdir}/pkgconfig/dri.pc

# in libgbm-devel
rm %{buildroot}/%{_includedir}/gbm.h
rm %{buildroot}/%{_libdir}/libgbm.so*
rm %{buildroot}/%{_libdir}/pkgconfig/gbm.pc

%else
%if 0%{?libglvnd} == 0
# Make a symlink to libGL.so.1.2 for compatibility (bnc#809359, bnc#831306)
test -f %{buildroot}%{_libdir}/libGL.so.1.2 || \
  ln -s `readlink %{buildroot}%{_libdir}/libGL.so.1` %{buildroot}%{_libdir}/libGL.so.1.2
%else
rm -f %{buildroot}%{_libdir}/libGLES*
# glvnd needs a default provider for indirect rendering where it cannot
# determine the vendor
ln -s %{_libdir}/libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_indirect.so.0
%endif

for dir in ../xc/doc/man/{GL/gl,GL/glx}; do
 pushd $dir
   xmkmf -a
   make %{?_smp_mflags}
   make install.man DESTDIR=%{buildroot} MANPATH=%{_mandir} LIBMANSUFFIX=3gl
 popd
done
%endif

%fdupes -s %{buildroot}/%{_mandir}

%if !%{drivers}
# Use dummy README file that can be included in both Mesa and Mesa-32bit. This way Mesa-32bit will be build (otherwise it would be skipped as empty) and it can be used by the other *-32bit packages.
echo "The \"Mesa\" package does not have the ability to render, but is supplemented by \"Mesa-dri\" and \"Mesa-gallium\" which contain the drivers for rendering" > docs/README.package.%{_arch}
%endif

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post   libEGL1 -p /sbin/ldconfig

%postun libEGL1 -p /sbin/ldconfig

%post   libGL1 -p /sbin/ldconfig

%postun libGL1 -p /sbin/ldconfig

%post   libGLESv1_CM1 -p /sbin/ldconfig

%postun libGLESv1_CM1 -p /sbin/ldconfig

%post   libGLESv2-2 -p /sbin/ldconfig

%postun libGLESv2-2 -p /sbin/ldconfig

%post   -n libOSMesa8 -p /sbin/ldconfig

%postun -n libOSMesa8 -p /sbin/ldconfig

%post   -n libgbm1 -p /sbin/ldconfig

%postun -n libgbm1 -p /sbin/ldconfig

%post   -n libxatracker2 -p /sbin/ldconfig

%postun -n libxatracker2 -p /sbin/ldconfig

%post   -n libXvMC_nouveau -p /sbin/ldconfig

%postun -n libXvMC_nouveau -p /sbin/ldconfig

%post   -n libXvMC_r600 -p /sbin/ldconfig

%postun -n libXvMC_r600 -p /sbin/ldconfig

%post   -n libvdpau_r300 -p /sbin/ldconfig

%postun -n libvdpau_r300 -p /sbin/ldconfig

%post   -n libvdpau_r600 -p /sbin/ldconfig

%postun -n libvdpau_r600 -p /sbin/ldconfig

%post   -n libvdpau_radeonsi -p /sbin/ldconfig

%postun -n libvdpau_radeonsi -p /sbin/ldconfig

%post   libglapi0 -p /sbin/ldconfig

%postun libglapi0 -p /sbin/ldconfig

%post   -n libwayland-egl1 -p /sbin/ldconfig

%postun -n libwayland-egl1 -p /sbin/ldconfig

%post -n Mesa-libd3d -p /sbin/ldconfig

%postun -n Mesa-libd3d -p /sbin/ldconfig

%post   -n Mesa-libOpenCL -p /sbin/ldconfig

%postun -n Mesa-libOpenCL -p /sbin/ldconfig

%post -n Mesa-libva -p /sbin/ldconfig

%postun -n Mesa-libva -p /sbin/ldconfig

%post -n libvulkan_intel -p /sbin/ldconfig

%postun -n libvulkan_intel -p /sbin/ldconfig

%if !%{drivers}
%files
%defattr(-,root,root)
%doc docs/README* docs/license.html
%config %{_sysconfdir}/drirc

%files libEGL1
%defattr(-,root,root)
%if 0%{?libglvnd}
%{_libdir}/libEGL_mesa.so*
%dir %{_datadir}/glvnd
%dir %{_datadir}/glvnd/egl_vendor.d
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%else
%{_libdir}/libEGL.so.1*
%endif

%files libEGL-devel
%defattr(-,root,root)
%{_includedir}/EGL
%{_includedir}/KHR
%if !0%{?libglvnd}
%{_libdir}/libEGL.so
%endif
%{_libdir}/pkgconfig/egl.pc

%files libGL1
%defattr(-,root,root)
%if 0%{?libglvnd}
%{_libdir}/libGLX_mesa.so*
%{_libdir}/libGLX_indirect.so*
%else
%{_libdir}/libGL.so.1*
%endif

%files libGL-devel
%defattr(-,root,root)
%dir %{_includedir}/GL
%{_includedir}/GL/*.h
%exclude %{_includedir}/GL/osmesa.h
%if 0%{?libglvnd} == 0
%{_libdir}/libGL.so
%endif
%{_libdir}/pkgconfig/gl.pc
%{_mandir}/man3/gl[A-Z]*

%files libGLESv1_CM1
%defattr(-,root,root)
%if 0%{?libglvnd} == 0
%{_libdir}/libGLESv1_CM.so.1*
%endif

%files libGLESv1_CM-devel
%defattr(-,root,root)
%{_includedir}/GLES
%if 0%{?libglvnd} == 0
%{_libdir}/libGLESv1_CM.so
%endif
%{_libdir}/pkgconfig/glesv1_cm.pc

%files libGLESv2-2
%defattr(-,root,root)
%if 0%{?libglvnd} == 0
%{_libdir}/libGLESv2.so.2*
%endif

%files libGLESv2-devel
%defattr(-,root,root)
%{_includedir}/GLES2
%if 0%{?libglvnd} == 0
%{_libdir}/libGLESv2.so
%endif
%{_libdir}/pkgconfig/glesv2.pc

%files libGLESv3-devel
%defattr(-,root,root)
%{_includedir}/GLES3
#%_libdir/libGLESv3.so
#%_libdir/pkgconfig/glesv3.pc

%files -n libOSMesa8
%defattr(-,root,root)
%{_libdir}/libOSMesa.so.8.0.0
%{_libdir}/libOSMesa.so.8

%files -n libOSMesa-devel
%defattr(-,root,root)
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%if 0%{?suse_version} > 1320 || (0%{?sle_version} >= 120300 && 0%{?is_opensuse})
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
%endif

%if %{drivers}
%ifarch aarch64 %ix86 x86_64 %arm ppc64 ppc64le
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
%endif

%if !%{drivers}
%files libglapi0
%defattr(-,root,root)
%{_libdir}/libglapi.so.0*

%files libglapi-devel
%defattr(-,root,root)
%{_libdir}/libglapi.so
%endif

%if %{drivers}
%files -n Mesa-dri
%dir %{_libdir}/dri
%{_libdir}/dri/*_dri.so
%if 0%{?is_opensuse}
%ifarch %ix86 x86_64 aarch64 %arm ppc64 ppc64le
%exclude %{_libdir}/dri/nouveau_dri.so
%exclude %{_libdir}/dri/nouveau_vieux_dri.so
%endif
%endif

%if 0%{with_opencl}
# only built with opencl
%files -n Mesa-gallium
%dir %{_libdir}/gallium-pipe/
%{_libdir}/gallium-pipe/pipe_*.so
%endif

%if 0%{?is_opensuse}
%ifarch %ix86 x86_64 aarch64 %arm ppc64 ppc64le
%files -n Mesa-dri-nouveau
%{_libdir}/dri/nouveau_dri.so
%{_libdir}/dri/nouveau_vieux_dri.so
%endif
%endif

# drivers
%endif

%if !%{drivers}
%files dri-devel
%defattr(-,root,root)
%{_includedir}/GL/internal
%{_libdir}/pkgconfig/dri.pc

%files devel
%defattr(-,root,root)
%doc docs/*.html

# !drivers
%endif

%if 0%{?with_nine}
%files -n Mesa-libd3d
%defattr(-,root,root)
%dir %{_libdir}/d3d/
%{_libdir}/d3d/*.so.*
#%%{_sysconfdir}/OpenCL/vendors/mesa.icd

%files -n Mesa-libd3d-devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/d3d.pc
%{_includedir}/d3dadapter/
%{_libdir}/d3d/*.so
%endif

%if 0%{with_opencl}
%files -n Mesa-libOpenCL
%defattr(-,root,root)
%dir %{_sysconfdir}/OpenCL
%dir %{_sysconfdir}/OpenCL/vendors
%{_sysconfdir}/OpenCL/vendors/mesa.icd
%{_libdir}/libMesaOpenCL.so*
%endif

%if %{drivers}
%ifarch %ix86 x86_64 aarch64 %arm ppc64 ppc64le
%files -n Mesa-libva
%defattr(-,root,root)
%{_libdir}/dri/*_drv_video.so
%endif
%endif

%if 0%{with_vulkan}
%files -n libvulkan_intel
%defattr(-,root,root)
%dir %{_datadir}/vulkan
%dir %{_datadir}/vulkan/icd.d
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%{_libdir}/libvulkan_intel.so

%files -n libvulkan_radeon
%defattr(-,root,root)
%{_libdir}/libvulkan_radeon.so
%dir %{_datadir}/vulkan
%dir %{_datadir}/vulkan/icd.d
%{_datadir}/vulkan/icd.d/radeon_icd.*.json

%files -n Mesa-libVulkan-devel
%defattr(-,root,root)
%dir %_includedir/vulkan
%_includedir/vulkan
%endif

%changelog
