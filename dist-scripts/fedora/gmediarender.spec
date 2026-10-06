Name:           gmediarender
Version:        0.3.2
Release:        1%{?dist}
Summary:        Resource efficient UPnP/DLNA renderer

License:        GPL-2.0-or-later
URL:            https://github.com/oopen/gmrender-resurrect
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  glib2-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  libupnp-devel
BuildRequires:  systemd-rpm-macros

Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       libupnp
Requires(pre):  shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
GMediaRender is a resource efficient UPnP/DLNA renderer.
It is controlled by a UPnP/DLNA control point and plays the media through
GStreamer.

%prep
%setup -q

%build
%configure
%make_build

%pre
getent group gmediarender >/dev/null || groupadd -r gmediarender
getent passwd gmediarender >/dev/null || \
    useradd -r -g gmediarender -G audio -M -d /usr/share/gmediarender -s /sbin/nologin \
    -c "GMediaRender DLNA/UPnP Renderer" gmediarender
exit 0

%install
%make_install
install -d %{buildroot}%{_unitdir}
install -m 0644 dist-scripts/fedora/%{name}.service %{buildroot}%{_unitdir}/
install -d %{buildroot}%{_prefix}/lib/firewalld/services
install -m 0644 dist-scripts/fedora/%{name}.xml %{buildroot}%{_prefix}/lib/firewalld/services/
install -m 0644 dist-scripts/fedora/ssdp.xml %{buildroot}%{_prefix}/lib/firewalld/services/

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
getent passwd gmediarender >/dev/null && userdel gmediarender
getent group gmediarender >/dev/null && groupdel gmediarender
%systemd_postun_with_restart %{name}.service

%files
%license COPYING
%doc README.md NEWS
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_prefix}/lib/firewalld/services/ssdp.xml
%{_datadir}/%{name}/

%changelog
* Tue Oct 06 2026 oopen <oopen@users.noreply.github.com> - 0.3.2-1
- Update to 0.3.2: GStreamer 1.x and libupnp 1.8+, systemd unit.
* Sun Mar 29 2015 <admin@vortexbox.org>
- Updated for systemd snippets, added automatic system user/group add and removal upon installation, added FirewallD support
* Mon Sep 16 2013 <admin@vortexbox.org>
- Initial release
