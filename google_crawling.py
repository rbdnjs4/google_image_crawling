from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
from PyQt5.QtWidgets import *

class MyDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        Name = QLabel("검색어를 지정하세요.")
        self.editName = QLineEdit(self)
        Name2 = QLabel("저장하실 폴더를 지정하세요.")
        self.editName2 = QLineEdit(self)
        btnOk = QPushButton("crawling")
        btnOk.clicked.connect(self.btnOk_clicked)



        layout = QVBoxLayout()
        layout.addWidget(Name)
        layout.addWidget(self.editName)
        layout.addWidget(Name2)
        layout.addWidget(self.editName2)
        layout.addWidget(btnOk)


        self.setLayout(layout)
    
    def btnOk_clicked(self):
        QMessageBox.about(self, "message", "크롤링을 시작합니다.")

        if not os.path.isdir(self.editName2.text()):
            os.mkdir(self.editName2.text())

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)

        driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
        elem = driver.find_element_by_name("q")
        elem.send_keys(self.editName.text())
        elem.send_keys(Keys.RETURN)

        SCROLL_PAUSE_TIME = 1
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    driver.find_element_by_css_selector(".mye4qd").click()
                except:
                    break
            last_height = new_height

        images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
        count = 1
        for image in images:
            try:
                image.click()
                time.sleep(2)
                imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img').get_attribute("src")
                print(imgUrl)
                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(imgUrl, self.editName2.text() + "/" + str(count) + ".jpg")
                count = count + 1
            except:
                pass

        driver.close()

app = QApplication([])
dialog = MyDialog()
dialog.show()
app.exec_()