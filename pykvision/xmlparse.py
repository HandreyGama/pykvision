import xmltodict

def xml_parse_dict(xml:str) -> dict:
    dic = xmltodict.parse(xml)
    return dic

def dict_parse_xml(dict:dict) -> str:
    xml = xmltodict.unparse(dict)
    return xml

def to_bool_xml(value):
    if isinstance(value,bool):
        return value
    if value is None:
        return False
    return str(value).lower() == "true"