Summary:	Process monitoring utilities
Summary(de):	Dienstprogramm zur Proze��berwachung
Summary(fr):	Utilitaires de surveillance des processus.
Summary(pl):	Narz�dzia do monitorowania proces�w
Summary(tr):	S�re� izleme ara�lar�
Name:		procps
Version:	1.9.0
%define		date	981104
Release:	2d
Copyright:	GPL
Group:		Utilities/System
Group(pl):	U�ytki/System
URL:		http://www.cs.uml.edu/~acahalan/linux
Source:		%{name}-%{date}.tar.gz
Patch0:		%{name}-opt.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-ps.patch
Patch3:		%{name}-w.patch
Buildroot:	/tmp/%{name}-%{version}-root

%description
A package of utilities which report on the state of the system,
including the states of running processes, amount of memory available,
and currently-logged-in users.

%description -l de
Ein Paket mit Utilities, die den Status des Systems melden, 
einschlie�lich des Status laufender Prozesse, der Menge des 
verf�gbaren Speicherplatzes und der momentan angemeldeten Benutzer.

%description -l fr
Paquetage d'utilitaires donnant des informations sur l'�tat du syst�me,
dont les �tats des processus en cours, le total de m�moire disponible,
et les utilisateurs logg�s.

%description -l pl
Pakiet zawiera podstawowe narz�dzia do monitorowania pracy systemu. Dzi�ki
tym programom b�dziesz m�g� na bie��co kontralowa� jakie procesy s� w danej
chwili uruchomione, ilo�� wolnej pami�ci, kto jest w danej chwili zalogowany,
jakie jest aktualne obci��enie systemu itp.

%description -l tr
Sistemin durumunu rapor eden ara�lar paketidir. Ko�an s�re�lerin durumunu,
kullan�labilir bellek miktar�n�, ve o an i�in sisteme girmi� kullan�c�lar�
bildirir.

%package	X11
Summary:	X-based process monitoring utilities
Summary(de):	Proze��berwachungs-Dienstprogramme f�r X
Summary(fr):	Utilitaires de surveillance des processus sous X
Summary(pl):	Narz�dzia do monitorowania proces�w pod X Window
Summary(tr):	X tabanl� s�re� izleme ara�lar�
Group:		X11/Utilities
Group(pl):	X11/U�ytki
Requires:	%{name} = %{version}  

%description X11
A package of X-based utilities which report on the state of the system.
These utilities generally provide graphical presentations of information
available from tools in the procps suite.

%description -l de X11
Ein Utility-Paket auf X-Basis, die �ber den Systemstatus orientieren. 
Dabei werden die von den Tools aus der procps-Suite gelieferten Daten 
n grafischer Weise dargestellt.

%description -l fr X11
Paquetage d'utilitaires X rapportant l'�tat du syst�me. Ces utilitaires
offrent g�n�ralement des repr�sentations graphiques des informations
disponibles � partir d'outils de la suite procps.

%description -l pl X11
Pakiet zawiera narz�dzia do monitorowania systemu pod X Window. Inmformacje
o stanie systemu s� prezentowane w spos�b graficzny.

%description -l tr X11
Sistemin durumunu g�steren, X tabanl� ara�lar. Bu ara�lar, genellikle
procps paketinde yer alan ara�larla edinebilece�iniz bilgileri grafik olarak
g�r�nt�lerler.

%prep
%setup -q -n %{name}-%{date}
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 

%build
PATH=/usr/X11R6/bin:$PATH

make OPT="$RPM_OPT_FLAGS -pipe" 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/X11/wmconfig,bin,lib}
install -d $RPM_BUILD_ROOT/usr/{bin,man/{man1,man8}}

make install DESTDIR=$RPM_BUILD_ROOT BINGRP=`id -g`

install top.wmconfig $RPM_BUILD_ROOT/etc/X11/wmconfig/top

rm -f  $RPM_BUILD_ROOT/usr/bin/snice
ln -sf skill $RPM_BUILD_ROOT/usr/bin/snice

rm -f $RPM_BUILD_ROOT/usr/man/man1/snice.1
echo .so skill.1 > $RPM_BUILD_ROOT/usr/man/man1/snice.1

strip $RPM_BUILD_ROOT/lib/*.so.*.*

gzip -9fn $RPM_BUILD_ROOT/usr/man/{man1/*,man8/*}
bzip2 -9 NEWS BUGS 

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig
if [ -f /proc/uptime ] ; then
  /bin/ps </dev/null >/dev/null 2>&1
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc {NEWS,BUGS}.bz2 

%config(missingok) /etc/X11/wmconfig/top

%attr(755,root,root) /lib/*.so.*
%attr(755,root,root) /bin/*
%attr(755,root,root) /usr/bin/*
%attr(644,root, man) /usr/man/man[18]/*

%files X11
%attr(755,root,root) /usr/X11R6/bin/XConsole

%changelog
* Sat Feb 06 1999 Marek Druzd <raven@lo14.szczecin.pl>
  [1.9.0-2d]
- fixed idle time (w-patch),
- gziping man pages,
- added Group(pl).

* Wed Dec 30 1998 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [981104]
- final build for PLD,
- stripping shared libraries.

* Sun Oct 25 1998 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [1.2.9-1d]
- updated to 1.2.9,
- major changes.

* Sun Sep 13 1998 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [1.2.8-1d]
- changed Buildroot to /var/tmp/%%{name}-%%{version}-%%{release}-root,
- fixed files permission,
- build against GNU libc-2.1,
- removed striping shared libraries.

* Fri Sep 11 1998 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.2.8-4]
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- added using %%{name} and %%{version} in Source,
- added %postun -p /sbin/ldconfig,
- simplification in %files,
- procps is now linked with libncurse instead libtermcap,
- fixed passing $RPM_OPT_FALGS (procps-rpm_opt_flags.patch),
- added striping shared libraries.

* Wed Sep 09 1998 Wojtek �lusarczyk <wojtek@SHADOW.EU.ORG>
  [1.2.7-2]
- added pl translation,
- build from non root's account.

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- no writable strings patch (problem #856)

* Wed Jun 03 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr
