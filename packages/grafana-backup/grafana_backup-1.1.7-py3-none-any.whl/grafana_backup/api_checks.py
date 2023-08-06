from grafana_backup.commons import print_horizontal_line
from grafana_backup.dashboardApi import health_check, auth_check, uid_feature_check, paging_feature_check


def main(settings):
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    (status, json_resp) = health_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if not status == 200:
        return (status, json_resp, None, None)

    (status, json_resp) = auth_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if not status == 200:
        return (status, json_resp, None, None)

    uid_support = uid_feature_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if isinstance(uid_support, str):
        raise Exception(uid_support)

    paging_support = paging_feature_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if isinstance(paging_support, str):
        raise Exception(paging_support)

    print_horizontal_line()

    return (status, json_resp, uid_support, paging_support)
