from jadi import service
import aj


@service
class ClientCertificateVerificator():
    def __init__(self, context):
        self.context = context

    def verify(self, x509):
        serial = x509.get_serial_number()
        digest = x509.digest('sha1')
        # logging.debug('SSL verify: %s / %s' % (x509.get_subject(), digest))
        for c in aj.config.data['ssl']['client_auth']['certificates']:
            if int(c['serial']) == serial and c['digest'].encode('utf-8') == digest:
                return c['user']
