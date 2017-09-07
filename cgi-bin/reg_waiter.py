#!/usr/bin/env python3

import urllib3
import requests
import xml.etree.ElementTree as ET

print("Content-type: text/html;charset=utf8\r\n\r\n")
print("<html>")
#print("<head>Something</head>")
print("<body>")
def reg_waiter(i, p, user_name, pass_word):

    session = requests.session()

    result = ""

    ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
    # Регистрируем пользователя
    xml_register_waiter_string = '<RK7Query><RK7CMD CMD="RegisterEmployee"> <Waiter code = "9999"/><Station code = "1"/></RK7CMD></RK7Query>'
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    xml_unicode_register_waiter_string = xml_register_waiter_string.encode('utf-8')

    response_register_waiter = session.request(method='POST', url=ip_string,
                                               data=xml_unicode_register_waiter_string,
                                               auth=(user_name, pass_word), verify=False)

    response_register_waiter.encoding = 'UTF-8'

    parsed_response_nodes = ET.fromstring(response_register_waiter.content)
    '''Перебираем все ноды "Item" в прямой дочерней ноде "Dishes"'''
    parsed_register_waiter = parsed_response_nodes.attrib
    # Проверяем возможность создания заказа - если статус что-нибудь, кроме "Ок" кидаем исключение.
    if parsed_register_waiter.get('Status') != "Ok":
        result = parsed_register_waiter.get('ErrorText')

    if 'Status="Ok"' in response_register_waiter.text:
        result = "User has been logged"
    elif 'Status="Query Executing Error"' and 'RK7ErrorN="2101"' in response_register_waiter.text:
        result = "User already has been logged"
    return result

result = reg_waiter("127.0.0.1", "4545", "Admin", "1")
print()
print("<h2>" + result + "</h2>")