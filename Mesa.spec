#
# spec file for package Mesa (Version 6.5.3)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           Mesa
BuildRequires:  gcc-c++ libdrm-devel pkgconfig xorg-x11-devel
URL:            http://www.mesa3d.org
License:        X11/MIT
Group:          System/Libraries
Provides:       xorg-x11-Mesa
Obsoletes:      xorg-x11-Mesa
Autoreqprov:    on
Version:        6.5.3
Release:        1
Summary:        Mesa is a 3-D graphics library with an API which is very similar to that of OpenGL.*
Source:         MesaLib-%{version}rc2.tar.gz
Source1:        MesaDemos-%{version}rc2.tar.gz
Source3:        README.updates
Source4:        manual-pages.tar.bz2
Source5:        via.csh
Source6:        via.sh
Patch0:         disable-sis_dri.diff
Patch1:         dri_driver_dir.diff
Patch2:         i915-crossbar.diff
Patch4:         libIndirectGL.diff
Patch5:         static.diff
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
Requires:       Mesa = %version xorg-x11-devel
Summary:        Libraries, includes and more to develop Mesa applications
Group:          System/Libraries
Provides:       xorg-x11-Mesa-devel
Obsoletes:      xorg-x11-Mesa-devel

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

%package devel-static
Requires:       Mesa-devel = %version
Summary:        Static GL library - Usually not required at all
Group:          System/Libraries
Provides:       xorg-x11-Mesa-devel-static
Obsoletes:      xorg-x11-Mesa-devel-static

%description devel-static
Static GL library. It is not recommended at all to link against the
static GL library. Only included for legacy reasons.



Authors:
--------
    Brian Paul

%prep
%setup -n %{name}-%{version}rc2 -b1 -b4
# make legal department happy (Bug #204110)
test -f src/mesa/drivers/directfb/idirectfbgl_mesa.c && exit 1
test -f progs/ggi/asc-view.c && exit 1
# no need to build GLUT and (GLUT-)Demos
rm -rf src/glut progs/{demos,redbook,samples,xdemos,glsl}
# we use freeglut
rm -f include/GL/{glut.h,uglglutshapes.h,glutf90.h}
# extra package for GLw (MesaGLw)
rm -rf src/glw/
%patch0
%patch1
%patch2
%patch5

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
%ifnarch s390 s390x ppc64
# build and install Indirect Rendering only libGL
patch -p0 -s < $RPM_SOURCE_DIR/libIndirectGL.diff
make realclean
make linux-indirect OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
mkdir -p $RPM_BUILD_ROOT/usr/%{_lib}
cp -a lib/libIndirectGL.so.* $RPM_BUILD_ROOT/usr/%{_lib}
patch -p0 -s -R < $RPM_SOURCE_DIR/libIndirectGL.diff
%endif
for dir in ../xc/doc/man/{GL/gl,GL/glx,GLU}; do
pushd $dir
  xmkmf -a
  make
  make install.man DESTDIR=$RPM_BUILD_ROOT MANPATH=%{_mandir} LIBMANSUFFIX=3gl
popd
done
make realclean
%ifarch %ix86 ppc x86_64
%ifarch %ix86
make linux-dri-x86 OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -DDEFAULT_DRIVER_DIR='\"'/usr/%{_lib}/dri/updates:/usr/%{_lib}/dri'\"'"
make install DESTDIR=$RPM_BUILD_ROOT/usr INSTALL_DIR=$RPM_BUILD_ROOT/usr DRI_DRIVER_INSTALL_DIR=$RPM_BUILD_ROOT/usr/%{_lib}/dri
make realclean
make linux-x86-static OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
%ifarch ppc
make linux-dri-ppc OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -DDEFAULT_DRIVER_DIR='\"'/usr/%{_lib}/dri/updates:/usr/%{_lib}/dri'\"'"
make install DESTDIR=$RPM_BUILD_ROOT/usr INSTALL_DIR=$RPM_BUILD_ROOT/usr DRI_DRIVER_INSTALL_DIR=$RPM_BUILD_ROOT/usr/%{_lib}/dri
make realclean
make linux-ppc-static OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
%ifarch x86_64
make linux-dri-x86-64 OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -DDEFAULT_DRIVER_DIR='\"'/usr/%{_lib}/dri/updates:/usr/%{_lib}/dri'\"'"
make install DESTDIR=$RPM_BUILD_ROOT/usr INSTALL_DIR=$RPM_BUILD_ROOT/usr DRI_DRIVER_INSTALL_DIR=$RPM_BUILD_ROOT/usr/%{_lib}/dri
make realclean
make linux-x86-64-static OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
%else
%ifnarch s390 s390x ppc64
make linux-dri OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -DDEFAULT_DRIVER_DIR='\"'/usr/%{_lib}/dri/updates:/usr/%{_lib}/dri'\"'"
%else
make linux OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
make install DESTDIR=$RPM_BUILD_ROOT/usr INSTALL_DIR=$RPM_BUILD_ROOT/usr DRI_DRIVER_INSTALL_DIR=$RPM_BUILD_ROOT/usr/%{_lib}/dri
make realclean
make linux-static OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
%ifarch ppc64 s390x
mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT/usr/%{_lib}
install -m 644 lib/libGL.a  $RPM_BUILD_ROOT/usr/%{_lib}
install -m 644 lib/libGLU.a $RPM_BUILD_ROOT/usr/%{_lib}
%else
install -m 644 %{_lib}/libGL.a  $RPM_BUILD_ROOT/usr/%{_lib}
install -m 644 %{_lib}/libGLU.a $RPM_BUILD_ROOT/usr/%{_lib}
%endif
ln -snf libGL.a $RPM_BUILD_ROOT/usr/%{_lib}/libMesaGL.a
rm -f $RPM_BUILD_ROOT/usr/%{_lib}/libOSMesa.a
# build and install OffScreen Mesa library
make realclean
make linux-osmesa OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
cp -a lib/libOSMesa.so* $RPM_BUILD_ROOT/usr/%{_lib}
# create dummy nvidia libGLcore.so.1 for applications, which are still
# linked against libGL.so.1 of older nvidia driver releases
> libGLcore.c
gcc -Wall -ansi -pedantic -c libGLcore.c -fPIC
ld -shared -soname libGLcore.so.1 -o $RPM_BUILD_ROOT/usr/%{_lib}/libGLcore.so.1.0 libGLcore.o
/sbin/ldconfig -n $RPM_BUILD_ROOT/usr/%_lib
%ifnarch s390 s390x ppc64
# DRI driver update mechanism
mkdir -p $RPM_BUILD_ROOT/usr/%{_lib}/dri/updates
install -m 644 $RPM_SOURCE_DIR/README.updates \
  $RPM_BUILD_ROOT/usr/%{_lib}/dri/updates
%endif
%if %suse_version > 1010
%ifnarch s390 s390x ppc64
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 644 $RPM_SOURCE_DIR/via.{sh,csh} $RPM_BUILD_ROOT/etc/profile.d
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs/*
%if %suse_version > 1010
%ifnarch s390 s390x ppc64
/etc/profile.d/via.*
%endif
%endif
/usr/include/GL/
/usr/%{_lib}/libGL.so
/usr/%{_lib}/lib*.so.*
%ifnarch s390 s390x ppc64
/usr/%{_lib}/dri/
%endif

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libGLU.so
/usr/%{_lib}/libOSMesa.so
%{_mandir}/man3/*

%files devel-static
%defattr(-,root,root)
/usr/%{_lib}/libGL.a
/usr/%{_lib}/libGLU.a
/usr/%{_lib}/libMesaGL.a

%changelog
* Sun Apr 22 2007 - sndirsch@suse.de
- updated to Mesa 6.5.3rc2
  * a number of bug fixes since the first RC
* Sat Apr 21 2007 - sndirsch@suse.de
- updated to Mesa 6.5.3rc1
- obsoletes the following patches:
  * bug-211314_mesa-destroy_buffers.diff
  * bug-211314_mesa-framebuffer-counting.diff
  * bug-211314-patch-1.diff
  * bug-211314-patch-2.diff
  * bug-211314-patch-3.diff
  * bug-211314-patch-4.diff
  * bug-211314-patch-5.diff
  * bug-211314-patch-6.diff
  * bug-211314-patch-7.diff
  * bug-211314-patch-8.diff
  * bug-211314-patch-9.diff
  * bug-211314-patch-10.diff
  * bug-211314-patch-11.diff
  * bug-211314_mesa-refcount-memleak-fixes.diff
  * Mesa-6.5.2-fix_radeon_cliprect.diff
* Tue Apr 10 2007 - sndirsch@suse.de
- Mesa-6.5.2-fix_radeon_cliprect.diff:
  * fixes X.Org Bug #9876
* Wed Apr 04 2007 - sndirsch@suse.de
- bug-211314_mesa-refcount-memleak-fixes.diff:
  * Fix for memleaks and refount bugs (Bug #211314)
* Mon Mar 19 2007 - sndirsch@suse.de
- no longer apply bug-211314_mesa-context.diff (Bug #211314,
  commment #114)
- added different Mesa patches (Bug #211314, comments #114/#115)
* Wed Mar 14 2007 - sndirsch@suse.de
- removed libIndirectGL.so (Bug #254317)
- README.updates: new location of DRI drivers (Bug #254318)
* Thu Jan 25 2007 - sndirsch@suse.de
- fixed build on ppc64/s390/s390x
* Thu Jan 18 2007 - sndirsch@suse.de
- added libIndirectGL for indirect rendering only (Bug #234154)
* Wed Jan 17 2007 - sndirsch@suse.de
- bug-211314_mesa-context.diff:
  * fixes Xserver crash in software rendering fallback (Bug #211314)
* Tue Jan 09 2007 - sndirsch@suse.de
- disabled build of sis DRI driver on i64 to fix build
* Sat Dec 02 2006 - sndirsch@suse.de
- updated to Mesa 6.5.2
  * New features
    - New DRI memory manager system. Currently used by the i915tex
  driver. Other DRI drivers will be updated to use the new memory
  manager in coming months. To use the new driver you'll need the
  most recent DRM library and drivers (version 2.2 or later) and a
  recent xf86-video-intel driver module from X.org. New features
  resulting from this work include:
  * EXT_framebuffer_objects, render to texture
  * ARB_pixel_buffer_objects
  * Accelerated CopyTexSubimage, DrawPixels, ReadPixels, CopyPixels
  * Accelerated texture uploads from pixel buffer objects
  * Potentially texturing directly from the pixel buffer object
  (zero copy texturing).
    - New Intel i965 DRI driver
    - New minstall script to replace normal install program
    - Faster fragment program execution in software
    - Added (or fixed) support for GLX_SGI_make_current_read to the
  following drivers:
  * radeon
  * savage
  * mga
  * tdfx
    - Added support for ARB_occlusion_query to the tdfx driver
  (Ian Romanick).
  * Bug fixes
    - fixed invalid memory read while rendering textured points (bug 8320)
    - fixed problems with freebsd-dri configuration (bug 8344)
    - Mesa's fake glxGetCurrentContext() wasn't thread-aware
    - OPTION NV_position_invariant didn't work in NV vertex programs
    - glDrawPixels into a user-created framebuffer object could crash Xlib driver
    - Line clipping was broken in some circumstances
    - fragment.fogcoord register didn't always contain the correct value
    - RGBA logicops didn't work reliably in some DRI drivers
    - Fixed broken RGBA LogicOps in Intel DRI drivers
    - Fixed some fragment program bugs in Intel i915 DRI driver
    - Fixed glGetVertexAttribfvARB bug 8883
    - Implemented glGetUniform[fi]vARB() functions
    - Fixed glDrawPixels(GL_COLOR_INDEX, GL_BITMAP) segfault (bug 9044)
    - Fixed some gluBuild2DMipmaps() bugs (Greg McGarragh)
    - Fixed broken "mgl" name mangling
    - Indirect rending was broken for glMap* functions (bug 8899)
  * Internal code changes
    - The device driver functions ResizeBuffers and GetBufferSize have
  been decprecated.
    - OpenGL 2.0 and 2.1 support is nearly done. We need to do quite a
  bit more testing of the shading language functions.
* Thu Nov 23 2006 - sndirsch@suse.de
- enabled build of i965 DRI driver on x86_64
* Fri Nov 10 2006 - sndirsch@suse.de
- fixed typos (Bug #219732)
* Wed Oct 18 2006 - sndirsch@suse.de
- added static libGLU to Mesa-devel-static package (Bug #212532)
* Tue Oct 10 2006 - sndirsch@suse.de
- fixed build on s390x
* Mon Oct 09 2006 - sndirsch@suse.de
- i915-crossbar.diff:
  * fixes ARB_texture_env_crossbar extension (X.Org Bug #8292)
* Mon Sep 18 2006 - sndirsch@suse.de
- updated to Mesa 6.5.1:
  New:
  * Intel i965 DRI driver
  * GL_APPLE_vertex_array_object extension (Ian Romanick)
  * GL_EXT_texture_sRGB extension
  * GL_EXT_gpu_program_parameters (Ian Romanick)
  * "engine" demo
  * updated fbdev driver and GLUT for fbdev (Sean D'Epagnier)
  * many updates to the DRI drivers
  Changes:
  * The glVertexAttribARB functions no longer alias the
  conventional vertex attributes.
  * glxinfo program prints more info with -l option
  * GL_FRAGMENT_PROGRAM_NV and GL_FRAGMENT_PROGRAM_ARB are now
  compatible, in terms of glBindProgramARB()
  * The GL_ARB_vertex_program attribute vertex.weight is now
  accepted by the parser, even though the GL_ARB_vertex_blend and
  GL_EXT_vertex_weighting extensions aren't supported. Allows Warcraft
  to run.
  Bug fixes:
  * fixed broken texture border handling for depth textures (bug 6498)
  * removed the test for duplicated framebuffer attachments, per
  version 117 of the GL_EXT_framebuffer_object specification
  * fixed a few render-to-texture bugs, including render to depth
  texture
  * clipping of lines against user-defined clip planes was broken
  (6512)
  * assembly language dispatch for SPARC was broken (bug 6484)
  * assorted compilation fixes on various Unix platforms (Dan Schikore)
  * glPopAttrib could restore an invalid value for GL_DRAW_BUFFER
  * assorted minor fixes for 16 and 32 bit/channel modes
  * fixed assorted bugs in texture compression paths
  * fixed indirect rendering vertex array crashes (bug 6863)
  * glDrawPixels GL_INDEX_OFFSET didn't always work
  * fixed convolution memory leak (bug 7077)
  * rectangular depth textures didn't work
  * invalid mode to glBegin didn't generate an error (bug 7142)
  * 'normalized' parameter to glVertexAttribPointerARB didn't work
  * disable bogus GLX_SGI_video_sync extension in xlib driver
  * fixed R128 driver locking bug (Martijn van Oosterhout)
  * using evaluators with vertex programs caused crashes (bug 7564)
  * fragment.position wasn't set correctly for point/line primitives
  * fixed parser bug for scalar sources for GL_NV_fragment_program
  * max fragment program length was incorrectly 128, now 1024
  * writes to result.depth in fragment programs weren't clamped to
  [0,1]
  * fixed potential dangling pointer bug in glBindProgram()
  * fixed some memory leaks (and potential crashes) in Xlib driver
* Sat Sep 09 2006 - sndirsch@suse.de
- removed two source files with imcompatible license from Mesa
  tarball (Bug #204110)
- added a check to specfile to make sure that these will not be
  reintroduced with the next Mesa update again (Bug #204110)
* Mon Aug 21 2006 - sndirsch@suse.de
- moved via profile.d scripts from x11-tools to this package
* Thu Aug 17 2006 - sndirsch@suse.de
- dri_driver_dir.diff:
  * DEFAULT_DRIVER_DIR is set during make call in specfile
  (Bug #199958)
- disabled build of GLw (extra package MesaGLw)
* Mon Jul 31 2006 - sndirsch@suse.de
- updated to Mesa 6.5_20060712; required by xorg-server 1.1.99.3
- cleanup
* Wed Jul 19 2006 - ro@suse.de
- adapt to /usr/lib move
* Sun Jun 25 2006 - sndirsch@suse.de
- fixed build for X.Org 7.1
* Wed Jun 21 2006 - sndirsch@suse.de
- udpated to Mesa 6.5
  * obsoletes
    - Mesa-glx-x11-render-texture-2.diff
    - Mesa-radeon-large-textures-1.diff
    - Mesa_945GM.patch
    - mesa-6.4.2-dri-copy-sub-buffer-2.patch
    - mesa-6.4.2-scissor-fix-1.patch
- cleanup: removed no longer used sources/patches
  * missing-headers.diff
  * missing-headers.tar.bz2
  * glidelibs-i386.tar.gz
* Mon Jun 19 2006 - sndirsch@suse.de
- added missing manual pages (Bug #185707)
* Fri Jun 16 2006 - dreveman@suse.de
- Fix issue in copy-sub-buffer patch. Extension was not
  enabled on all radeon cards. (bnc 174839)
- Add radeon large texture patch (back port from latest stable
  release of Mesa). (bnc 174839)
* Tue May 23 2006 - sndirsch@suse.de
- no longer remove NVIDIA installer in %%pre
* Mon May 22 2006 - sndirsch@suse.de
- reverted Mesa/MesaGLU split
- fixed libGLcore.so.1 (e.g. soname); required to create a
  non-conflicting package for the NVIDIA driver (Bug #175683)
* Tue May 16 2006 - sndirsch@suse.de
- splitted off MesaGLU/MesaGLU-devel
- added ldconfig to %%postun
* Sat Apr 22 2006 - sndirsch@suse.de
- licensefix.patch:
  * fixed incompatible GPL license (Bug #133238, Mesa Bug #6490)
* Thu Apr 13 2006 - sndirsch@suse.de
- added /usr/X11R6/%%{_lib}/modules/dri/updates/README.updates to
  document DRI driver update mechanism
* Wed Apr 12 2006 - sndirsch@suse.de
- enhanced search path for DRI driver updates (FATE #300553)
* Mon Apr 03 2006 - sndirsch@suse.de
- mesa-6.4.2-dri-copy-sub-buffer-1.patch:
  * needed for open source drivers to work with Xgl (David Reveman)
* Wed Mar 15 2006 - mhopf@suse.de
- Fix for bug #157051, issue 1:
  On intel the graphics is only displayed correctly after a scissor region
  other than full screen is specified.
* Mon Feb 06 2006 - sndirsch@suse.de
- update to Mesa 6.4.2 (obsoletes tnl_init.diff)
  * New items:
    - added OSMesaColorClamp() function/feature
    - added wglGetExtensionStringARB() function
  * Bug fixes:
    - fixed some problems when building on Windows
    - GLw header files weren't installed by installmesa script (bug 5396)
    - GL/glfbdev.h file was missing from tarballs
    - fixed TNL initialization bug which could lead to crash (bug 5791)
* Mon Feb 06 2006 - sndirsch@suse.de
- tnl_init.diff (Mesa Bug #5791):
  * fixes TNL initialization bug which could lead to crash
  (CVS changelog: use calloc instead of malloc so try_codegen
  field is initialized to zero)
* Mon Jan 30 2006 - sndirsch@suse.de
- glxext-sgi-hyperpipe.patch:
  * GLX_SGIX_hyperpipe_group -> GLX_SGIX_hyperpipe (Bug #146646)
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 20 2006 - sndirsch@suse.de
- Mesa_945GM.patch:
  * 945GM support by Charles Johnson (FATE #151391)
* Wed Dec 28 2005 - sndirsch@suse.de
- moved header files and libGL.so from Mesa-devel to Mesa to make
  uninstallation of nvidia driver in %%pre of Mesa-devel obsolete
* Wed Nov 30 2005 - sndirsch@suse.de
- update to Mesa 6.4.1
* Fri Nov 18 2005 - sndirsch@suse.de
- updated to Mesa 6.4 branch (2005-11-18)
- added static libGL (new Mesa-devel-static package)
- removed glut headers from installation (we use freeglut!)
* Tue Nov 15 2005 - sndirsch@suse.de
- updated to Mesa 6.4 branch (2005-11-12)
* Wed Nov 09 2005 - sndirsch@suse.de
- fixed libOSMesa build
* Tue Nov 08 2005 - sndirsch@suse.de
- added build of libOSMesa, e.g. required by tulip package
* Tue Nov 08 2005 - sndirsch@suse.de
- added include files for SGI's OpenGL Xt/Motif widgets, e.g.
  required by z88 package
  * GLwMDrawA.h
  * GLwDrawAP.h
  * GLwMDrawAP.h
  * GLwDrawA.h
- enabled Motif support in libGLw, also required by z88 package
* Mon Nov 07 2005 - sndirsch@suse.de
- use glx headers from xorg-x11-devel package
* Fri Oct 28 2005 - sndirsch@suse.de
- Mesa-glx-x11-render-texture-2.diff/missing-headers.diff:
  * new MESA_render_texture extension for Xgl (dreveman/mhopf)
* Tue Oct 25 2005 - sndirsch@suse.de
- fixed DRI driver path for 64bit platforms
* Tue Oct 25 2005 - sndirsch@suse.de
- update to Mesa 6.4
* Mon Oct 24 2005 - sndirsch@suse.de
- build DRI compatible libGL
* Fri Oct 21 2005 - sndirsch@suse.de
- added dummy nvidia libGLcore.so.1 for applications, which are
  still linked against libGL.so.1 of older nvidia driver releases
- duplicate libGL (located in /usr/lib/GL) to make workarounds
  like LD_PRELOAD possible if nvidia driver is installed and its
  libGl does not work
* Wed Oct 19 2005 - sndirsch@suse.de
- no longer install libglide (disables 3Dfx DRI support)
* Sun Oct 02 2005 - sndirsch@suse.de
- created package
