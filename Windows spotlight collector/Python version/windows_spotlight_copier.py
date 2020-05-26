# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:01:19 2020
@author: Sivaraman Lakshmipathy
"""

import os
import shutil
import datetime
import webbrowser
from logger_handler import *


class SpotlightHandler:
    # Only files with size > size_threshold (in KB) will be copied
    # This is to filter non-spotlight images.
    size_threshold_kb = 300

    logger = CustomLogger()

    windows_spotlight_path = None
    copy_folder_root = None
    config_file = None
    system_config_file = None
    error_url = "https://github.com/sivaramanl/Personal-projects/blob/master/Windows%20spotlight%20collector/windows_spotlight_error.txt"

    def __init__(self):
        self.logger.log_message("Initializing Windows Spotlight copier task.", logger_handler.log_level_INFO)
        try:
            self.load_config()
            if self.already_handled_today():
                return

            self.spotlight_files = os.listdir(self.windows_spotlight_path)
            self.size_threshold = self.size_threshold_kb * 1024
            if self.spotlight_files is None:
                return

            if self.ensure_path_availability():
                self.handler()
                self.update_config_file()
                self.logger.log_message("Exiting Windows Spotlight copier task.", logger_handler.log_level_INFO)
            else:
                self.handle_invoke_error()
        except Exception as e:
            self.logger.log_message("Exception in windows spotlight copier task:" + str(e), logger_handler.log_level_ERROR)
            self.handle_invoke_error()

    def load_config(self):
        current_dir = os.path.dirname(__file__)
        self.system_config_file = current_dir + os.path.sep + "config" + os.path.sep + "spotlight_config"

        if not os.path.exists(self.system_config_file):
            logger_handler.log_message("System config file not found!", logger_handler.log_level_ERROR)
            return

        with open(self.system_config_file) as f:
            config_entries = f.readlines()

        for entry in config_entries:
            if "windows_spotlight_path" in entry:
                self.windows_spotlight_path = entry.split("windows_spotlight_path =")[1].strip()
            if "copy_folder_root" in entry:
                self.copy_folder_root = entry.split("copy_folder_root =")[1].strip()
            if "config_file" in entry:
                self.config_file = entry.split("config_file =")[1].strip()

        if self.config_file is None or self.config_file == "":
            self.config_file = current_dir + os.path.sep + "config" + os.path.sep + "config.txt"
        if self.windows_spotlight_path is None or self.windows_spotlight_path == "":
            candidate_path = "C:" + os.path.sep + "Users" + os.path.sep + os.getlogin() + os.path.sep + "AppData" + os.path.sep + "Local" + os.path.sep + "Packages"
            candidate_files = os.listdir(candidate_path)
            for entry in candidate_files:
                if entry.startswith("Microsoft.Windows.ContentDeliveryManager"):
                    self.windows_spotlight_path = "C:" + os.path.sep + "Users" + os.path.sep + os.getlogin() + os.path.sep + "AppData" + os.path.sep + "Local" + os.path.sep + "Packages" + os.path.sep + entry + os.path.sep + "LocalState" + os.path.sep + "Assets"
                    break
        if self.copy_folder_root is None or self.copy_folder_root == "":
            self.copy_folder_root = current_dir + os.path.sep + "data"

    # This method reads the config file that contains the date the handler was invoked last
    # Ensures that this handler doesn't redo work based on current data as data is expected to change on a daily basis
    # but the handler will be invoked multiple times per day.
    def already_handled_today(self):
        date_val = None
        cur_date = datetime.date.today()
        if os.path.exists(self.config_file):
            f = open(self.config_file, "r")
            stored_date = f.read().strip()
            temp_date_vals = stored_date.split("-")
            date_val = datetime.date(int(temp_date_vals[0]), int(temp_date_vals[1]), int(temp_date_vals[2]))
            f.close()
        if date_val is None or date_val < cur_date:
            return False
        return True

    def update_config_file(self):
        try:
            f = open(self.config_file, "w")
            f.write(str(datetime.date.today()))
            f.close()
        except Exception as e:
            self.logger.log_message("Error while updating config file:" + str(e), logger_handler.log_level_WARNING)

    def handle_invoke_error(self):
        # This block of code intends to let the end user know that the handler failed to be launched
        webbrowser.open(self.error_url)

    def ensure_path_availability(self):
        if self.windows_spotlight_path is None or not os.path.exists(self.windows_spotlight_path):
            self.logger.log_message("Windows spotlight directory not available.", logger_handler.log_level_ERROR)
            return False
        if not os.path.exists(self.copy_folder_root):
            try:
                os.mkdir(self.copy_folder_root)
                return True
            except Exception as e:
                self.logger.log_message("Exception while creating data directory:" + str(e), logger_handler.log_level_ERROR)
                return False
        return True

    @staticmethod
    def is_jpg_or_jpeg(filePath):
        with open(filePath, "rb") as f:
            hexVal = f.read(3).hex()
            # https://en.wikipedia.org/wiki/List_of_file_signatures
            # Hex value of jp(e)g image file signature begins as "FF D8 FF"
            if "ffd8ff" == hexVal:
                return True
        return False

    def handler(self):
        for entry in self.spotlight_files:
            dest = self.copy_folder_root + os.path.sep + entry + ".png"
            if os.path.exists(dest):
                continue

            src = self.windows_spotlight_path + os.path.sep + entry
            if self.is_jpg_or_jpeg(src) and os.path.getsize(src) >= self.size_threshold:
                shutil.copy(src, dest)


def main():
    SpotlightHandler()


if __name__ == '__main__':
    main()
