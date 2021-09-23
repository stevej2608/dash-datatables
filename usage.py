import logging
from demo import SinglePageApp
from demo import employees, solar, editable

from app import app

NAV_BAR_ITEMS = {
    'left' : [
        {'title' : 'Solar', 'href' : '/solar', 'layout': solar.layout },
        {'title' : 'Employees', 'href' : '/employees', 'layout': employees.layout},
        {'title' : 'Editable', 'href' : '/editable', 'layout': editable.layout},
    ],
    'right': [
    ]
}


spa = SinglePageApp(app, navitems=NAV_BAR_ITEMS)

if __name__ == '__main__':

    # Turn off werkzeug  logging as it's very noisy

    aps_log = logging.getLogger('werkzeug')
    aps_log.setLevel(logging.ERROR)

    logging.basicConfig(
        level=logging.INFO,
        # format='%(name)s %(levelname)s %(asctime)s.%(msecs)03d %(module)10s/%(lineno)-5d %(message)s'
        format='%(levelname)s %(asctime)s.%(msecs)03d %(module)10s/%(lineno)-5d %(message)s'
    )

    print('\nvisit http://default:8050/solar\n')

    spa.run_server(debug=False, threaded=False)
