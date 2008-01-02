%define name	xconq
%define version	7.5.0
%define pre	20050612
%define release	%mkrel 1.%{pre}.2
%define Summary	General turn-based 2D strategy game system

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
URL:		http://xconq.org
License:	GPL
Group:		Games/Strategy
Source0:	http://prdownloads.sourceforge.net/xconq/%{name}-%{version}-0pre.0.%{pre}.tar.bz2
Patch0:		%{name}-7.5.0.makefile.patch.bz2
Patch1:		%{name}-7.5.0.tclpath.patch.bz2
Patch2:		xconq-7.5.0-64bit-fix.patch
BuildRequires:	paragui-devel >= 1.0.4 freetype2-devel SDL-devel >= 1.2.0
BuildRequires:	ncurses-devel tk tk-devel tcl tcl-devel texinfo ImageMagick
BuildRequires:	X11-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Xconq is a general strategy game system.  It is a complete system that
includes all the components: a portable engine, graphical interfaces
for Unix/Linux/X11, Macintosh, and Windows, multiple AIs, networking
for multi-player games, and an extensive game library.

In addition to Xconq's "standard" game, which is similar to the
classic Empire/Empire Deluxe games of years ago, the game library
includes games for ancient civilizations, the Peloponnesian War, the
Roman Civil War, Frederician strategy, Napoleonic strategy, Gettysburg
at a brigade scale, the Russian revolution, the Normandy invasion,
WWII at scales from tactical to grand strategic, Beirut street
fighting, voyages of discovery, African exploration, and many others,
including space and fantasy games.

As befits its emphasis on strategy, Xconq's forte is turn-based play
using overhead or isometric views of a tiled world.  The world is 
basically two-dimensional, although varying elevations are available 
for games that need elevation effects or line-of-sight.  Xconq is 
especially interesting for games about unusual or lesser-known strategic
situations; it is unique in providing a single system for modelling
the conflicts and strategies of any period in history.

%package	tcltk
Summary:	The Tcl/Tk user interface for the Xconq game system
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description	tcltk
The Tcl/Tk user interface for the Xconq game engine relies on a mixture of 
Tcl scripts and C code to provide a multi-windowed user experience. This 
is presently the one which most players use.

%package	curses
Summary:	The curses (console) user interface for the Xconq game system
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description	curses
The Curses user interface is for running games in the Xconq engine on a 
text console. It is quick, but lacking the more complete experience and 
conveniecne of a graphical user interface.

%package	sdl
Summary:	The SDL user interface for the Xconq game system
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description	sdl
The SDL user interface is in its infancy and much development needs to be 
done on it. However, it is a more modern game interface following the 
single-window paradigm, and it is speedy.

%prep
%setup -q -n %{name}-%{version}-0pre.0.%{pre}
%patch0 -p1 -b .makefile
%patch1 -p0 -b .tclpath
%patch2 -p1 -b .64bit

%build
%configure	--disable-freetypetest \
		--disable-paraguitest \
		--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir}/%{name} \
		--enable-alternate-scoresdir=%{_localstatedir}/games/%{name}
make	all \
	all-cconq \
	all-sdlconq \
	info

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_gamesdatadir}/games
install -d -m 755 %{buildroot}%{_localstatedir}/games
%makeinstall \
	install-cconq \
	install-sdlconq \
	install-info \
	bindir=$RPM_BUILD_ROOT%{_gamesbindir} \
	datadir=$RPM_BUILD_ROOT%{_gamesdatadir}/%{name} \
	scoresdir=$RPM_BUILD_ROOT%{_localstatedir}/games/%{name}

mv %{buildroot}%{_gamesbindir}/{x,tk}conq
mv %{buildroot}%{_mandir}/man6/{x,tk}conq.6

# icons
install -d %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir}}
convert images/default.gif -resize 16x16! %{buildroot}%{_miconsdir}/%{name}.png
convert images/default.gif -resize 32x32! %{buildroot}%{_iconsdir}/%{name}.png
convert images/default.gif -resize 48x48! %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-tcltk.desktop << EOF
[Desktop Entry]
Name=Xconq Tk interface
Comment=%{Summary}, Tk interface
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;StrategyGame;X-MandrivaLinux-MoreApplications-Games-Strategy;
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-sdl.desktop << EOF
[Desktop Entry]
Name=Xconq SDL interface
Comment=%{Summary}, SDL interface
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;StrategyGame;X-MandrivaLinux-MoreApplications-Games-Strategy;
EOF

%post tcltk
%{update_menus}

%post sdl
%{update_menus}

%postun tcltk
%{clean_menus}

%postun sdl
%{clean_menus}

%clean
rm -rf %{buildroot}

%post
%_install_info hacking.info
%_install_info xcdesign.info-1
%_install_info xcdesign.info-2
%_install_info xcdesign.info-3
%_install_info xcdesign.info 
%_install_info xconq.info

%postun
%_remove_install_info hacking.info
%_remove_install_info xcdesign.info-1
%_remove_install_info xcdesign.info-2
%_remove_install_info xcdesign.info-3
%_remove_install_info xcdesign.info 
%_remove_install_info xconq.info

%files
%defattr(-,root,root)
%doc README ChangeLog NEWS doc/*.html changelogs
%{_gamesdatadir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_infodir}/*
%dir %attr(-,games,games) %{_localstatedir}/games/%{name}

%files tcltk
%defattr(-,root,root)
%attr(2755,root,games) %{_gamesbindir}/tkconq
%{_gamesbindir}/imfapp
%{_gamesbindir}/imf2x
%{_gamesbindir}/x2imf
%{_mandir}/man6/tkconq.6*
%{_datadir}/applications/mandriva-%{name}-tcltk.desktop

%files curses
%defattr(-,root,root)
%attr(2755,root,games) %{_gamesbindir}/cconq
%{_mandir}/man6/cconq.6*

%files sdl
%defattr(-,root,root)
%attr(2755,root,games) %{_gamesbindir}/sdlconq
%{_datadir}/applications/mandriva-%{name}-sdl.desktop
