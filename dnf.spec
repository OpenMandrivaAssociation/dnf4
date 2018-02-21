# Warning: This package is synced from Mageia and Fedora!

%global hawkey_version 0.11.1
%global librepo_version 1.7.19
%global libcomps_version 0.1.8
%global rpm_version 4.13.0
%global min_plugins_core 2.1.3
%global min_plugins_extras 0.10.0

%global confdir %{_sysconfdir}/dnf

%global pluginconfpath %{confdir}/plugins
%global py2pluginpath %{python2_sitelib}/dnf-plugins
%global py3pluginpath %{python3_sitelib}/dnf-plugins

%bcond_without tests

Name:           dnf
Version:        2.7.5
Release:        1
Summary:        Package manager forked from Yum, using libsolv as a dependency resolver
Group:          System/Configuration/Packaging
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:        GPLv2+ and GPLv2 and GPL
URL:            https://github.com/rpm-software-management/dnf
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# Backports from upstream

# OpenMandriva specific patches
Patch1001:      dnf-2.7.5-Fix-detection-of-Python-2.patch

BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  python-bugzilla
BuildRequires:  python-sphinx
BuildRequires:  systemd-devel


Requires:   python3-dnf = %{version}-%{release}
Recommends: dnf-yum
Recommends: dnf-plugins-core
Conflicts:  dnf-plugins-core < %{min_plugins_core}
# dnf-langpacks is no longer supported
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
Provides:           dnf-command(autoremove)
Provides:           dnf-command(check-update)
Provides:           dnf-command(clean)
Provides:           dnf-command(distro-sync)
Provides:           dnf-command(downgrade)
Provides:           dnf-command(group)
Provides:           dnf-command(history)
Provides:           dnf-command(info)
Provides:           dnf-command(install)
Provides:           dnf-command(list)
Provides:           dnf-command(makecache)
Provides:           dnf-command(mark)
Provides:           dnf-command(provides)
Provides:           dnf-command(reinstall)
Provides:           dnf-command(remove)
Provides:           dnf-command(repolist)
Provides:           dnf-command(repoquery)
Provides:           dnf-command(repository-packages)
Provides:           dnf-command(search)
Provides:           dnf-command(updateinfo)
Provides:           dnf-command(upgrade)
Provides:           dnf-command(upgrade-to)
%description
Package manager forked from Yum, using libsolv as a dependency resolver.

%package conf
Summary:    Configuration files for DNF
Group:      System/Configuration/Packaging
# dnf-langpacks is no longer supported
Obsoletes:  dnf-langpacks-conf < %{dnf_langpacks_ver}

%description conf
Configuration files for DNF.

%package yum
Group:      System/Configuration/Packaging
Conflicts:  yum
Requires:   dnf = %{version}-%{release}
Summary:    As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF
%description yum
As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF.

%package -n python2-dnf
Summary:    Python 2 interface to DNF
Group:      System/Configuration/Packaging
Provides:   python-dnf = %{version}-%{release}
BuildRequires:  python2-devel
BuildRequires:  python2-gpg
BuildRequires:  python2-lzma
BuildRequires:  python2-hawkey >= %{hawkey_version}
BuildRequires:  python2-iniparse
BuildRequires:  python2-libcomps >= %{libcomps_version}
BuildRequires:  python2-librepo >= %{librepo_version}
BuildRequires:  python2-nose
BuildRequires:  python2-rpm >= %{rpm_version}
Recommends: bash-completion
Recommends: python-dbus
Recommends: rpm-plugin-systemd-inhibit
Requires:   dnf-conf = %{version}-%{release}
Requires:   mageia-dnf-conf
Requires:   deltarpm
Requires:   python2-gpg
Requires:   python2-lzma
Requires:   python2-hawkey >= %{hawkey_version}
Requires:   python2-iniparse
Requires:   python2-libcomps >= %{libcomps_version}
Requires:   python2-librepo >= %{librepo_version}
Requires:   python2-rpm >= %{rpm_version}
# DNF 2.0 doesn't work with old plugins
Conflicts:  python2-dnf-plugins-core < %{min_plugins_core}
Conflicts:  python2-dnf-plugins-extras-common < %{min_plugins_extras}

%description -n python2-dnf
Python 2 interface to DNF.

%package -n python-dnf
Summary:    Python 3 interface to DNF
Group:      System/Configuration/Packaging
BuildRequires:  python-devel
BuildRequires:  python-hawkey >= %{hawkey_version}
BuildRequires:  python-iniparse
BuildRequires:  python-libcomps >= %{libcomps_version}
BuildRequires:  python-librepo >= %{librepo_version}
BuildRequires:  python-nose
BuildRequires:  python-gpg
BuildRequires:  python-rpm >= %{rpm_version}
Recommends: bash-completion
Recommends: python-dbus
Recommends: rpm-plugin-systemd-inhibit
Requires:   dnf-conf = %{version}-%{release}
Requires:   deltarpm
Requires:   python-hawkey >= %{hawkey_version}
Requires:   python-iniparse
Requires:   python-libcomps >= %{libcomps_version}
Requires:   python-librepo >= %{librepo_version}
Requires:   python-gpg
Requires:   python-rpm >= %{rpm_version}
# DNF 2.0 doesn't work with old plugins
Conflicts:  python-dnf-plugins-core < %{min_plugins_core}
Conflicts:  python-dnf-plugins-extras-common < %{min_plugins_extras}

%description -n python3-dnf
Python 3 interface to DNF.

%package automatic
Summary:    Alternative CLI to "dnf upgrade" suitable for automatic, regular execution
Group:      System/Configuration/Packaging
BuildRequires:  systemd-devel
Requires:   dnf = %{version}-%{release}
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%description automatic
Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.

%prep
%autosetup -p1

mkdir py3

%build
%cmake -DPYTHON_DESIRED:str=2
%make_build
make doc-man

pushd ../py3
%cmake -DPYTHON_DESIRED:str=3 -DWITH_MAN=0 ../../
%make_build
popd

%install
pushd ./build
%make_install
popd
%find_lang %{name}

pushd ./py3/build
%make_install
popd

mkdir -p %{buildroot}%{pluginconfpath}
mkdir -p %{buildroot}%{py2pluginpath}
mkdir -p %{buildroot}%{py3pluginpath}
mkdir -p %{buildroot}%{_localstatedir}/log
mkdir -p %{buildroot}%{_var}/cache/dnf
touch %{buildroot}%{_localstatedir}/log/%{name}.log
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
rm %{buildroot}%{_bindir}/dnf-automatic-2
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/yum

%if %{with tests}
%check
pushd ./build
make ARGS="-V" test
popd

pushd ./py3/build
make ARGS="-V" test
popd
%endif

%files -f %{name}.lang
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/dnf
%{_mandir}/man8/dnf.8.*
%{_mandir}/man8/yum2dnf.8.*
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
%{_sysconfdir}/bash_completion.d/dnf
%{_mandir}/man5/dnf.conf.5.*
%{_tmpfilesdir}/dnf.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf

%files yum
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/yum
%{_mandir}/man8/yum.8.*

%files -n python2-dnf
%license COPYING PACKAGE-LICENSING
%{_bindir}/dnf-2
%doc AUTHORS README.rst
%exclude %{python2_sitelib}/dnf/automatic
%{python2_sitelib}/dnf/
%dir %{py2pluginpath}

%files -n python3-dnf
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

