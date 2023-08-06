import xml.etree.ElementTree as ET
from .xml_etree_to_dict import xml_etree_to_dict


def convert_xml_to_dict(xml_string):
    no_namespace_xml_string = str(xml_string).replace('xmlns="http://queue.amazonaws.com/doc/2012-11-05/"', "")
    rootelm = ET.fromstring(no_namespace_xml_string)
    return xml_etree_to_dict(rootelm)