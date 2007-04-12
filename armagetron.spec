%define name		armagetron
%define sourcename	armagetronad
%define version		0.2.7.1
%define release		%mkrel 5

Summary:	Armagetron Advanced, another 3d lightcycle game using OpenGL
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Arcade

URL:		http://armagetronad.net/

Source:		http://prdownloads.sourceforge.net/armagetronad/%{sourcename}-%{version}.tar.bz2
Source1:	%{name}-png.tar.bz2

#Patch0:	armagetron-configure-fix.patch.bz2
#Patch2:	armagetron-distrib.patch.bz2
#Patch3:		armagetron-0.2.6.0-64bit-fixes.patch.bz2
#Patch4:		%{name}-0.2.4-fixes.patch.bz2
#Patch5:		armagetron-0.2.6.0-gcc3_4.patch.bz2
#Patch6:		armagetron-0.2.6.0-lib64.patch.bz2
Patch10:	armagetron-0.2.7.1-gcc4.patch
BuildRoot:	%{_tmppath}/%{sourcename}-%{version}-buildroot
BuildRequires:	SDL_image-devel
BuildRequires:	XFree86-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	esound-devel
BuildRequires:	libMesaGLU-devel
BuildRequires:	libpng-devel
BuildRequires:	autoconf2.1
#(peroyvind) dunno what this is nor why it's required, but we don't have it and it shouldn't be required
%define	_requires_exceptions	BEGIN_RIM

%description
Another very nice and networked Tron game using OpenGL. Armagetron Advanced is
the continuation of the original Armagetron game.

%prep

%setup -q -n %{sourcename}-%{version}
%patch10 -p0 -b .gcc4
autoconf

%build
%configure2_5x

%make "-I. -I.. -I../.. `sdl-config --cflags` $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_gamesbindir}
cat <<EOF >$RPM_BUILD_ROOT%{_gamesbindir}/%{name}
#!/bin/sh -e

REALTRON=%{_gamesbindir}/%{name}.real

DATADIR=%{_gamesdatadir}/%{name}
CONFDIR=%{_sysconfdir}/%{name}
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

install -m0755 src/tron/%{sourcename} $RPM_BUILD_ROOT%{_gamesbindir}/%{name}.real
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/games/%{name}
mkdir -p $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
cp -a arenas models sound textures language \
	$RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
rm -f $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/language/.tag
chmod -R a+r $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
chmod a+r COPYING.txt README

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

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING.txt README
%attr(0755,root,games) %{_gamesbindir}/%{name}
%attr(2755,root,games) %{_gamesbindir}/%{name}.real
%{_gamesdatadir}/%{name}
%dir %attr(0775,games,games) %{_localstatedir}/games/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop


