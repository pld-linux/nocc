Summary:	WebMail package
Summary(pl):	Poczta przez WWW
Name:		nocc
Version:	0.9.5
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://heanet.dl.sourceforge.net/sourceforge/nocc/%{name}-%{version}.tar.gz
Patch0:		%{name}-sec.patch
URL:		http://nocc.sourceforge.net/
Requires:	webserver
Requires:	php
Requires:	php-imap
Provides:	webmail
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noccdir	/home/services/httpd/html/nocc

%description
NOCC is a webmail client written in PHP. It provides webmail access to IMAP and POP3 accounts.

%description -l pl
NOCC jest klientem poczty napisanym w PHP. Umozliwia dostep do kont pocztowych IMAP i POP3 przez www.


%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_noccdir}
install -d $RPM_BUILD_ROOT%{_noccdir}/profiles
cp -avR * $RPM_BUILD_ROOT%{_noccdir}
install -D conf.php.dist $RPM_BUILD_ROOT%{_noccdir}/conf.php
rm -rf $RPM_BUILD_ROOT%{_noccdir}/docs
rm -f $RPM_BUILD_ROOT%{_noccdir}/{COPYING,INSTALL,README,*.sh}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(730,root,http) %dir %{_noccdir}
%attr(770,root,http) %dir %{_noccdir}/profiles
%attr(640,root,http) %{_noccdir}/action.php
%attr(640,root,http) %{_noccdir}/check_lang.php
%attr(640,root,http) %{_noccdir}/check.php
%attr(640,root,http) %{_noccdir}/class_send.php
%attr(640,root,http) %{_noccdir}/class_smtp.php
%attr(640,root,http) %{_noccdir}/conf_lang.php
%attr(640,root,http) %{_noccdir}/delete.php
%attr(640,root,http) %{_noccdir}/download.php
%attr(640,root,http) %{_noccdir}/exception.php
%attr(640,root,http) %{_noccdir}/functions.php
%attr(640,root,http) %{_noccdir}/get_img.php
%attr(640,root,http) %{_noccdir}/help.php
%attr(640,root,http) %{_noccdir}/index.php
%attr(640,root,http) %{_noccdir}/is_uploaded_file.php
%attr(640,root,http) %{_noccdir}/logout.php
%attr(640,root,http) %{_noccdir}/mime.php
%attr(640,root,http) %{_noccdir}/prefs.php
%attr(640,root,http) %{_noccdir}/send.php
%attr(640,root,http) %{_noccdir}/wrong.php
%attr(640,root,http) %config(noreplace) %{_noccdir}/conf.php
%attr(730,root,http) %dir %{_noccdir}/html
%attr(640,root,http) %{_noccdir}/html/*
%attr(730,root,http) %dir %{_noccdir}/lang
%attr(640,root,http) %{_noccdir}/lang/*
%attr(750,root,http) %dir %{_noccdir}/themes
%attr(730,root,http) %dir %{_noccdir}/themes/blue
%attr(730,root,http) %dir %{_noccdir}/themes/blue/img
%attr(640,root,http) %{_noccdir}/themes/blue/img/*
%attr(640,root,http) %{_noccdir}/themes/blue/*.css
%attr(640,root,http) %{_noccdir}/themes/blue/*.php
%attr(730,root,http) %dir %{_noccdir}/themes/newlook
%attr(730,root,http) %dir %{_noccdir}/themes/newlook/img
%attr(640,root,http) %{_noccdir}/themes/newlook/img/*
%attr(640,root,http) %{_noccdir}/themes/newlook/*.css
%attr(640,root,http) %{_noccdir}/themes/newlook/*.php
%attr(730,root,http) %dir %{_noccdir}/themes/standard
%attr(730,root,http) %dir %{_noccdir}/themes/standard/img
%attr(640,root,http) %{_noccdir}/themes/standard/img/*
%attr(640,root,http) %{_noccdir}/themes/standard/*.css
%attr(640,root,http) %{_noccdir}/themes/standard/*.php
%doc docs/*
%doc addcgipath.sh
%doc conf.php.dist
