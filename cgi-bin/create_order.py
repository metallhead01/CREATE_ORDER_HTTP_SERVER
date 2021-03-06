#!C:\Users\Rustam\AppData\Local\Programs\Python\Python36\python.exe

import urllib3
import requests
import xml.etree.ElementTree as ET

print("Content-type: text/html;charset=utf8\r\n\r\n")
print("<html>")
#print("<head>Something</head>")
print("<body>")

def order_creating(i, p, user_name, pass_word):
    result = ""
    guid = ""

    session = requests.session()

    ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
    #Собираем строку для запроса

    try:
        xml_request_string = ('<?xml version="1.0" encoding="UTF-8"?><RK7Query>'
        '<RK7CMD CMD="CreateOrder"><Order><OrderType code= "1" /><Waiter code="9999"/><Table code = "4" /></Order></RK7CMD></RK7Query>')

        xml_unicode_request_string = xml_request_string.encode('utf-8')
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response_create_order = session.request(method='POST', url=ip_string,
                                                data=xml_unicode_request_string,
                                                auth=(user_name, pass_word), verify=False)

        response_create_order.encoding = 'UTF-8'

        print(response_create_order.text)

        parsed_ident_nodes = ET.fromstring(response_create_order.content)
        '''Перебираем все ноды "Item" в прямой дочерней ноде "Dishes"'''
        parsed_create_order = parsed_ident_nodes.attrib
        # Проверяем возможность создания заказа - если статус что-нибудь, кроме "Ок" кидаем исключение.
        if parsed_create_order.get('Status') != "Ok":
            result = parsed_create_order.get('ErrorText')
            raise NameError(parsed_create_order.get('ErrorText'))

    except NameError as m:
        result = m

    else:
        # Парсим ID визита
        visit_id = parsed_create_order.get('VisitID')

        xml_save_order = ('<RK7Query><RK7CMD CMD="SaveOrder" deferred="1" dontcheckLicense="1"><Order visit="' +
                          str(visit_id) + '" orderIdent="256" /><Session><Station code="1" />' +
                          '<Creator code="9999"/><Dish id= "1000010" quantity= "2000"></Dish></Session></RK7CMD></RK7Query>')

        xml_save_order_string = xml_save_order.encode('utf-8')
        response_save_order = session.request(method='POST', url=ip_string, data=xml_save_order_string,
                                          auth=(user_name, pass_word), verify=False)
        # Перекодируем response_save_order в нужную нам кодировку (кириллица поломана)
        response_save_order.encoding = 'UTF-8'

        #print(response_save_order.text)

        # Распарсим полученый ответ для того, чтобы получить GUID только что созданного заказа.
        parsed_guid_nodes = ET.fromstring(response_save_order.content)

        for item in parsed_guid_nodes.findall("./Order"):
            attr_of_item_node = (item.attrib)
            guid = str(attr_of_item_node.get('guid'))

        parsed_create_order = parsed_guid_nodes.attrib
        response_save_order.encoding = 'UTF-8'
        if parsed_create_order.get('Status') != "Ok":
            result = str(parsed_create_order.get('ErrorText'))
        else:
            result = "Order " + guid + " has been successfully created."

    return result


call_func = str(order_creating("127.0.0.1", "4545", "Admin", "1"))

print("Content-type: text/html")
print()
print("<h2>" + call_func + "</h2>")
