# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:01:19 2020
@author: Sivaraman Lakshmipathy
"""

import os
import xml.etree.ElementTree as ET


def update_xml():
    xml_tree = ET.parse(os.path.dirname(__file__) + os.path.sep + "windows_spotlight_copier.xml")
    xml_root = xml_tree.getroot()
    for i in range(len(xml_root)):
        if "Actions" in xml_root[i].tag:
            for j in range(len(xml_root[i])):
                if "Exec" in xml_root[i][j].tag:
                    for k in range(len(xml_root[i][j])):
                        if "Command" in xml_root[i][j][k].tag:
                            xml_root[i][j][k].text = os.path.dirname(__file__) + os.path.sep + "windows_spotlight_copier.bat"
                            break

    ET.register_namespace('', "http://schemas.microsoft.com/windows/2004/02/mit/task")
    xml_tree.write(os.path.dirname(__file__) + os.path.sep + "windows_spotlight_copier.xml")


def main():
    update_xml()


if __name__ == '__main__':
    main()
