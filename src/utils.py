import yaml


SERVICES = ['confluence', 'github']
def get_credentials(service):
    """
    Get specified credentials in .credentials file for a service
    :param service:
    :return:
    """
    assert service in SERVICES, print('must be valid servie')
    CREDENTIALS = yaml.load(open('src/.credentials.yml').read())
    return {'user': CREDENTIALS[service]['user'],
            'password': CREDENTIALS[service]['password'],
            'domain':CREDENTIALS[service]['domain']}
