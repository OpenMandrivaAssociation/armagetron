#(peroyvind) dunno what this is nor why it's required, but we don't have it and it shouldn't be required
%define	_requires_exceptions	BEGIN_RIM

%define sourcename	armagetronad

Summary:	Armagetron Advanced, another 3d lightcycle game using OpenGL
Name:		armagetron
Version:	0.2.8.3.2
Release:	%mkrel 2
License:	GPL
Group:		Games/Arcade
URL:		http://armagetronad.net/
Source: 	http://prdownloads.sourceforge.net/armagetronad/%{sourcename}-%{version}.src.tar.bz2
Source1:	%{name}-png.tar.bz2
Patch0:         armagetronad-0.2.8.3.1-empty-master.srv-fix.patch
Patch1:         armagetron-0.2.8.3.2-libpng1.5.patch
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
%patch0 -p0 -b .empty-master.srv
%patch1 -p0 -b .libpng

%build
autoreconf -fi
export CXXFLAGS="%{optflags} -fpermissive"
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--disable-games \
	--disable-uninstall

%make "-I. -I.. -I../.. `sdl-config --cflags` %{optflags}"

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
mv %{buildroot}%{_gamesdatadir}/doc %{buildroot}%{_datadir}

# remove unwanted files
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
Exec=soundwrapper %{_gamesbindir}/%{name}
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

