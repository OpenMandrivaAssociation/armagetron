#(peroyvind) dunno what this is nor why it's required, but we don't have it and it shouldn't be required
%define	_requires_exceptions	BEGIN_RIM

%define sourcename	armagetronad

Summary:	Armagetron Advanced, another 3d lightcycle game using OpenGL
Name:		armagetron
Version:	0.2.8.2.1
Release:	%mkrel 15
License:	GPL
Group:		Games/Arcade
URL:		http://armagetronad.net/
Source: 	http://prdownloads.sourceforge.net/armagetronad/%{sourcename}-%{version}.src.tar.gz
Source1:	%{name}-png.tar.bz2
Patch0:		armagetronad-gcc43.diff
Patch1:		armagetronad-0.2.8.2.1-empty-master.srv-fix.patch
BuildRequires:	SDL_image-devel
BuildRequires:	mesaglu-devel
BuildRequires:	libpng-devel
BuildRequires:	libxml2-devel
BuildRoot:	%{_tmppath}/%{sourcename}-%{version}-buildroot

%description
Another very nice and networked Tron game using OpenGL. Armagetron Advanced is
the continuation of the original Armagetron game.

%prep

%setup -q -n %{sourcename}-%{version}
%patch0 -p1 -b .gcc43
%patch1 -p1 -b .empty-master.srv

%build
export CXXFLAGS="%optflags -fpermissive"
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--disable-games

%make "-I. -I.. -I../.. `sdl-config --cflags` $RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
mv %{buildroot}%{_gamesdatadir}/doc %{buildroot}%{_datadir}

# remove unwanted files
rm -f %{buildroot}%{_gamesbindir}/armagetronad-uninstall
rm -rf %{buildroot}%{_gamesdatadir}/%{sourcename}/{desktop,scripts}
rm -rf %{buildroot}%{_datadir}/{applnk,icons}
rm -rf %{buildroot}/opt/kde3/share/{applnk,icons}

cat <<EOF >%{buildroot}%{_gamesbindir}/%{name}
#!/bin/sh -e

REALTRON=%{_gamesbindir}/%{sourcename}

DATADIR=%{_gamesdatadir}/%{sourcename}
CONFDIR=%{_sysconfdir}/%{sourcename}
USERCONFDIR=\$HOME/.%{name}
USERDATADIR=\$USERCONFDIR/data
VARDIR=\$HOME/.%{name}
AUTORESOURCEDIR=\$HOME/.%{name}/resource
if [ ! -d \$USERCONFDIR ]; then
	# have to create configuration directory
	install -d \$USERCONFDIR
fi
if [ -f \$HOME/.%{name}rc ]; then
	# upgrade from before 0.2
	mv -f \$HOME/.%{name}rc \$USERCONFDIR/user.cfg
fi
# remove empty master.srv file created by earlier revisions
if [ -r \$USERCONFDIR/master.srv ] && ! [ -s \$USERCONFDIR/master.srv ]; then
  rm -f \$USERCONFDIR/master.srv
fi

CMDLINE="--datadir \$DATADIR --configdir \$CONFDIR --userconfigdir \$USERCONFDIR --vardir \$VARDIR --autoresourcedir \$AUTORESOURCEDIR"
if [ -d \$USERDATADIR ]; then
	CMDLINE="\$CMDLINE --userdatadir \$USERDATADIR"
fi
exec \$REALTRON \$CMDLINE "\$@"
EOF

tar xjf %{SOURCE1}
install -m0644 %{name}-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m0644 %{name}-32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 %{name}-48.png -D %{buildroot}%{_liconsdir}/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Armagetron Advanced
Comment=Another 3d lightcycle game
Exec=soundwrapper %_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%attr(0755,root,games) %{_gamesbindir}/%{name}
%attr(2755,root,games) %{_gamesbindir}/%{sourcename}
%{_gamesdatadir}/%{sourcename}
%dir %{_sysconfdir}/%{sourcename}
%config(noreplace) %{_sysconfdir}/%{sourcename}/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%{_defaultdocdir}/%{sourcename}



%changelog
* Tue May 03 2011 Funda Wang <fwang@mandriva.org> 0.2.8.2.1-13mdv2011.0
+ Revision: 663758
- use fpermissive to build

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Wed Feb 02 2011 Funda Wang <fwang@mandriva.org> 0.2.8.2.1-12
+ Revision: 634998
- rebuild
- tighten BR

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.8.2.1-11mdv2011.0
+ Revision: 603183
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.8.2.1-10mdv2010.1
+ Revision: 522030
- rebuilt for 2010.1

* Sun May 24 2009 Christiaan Welvaart <spturtle@mandriva.org> 0.2.8.2.1-9mdv2010.0
+ Revision: 379301
- startup script: remove empty master.srv from user config dir

* Sun May 24 2009 Christiaan Welvaart <spturtle@mandriva.org> 0.2.8.2.1-8mdv2010.0
+ Revision: 379161
- patch1: disable autosave of master.srv which caused an empty file to be written (replaces previous fix for #51152)
- put downloaded resources in $HOME/.armagetron/resource

* Sat May 23 2009 Samuel Verschelde <stormi@mandriva.org> 0.2.8.2.1-7mdv2010.0
+ Revision: 379017
- let the program use ~/.armagetronad for user settings (fixes #51152)

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 0.2.8.2.1-6mdv2009.1
+ Revision: 349992
- 2009.1 rebuild

* Sun Jul 06 2008 Christiaan Welvaart <spturtle@mandriva.org> 0.2.8.2.1-5mdv2009.0
+ Revision: 232246
- remove kde files if installed, do not include them in the package

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix unpacked files
    - added a gcc43 patch
    - rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix mesaglu-devel BR
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 04 2007 Christiaan Welvaart <spturtle@mandriva.org> 0.2.8.2.1-3mdv2008.1
+ Revision: 115207
- drop /var/lib/games/armagetron dir, put all settings and results in $HOME/.armagetron

  + Thierry Vignaud <tv@mandriva.org>
    - buildrequires X11-devel instead of XFree86-devel
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Thu Aug 16 2007 Thierry Vignaud <tv@mandriva.org> 0.2.8.2.1-2mdv2008.0
+ Revision: 64188
- rebuild

* Tue May 22 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.2.8.2.1-1mdv2008.0
+ Revision: 29746
- Updated to 0.2.8.2.1.


* Tue Jan 30 2007 Nicolas Lécureuil <neoclust@mandriva.org> 0.2.7.1-5mdv2007.0
+ Revision: 115470
- kill old debian menu

* Sat Dec 02 2006 Olivier Blin <oblin@mandriva.com> 0.2.7.1-4mdv2007.1
+ Revision: 89973
- xdg menu
- Import armagetron

* Thu Aug 25 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.2.7.1-3mdk
- Fix summary, menu name and URL

* Mon Aug 01 2005 Guillaume Bedot <littletux@mandriva.org> 0.2.7.1-2mdk
- rebuild
- Patch10: allows to build with g++4

* Tue Apr 26 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.2.7.1-1mdk
- 0.2.7.1
- Drop patches 3 to 6

* Wed Oct 27 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.2.6.0-4mdk
- lib64 fixes
- put back 64-bit fixes that got nuked away somehow since 9.2

* Sat Aug 21 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.6.0-3mdk
- Rebuild with new menu

* Tue Jul 20 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.2.6.0-2mdk
- rebuild with gcc 3.4 (patch5)

* Sat Apr 24 2004 Michael Scherer <misc@mandrake.org> 0.2.6.0-1mdk
- New release 0.2.6.0

