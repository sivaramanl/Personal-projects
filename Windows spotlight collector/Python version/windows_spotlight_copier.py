import os
import datetime
from datetime import date
import webbrowser
import shutil

class spotlight_handler:
    windows_spotlight_path = "C:\\Users\\suji1\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"
    copy_folder_root = "D:\\OneDrive\\Photos\\General\\Windows_Spotlight\\Data"
    config_file = "D:\OneDrive\Photos\General\Windows_Spotlight\Config\\config.txt"
    # Only files with size > size_threshold (in KB) will be copied
    # This is to filter non-spotlight images but is not fool proof. Have to rethink
    size_threshold_kb = 300

    def __init__(self):
        if self.alreadyHandledForToday():
            return

        self.spotlight_files = os.listdir(self.windows_spotlight_path)
        self.size_threshold = self.size_threshold_kb * 1024
        if self.spotlight_files is None:
            return

        if self.ensurePathAvailability():
            self.handler()
            self.updateConfigFile()
        else:
            self.handleInvokeError()

    # This method reads the config file that contains the date the handler was invoked last
    # It ensures that this handler doesn't redo work based on current data as data is expected to change on a daily basis
    # but the handler will be invoked multiple times per day.
    def alreadyHandledForToday(self):
        dateVal = None
        curDate = date.today()
        if os.path.exists(self.config_file):
            f = open(self.config_file, "r")
            storedDate = f.read().strip()
            temp_dateVals = storedDate.split("-")
            dateVal = datetime.date(int(temp_dateVals[0]), int(temp_dateVals[1]), int(temp_dateVals[2]))
            f.close()
        if dateVal is None or dateVal < curDate:
            return False
        return True

    def updateConfigFile(self):
        f = open(self.config_file, "w")
        f.write(str(date.today()))
        f.close()

    def handleInvokeError(self):
        #This block of code intends to let the end user know that the handler failed to be launched
        url = "https://en.wikipedia.org/wiki/Windows_Spotlight"
        chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open(url)

    def ensurePathAvailability(self):
        if not os.path.exists(self.windows_spotlight_path):
            return False
        if not os.path.exists(self.copy_folder_root):
            return False
        return True

    def isJPGorJPEF(self, filePath):
        with open(filePath, "rb") as f:
            hexVal = f.read(3).hex()
            #https://en.wikipedia.org/wiki/List_of_file_signatures
            #Hex value of jp(e)g image file signature begins as "FF D8 FF"
            if "ffd8ff" == hexVal:
                return True
        return False

    def handler(self):
        for entry in self.spotlight_files:
            dest = self.copy_folder_root + os.path.sep + entry + ".png"
            if os.path.exists(dest):
                continue

            src = self.windows_spotlight_path + os.path.sep + entry
            if self.isJPGorJPEF(src) and os.path.getsize(src) >= self.size_threshold:
                shutil.copy(src, dest)

def main():
    spotlight_handler()

if __name__ == '__main__':
    main()