%define sourcename	armagetronad

Summary:	Armagetron Advanced, another 3d lightcycle game using OpenGL
Name:		armagetron
Version:	0.2.9.1.0
Release:	2
License:	GPL
Group:		Games/Arcade
URL:		https://armagetronad.net/
Source: 	https://launchpad.net/armagetronad/%(echo %{version}|cut -d. -f1-3)/%{version}/+download/armagetronad-%{version}.tbz
Source1:	%{name}-png.tar.bz2
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	gcc-c++, gcc, gcc-cpp


%description
Another very nice and networked Tron game using OpenGL. Armagetron Advanced is
the continuation of the original Armagetron game.

%prep
%autosetup -p1 -n %{sourcename}-%{version}

%build
#export CC=gcc
#export CXX=g++

export CXXFLAGS="%optflags -fpermissive"
%configure \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--disable-games

%make "-I. -I.. -I../.. `sdl-config --cflags` $RPM_OPT_FLAGS"

%install
%makeinstall_std
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

%files
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
%{_datadir}/metainfo/armagetronad.appdata.xml
