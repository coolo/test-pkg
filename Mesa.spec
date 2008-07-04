#
# spec file for package Mesa (Version 7.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           Mesa
BuildRequires:  gcc-c++ libdrm-devel pkgconfig xorg-x11-devel
Url:            http://www.mesa3d.org
License:        X11/MIT
Group:          System/Libraries
Provides:       xorg-x11-Mesa
Obsoletes:      xorg-x11-Mesa
AutoReqProv:    on
Version:        7.1
Release:        1
Summary:        Mesa is a 3-D graphics library with an API which is very similar to that of OpenGL
#Source:        MesaLib-%{version}-rc1.tar.bz2
Source:         MesaLib-6befdca.tar.bz2
Source1:        MesaDemos-%{version}-rc1.tar.bz2
Source3:        README.updates
Source4:        manual-pages.tar.bz2
Patch1:         dri_driver_dir.diff
Patch2:         MesaLib-6befdca.diff
Patch6:         link-shared.diff
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
License:        X11/MIT
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
License:        X11/MIT
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
#%setup -n %{name}-%{version}-rc1 -b1 -b4
%setup -n mesa -b4
#rm docs/README.MINGW32.orig
# make legal department happy (Bug #204110)
test -f src/mesa/drivers/directfb/idirectfbgl_mesa.c && exit 1
test -f progs/ggi/asc-view.c && exit 1
# no need to build (GLUT-)Demos
rm -rf src/glut progs/{demos,redbook,samples,xdemos,glsl}
# we use freeglut
rm -f include/GL/{glut.h,uglglutshapes.h,glutf90.h}
%patch1
sed -i 's/REPLACE/%_lib/g' src/glx/x11/Makefile
%patch2
%ifarch %ix86 x86_64 ppc
### FIXME
#%patch6
%endif

%build

%install
#autoreconf -fi
### libGL (disable savage/mga, bnc #402132/#403071)
%configure --disable-glw \
%ifarch ia64
          --with-driver=dri \
%endif
%ifnarch s390 s390x ppc64
           --with-dri-drivers=i915,i965,mach64,r128,r200,r300,radeon,tdfx,unichrome,swrast \
%endif
           --disable-glut
gmake
make install DESTDIR=$RPM_BUILD_ROOT
%ifnarch s390 s390x ppc64
# build and install Indirect Rendering only libGL
make realclean
%configure --with-driver=xlib \
           --disable-glu \
           --disable-glw \
           --disable-glut
sed -i 's/GL_LIB = .*/GL_LIB = IndirectGL/g' configs/autoconf
gmake 
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/usr/%{_lib}/libIndirectGL.so
%endif
### static libGL
make realclean
%configure --with-driver=xlib \
           --disable-shared \
           --enable-static \
           --disable-glw \
           --disable-glut
gmake
make install DESTDIR=$RPM_BUILD_ROOT
%ifnarch s390
for dir in ../xc/doc/man/{GL/gl,GL/glx,GLU}; do
pushd $dir
  xmkmf -a
  make
  make install.man DESTDIR=$RPM_BUILD_ROOT MANPATH=%{_mandir} LIBMANSUFFIX=3gl
popd
done
%endif
%ifnarch s390 s390x ppc64
# DRI driver update mechanism
mkdir -p $RPM_BUILD_ROOT/usr/%{_lib}/dri/updates
install -m 644 $RPM_SOURCE_DIR/README.updates \
  $RPM_BUILD_ROOT/usr/%{_lib}/dri/updates
%endif
# required for building Xserver glx extension later
%ifarch s390 s390x
mkdir -p $RPM_BUILD_ROOT//usr/include/GL/internal/
install -m 644 include/GL/internal/{dri_interface.h,dri_sarea.h} \
               $RPM_BUILD_ROOT//usr/include/GL/internal/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs/README* docs/COPYING
/usr/include/GL/gl.h
/usr/include/GL/glext.h
/usr/include/GL/glx.h
/usr/include/GL/glxext.h
/usr/%{_lib}/libGL.so
/usr/%{_lib}/lib*.so.*
%ifnarch s390 s390x
/usr/%{_lib}/dri/
%endif

%files devel
%defattr(-,root,root)
%doc docs/*.html docs/*.spec
/usr/include/GL/amesa.h
/usr/include/GL/dmesa.h
/usr/include/GL/fxmesa.h
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
/usr/include/GL/uglmesa.h
/usr/include/GL/vms_x_fix.h
/usr/include/GL/wmesa.h
/usr/include/GL/xmesa.h
/usr/include/GL/xmesa_x.h
/usr/include/GL/xmesa_xf86.h
/usr/include/GL/internal/dri_interface.h
/usr/include/GL/internal/dri_sarea.h
/usr/include/GL/directfbgl.h
/usr/include/GL/miniglx.h
/usr/%{_lib}/libGLU.so
%ifnarch ppc64
/usr/%{_lib}/libOSMesa.so
%endif
/usr/%{_lib}/pkgconfig/dri.pc
/usr/%{_lib}/pkgconfig/gl.pc
/usr/%{_lib}/pkgconfig/glu.pc
%ifnarch s390
%{_mandir}/man3/*
%endif

%files devel-static
%defattr(-,root,root)
/usr/%{_lib}/libGL.a
/usr/%{_lib}/libGLU.a
/usr/%{_lib}/libOSMesa.a

%changelog
* Sat Jul 05 2008 sndirsch@suse.de
- udpated to Mesa 7.1-pre
* Tue Apr 15 2008 sndirsch@suse.de
- unichrome-context.diff
  * Do not clear the current context before attempting to use it.
  (bnc #285496)
- no longer need to use LIBGL_ALWAYS_INDIRECT=1 on via hardware
  (bnc #285496)
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Sat Apr 05 2008 sndirsch@suse.de
- update to Mesa bugfix release 7.0.3 (final)
* Wed Apr 02 2008 sndirsch@suse.de
- update to Mesa bugfix release 7.0.3 RC3
  * obsoletes commit-185320a.diff
* Thu Mar 13 2008 sndirsch@suse.de
- commit-185320a.diff
  Only call ProgramStringNotify if program parsing succeeded.
  Wine intentionally tries some out-of-spec programs to test
  strictness, and calling ProgramStringNotify on the results
  of a failed program parse resulted in crashes in the 965
  driver. (bfo #13492)
* Fri Feb 22 2008 sndirsch@suse.de
- update to Mesa bugfix release 7.0.3 RC2
  * Fixed GLX indirect vertex array rendering bug (14197)
  * Fixed crash when deleting framebuffer objects (bugs 13507,
  14293)
  * User-defined clip planes enabled for R300 (bug 9871)
  * Fixed glBindTexture() crash upon bad target (bug 14514)
  * Fixed potential crash in glDrawPixels(GL_DEPTH_COMPONENT) (bug
  13915)
  * Bad strings given to glProgramStringARB() didn't generate
  GL_INVALID_OPERATION
  * Fixed minor point rasterization regression (bug 11016)
* Wed Jan 23 2008 sndirsch@suse.de
- update to Mesa bugfix release 7.0.3 RC1
  * Added missing glw.pc.in file to release tarball
  * Fix GLUT/Fortran issues
  * GLSL gl_FrontLightModelProduct.sceneColor variable wasn't
  defined
  * Fix crash upon GLSL variable array indexes (not yet supported)
  * Two-sided stencil test didn't work in software rendering
  * Fix two-sided lighting bugs/crashes (bug 13368)
  * GLSL gl_FrontFacing didn't work properly
  * glGetActiveUniform returned incorrect sizes (bug 13751)
  * Fix several bugs relating to uniforms and attributes in GLSL
  API (Bruce Merry, bug 13753)
  * glTexImage3D(GL_PROXY_TEXTURE_3D) mis-set teximage depth field
* Sat Nov 10 2007 sndirsch@suse.de
- updated to Mesa 7.0.2
  * New features:
    - Updated Windows VC7 project files
    - Added DESTDIR variable for 'make install'
    - Added pkg-config files for gl, glu, glut and glw libraries
    - Added bluegene-xlc-osmesa and catamount-osmesa-pgi configs
    - Support for Intel G33/Q33/Q35 graphics chipsets
  * Bug fixes:
    - Fixed a vertex buffer wrapping issue (bug 9962)
    - Added mutex protection around texture object reference
  counters
    - Added checking/support for additional chips in the i915/i945
  family (see 11978)
    - Fixed a blending/banding issue (bug 11931)
    - Fixed a GLU matrix inversion bug (#6748)
    - Fixed problem with large glDrawArrays calls and indirect
  rendering (bug 12141)
    - Fixed an assortment of i965 driver bugs
    - Fixed x86-64 vertex transformation bug (12216)
    - Fixed X server crash caused by multiple indirect rendering
  clients
    - Parsing of state.texgen in ARB vertex/fragment programs
  didn't work (bug 12313)
    - Fixed a glCopyPixels/glPixelZoom bug (12417)
    - Fixed a bug when using glMaterial in display lists (10604)
    - Fixed a few GLUT/Fortran issues (Bill Mitchell)
    - Fixed Blender crash bug (12164)
    - Fixed some issues preventing cross-compiling
    - Fixed up broken GL_ATI_separate_stencil extension
    - glDrawArrays(count=0) led to a crash
    - Fix SSE code gen memory leak, possible crash
    - Fixed MMX 565 rgb conversion problem (bug 12614)
    - Added -fno-strict-aliasing and -fPIC flags for gcc
    - Fixed Blender crash in Unichrome driver (bug 13142)
* Wed Nov 07 2007 sndirsch@suse.de
- updated to Mesa 7.0.2 RC2
  * added -fPIC and -fno-strict-aliasing flags for gcc
  * applied a few patches (mmx code, edgeflag ptr check)
  * r200 texture from pixmap fixes
- obsoletes pic.diff
* Mon Nov 05 2007 sndirsch@suse.de
- pic.diff
  * fixes shared lib on i386 (X.Org Bug #1809)
* Wed Oct 31 2007 sndirsch@suse.de
- updated to Mesa 7.0.2 RC1
- obsoletes disable-libGL-warning.diff, i915-g33.diff and
  i915tex-g33.diff
- adjusted link-shared.diff and static.diff
* Mon Aug 13 2007 sndirsch@suse.de
- disable-libGL-warning.diff:
  * Just filters warnings about unsupported non-conformant visuals
  instead of relying on the visual id. (X.Org Bug #6689)
* Sun Aug 12 2007 sndirsch@suse.de
- disable-libGL-warning.diff:
  * ignore unsupported visual 0x4b (Bug #247471, X.Org Bug #6689)
* Sat Aug 04 2007 sndirsch@suse.de
- updated to bugfix relelase 7.0.1
* Wed Jul 04 2007 sndirsch@suse.de
- i915-g33.diff/i915tex-g33.diff
  * support for G33/Q33/Q35
* Sat Jun 23 2007 sndirsch@suse.de
- updated to final release 7.0
* Thu Jun 21 2007 sndirsch@suse.de
- updated Mesa to release 7.0 RC1
  * Mesa 7.0 is a stable, follow-on release to Mesa 6.5.3. The only
  difference is bug fixes. The major version number bump is due
  to OpenGL 2.1 API support.
* Mon May 28 2007 sndirsch@suse.de
- move GL headers, which conflict with GL headers of NVIDIA driver,
  from Mesa-devel back to Mesa; this still make rpmlint happy
* Sat May 26 2007 dmueller@suse.de
- add missing ldconfig call to %%post
- move include files to -devel package
* Fri May 25 2007 dmueller@suse.de
- fix undefined symbols for i915 (#277744)
* Tue May 22 2007 dmueller@suse.de
- fix various undefined symbols in dri drivers (#272875)
- build parallel
* Mon May 14 2007 sndirsch@suse.de
- link-shared.diff:
  * use shared lib for DRI drivers to save a lot of space (Bug
  [#272875])
* Tue May 01 2007 sndirsch@suse.de
- updated to Mesa 6.5.3
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
* Fri Apr 27 2007 sndirsch@suse.de
- back to Mesa 6.5.2 (Bug #269155/269042)
* Wed Apr 25 2007 sndirsch@suse.de
- 4th RC ready
  * This fixes some breakage in RC3.
* Tue Apr 24 2007 sndirsch@suse.de
- 3rd release candidate
  * updated Windows/VC8 project files.
* Sun Apr 22 2007 sndirsch@suse.de
- updated to Mesa 6.5.3rc2
  * a number of bug fixes since the first RC
* Sat Apr 21 2007 sndirsch@suse.de
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
* Tue Apr 10 2007 sndirsch@suse.de
- Mesa-6.5.2-fix_radeon_cliprect.diff:
  * fixes X.Org Bug #9876
* Thu Apr 05 2007 sndirsch@suse.de
- bug-211314_mesa-refcount-memleak-fixes.diff:
  * Fix for memleaks and refount bugs (Bug #211314)
* Mon Mar 19 2007 sndirsch@suse.de
- no longer apply bug-211314_mesa-context.diff (Bug #211314,
  commment #114)
- added different Mesa patches (Bug #211314, comments #114/#115)
* Wed Mar 14 2007 sndirsch@suse.de
- removed libIndirectGL.so (Bug #254317)
- README.updates: new location of DRI drivers (Bug #254318)
* Thu Jan 25 2007 sndirsch@suse.de
- fixed build on ppc64/s390/s390x
* Thu Jan 18 2007 sndirsch@suse.de
- added libIndirectGL for indirect rendering only (Bug #234154)
* Wed Jan 17 2007 sndirsch@suse.de
- bug-211314_mesa-context.diff:
  * fixes Xserver crash in software rendering fallback (Bug #211314)
* Wed Jan 10 2007 sndirsch@suse.de
- disabled build of sis DRI driver on i64 to fix build
* Sun Dec 03 2006 sndirsch@suse.de
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
* Fri Nov 24 2006 sndirsch@suse.de
- enabled build of i965 DRI driver on x86_64
* Fri Nov 10 2006 sndirsch@suse.de
- fixed typos (Bug #219732)
* Wed Oct 18 2006 sndirsch@suse.de
- added static libGLU to Mesa-devel-static package (Bug #212532)
* Tue Oct 10 2006 sndirsch@suse.de
- fixed build on s390x
* Mon Oct 09 2006 sndirsch@suse.de
- i915-crossbar.diff:
  * fixes ARB_texture_env_crossbar extension (X.Org Bug #8292)
* Mon Sep 18 2006 sndirsch@suse.de
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
* Sat Sep 09 2006 sndirsch@suse.de
- removed two source files with imcompatible license from Mesa
  tarball (Bug #204110)
- added a check to specfile to make sure that these will not be
  reintroduced with the next Mesa update again (Bug #204110)
* Mon Aug 21 2006 sndirsch@suse.de
- moved via profile.d scripts from x11-tools to this package
* Thu Aug 17 2006 sndirsch@suse.de
- dri_driver_dir.diff:
  * DEFAULT_DRIVER_DIR is set during make call in specfile
  (Bug #199958)
- disabled build of GLw (extra package MesaGLw)
* Mon Jul 31 2006 sndirsch@suse.de
- updated to Mesa 6.5_20060712; required by xorg-server 1.1.99.3
- cleanup
* Wed Jul 19 2006 ro@suse.de
- adapt to /usr/lib move
* Sun Jun 25 2006 sndirsch@suse.de
- fixed build for X.Org 7.1
* Wed Jun 21 2006 sndirsch@suse.de
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
* Mon Jun 19 2006 sndirsch@suse.de
- added missing manual pages (Bug #185707)
* Fri Jun 16 2006 dreveman@suse.de
- Fix issue in copy-sub-buffer patch. Extension was not
  enabled on all radeon cards. (bnc 174839)
- Add radeon large texture patch (back port from latest stable
  release of Mesa). (bnc 174839)
* Tue May 23 2006 sndirsch@suse.de
- no longer remove NVIDIA installer in %%pre
* Tue May 23 2006 sndirsch@suse.de
- reverted Mesa/MesaGLU split
- fixed libGLcore.so.1 (e.g. soname); required to create a
  non-conflicting package for the NVIDIA driver (Bug #175683)
* Tue May 16 2006 sndirsch@suse.de
- splitted off MesaGLU/MesaGLU-devel
- added ldconfig to %%postun
* Sat Apr 22 2006 sndirsch@suse.de
- licensefix.patch:
  * fixed incompatible GPL license (Bug #133238, Mesa Bug #6490)
* Thu Apr 13 2006 sndirsch@suse.de
- added /usr/X11R6/%%{_lib}/modules/dri/updates/README.updates to
  document DRI driver update mechanism
* Wed Apr 12 2006 sndirsch@suse.de
- enhanced search path for DRI driver updates (FATE #300553)
* Tue Apr 04 2006 sndirsch@suse.de
- mesa-6.4.2-dri-copy-sub-buffer-1.patch:
  * needed for open source drivers to work with Xgl (David Reveman)
* Wed Mar 15 2006 mhopf@suse.de
- Fix for bug #157051, issue 1:
  On intel the graphics is only displayed correctly after a scissor region
  other than full screen is specified.
* Mon Feb 06 2006 sndirsch@suse.de
- update to Mesa 6.4.2 (obsoletes tnl_init.diff)
  * New items:
    - added OSMesaColorClamp() function/feature
    - added wglGetExtensionStringARB() function
  * Bug fixes:
    - fixed some problems when building on Windows
    - GLw header files weren't installed by installmesa script (bug 5396)
    - GL/glfbdev.h file was missing from tarballs
    - fixed TNL initialization bug which could lead to crash (bug 5791)
* Mon Feb 06 2006 sndirsch@suse.de
- tnl_init.diff (Mesa Bug #5791):
  * fixes TNL initialization bug which could lead to crash
  (CVS changelog: use calloc instead of malloc so try_codegen
  field is initialized to zero)
* Mon Jan 30 2006 sndirsch@suse.de
- glxext-sgi-hyperpipe.patch:
  * GLX_SGIX_hyperpipe_group -> GLX_SGIX_hyperpipe (Bug #146646)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 20 2006 sndirsch@suse.de
- Mesa_945GM.patch:
  * 945GM support by Charles Johnson (FATE #151391)
* Wed Dec 28 2005 sndirsch@suse.de
- moved header files and libGL.so from Mesa-devel to Mesa to make
  uninstallation of nvidia driver in %%pre of Mesa-devel obsolete
* Thu Dec 01 2005 sndirsch@suse.de
- update to Mesa 6.4.1
* Fri Nov 18 2005 sndirsch@suse.de
- updated to Mesa 6.4 branch (2005-11-18)
- added static libGL (new Mesa-devel-static package)
- removed glut headers from installation (we use freeglut!)
* Tue Nov 15 2005 sndirsch@suse.de
- updated to Mesa 6.4 branch (2005-11-12)
* Wed Nov 09 2005 sndirsch@suse.de
- fixed libOSMesa build
* Tue Nov 08 2005 sndirsch@suse.de
- added build of libOSMesa, e.g. required by tulip package
* Tue Nov 08 2005 sndirsch@suse.de
- added include files for SGI's OpenGL Xt/Motif widgets, e.g.
  required by z88 package
  * GLwMDrawA.h
  * GLwDrawAP.h
  * GLwMDrawAP.h
  * GLwDrawA.h
- enabled Motif support in libGLw, also required by z88 package
* Mon Nov 07 2005 sndirsch@suse.de
- use glx headers from xorg-x11-devel package
* Fri Oct 28 2005 sndirsch@suse.de
- Mesa-glx-x11-render-texture-2.diff/missing-headers.diff:
  * new MESA_render_texture extension for Xgl (dreveman/mhopf)
* Tue Oct 25 2005 sndirsch@suse.de
- fixed DRI driver path for 64bit platforms
* Tue Oct 25 2005 sndirsch@suse.de
- update to Mesa 6.4
* Tue Oct 25 2005 sndirsch@suse.de
- build DRI compatible libGL
* Fri Oct 21 2005 sndirsch@suse.de
- added dummy nvidia libGLcore.so.1 for applications, which are
  still linked against libGL.so.1 of older nvidia driver releases
- duplicate libGL (located in /usr/lib/GL) to make workarounds
  like LD_PRELOAD possible if nvidia driver is installed and its
  libGl does not work
* Wed Oct 19 2005 sndirsch@suse.de
- no longer install libglide (disables 3Dfx DRI support)
* Mon Oct 03 2005 sndirsch@suse.de
- created package
