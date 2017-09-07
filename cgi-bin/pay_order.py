#!C:\Users\rusta\AppData\Local\Programs\Python\Python36\python.exe

#import cgitb; cgitb.enable()
import time
import urllib3
import requests
import xml.etree.ElementTree as ET

def pay_order(i, p, user_name, pass_word, pay_time):

    result = ""
    session = requests.session()
    ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
    xml_request_string = ('<?xml version="1.0" encoding="UTF-8"?><RK7Query>'
                          '<RK7CMD CMD="GetOrderList" onlyOpened = "1"/></RK7Query>')

    xml_unicode_request_string = xml_request_string.encode('utf-8')
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    """
    response_request_order = session.request(method='POST', url=ip_string,
                                            data=xml_unicode_request_string,
                                            auth=(user_name, pass_word), verify=False)

    response_request_order.encoding = 'UTF-8'
    # Распарсим полученый ответ для того, чтобы получить GUID только что созданного заказа.
    parsed_guid_nodes = ET.fromstring(response_request_order.content)

    guid = ''
    to_pay = ''

    for item in parsed_guid_nodes.findall("./Visit/Orders/Order"):

        attr_of_item_node = (item.attrib)
        guid = str(attr_of_item_node.get('guid'))
        to_pay = str(attr_of_item_node.get('ToPaySum'))

    # время ожидания перед оплатой
    time.sleep(int(pay_time))

    xml_pay_string = ('<RK7Query><RK7CMD CMD="PayOrder"><Order guid="' + guid + '"/>'
                      '<Cashier code="9999"/><Station code="4"/><Payment id="1" amount="' +
                     to_pay+'"/></RK7CMD></RK7Query>')

    xml_pay_string = xml_pay_string.encode('utf-8')

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response_pay_order = session.request(method='POST', url=ip_string, data=xml_pay_string,
                                         auth=(user_name, pass_word), verify=False)
    print(response_pay_order.text)
    parsed_pay_nodes = ET.fromstring(response_pay_order.content)

    parsed_pay_ok = parsed_pay_nodes.attrib
    response_pay_order.encoding = 'UTF-8'
    if parsed_pay_ok.get('Status') != "Ok":
        result = str(parsed_pay_ok.get('ErrorText'))
    else:
        result = "Order " + guid + " has been successfully paid."
    """
    #return result

call_func = pay_order("127.0.0.1", "4545", "Admin_QSR", "190186", "2")

print("Content-type: text/html\r\n\r\n")
print("<html>")
#print("<head>Something</head>")
print("<body>")
print("<h1>Paid</h1>")
print("</body>")
print("</html>")