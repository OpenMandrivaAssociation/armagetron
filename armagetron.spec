%define name		armagetron
%define sourcename	armagetronad
%define version 	0.2.8.2.1
%define release 	%mkrel 1

Summary:	Armagetron Advanced, another 3d lightcycle game using OpenGL
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Arcade

URL:		http://armagetronad.net/

Source: 	http://prdownloads.sourceforge.net/armagetronad/%{sourcename}-%{version}.src.tar.gz
Source1:	%{name}-png.tar.bz2

BuildRoot:	%{_tmppath}/%{sourcename}-%{version}-buildroot
BuildRequires:	SDL_image-devel
BuildRequires:	XFree86-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	esound-devel
BuildRequires:	libMesaGLU-devel
BuildRequires:	libpng-devel
#(peroyvind) dunno what this is nor why it's required, but we don't have it and it shouldn't be required
%define	_requires_exceptions	BEGIN_RIM

%description
Another very nice and networked Tron game using OpenGL. Armagetron Advanced is
the continuation of the original Armagetron game.

%prep
%setup -q -n %{sourcename}-%{version}

%build
%configure \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--disable-games

%make "-I. -I.. -I../.. `sdl-config --cflags` $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
mv $RPM_BUILD_ROOT%{_gamesdatadir}/doc $RPM_BUILD_ROOT%{_datadir}

# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_gamesbindir}/armagetronad-uninstall
rm -rf $RPM_BUILD_ROOT%{_gamesdatadir}/%{sourcename}/{desktop,scripts}
rm -rf $RPM_BUILD_ROOT%{_datadir}/{applnk,icons}

cat <<EOF >$RPM_BUILD_ROOT%{_gamesbindir}/%{name}
#!/bin/sh -e

REALTRON=%{_gamesbindir}/%{sourcename}

DATADIR=%{_gamesdatadir}/%{sourcename}
CONFDIR=%{_sysconfdir}/%{sourcename}
USERCONFDIR=\$HOME/.%{name}
USERDATADIR=\$USERCONFDIR/data
VARDIR=%{_localstatedir}/games/%{name}
if [ ! -d \$USERCONFDIR ]; then
	# have to create configuration directory
	install -d \$USERCONFDIR
fi
if [ -f \$HOME/.%{name}rc ]; then
	# upgrade from before 0.2
	mv -f \$HOME/.%{name}rc \$USERCONFDIR/user.cfg
fi

CMDLINE="--datadir \$DATADIR --configdir \$CONFDIR --userconfigdir \$USERCONFDIR --vardir \$VARDIR"
if [ -d \$USERDATADIR ]; then
	CMDLINE="\$CMDLINE --userdatadir \$USERDATADIR"
fi
exec \$REALTRON \$CMDLINE "\$@"
EOF

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/games/%{name}

tar xjf %{SOURCE1}
install -m0644 %{name}-16.png -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m0644 %{name}-32.png -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m0644 %{name}-48.png -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Armagetron Advanced
Comment=Another 3d lightcycle game
Exec=soundwrapper %_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%attr(0755,root,games) %{_gamesbindir}/%{name}
%attr(2755,root,games) %{_gamesbindir}/%{sourcename}
%{_gamesdatadir}/%{sourcename}
%dir %attr(0775,games,games) %{_localstatedir}/games/%{name}
%dir %{_sysconfdir}/%{sourcename}
%config(noreplace) %{_sysconfdir}/%{sourcename}/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%{_defaultdocdir}/%{sourcename}

