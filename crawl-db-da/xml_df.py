import xml.etree.ElementTree as ElementTree
import os, sys, csv
from urllib.request import urlopen
import pandas as pd
import numpy as np
import requests
import xml.etree.ElementTree as ET

class XML2DataFrame:
    root = ''
    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)


    def parse_root(self, root):
        return [self.parse_element(child) for child in iter(root)]

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()
        for key in element.keys():
            parsed[key] = element.attrib.get(key)
        if element.text:
            parsed[element.tag] = element.text
        for child in list(element):
            self.parse_element(child, parsed)
        return parsed

    def process_data(self,root):
        structure_data = self.parse_root(root)
        return pd.DataFrame(structure_data)


