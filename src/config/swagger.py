
# Swagger template and configuration setup

template = {
    'swagger': '2.0',
    'info': {
        'title': 'Yakitabu backend',
        'description': 'Yakitabu Book P2P Book Loan API',
        'contact': {
            'responsibleOrganization': '',
            'responsibleDeveloper': '',
            'email': 'yakitabu.io@yakitabu.com',
            'url': 'https://yakitabu-backend.herokuapp.com/',
        },
        'termsOfService': 'www.yakitabu.com/terms',
        'version': '1.0'
    },
    'basePath': '/api',  # base path for blueprint registration
    'schemes': [
        'http',
        'https'
    ]
}

swagger_config = {
    'headers': [
    ],
    'specs': [
        {
            'endpoint': 'apispec',
            'route': '/apispec.json',
            'rule_filter': lambda rule: True,  # all in
            'model_filter': lambda tag: True,  # all in
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/'
}
