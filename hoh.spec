# the game is close-sourced and no longer developed so debug is useless
%define		_enable_debug_packages %{nil}
%define		debug_package %{nil}

Name:		hoh
Version:	1.01
Release:	3
Summary:	Remake of the 80's 8-bit classic game Head over Heels
Group:		Games/Arcade
License:	Freeware
URL:		http://retrospec.sgn.net/game/hoh
Source0:	http://retrospec.sgn.net/games/hoh/bin/hohlin-101.tar.bz2
Source1:	http://retrospec.sgn.net/games/hoh/bin/hoh-update-101.tar.bz2
Source2:	%{name}.png
BuildRequires:	imagemagick
ExclusiveArch:	%{ix86}

%description
Remake of the 80's 8-bit classic game Head over Heels.

%prep
%setup -q -c -a1

%build

%install
%__rm -rf %{buildroot}

# wrapper script
%__mkdir_p %{buildroot}%{_bindir}
%__cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/bash
export LD_LIBRARY_PATH=%{_libdir}/%{name}/runtime
cd %{_libdir}/%{name}
exec ./HoH \$@
EOF
%__chmod 755 %{buildroot}%{_bindir}/%{name}

# game files
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -raf %{name}-install-%{version}/data/* %{buildroot}%{_libdir}/%{name}/
cp -raf %{name}-update-%{version}/data/HoH %{buildroot}%{_libdir}/%{name}/

# icons
for N in 16 32 64 128; do
	convert %{SOURCE2} -resize ${N}x${N} $N.png;
done
%__install -D 16.png %{buildroot}%{_miconsdir}/%{name}.png
%__install -D 32.png %{buildroot}%{_liconsdir}/%{name}.png
%__install -D %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%__install -D 64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%__install -D 128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

# menu-entry
%__mkdir_p  %{buildroot}%{_datadir}/applications
%__cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Head over Heels
Comment=Retro 80's classic
Exec=hoh
Icon=hoh
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

%files
%doc %{name}-install-%{version}/docs %{name}-install-%{version}/readme.txt
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/Sound
%dir %{_libdir}/%{name}/runtime
%attr(755,root,root) %{_libdir}/%{name}/runtime/*
%attr(755,root,root) %{_libdir}/%{name}/HoH
%{_libdir}/%{name}/HoHOriginal.dat
%{_datadir}/applications/%{name}.desktop
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.png

