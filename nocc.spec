Summary:	WebMail package
Summary(pl):	Poczta przez WWW
Name:		nocc
Version:	1.2
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/nocc/%{name}-%{version}.tar.gz
# Source0-md5:	5e0a790bdd5ac815cdc39e11f3cf616c
Source1:	%{name}.conf
Patch0:		%{name}-config.patch
URL:		http://nocc.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php >= 3:4.1.0
Requires:	php-iconv
Requires:	php-imap
Requires:	php-pcre
Requires:	webapps
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

%description -l pl
NOCC jest klientem poczty napisanym w PHP. Umo¿liwia dostêp do kont
pocztowych IMAP i POP3 przez WWW.

%prep
#%%setup -q -n %{name}-%{version}
%setup -q -c
%patch0 -p1

cat > apache.conf <<'EOF'
Alias /%{name} /usr/share/%{name}
<Directory /usr/share/%{name}>
        Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},%{_var}/lib/nocc}

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

cp -avR * $RPM_BUILD_ROOT%{_appdir}

install conf.php.dist $RPM_BUILD_ROOT/%{_sysconfdir}/conf.php
ln -s %{_sysconfdir}/conf.php $RPM_BUILD_ROOT%{_appdir}/conf.php

rm -rf $RPM_BUILD_ROOT%{_appdir}/docs
rm -f $RPM_BUILD_ROOT%{_appdir}/{COPYING,INSTALL,README,*.sh}
rm -rf $RPM_BUILD_ROOT%{_appdir}/debian
rm -f $RPM_BUILD_ROOT%{_appdir}/conf.php.dist
rm -f $RPM_BUILD_ROOT%{_appdir}/lang/*.sh

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%doc addcgipath.sh
%doc conf.php.dist
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%attr(770,root,http) %dir %{_var}/lib/nocc
%{_appdir}
