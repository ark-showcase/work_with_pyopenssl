from bs4 import BeautifulSoup

def get_element_attr(html_response, element_id, element_attr):
    soup = BeautifulSoup(html_response, 'html.parser')

    element = soup.find(id=element_id)
    if element:
        element_attr_value = element.get(element_attr)
        return element_attr_value

    return None