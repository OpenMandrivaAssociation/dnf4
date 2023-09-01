# Warning: This package is synced from Mageia and Fedora!

%define hawkey_version 0.71.0
%define libcomps_version 0.1.8
%define libmodulemd_version 2.9.3
%define rpm_version 4.18.0
%define min_plugins_core 4.0.26
%define min_plugins_extras 4.0.4

%define confdir %{_sysconfdir}/dnf
%define pluginconfpath %{confdir}/plugins
%define py3pluginpath %{python3_sitelib}/dnf-plugins

# (tpg) dnf5 is not yet ready to replace dnf
%bcond_with dnf5_default

Summary:	Package manager
Name:		dnf
Version:	4.17.0
Release:	1
Group:		System/Configuration/Packaging
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:	GPLv2+ and GPLv2 and GPL
URL:		https://github.com/rpm-software-management/dnf
Source0:	https://github.com/rpm-software-management/dnf/archive/%{version}/%{name}-%{version}.tar.gz

# Backports from upstream
Patch0:		https://github.com/rpm-software-management/dnf/commit/33fde245b0a49eb02837b6fedb2d14ed92c2d99f.patch

# Suitable for upstreaming
# Teach dnf about znver1 and znver1_32 sub-arches
Patch500:	dnf-3.0.2-znver1.patch

# OpenMandriva specific patches
Patch1002:	dnf-2.7.5-Allow-overriding-SYSTEMD_DIR-for-split-usr.patch
Patch1003:	dnf-4.1.0-sphinx-build.patch

# The makecache timer disables itself whenever it is run in a live environment.
# However, the upstream version of the unit only knows about the upstream dracut
# live environment module. Since we currently use a custom one in Mageia,
# we need to detect it and properly disable the timer. (ngompa)
Patch1100:	1001-Disable-the-dnf-makecache-timer-for-Mageia-live-envi.patch

BuildArch:	noarch
BuildRequires:	cmake
BuildRequires:	gettext
BuildRequires:	python-bugzilla
BuildRequires:	python-sphinx
BuildRequires:	systemd-rpm-macros

BuildRequires:	pkgconfig(bash-completion)
Requires:	python-%{name} = %{EVRD}
Recommends:	(python-dbus if networkmanager)
Conflicts:	python-dnf-plugins-core < %{min_plugins_core}
Conflicts:	python-dnf-plugins-extras-common < %{min_plugins_extras}

%description
Utility that allows users to manage packages on their systems.
It supports RPMs, modules and comps groups & environments.

%package data
Summary:	Common data and configuration files for DNF
Group:		System/Configuration/Packaging
Requires:	libreport-filesystem
Obsoletes:	%{name}-conf <= %{EVRD}
Provides:	%{name}-conf = %{EVRD}
%if %{with dnf5_default}
Requires:	%{_lib}dnf1 >= 5
%endif

%description data
Common data and configuration files for DNF.

%package yum
Summary:	As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF
Group:		System/Configuration/Packaging
Conflicts:	yum
Requires:	dnf = %{EVRD}

%description yum
As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF.

%package -n python-%{name}
Summary:	Python 3 interface to DNF
Group:		System/Configuration/Packaging
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-hawkey >= %{hawkey_version}
BuildRequires:	python-libdnf >= %{hawkey_version}
BuildRequires:	python-libcomps >= %{libcomps_version}
BuildRequires:	python-libdnf
BuildRequires:	pkgconfig(modulemd-2.0) >= %{libmodulemd_version}
Requires:	%{_lib}modulemd2 >= %{libmodulemd_version}
Requires:	dnf-data = %{EVRD}
Recommends:	deltarpm
Requires:	python-hawkey >= %{hawkey_version}
Requires:	python-libdnf >= %{hawkey_version}
Requires:	python-libcomps >= %{libcomps_version}
Requires:	python-libdnf
BuildRequires:	python-rpm >= %{rpm_version}
Requires:	python-rpm >= %{rpm_version}
Recommends:	(rpm-plugin-systemd-inhibit if systemd)
Provides:	dnf-command(alias)
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

%description -n python-%{name}
Python 3 interface to DNF.

%package automatic
Summary:	Alternative CLI to "dnf upgrade" suitable for automatic, regular execution
Group:		System/Configuration/Packaging
Requires:	python-dnf = %{EVRD}
%{?systemd_requires}

%description automatic
Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.

%prep
%autosetup -p1

%build
%cmake \
	-DPYTHON_DESIRED:FILEPATH="%{__python3}" \
	-DSYSTEMD_DIR:str="%{_unitdir}"

%make_build
make doc-man

%install
%make_install -C build

%find_lang %{name}

mkdir -p %{buildroot}%{confdir}/vars
mkdir -p %{buildroot}%{confdir}/aliases.d
mkdir -p %{buildroot}%{pluginconfpath}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/modules.d
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/modules.defaults.d
mkdir -p %{buildroot}%{py3pluginpath}/__pycache__/
mkdir -p %{buildroot}%{_localstatedir}/log
mkdir -p %{buildroot}%{_var}/cache/dnf
touch %{buildroot}%{_localstatedir}/log/%{name}.log
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
rm -vf %{buildroot}%{_bindir}/dnf-automatic-*
ln -sr %{buildroot}%{_bindir}/dnf %{buildroot}%{_bindir}/yum
rm -vf %{buildroot}%{confdir}/%{name}-strict.conf

# Ensure code is byte compiled
%py_compile %{buildroot}

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}-automatic.preset << EOF
enable %{name}-automatic.timer
enable %{name}-automatic-notifyonly.timer
enable %{name}-automatic-download.timer
disable %{name}-automatic-install.timer
EOF

%if %{with dnf5_default}
rm %{buildroot}%{confdir}/%{name}.conf
%else
# Set releasever
if ! grep -q releasever %{buildroot}%{confdir}/%{name}.conf; then
    . %{_sysconfdir}/os-release
    echo "releasever=$VERSION_ID" >>%{buildroot}%{confdir}/%{name}.conf
fi
%endif

%check
#make ARGS="-V" test -C build

%post
%systemd_post dnf-makecache.timer

%preun
%systemd_preun dnf-makecache.timer

%postun
%systemd_postun_with_restart dnf-makecache.timer

%post automatic
%systemd_post dnf-automatic.timer dnf-automatic-notifyonly.timer dnf-automatic-download.timer dnf-automatic-install.timer

%preun automatic
%systemd_preun dnf-automatic.timer dnf-automatic-notifyonly.timer dnf-automatic-download.timer dnf-automatic-install.timer

%postun automatic
%systemd_postun_with_restart dnf-automatic.timer dnf-automatic-notifyonly.timer dnf-automatic-download.timer dnf-automatic-install.timer

%files -f %{name}.lang
%{_bindir}/dnf
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%doc %{_mandir}/man8/dnf.8*
%doc %{_mandir}/man8/yum2dnf.8*
%doc %{_mandir}/man7/dnf.modularity.7*
%doc %{_mandir}/man5/dnf-transaction-json.5.*
%{_unitdir}/dnf-makecache.service
%{_unitdir}/dnf-makecache.timer
%{_var}/cache/dnf

%files data
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%dir %{confdir}
%dir %{confdir}/modules.d
%dir %{confdir}/modules.defaults.d
%dir %{pluginconfpath}
%if %{without dnf5_default}
%dir %{confdir}/protected.d
%dir %{confdir}/vars
%endif
%dir %{confdir}/aliases.d
%config(noreplace) %{confdir}/aliases.d/zypper.conf
%if %{without dnf5_default}
%config(noreplace) %{confdir}/%{name}.conf
%endif
# No longer using `noreplace` here. Older versions of DNF 4 marked `dnf` as a
# protected package, but since Fedora 39, DNF needs to be able to update itself
# to DNF 5, so we need to replace the old /etc/dnf/protected.d/dnf.conf.
%config %{confdir}/protected.d/%{name}.conf
# Protect python3-dnf instead, which does not conflict with DNF 5
%config(noreplace) %{confdir}/protected.d/python3-%{name}.conf
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
%doc %{_mandir}/man5/dnf.conf.5.*
%{_tmpfilesdir}/dnf.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf

%files yum
# No longer using `noreplace` here. Older versions of DNF 4 marked `yum` as a
# protected package, but since Fedora 39, DNF needs to be able to update itself
# to DNF 5, so we need to replace the old /etc/dnf/protected.d/yum.conf.
%config %{confdir}/protected.d/yum.conf
%{_bindir}/yum
%doc %{_mandir}/man1/yum-aliases.1*
%doc %{_mandir}/man5/yum.conf.5*
%doc %{_mandir}/man8/yum.8.*
%doc %{_mandir}/man8/yum-shell.8*

%files -n python-dnf
%{_bindir}/dnf-3
%exclude %{python3_sitelib}/dnf/automatic
%{python3_sitelib}/dnf/
%dir %{py3pluginpath}
%dir %{py3pluginpath}/__pycache__

%files automatic
%{_bindir}/%{name}-automatic
%config(noreplace) %{confdir}/automatic.conf
%{_presetdir}/86-%{name}-automatic.preset
%{_unitdir}/%{name}-automatic.service
%{_unitdir}/%{name}-automatic.timer
%{_unitdir}/%{name}-automatic-notifyonly.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-download.service
%{_unitdir}/%{name}-automatic-download.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-install.timer
%{python3_sitelib}/%{name}/automatic
%doc %{_mandir}/man8/dnf-automatic.8*
