# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:01:19 2020
@author: Sivaraman Lakshmipathy
"""

import os
import pathlib
import xml.etree.ElementTree as ET


def update_xml():
    current_dir = str(pathlib.Path(__file__).parent.absolute())
    namespaces = {'schema': 'http://schemas.microsoft.com/windows/2004/02/mit/task'}
    ET.register_namespace('', namespaces['schema'])
    xml_tree = ET.parse(current_dir + os.path.sep + "windows_spotlight_copier.xml")
    xml_root = xml_tree.getroot()
    target_node = xml_root.find('schema:Actions', namespaces).find('schema:Exec', namespaces).find('schema:Command', namespaces)
    target_node.text = current_dir + os.path.sep + "windows_spotlight_copier.bat"

    xml_tree.write(current_dir + os.path.sep + "windows_spotlight_copier.xml")


def main():
    update_xml()


if __name__ == '__main__':
    main()
