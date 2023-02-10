initial1 = [
    ('GET', '/api/v1/cluster/metrics'),
    ('POST', '/api/v1/cluster/{cluster}/plugins'),
    ('POST', '/api/v1/cluster/{cluster}/plugins/{plugin}')
]

expectted1 = {
    'cluster': {
        'plugins': 'POST',
        'metrics': 'GET'
    }
}


initial2 = [
    ("POST", "/api/v1/cluster/{cluster}/plugins/first/asecond"),
    ("GET", "/api/v1/cluster/freenodes/list"),
    ("GET", "/api/v1/cluster/nodes/supernode/wow"),
    ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
    ("POST", "/api/v1/cluster/{cluster}/plugins"),
    ("POST", "/api/v1/xluster/{cluster}/plugins"),
    ("POST", "/api/v1/cluster/{cluster}/plugins/first"),
    ("GET", "/api/v1/cluster/anodes/supernode/a/wow"),
]

expectted2 = {
    'cluster': {
        'anodes': {
            'supernode': {
                'a': {
                    'wow': 'GET'
                }
            }
        },
        'freenodes': {
            'list': 'GET'
        },
        'nodes': {
            'supernode': {
                'wow': 'GET'
            }
        },
        'plugins': {
            'first': {
                'asecond': 'POST'
            }
        }
    },
    'xluster': {
        'plugins': 'POST'
    }
}