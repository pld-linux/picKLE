# TODO
# - webapps
Summary:	Image gallery system created in PHP
Summary(pl.UTF-8):   System galeriowy oparty na PHP
Name:		picKLE
Version:	0.3
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/picklegallery/%{name}-%{version}.tar.gz
# Source0-md5:	6e089d56af3509d3085e727a3496f6b1
Source1:	%{name}.conf
URL:		http://picklegallery.sourceforge.net/
Requires:	ImageMagick
Requires:	webserver
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pickledir	%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

%description
picKLE is an image gallery system created in PHP. It generates
thumbnails and resampled images on the fly and caches them. It is made
to be extremely simple to install/configure.

%description -l pl.UTF-8
picKLE jest to system galeriowy oparty na PHP. Generuje w locie
miniaturki i pomniejszone zdjęcia, po czym zapisuje je w katalogu
cache. Dodatkowo wyróżnia się bardzo łatwą instalacją oraz
konfiguracją.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pickledir} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd}

cp -af  *.php  picKLE-*  *.css $RPM_BUILD_ROOT%{_pickledir}
rm -f $RPM_BUILD_ROOT%{_pickledir}/picKLE-conf.php

install picKLE-conf.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/picKLE-conf.php $RPM_BUILD_ROOT%{_pickledir}/picKLE-conf.php

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
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
		if [ -f /var/lock/subsys/httpd ]; then
			/usr/sbin/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc TODO INSTALL KNOWN-BUGS CHANGELOG
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%dir %{_pickledir}
%{_pickledir}/picKLE-*
%{_pickledir}/*.php
%{_pickledir}/*.css
