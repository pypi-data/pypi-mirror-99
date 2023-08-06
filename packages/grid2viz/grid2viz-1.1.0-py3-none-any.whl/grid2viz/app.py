# Copyright (C) 2021, RTE (http://www.rte-france.com/)
# See AUTHORS.txt
# SPDX-License-Identifier: MPL-2.0

"""
This file handles the html entry point of the application through dash components.
It will generate the layout of a given page and handle the routing
"""

import dash_bootstrap_components as dbc
from dash import Dash

# We need to create app before importing the rest of the project as it uses @app decorators
font_awesome = [
    {
        "href": "https://use.fontawesome.com/releases/v5.8.1/css/all.css",
        "rel": "stylesheet",
        "integrity": "sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf",
        "crossorigin": "anonymous",
    }
]
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, *font_awesome])

"""
Get Imports to create layout and callbacks 
"""
from grid2viz.main_callbacks import register_callbacks_main
from grid2viz.layout import make_layout as layout

from grid2viz.src.episodes.episodes_clbk import register_callbacks_episodes
from grid2viz.src.overview.overview_clbk import (
    register_callbacks_overview,
)  # as overview_clbk
from grid2viz.src.macro.macro_clbk import register_callbacks_macro  # as macro_clbk
from grid2viz.src.micro.micro_clbk import register_callbacks_micro  # as micro_clbk
from grid2viz.src.simulation.simulation_clbk import register_callbacks_simulation

"""
End Warning
"""

app.config.suppress_callback_exceptions = True

app.title = "Grid2Viz"
app.server.secret_key = "Grid2Viz"

##create layout
layout(app)

##create callbaks
register_callbacks_main(app)
register_callbacks_episodes(app)
register_callbacks_overview(app)
register_callbacks_macro(app)
register_callbacks_micro(app)
register_callbacks_simulation(app)


def app_run(port=8050, debug=False):
    app.run_server(port=port, debug=debug)


if __name__ == "__main__":
    app_run()
