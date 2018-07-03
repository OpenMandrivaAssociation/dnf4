# (ngompa) disable rpmlint to avoid terrible cyclic dependency problem in rpm5->rpm4 + python2->python3 transition
# remove after rpm5->rpm4 transition is complete
%undefine _build_pkgcheck_set
%undefine _build_pkgcheck_srpm
%undefine _nonzero_exit_pkgcheck_terminate_build
###

# Warning: This package is synced from Mageia and Fedora!

%define hawkey_version 0.11.1
%define librepo_version 1.7.19
%define libcomps_version 0.1.8
%define rpm_version 4.13.0
%define min_plugins_core 2.1.3
%define min_plugins_extras 0.10.0

%define confdir %{_sysconfdir}/dnf

%define pluginconfpath %{confdir}/plugins
%define py3pluginpath %{python3_sitelib}/dnf-plugins

# (tpg) enable when rpm4 migration is done
%bcond_with tests

Summary:	Package manager forked from Yum, using libsolv as a dependency resolver
Name:		dnf
Version:	3.0.2
Release:	6
Group:		System/Configuration/Packaging
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:	GPLv2+ and GPLv2 and GPL
URL:		https://github.com/rpm-software-management/dnf
Source0:	https://github.com/rpm-software-management/dnf/archive/%{version}.tar.gz

# Backports from upstream

# Suitable for upstreaming
# Teach dnf about znver1 and znver1_32 sub-arches
Patch500:	dnf-3.0.2-znver1.patch
# Shut up about collections.Sequence (should be collections.abc.Sequence)
Patch501:	dnf-3.0.2-python-3.8.patch

# OpenMandriva specific patches
Patch1001:	dnf-2.7.5-Fix-detection-of-Python-2.patch
Patch1002:	dnf-2.7.5-Allow-overriding-SYSTEMD_DIR-for-split-usr.patch

BuildArch:	noarch
BuildRequires:	cmake
BuildRequires:	gettext
BuildRequires:	python-bugzilla
BuildRequires:	python-sphinx
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd
Requires:	python-dnf = %{version}-%{release}
Requires:	python-libdnf
Requires:	python-smartcols
Requires:	python-gi
Requires:	typelib(Modulemd)
Requires:	%{_lib}glib-gir2.0
Requires:	gobject-introspection
Recommends:	dnf-yum
Recommends:	dnf-plugins-core
Conflicts:	dnf-plugins-core < %{min_plugins_core}
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Provides:	dnf-command(autoremove)
Provides:	dnf-command(check-update)
Provides:	dnf-command(clean)
Provides:	dnf-command(distro-sync)
Provides:	dnf-command(downgrade)
Provides:	dnf-command(group)
Provides:	dnf-command(history)
Provides:	dnf-command(info)
Provides:	dnf-command(install)
Provides:	dnf-command(list)
Provides:	dnf-command(makecache)
Provides:	dnf-command(mark)
Provides:	dnf-command(provides)
Provides:	dnf-command(reinstall)
Provides:	dnf-command(remove)
Provides:	dnf-command(repolist)
Provides:	dnf-command(repoquery)
Provides:	dnf-command(repository-packages)
Provides:	dnf-command(search)
Provides:	dnf-command(updateinfo)
Provides:	dnf-command(upgrade)
Provides:	dnf-command(upgrade-to)

%description
Package manager forked from Yum, using libsolv as a dependency resolver.

%package conf
Summary:	Configuration files for DNF
Group:		System/Configuration/Packaging

%description conf
Configuration files for DNF.

%package yum
Summary:	As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF
Group:		System/Configuration/Packaging
Conflicts:	yum
Requires:	dnf = %{version}-%{release}

%description yum
As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF.

%package -n python-dnf
Summary:	Python 3 interface to DNF
Group:		System/Configuration/Packaging
BuildRequires:	pkgconfig(python)
BuildRequires:	python-hawkey >= %{hawkey_version}
BuildRequires:	python-iniparse
BuildRequires:	python-libcomps >= %{libcomps_version}
BuildRequires:	python-librepo >= %{librepo_version}
BuildRequires:	python-nose
BuildRequires:	python-gpg
BuildRequires:	python-rpm >= %{rpm_version}
BuildRequires:	pkgconfig(bash-completion)
Recommends:	bash-completion
Recommends:	python-dbus
Recommends:	rpm-plugin-systemd-inhibit
Requires:	dnf-conf = %{version}-%{release}
Requires:	deltarpm
Requires:	python-hawkey >= %{hawkey_version}
Requires:	python-iniparse
Requires:	python-libcomps >= %{libcomps_version}
Requires:	python-librepo >= %{librepo_version}
Requires:	python-gpg
Requires:	python-rpm >= %{rpm_version}
# DNF 2.0 doesn't work with old plugins
Conflicts:	python-dnf-plugins-core < %{min_plugins_core}
Conflicts:	python-dnf-plugins-extras-common < %{min_plugins_extras}

%description -n python-dnf
Python 3 interface to DNF.

%package automatic
Summary:	Alternative CLI to "dnf upgrade" suitable for automatic, regular execution
Group:		System/Configuration/Packaging
BuildRequires:	pkgconfig(libsystemd)
Requires:	dnf = %{version}-%{release}
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description automatic
Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.

%prep
%autosetup -p1

%build
%cmake -DPYTHON_DESIRED:str=3 -DSYSTEMD_DIR:str="%{_systemunitdir}"
%make_build
make doc-man

%install
%make_install -C build

%find_lang %{name}

mkdir -p %{buildroot}%{pluginconfpath}
mkdir -p %{buildroot}%{py3pluginpath}
mkdir -p %{buildroot}%{_localstatedir}/log
mkdir -p %{buildroot}%{_var}/cache/dnf
touch %{buildroot}%{_localstatedir}/log/%{name}.log
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
ln -sr %{buildroot}%{_bindir}/dnf %{buildroot}%{_bindir}/yum

# Ensure code is byte compiled
%py_compile %{buildroot}

%if %{with tests}
%check
make ARGS="-V" test -C build
%endif

%files -f %{name}.lang
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/dnf
%{_mandir}/man5/yum.conf.5*
%{_mandir}/man8/dnf.8*
%{_mandir}/man8/yum2dnf.8*
%{_unitdir}/dnf-makecache.service
%{_unitdir}/dnf-makecache.timer
%{_var}/cache/dnf

%files conf
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%dir %{confdir}
%dir %{pluginconfpath}
%dir %{confdir}/protected.d
%config(noreplace) %{confdir}/%{name}.conf
%config(noreplace) %{confdir}/protected.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%ghost %{_localstatedir}/log/hawkey.log
%ghost %{_localstatedir}/log/%{name}.log
%ghost %{_localstatedir}/log/%{name}.librepo.log
%ghost %{_localstatedir}/log/%{name}.rpm.log
%ghost %{_localstatedir}/log/%{name}.plugin.log
%ghost %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/groups.json
%ghost %{_sharedstatedir}/%{name}/yumdb
%ghost %{_sharedstatedir}/%{name}/history
%{_datadir}/bash-completion/completions/dnf
%{_mandir}/man5/dnf.conf.5.*
%{_tmpfilesdir}/dnf.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf

%files yum
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/yum
%{_mandir}/man8/yum.8.*

%files -n python-dnf
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/dnf-3
%exclude %{python3_sitelib}/dnf/automatic
%{python3_sitelib}/dnf/
%dir %{py3pluginpath}

%files automatic
%license COPYING PACKAGE-LICENSING
%doc AUTHORS
%{_bindir}/%{name}-automatic
%config(noreplace) %{confdir}/automatic.conf
%{_mandir}/man8/%{name}.automatic.8.*
%{_unitdir}/%{name}-automatic.service
%{_unitdir}/%{name}-automatic.timer
%{_unitdir}/%{name}-automatic-notifyonly.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-download.service
%{_unitdir}/%{name}-automatic-download.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-install.timer
%{python3_sitelib}/%{name}/automatic

%post
%systemd_post %{name}-makecache.timer

%preun
%systemd_preun %{name}-makecache.timer

%postun
%systemd_postun_with_restart %{name}-makecache.timer

%post automatic
%systemd_post %{name}-automatic.timer
%systemd_post %{name}-automatic-notifyonly.timer
%systemd_post %{name}-automatic-download.timer
%systemd_post %{name}-automatic-install.timer

%preun automatic
%systemd_preun %{name}-automatic.timer
%systemd_preun %{name}-automatic-notifyonly.timer
%systemd_preun %{name}-automatic-download.timer
%systemd_preun %{name}-automatic-install.timer

%postun automatic
%systemd_postun_with_restart %{name}-automatic.timer
%systemd_postun_with_restart %{name}-automatic-notifyonly.timer
%systemd_postun_with_restart %{name}-automatic-download.timer
%systemd_postun_with_restart %{name}-automatic-install.timer
