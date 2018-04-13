from dnn.const.net import PORT


def build_url_from_ip(ip):
    return 'http://' + ip + ':' + PORT


def build_text_url_from_url(url):
    return url + '/text'


def build_text_url_from_ip(ip):
    return build_url_from_ip(ip) + '/text'
