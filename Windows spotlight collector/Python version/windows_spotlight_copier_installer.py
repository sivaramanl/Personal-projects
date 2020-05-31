# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:01:19 2020
@author: Sivaraman Lakshmipathy
"""

import os
import pathlib
import xml.etree.ElementTree as ET

from logger_handler import *


def update_xml():
    try:
        current_dir = str(pathlib.Path(__file__).parent.absolute())
        namespaces = {'schema': 'http://schemas.microsoft.com/windows/2004/02/mit/task'}
        ET.register_namespace('', namespaces['schema'])
        xml_tree = ET.parse(current_dir + os.path.sep + "windows_spotlight_copier.xml")
        xml_root = xml_tree.getroot()
        target_node = xml_root.find('schema:Actions', namespaces).find('schema:Exec', namespaces).find('schema:Command', namespaces)
        target_node.text = current_dir + os.path.sep + "windows_spotlight_copier.bat"
        xml_tree.write(current_dir + os.path.sep + "windows_spotlight_copier.xml")
        CustomLogger().log_message("Installer operations completed.")

        #Generate temporary file to signal the installation to continue
        f = open(current_dir + os.path.sep + "install_temp", "w")
        f.write(str(datetime.date.today()))
        f.close()
    except Exception as e:
        CustomLogger().log_message("Exception during installation: " + str(e), logger_handler.log_level_ERROR)


def main():
    update_xml()


if __name__ == '__main__':
    main()
