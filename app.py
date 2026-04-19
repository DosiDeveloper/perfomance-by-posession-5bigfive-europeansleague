import os
import dash
from dotenv import load_dotenv
from dash import Dash, Input, Output, State, callback
import dash_mantine_components as dmc

from src.config import config_default

load_dotenv()
app = Dash(
    pages_folder=str(config_default.dash_pages.absolute()),
    use_pages=True
)

app.layout = dmc.MantineProvider(
    dmc.AppShell(
        [
            dmc.AppShellHeader(
                dmc.Group(
                    [
                        dmc.Burger(id="burger", size="sm",
                                   hiddenFrom="sm", opened=False),
                        dmc.Title("Soccer Analytic", c="blue"),
                    ],
                    h="100%",
                    px="md",
                )
            ),
            dmc.AppShellNavbar(
                id="navbar",
                children=[
                    "Navbar",
                    *[dmc.Skeleton(height=28, mt="sm", animate=False)
                      for _ in range(15)],
                ],
                p="md",
            ),
            dmc.AppShellMain(dash.page_container),
        ],
        header={"height": 60},
        padding="md",
        navbar={
                "width": 300,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
        },
        id="appshell",
    )
)
    

@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar

if __name__ == "__main__":
    if bool(os.getenv("DEV_MODE")) == True:
        print("Running in development mode with hot reload enabled.")
        app.run(debug=True, dev_tools_hot_reload=True)
    else:
        app.run()
