Summary:	DB2 ODBC CLI driver
Summary(pl.UTF-8):	Sterownik DB2 ODBC CLI
Name:		ibm-db2-clidriver
Version:	11.5.9
Release:	1
License:	proprietary (parts redistributable with application)
Group:		Libraries
Source0:	https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/v%{version}/linuxia32_odbc_cli.tar.gz
# NoSource0-md5:	cc8cc919293e41790ba6ad9122b46d0b
Source1:	https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/v%{version}/linuxx64_odbc_cli.tar.gz
# NoSource1-md5:	e9f36d85b8a6d9e0f7114b1c8b1e244d
Source2:	https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/v%{version}/ppc64le_odbc_cli.tar.gz
# NoSource2-md5:	c624a816edc73ec6857874c54dedbf25
Source3:	https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/v%{version}/s390x64_odbc_cli.tar.gz
# NoSource3-md5:	7758b4132171445d1f146c4eadf197ee
# there are also older drivers for other archs:
# v11.1.4 for s390: https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/v11.1.4/s390_odbc_cli.tar.gz
# v10.5.0.5 (20141215) for ppc: https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/ppc32_odbc_cli.tar.gz
# v10.5.0.5 (20141215) for ppc64 BE: https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/ppc64_odbc_cli.tar.gz
URL:		https://www.ibm.com/support/pages/db2-odbc-cli-driver-download-and-installation-information
NoSource:	0
NoSource:	1
NoSource:	2
NoSource:	3
ExclusiveArch:	%{ix86} %{x8664} ppc64le s390x
# + possible older versions: ppc ppc64 s390
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664} ppc64le s390x
%define		gsktag	_64
%else
%define		gsktag	%{nil}
%endif

%description
DB2 ODBC CLI driver provides runtime support for applications using
CLI APIs, or ODBC APIs without the need of installing the Data Server
Client or the Data Server Runtime Client.

The IBM Data Server Driver for ODBC and CLI provides runtime support
for:
- the DB2 CLI application programming interface (API)
- the ODBC API
- the XA API
- database connectivity
- the DB2 Interactive Call Level Interface (db2cli)
- LDAP support (but LDAP cache is not saved to disk)
- tracing, logging, and diagnostic support.

%description -l pl.UTF-8
Sterownik DB2 ODBC CLI zapewnia wsparcie uruchomieniowe dla aplikacji
wykorzystujących API CLI lub ODBC bez potrzeby instalowania produktów
Data Server Client czy Data Server Runtime Client.

IBM Data Server Driver for ODBC and CLI zapewnia obsługę:
- aplikacji wykorzystujących interfejs DB2 CLI
- API ODBC
- API XA
- łączności z bazą danych
- interfejs DB2 Interactive Call Level (db2cli)
- LDAP (ale pamięć podręczna LDAP nie jest zapisywana na dysk)
- śledzenia, logowania i diagnostyki.

%package devel
Summary:	Header files for DB2 ODBC CLI driver
Summary(pl.UTF-8):	Pliki nagłówkowe sterownika DB2 ODBC CLI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for DB2 ODBC CLI driver.

%description devel -l pl.UTF-8
Pliki nagłówkowe sterownika DB2 ODBC CLI.

%prep
%ifarch %{ix86}
%setup -q -c
%endif
%ifarch %{x8664}
%setup -q -c -T -a1
%endif
%ifarch ppc64le
%setup -q -c -T -a2
%endif
%ifarch s390x
%setup -q -c -T -a3
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}}

cp -a clidriver $RPM_BUILD_ROOT%{_libdir}/clidriver
# files packaged as %doc; dir itself needed for DB2 Connect license files
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/clidriver/license/*

for f in $RPM_BUILD_ROOT%{_libdir}/clidriver/bin/* ; do
	bn="$(basename "$f")"
	ln -sf "../%{_lib}/clidriver/bin/$bn" "$RPM_BUILD_ROOT%{_bindir}/$bn"
done
for f in $RPM_BUILD_ROOT%{_libdir}/clidriver/lib/libDB2xml4c.so.*.* \
	 $RPM_BUILD_ROOT%{_libdir}/clidriver/lib/libdb2.so.1 \
	 $RPM_BUILD_ROOT%{_libdir}/clidriver/lib/libdb2clixml4c.so.1 ; do
	bn="$(basename "$f")"
	ln -sf "clidriver/lib/$bn" "$RPM_BUILD_ROOT%{_libdir}/$bn"
done
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/clidriver/lib/libDB2xml4c.so.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libDB2xml4c.so.58
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/clidriver/lib/libDB2xml4c.so.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libDB2xml4c.so
ln -sf libdb2.so.1 $RPM_BUILD_ROOT%{_libdir}/libdb2.so
ln -sf libdb2clixml4c.so.1 $RPM_BUILD_ROOT%{_libdir}/libdb2clixml4c.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc clidriver/license/{odbc_REDIST,odbc_notices}.txt clidriver/license/UNIX/odbc_LI_en
%lang(cs) %doc clidriver/license/UNIX/odbc_LI_cs
%lang(de) %doc clidriver/license/UNIX/odbc_LI_de
%lang(el) %doc clidriver/license/UNIX/odbc_LI_el
%lang(es) %doc clidriver/license/UNIX/odbc_LI_es
%lang(fr) %doc clidriver/license/UNIX/odbc_LI_fr
%lang(in) %doc clidriver/license/UNIX/odbc_LI_in
%lang(it) %doc clidriver/license/UNIX/odbc_LI_it
%lang(ja) %doc clidriver/license/UNIX/odbc_LI_ja
%lang(ko) %doc clidriver/license/UNIX/odbc_LI_ko
%lang(lt) %doc clidriver/license/UNIX/odbc_LI_lt
%lang(pl) %doc clidriver/license/UNIX/odbc_LI_pl
%lang(pt) %doc clidriver/license/UNIX/odbc_LI_pt
%lang(ru) %doc clidriver/license/UNIX/odbc_LI_ru
%lang(sl) %doc clidriver/license/UNIX/odbc_LI_sl
%lang(tr) %doc clidriver/license/UNIX/odbc_LI_tr
%lang(zh) %doc clidriver/license/UNIX/odbc_LI_zh
%lang(zh_TW) %doc clidriver/license/UNIX/odbc_LI_zh_TW
%dir %{_libdir}/clidriver
%dir %{_libdir}/clidriver/bin
%attr(755,root,root) %{_libdir}/clidriver/bin/db2*
%{_libdir}/clidriver/bnd
%{_libdir}/clidriver/cfg
%{_libdir}/clidriver/cfgcache
%{_libdir}/clidriver/conv
%{_libdir}/clidriver/db2dump
%dir %{_libdir}/clidriver/lib
%attr(755,root,root) %{_libdir}/clidriver/lib/libDB2xml4c.so.*
%attr(755,root,root) %{_libdir}/clidriver/lib/libdb2.so.*
%attr(755,root,root) %{_libdir}/clidriver/lib/libdb2clixml4c.so.*
%dir %{_libdir}/clidriver/lib/icc
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8acmeidup%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8cms%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8dbfl%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8drld%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8iccs%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8kicc%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8km%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8km2%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8ldap%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8p11%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8ssl%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8sys%{gsktag}.so
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/libgsk8valn%{gsktag}.so
%dir %{_libdir}/clidriver/lib/icc/C
%dir %{_libdir}/clidriver/lib/icc/C/icc
%dir %{_libdir}/clidriver/lib/icc/C/icc/icclib
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/C/icc/icclib/libicclib084.so
%{_libdir}/clidriver/lib/icc/C/icc/icclib/ICCSIG.txt
%dir %{_libdir}/clidriver/lib/icc/N
%dir %{_libdir}/clidriver/lib/icc/N/icc
%dir %{_libdir}/clidriver/lib/icc/N/icc/icclib
%attr(755,root,root) %{_libdir}/clidriver/lib/icc/N/icc/icclib/libicclib085.so
%{_libdir}/clidriver/lib/icc/N/icc/icclib/ICCSIG.txt
%dir %{_libdir}/clidriver/license
%dir %{_libdir}/clidriver/msg
%{_libdir}/clidriver/msg/en_US.iso88591
%{_libdir}/clidriver/properties
%{_libdir}/clidriver/scripts
%dir %{_libdir}/clidriver/security32
%dir %{_libdir}/clidriver/security32/plugin
%dir %{_libdir}/clidriver/security32/plugin/IBM
%dir %{_libdir}/clidriver/security32/plugin/IBM/client
%attr(755,root,root) %{_libdir}/clidriver/security32/plugin/IBM/client/IBMIAMauth.so
%attr(755,root,root) %{_libdir}/clidriver/security32/plugin/IBM/client/IBMkrb5.so
%attr(755,root,root) %{_bindir}/db2cli
%attr(755,root,root) %{_bindir}/db2diag
%attr(755,root,root) %{_bindir}/db2drdat
%attr(755,root,root) %{_bindir}/db2dsdcfgfill
%attr(755,root,root) %{_bindir}/db2ldcfg
%attr(755,root,root) %{_bindir}/db2lddrg
%attr(755,root,root) %{_bindir}/db2level
%attr(755,root,root) %{_bindir}/db2support
%attr(755,root,root) %{_bindir}/db2trc
%attr(755,root,root) %{_libdir}/libDB2xml4c.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libDB2xml4c.so.58
%attr(755,root,root) %{_libdir}/libdb2.so.1
%attr(755,root,root) %{_libdir}/libdb2clixml4c.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/clidriver/include
%attr(755,root,root) %{_libdir}/clidriver/lib/libDB2xml4c.so
%attr(755,root,root) %{_libdir}/clidriver/lib/libdb2.so
%attr(755,root,root) %{_libdir}/clidriver/lib/libdb2clixml4c.so
%attr(755,root,root) %{_libdir}/libDB2xml4c.so
%attr(755,root,root) %{_libdir}/libdb2.so
%attr(755,root,root) %{_libdir}/libdb2clixml4c.so
