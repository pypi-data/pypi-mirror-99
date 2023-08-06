# Copyright (c) 2017 Orange.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from bgpvpn_dashboard.dashboards.project.bgpvpn.network_associations \
    import tabs as network_tabs
from bgpvpn_dashboard.dashboards.project.bgpvpn.router_associations \
    import tabs as router_tabs
from bgpvpn_dashboard.dashboards.project.bgpvpn import tabs as project_tabs


class OverviewTab(project_tabs.OverviewTab):
    template_name = "admin/bgpvpn/_detail_overview.html"


class BgpvpnDetailsTabs(project_tabs.BgpvpnDetailsTabs):
    tabs = (OverviewTab,
            network_tabs.NetworkAssociationsTab,
            router_tabs.RouterAssociationsTab)
