# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'BGPVPN Interconnections'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'project'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'network'

# Python panel class of the PANEL to be added.
ADD_PANEL = ('bgpvpn_dashboard.'
             'dashboards.project.bgpvpn.panel.BGPVPNInterconnections')
