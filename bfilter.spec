#
# Conditional build:
%bcond_with	gui	# Enable GTK+ UI (doesn't build)
#
Summary:	A filtering Web proxy
Summary(pl):	Filtruj�ce proxy WWW
Name:		bfilter
Version:	0.9.4
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	72ca85565bd4c556b06e3a264c0c24f1
Source1:	%{name}.init
URL:		http://bfilter.sf.net
BuildRequires:	libsigc++12-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	zlib-devel
Requires(post):	/usr/sbin/groupadd
Requires(post):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description 
BFilter is a filtering web proxy. It was originally intended for
removing banner ads only, but at some point it has been extended to
remove popups and webbugs.  Its main advantage over the similar tools
is its heuristic ad detection algorithm. 

%description -l pl
BFilter jest filtruj�cym proxy WWW. Pierwotnie mia� on filtrowa� tylko
bannery, jednak rozszerzono go o usuwanie popup�w i innych reklam.
G��wn� jego przewag� nad innymi tego rodzaju narz�dziami jest
heurystyczny algorytm rozpoznawania reklam.

%prep
%setup -q

%build
%configure \
	--with%{!?with_gui:out}-gui
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# XXX: unify
/usr/sbin/groupadd -r -f %{name}
/usr/sbin/useradd -r -s /bin/false -d / -M -g %{name} -c 'BFilter filtering proxy' %{name}

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/%{name} start\" to start %{name}." 1>&2
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name} ]; then
                /etc/rc.d/init.d/%{name} stop 1>&2
        fi
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/*.html doc/*.png
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) /etc/rc.d/init.d/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/config
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/rules.local
%{_sysconfdir}/%{name}/config.default
%{_sysconfdir}/%{name}/rules
