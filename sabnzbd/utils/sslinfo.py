# v23 indicates "negotiate highest possible"
_ALL_PROTOCOLS = ('v23', 't12', 't11', 't1', 'v3', 'v2')
_SSL_PROTOCOLS = {}
_SSL_PROTOCOLS_LABELS = []

def ssl_potential():
    ''' Return a list of potentially supported SSL protocols'''
    try:
        import ssl
    except ImportError:
        return []
    return [p[9:] for p in dir(ssl) if p.startswith('PROTOCOL_')]

try:
    from OpenSSL import SSL

    _potential = ssl_potential()
    try:
        if 'SSLv23' in _potential:
            _SSL_PROTOCOLS['v23'] = SSL.SSLv23_METHOD
    except AttributeError:
        pass
    try:
        if 'TLSv1_2' in _potential:
            _SSL_PROTOCOLS['t12'] = SSL.TLSv1_2_METHOD
            _SSL_PROTOCOLS_LABELS.append('TLS v1.2')
    except AttributeError:
        pass
    try:
        if 'TLSv1_1' in _potential:
            _SSL_PROTOCOLS['t11'] = SSL.TLSv1_1_METHOD
            _SSL_PROTOCOLS_LABELS.append('TLS v1.1')
    except AttributeError:
        pass
    try:
        if 'TLSv1' in _potential:
            _SSL_PROTOCOLS['t1'] = SSL.TLSv1_METHOD
            _SSL_PROTOCOLS_LABELS.append('TLS v1')
    except AttributeError:
        pass
    try:
        if 'SSLv3' in _potential:
            _SSL_PROTOCOLS['v3'] = SSL.SSLv3_METHOD
            _SSL_PROTOCOLS_LABELS.append('SSL v3')
    except AttributeError:
        pass
    try:
        if 'SSLv2' in _potential:
            _SSL_PROTOCOLS['v2'] = SSL.SSLv2_METHOD
            _SSL_PROTOCOLS_LABELS.append('SSL v2')
    except AttributeError:
        pass
except ImportError:
    SSL = None


def ssl_method(method):
    ''' Translate SSL acronym to a method value '''
    if method in _SSL_PROTOCOLS:
        return _SSL_PROTOCOLS[method]
    else:
        # The default is "negotiate a protocol"
        try:
            return SSL.SSLv23_METHOD
        except AttributeError:
            return _SSL_PROTOCOLS[0]


def ssl_protocols():
    ''' Return acronyms for SSL protocols, highest quality first '''
    return [p for p in _ALL_PROTOCOLS if p in _SSL_PROTOCOLS]


def ssl_protocols_labels():
    ''' Return human readable labels for SSL protocols, highest quality first '''
    return _SSL_PROTOCOLS_LABELS


def ssl_version():
    if SSL:
        try:
            return SSL.SSLeay_version(SSL.SSLEAY_VERSION)
        except AttributeError:
            try:
                import ssl
                return ssl.OPENSSL_VERSION
            except (ImportError, AttributeError):
                return 'No OpenSSL installed'
    else:
        return None


def pyopenssl_version():
    if SSL:
        try:
            import OpenSSL
            return OpenSSL.__version__
        except ImportError:
            return 'No pyOpenSSL installed'
    else:
        return None

if __name__ == '__main__':

    print 'SSL version: %s' % ssl_version()
    print 'pyOpenSSL version: %s' % pyopenssl_version()
    print 'Potentials: %s' % ssl_potential()
    print 'Actuals: %s' % ssl_protocols()
