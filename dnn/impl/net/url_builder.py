from dnn.const.net import PORT, EDGE_IP


def build_url_from_ip(ip):
    return 'http://' + ip + ':' + PORT


def build_text_url_from_url(url):
    return url + '/text'


def build_image_url_from_url(url):
    return url + '/img'


def build_text_url_from_ip(ip):
    return build_url_from_ip(ip) + '/text'


def build_edge_url():
    return build_url_from_ip(EDGE_IP)


def build_edge_image_url():
    return build_image_url_from_url(build_edge_url())
