import xml.etree.ElementTree as ET
from .xml_etree_to_dict import xml_etree_to_dict


def convert_xml_to_dict(xml_string):
    rootelm = ET.fromstring(xml_string)
    return xml_etree_to_dict(rootelm)