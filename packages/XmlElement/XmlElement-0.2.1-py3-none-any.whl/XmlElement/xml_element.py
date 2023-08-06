from __future__ import annotations
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
from typing import List, Union
from XmlElement.element_tag_value import ElementTagValue
import re

class XmlElement():
    def __init__(self, n: str, a: dict = {}, s: List[XmlElement] = [], t: str = None):
        """Create a new XmlElement.
        Keyword arguments:
        n -- XML tag name
        a -- Dictionary of XML attributes (default {})
        s -- Array of sublements for the XML element (default [])
        t -- Text content of the XML element
        """
        self.name = n
        self.attributes = a
        self.subelements = s
        self.__add_subelement_attribute__(s)
        self.text = t
    

    def __add_subelement_attribute__(self, subelements:List[XmlElement]) -> None:
        """Internal function to allow the shorthand . operator to access findall()"""
        for subelement in subelements:
            setattr(self, subelement.name, ElementTagValue(self, subelement.name))


    def __getitem__(self, tag_name:str) -> List[XmlElement]:
        return self.findall(tag_name)


    # def __setitem__(self, tag_name:str, elements:List[XmlElement]):
    #     for e in elements:
    #         if e.name != tag_name:
    #             raise KeyError(f'Not all tag names equals "{tag_name}" in new XmlElements list.')
    #     self.__delitem__(tag_name)
    #     self.extend(elements)

    
    # def __delitem__(self, tag_name:str):
    #     for e in self.findall(tag_name):
    #         self.subelements.remove(e)
    #     super().__delattr__(tag_name)


    def set(self, key: str, value:str) -> None:
        """Create or update an attribute
        Keyword arguments:
        key -- XML attribute name
        value -- XML attribute value
        """
        self.attributes = { **self.attributes, **{key: value} }


    def append(self, subelement: XmlElement) -> None:
        """Add a new subelement to this XmlElement
        Keyword arguments:
        subelement -- XmlElement
        """
        self.__add_subelement_attribute__([subelement])
        self.subelements = [ *self.subelements, subelement]


    def extend(self, subelements: List[XmlElement]) -> None:
        """Add a set of subelements
        Keyword arguments:
        subelement -- Set of XmlElements
        """
        self.__add_subelement_attribute__(subelements)
        self.subelements = [ *self.subelements, *subelements ]
        

    def to_etree_element(self) -> Element:
        """Render this XmlElement to an xml.etree.ElementTree.Element object"""
        e = Element(self.name)
        for k, v in self.attributes.items():
            e.set(k, v)
        for s in self.subelements:
            if not s == None:
                e.append(s.to_etree_element())
        e.text = self.text
        return e

    def to_dict(self, recognize_numbers=True, recognize_bool=True) -> dict:
        """Render this XmlElement to a (cascaded) dictionary. 
        Keyword arguments:
        recognize_numbers -- (Optional) Try to recognize numbers (default: True)
        recognize_bool -- (Optional) Try to recognize numbers (default: True)
        """

        d = { '@'+k: XmlElement.__infer_type__(v, recognize_numbers, recognize_bool) for k, v in self.attributes.items() }

        for e in self.subelements:
            if e.name in d and isinstance(d[e.name], list):
                d[e.name].append(XmlElement.__infer_type__(e.to_dict(recognize_numbers, recognize_bool), recognize_numbers, recognize_bool))
            elif e.name in d:
                d[e.name] = [ d[e.name], XmlElement.__infer_type__(e.to_dict(recognize_numbers, recognize_bool), recognize_numbers, recognize_bool) ]
            else:
                d[e.name] = XmlElement.__infer_type__(e.to_dict(recognize_numbers, recognize_bool), recognize_numbers, recognize_bool)

        text = XmlElement.__infer_type__(self.text, recognize_numbers, recognize_bool)

        if len(d) > 0:
            if text:
                d['#'] = text
            return d
        else:
            return text


    @staticmethod
    def __infer_type__(value:any, recognize_numbers:bool=True, recognize_bool:bool=True) -> any:
        result = value
        if isinstance(value, str):
            if recognize_numbers and re.match(r'^-?\d+(?:\.\d+)$', value):
                result = float(value)
            elif recognize_numbers and value.isnumeric():
                result = int(value)
            elif recognize_bool and value == 'true':
                result = True
            elif recognize_bool and value == 'false':
                result = False
        return result

    def to_string(self, encoding:str = "unicode") -> str:
        """Render this XmlElement to string
        Keyword arguments:
        encoding -- The output encoding (default: 'unicode')
        """
        return tostring(self.to_etree_element(), encoding=encoding)


    def find(self, tag_name: str = None) -> Union[XmlElement, None]:
        """Return the first subelement with a given name or 
        None if no element with such a name exists
        Keyword arguments:
        name -- Tag name of the subelement searched for
        """
        for s in self.subelements:
            if not s == None:
                if tag_name == None or s.name == tag_name:
                    return s
        return None


    def findall(self, tag_name:str = None) -> List[XmlElement]:
        """Return all subelements with a given name or an empty 
        list if no element with such a name exists
        Keyword arguments:
        name -- Tag name of the subelement searched for
        """
        result = []
        for s in self.subelements:
            if not s == None:
                if tag_name == None or s.name == tag_name:
                    result.append(s)
        return result
        

    @staticmethod
    def from_etree_element(element: Element) -> XmlElement:
        """Recursively create a XmlElement from a given xml.etree.ElementTree.Element object
        Keyword arguments:
        element -- The xml.etree.ElementTree.Element to import
        """
        return XmlElement(
            element.tag, 
            a={k: v for k, v in element.items()},
            s=[XmlElement.from_etree_element(child) for child in element],
            t=element.text
        )


    @staticmethod
    def from_string(xml_string: str) -> XmlElement:
        """Create a XmlElement and its subelements from a XML file string
        Keyword arguments:
        xml_string -- The XML input data to import
        """
        return XmlElement.from_etree_element(fromstring(xml_string))


    @staticmethod
    def from_object(node_name:str, data:Union[dict, list, tuple, str, int, bool]) -> XmlElement:
        """Create a XmlElement and its subelements from a dictionary or list

        Keyword arguments:
        node_name -- The name of the root node
        data -- The dict input data
        """
        elem = None

        if isinstance(data, (list, tuple)):
            elem = [ XmlElement.from_object(node_name, item) for item in data ]
        
        elif isinstance(data, dict):
            elem = XmlElement(
                n=node_name,
                t=next(iter([ v for k, v in data.items() if len(k) == 0 or k[0] == '#' ]), None)
            )
            for k, v in [ (k[1:], v) for k, v in data.items() if len(k) > 1 and k[0] == '@' ]:
                if isinstance(v, str):
                    elem.set(k, v)
                elif isinstance(v, bool):
                    elem.set(k, 'true' if v else 'false')
                else:
                    elem.set(k, str(v))

            for s in [ XmlElement.from_object(k, v) for k, v in data.items() if len(k) > 0 and k[0] != '@' ]:
                if isinstance(s, (list, tuple)):
                    elem.extend(s)
                else:
                    elem.append(s)

        elif isinstance(data, str):
            elem = XmlElement(n=node_name, t=data)
        
        elif isinstance(data, bool):
            elem = XmlElement(
                n=node_name, 
                t='true' if data else 'false'
            )
        
        else:
            elem = XmlElement(n=node_name, t=str(data))
    
        return elem


    def __str__(self) -> str:
        return self.to_string()


    def __repr__(self) -> str:
        return f'XmlElement({self.name})'

    
    def __len__(self) -> int:
        return len(self.subelements)