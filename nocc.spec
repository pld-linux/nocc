Summary:	WebMail package
Summary(pl.UTF-8):	Poczta przez WWW
Name:		nocc
Version:	1.7
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/nocc/%{name}-%{version}.tar.gz
# Source0-md5:	4c13e9e3f4e40e2e4420442dbc22bcbd
Patch0:		%{name}-config.patch
URL:		http://nocc.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(iconv)
Requires:	php(imap)
Requires:	php(pcre)
Requires:	webapps
Requires:	webserver(php) >= 4.1.0
Provides:	webmail
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		nocc
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
NOCC is a webmail client written in PHP. It provides webmail access to
IMAP and POP3 accounts.

%description -l pl.UTF-8
NOCC jest klientem poczty napisanym w PHP. Umożliwia dostęp do kont
pocztowych IMAP i POP3 przez WWW.

%prep
%setup -q -c %{name}-%{version}

%patch0 -p1

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

%build
find -type d -name CVS | while read cvsdir; do
	rm -rf $cvsdir
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},%{_var}/lib/nocc}
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

install config/conf.php.dist config/conf.php
mv config $RPM_BUILD_ROOT%{_sysconfdir}/
cp -avR * $RPM_BUILD_ROOT%{_appdir}

ln -s %{_sysconfdir}/config $RPM_BUILD_ROOT%{_appdir}/

rm -rf $RPM_BUILD_ROOT%{_appdir}/docs
rm -f $RPM_BUILD_ROOT%{_appdir}/{COPYING,INSTALL,README,*.sh}
rm -rf $RPM_BUILD_ROOT%{_appdir}/debian
rm -f $RPM_BUILD_ROOT%{_appdir}/lang/*.sh

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%dir %attr(750,root,http) %{_sysconfdir}
%dir %attr(750,root,http) %{_sysconfdir}/config
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/*
%attr(770,root,http) %dir %{_var}/lib/nocc
%{_appdir}
