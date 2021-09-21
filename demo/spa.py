from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


class SinglePageApp:

    def __init__(self, app, navitems=None):
        self.navitems = navitems
        self.app = app
        self.app.layout = self.pageLayout()


    def run_server(self, debug=True, threaded=True):
        #self.app.run_server(debug=debug)
        self.app.run_server(debug=debug, host="0.0.0.0", threaded=threaded, dev_tools_serve_dev_bundles=True)


    def pageLayout(self):

        @self.app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
        def _display_page(pathname):
            return self.display_page(pathname)

        layout = html.Div([
            dcc.Location(id='url', refresh=False),
            self.navBar(),
            html.Br(),
            html.Div([
                html.Div([
                    html.Div([], className="col-md-2"),
                    html.Div(id='page-content', className="col-md-8"),
                    html.Div([], className="col-md-2")
                ], className='row')
            ], className="container-fluid"),
            html.Div(id='null')
        ])
        return layout


    def display_page(self, pathname):
        for page in self.navitems['left'] + self.navitems['right']:
            if page['href'] == pathname:
                return page['layout']
        return self.show404(str(pathname)) 


    def show404(self, url):
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H1('Oops!'),
                        html.H2('404 Not Found'),
                        html.Div('Sorry, an error has occurred, Requested page not found!', className='error-details'),
                        html.Div([

                            dcc.Link([
                                html.Span(className='fa fa-home'),
                                ' Take Me Home'
                            ], href='/', className='btn btn-secondary btn-lg'),

                            dcc.Link([
                                html.Span(className='fa fa-envelope'),
                                ' Contact Support'
                            ], href='/support', className='btn btn-secondary btn-lg'),



                        ], className='error-actions')
                    ], className='error-template')
                ], className='col-md-12')
            ], className='row')
        ], className='container')



    def getItems(self, items):

        def item(item):
            if 'icon' in item:
                return dbc.NavItem([
                    dbc.NavLink([html.I(className=item['icon']), ' ' + item['title']], href=item["href"])
                ])
            else:
                return dbc.NavItem(dbc.NavLink(item['title'], href=item["href"]))

        return dbc.Nav([
            item(x) for x in items
        ])

    def getItemsLeft(self):   
        return self.getItems(self.navitems['left'])    

    def getItemsRight(self):   
        return self.getItems(self.navitems['right'])    

    def navBar(self):
        navbar = dbc.Navbar(
            children=[
                dbc.NavbarBrand(html.Strong('Datatables'), href="https://datatables.net/"),

                # Left hand side
             
                dbc.NavItem(self.getItemsLeft(), className='navbar-nav mr-auto'),

                # Right hand side

                dbc.NavItem(self.getItemsRight(), className='navbar-nav ml-auto')


            ], className="navbar-default",  dark=True, color='secondary',  expand="md" )

        return navbar
