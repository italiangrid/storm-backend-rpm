## Turn off meaningless jar repackaging (works only on SL6)
%define __jar_repack 0

%global release_version 1

%if %{?build_number:1}%{!?build_number:0}
%define release_ 0.build%{build_number}%{?dist}
%else
%define release_  %{release_version}%{?dist}
%endif

%define _modulename backend-server
%define prefixname storm

Name:    storm-backend-server
Version: 1.11.11
Release: %{release_}
Summary: The StoRM backend server

Group: Applications/File
License:  ASL 2.0
Url: https://github.com/italiangrid/storm
Source:    %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}

BuildArch: noarch

BuildRequires: apache-maven
BuildRequires: jpackage-utils
BuildRequires: java-1.6.0-openjdk-devel

Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts

Requires: java-1.6.0-openjdk
Requires: mysql
Requires: mysql-server
Requires: nc
Requires: xml-commons-apis
Requires: mysql-connector-java
Requires: jpackage-utils
Requires: storm-native-libs >= 1.0.2
Requires: storm-native-libs-lcmaps >= 1.0.2
Requires: storm-native-libs-java >= 1.0.2

%description
StoRM provides an SRM interface to any POSIX filesystem with direct file
access ("file:" transport protocol), but can take advantage of special
features of high performance parallel and cluster file systems, as GPFS from 
IBM and Lustre from SUN. 

This package contains the StoRM backend server.


%prep
%setup -q -n %{name}

%build
mvn -s mirror-settings.xml -DskipTests -U clean package

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar -C $RPM_BUILD_ROOT -xvzf target/%{name}.tar.gz

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)

%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar

%attr(755,root,root) %{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_database_config.sh
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_be_ISAM_mysql_update_from_1.0.0_to_1.1.0.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_mysql_grant.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_mysql_tbl.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_mysql_update_from_1.7.0_to_1.7.1.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_mysql_update_from_1.7.1_to_1.7.2.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/lcmaps.db
%config(noreplace) %{_sysconfdir}/%{prefixname}/%{_modulename}/logging.xml
%{_sysconfdir}/%{prefixname}/%{_modulename}/namespace-1.5.0.xsd
%config(noreplace) %{_sysconfdir}/%{prefixname}/%{_modulename}/namespace.xml
%config(noreplace) %{_sysconfdir}/%{prefixname}/%{_modulename}/path-authz.db
%{_sysconfdir}/%{prefixname}/%{_modulename}/storm.properties.template
%{_sysconfdir}/%{prefixname}/%{_modulename}/used-space.ini.template
%{_sysconfdir}/%{prefixname}/%{_modulename}/welcome.txt
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(755,root,root) %{_sysconfdir}/init.d/%{name}

%dir %{_localstatedir}/log/%{prefixname}


%post
# when installing
if [ "$1" = "1" ] ; then
  # add the service to chk
  /sbin/chkconfig --add %{name}
  # create mysql-connector-java jar link
  /bin/ln -sf /usr/share/java/mysql-connector-java.jar %{_javadir}/%{name}/mysql-connector-java.jar
# when upgrading
elif [ $1 -gt 1 ] ; then
  # create mysql-connector-java jar link if it does not exist
  if [ ! -L %{_javadir}/%{name}/mysql-connector-java.jar ] ; then
    /bin/ln -sf /usr/share/java/mysql-connector-java.jar %{_javadir}/%{name}/mysql-connector-java.jar
  fi
  # remove old mysql-connector-java jar link
  if [ -L %{_javadir}/%{name}/mysql-connector-java-5.1.12.jar ] ; then
    /bin/unlink %{_javadir}/%{name}/mysql-connector-java-5.1.12.jar
  fi    
  # start the service
  /sbin/service %{name} restart >/dev/null 2>&1 || :
fi;

%preun
# when uninstalling
if [ "$1" = "0" ] ; then
  # stop the service
  /sbin/service %{name} stop >/dev/null 2>&1 || :
  # remove the service from chk
  /sbin/chkconfig --del %{name}
  # remove mysql-connector-java jar link
  /bin/unlink %{_javadir}/%{name}/mysql-connector-java.jar
fi;

%changelog
* Wed Feb 3 2016 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.11-0
- Bumped packaging version for 1.11.11 release.

* Fri Dec 18 2015 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.10-1
- Bumped packaging version for 1.11.10 release.

* Wed Jun 3 2015 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.9-1
- Bumped packaging version for 1.11.9 release.

* Fri Mar 13 2015 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.8-1
- Bumped packaging version for 1.11.8 release.

* Tue Jan 29 2015 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.7-1
- Bumped packaging version for 1.11.7 release.

* Tue Jan 19 2015 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.6-1
- Bumped packaging version for 1.11.6 release.

* Tue Jan 14 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.5-1
- Bumped packaging version for 1.11.5 release.

* Tue Jan 14 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.4-1
- Bumped packaging version for 1.11.4 release.

* Wed Oct 30 2013 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.3-1
- Fix for https://issues.infn.it/jira/browse/STOR-341
- Fix for https://issues.infn.it/jira/browse/STOR-342
- Fix for https://issues.infn.it/jira/browse/STOR-344

* Wed Jun 12 2013 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.2-1
- Integrated native libs interface v. 1.0.1
