Summary:	WebMail package
Summary(pl):	Poczta przez WWW
Name:		nocc
Version:	1.0.0
Release:	rc1.1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/nocc/%{name}-%{version}rc1.tar.gz
# Source0-md5:	3afd4ab1432dc347573f5a24967a205a
Source1:	%{name}.conf
Patch0:		%{name}-config.patch
URL:		http://nocc.sourceforge.net/
Requires:	webserver
Requires:	php >= 4.1.0
Requires:	php-iconv
Requires:	php-imap
Requires:	php-pcre
Provides:	webmail
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noccdir	/usr/share/nocc

%description
NOCC is a webmail client written in PHP. It provides webmail access to
IMAP and POP3 accounts.

%description -l pl
NOCC jest klientem poczty napisanym w PHP. Umo¿liwia dostêp do kont
pocztowych IMAP i POP3 przez WWW.

%prep
%setup -q -n %{name}-%{version}rc1
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_noccdir},%{_var}/lib/nocc,/etc/nocc,/etc/httpd}
cp -avR * $RPM_BUILD_ROOT%{_noccdir}

install conf.php.dist $RPM_BUILD_ROOT/etc/nocc/conf.php
ln -s /etc/nocc/conf.php $RPM_BUILD_ROOT%{_noccdir}/conf.php

rm -rf $RPM_BUILD_ROOT%{_noccdir}/docs
rm -f $RPM_BUILD_ROOT%{_noccdir}/{COPYING,INSTALL,README,*.sh}
rm -rf $RPM_BUILD_ROOT%{_noccdir}/debian
rm -f $RPM_BUILD_ROOT%{_noccdir}/conf.php.dist
rm -f $RPM_BUILD_ROOT%{_noccdir}/lang/*.sh

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%doc addcgipath.sh
%doc conf.php.dist
%dir /etc/nocc
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) /etc/nocc/conf.php
%attr(770,root,http) %dir %{_var}/lib/nocc
%{_noccdir}
