#
# Conditional build:
%bcond_with	gui	# Enable GTK+ UI (doesn't build)
#
Summary:	A filtering Web proxy
Summary(pl.UTF-8):	Filtrujące proxy WWW
Name:		bfilter
Version:	0.9.4
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/bfilter/%{name}-%{version}.tar.gz
# Source0-md5:	72ca85565bd4c556b06e3a264c0c24f1
Source1:	%{name}.init
URL:		http://bfilter.sf.net
BuildRequires:	libsigc++12-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(bfilter)
Provides:	user(bfilter)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BFilter is a filtering web proxy. It was originally intended for
removing banner ads only, but at some point it has been extended to
remove popups and webbugs. Its main advantage over the similar tools
is its heuristic ad detection algorithm.

%description -l pl.UTF-8
BFilter jest filtrującym proxy WWW. Pierwotnie miał on filtrować tylko
bannery, jednak rozszerzono go o usuwanie popupów i innych reklam.
Główną jego przewagą nad innymi tego rodzaju narzędziami jest
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
%groupadd -r -g 199 %{name}
%useradd -r -u 199 -s /bin/false -d / -g %{name} -c "BFilter filtering proxy" %{name}

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "BFilter filtering proxy"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/*.html doc/*.png
%attr(755,root,root) %{_bindir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/rules.local
%{_sysconfdir}/%{name}/config.default
%{_sysconfdir}/%{name}/rules
