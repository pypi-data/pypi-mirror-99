import os
import re
import shutil
import shelve
from time import sleep
from selenium import webdriver
from send2trash import send2trash
from os import getlogin, path, mkdir, system
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

os.environ['WDM_LOG_LEVEL'] = '0'
last = ''

class Message:

    def __init__(self, author, content, time, date):
        self.author  = author
        self.time    = time
        self.date    = date
        self.content = content
    
    def __str__(self):
        return f'Author: {self.author}\nTime: {self.time}\nDate: {self.date}\nContent: {self.content}'

class Whatsapp:

    def get_qrcode(self):
        """Opens a new chrome page with the QRCode"""

        usr_path = f"C:\\Users\\{getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        self.mydata = shelve.open('data/data')

        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=OFF")
        options.add_argument(f'--user-data-dir={usr_path}')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        driver.get('https://web.whatsapp.com')

        self.mydata['user_agent'] = driver.execute_script("return navigator.userAgent;")

        while True:
            try:
                driver.find_element_by_css_selector(
                    '#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text')
                break
            except: pass
        driver.close()


    def login(self, visible: bool=False):
        """Logs in whatsapp and shows the QRCode if necessary

        Args:
            visible (bool, optional): Shows the process. Defaults to False.
        """

        usr_path = f"C:\\Users\\{getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        try:
            self.mydata = shelve.open('data/data')
        except:
            mkdir('data')
            self.mydata = shelve.open('data/data')

        try:
            print(f'Logging as: {self.mydata["user_agent"]}')
        except:
            self.get_qrcode()
            
        
        options = webdriver.ChromeOptions()
        options.add_argument(f'--user-data-dir={usr_path}')
        options.add_argument(f"--user-agent={self.mydata['user_agent']}")
        options.add_argument("--start-maximized")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=OFF")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        if not visible:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get('https://web.whatsapp.com')

        while True:
            try:
                try: 
                    self.driver.find_element_by_css_selector(
                        '#app > div > div > div.landing-window > div.landing-main > div > div.O1rXL > div > canvas')
                    self.driver.close()
                    self.get_qrcode()
                    self.login(visible=visible)
                    break

                except:
                    try:
                        self.driver.find_element_by_xpath(
                            "//a[@title='Atualize o Google Chrome']")
                        self.driver.close()
                        self.get_qrcode()
                        self.login(visible=visible)
                        break
                    
                    except:
                        self.driver.find_element_by_css_selector(
                            '#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text')
                        print('Logged in')
                        break
            except:
                pass


    def exit(self):
        """Exit the whatsapp"""

        self.driver.close()
        exit()


    def select_chat(self, chat_name: str):
        """Go to the selected chat

        Args:
            chat_name (str): Contact/Group name
        """

        self.driver.find_element_by_css_selector(
            '#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text').send_keys(chat_name)
        self.driver.find_element_by_css_selector(
            '#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text').send_keys(Keys.ENTER)
    

    def get_recent_chats(self):
        """Returns a list of all recent chats

        Returns:
            List: All the recent chats
        """
        
        try:
            array = self.driver.execute_script('''
            let asd = document.querySelectorAll('._2Z4DV');
            let newArray = new Array();
            for (var i = 0; i < asd.length; i++){
                newArray.push(asd[i].querySelector('.N2dUK').textContent);
            };

            return newArray;
            ''')

            return array
        except:
            print('Something gone wrong')

    
    def get_pinned_chats(self):
        """Returns a list of all pinned chats

        Returns:
            List: All the pinned chats
        """

        try:
            array = self.driver.execute_script('''
            let pin = document.querySelectorAll('._3EhXO');
            let newArray = new Array();
            for (var i = 0; i < pin.length; i++) {
                newArray.push(pin[i].parentNode.parentNode.parentNode.parentNode.querySelector('._3Dr46').textContent)
            }

            return newArray
            ''')

            return array
        except:
            print('Something gone wrong')


    def last_message(self):
        """Gets the last message from the chat

        Returns:
            Class: Last message
        """

        global Message

        try:
            info = self.driver.execute_script('''
                var a = document.querySelectorAll(".GDTQm .message-in .copyable-text");
                return a[a.length - 2].dataset.prePlainText;
            ''')
            
            content = self.driver.execute_script('''
                var a = document.querySelectorAll(".GDTQm .message-in .copyable-text");
                return a[a.length - 1].innerText;
            ''')

            time = re.compile(r'(\d+:\d+(\s)?(AM|PM)?)').findall(info)[0][0]
            date = re.compile(r'(\d+/\d+/\d+)').findall(info)[0]
            author = re.compile(r'] (.*):').findall(info)[0]

            return Message(author=author, content=content, time=time, date=date)
        except:
            print('Something gone wrong')


    def new_message(self):
        """Returns True for a new message

        Returns:
            Bool: New message
        """

        global last
        
        try:
            message = whatsapp.last_message()
            if last == '': last = message.content

            if message.content != last:
                last = message.content
                return True
            
            else:
                return False
        except:
            pass

    def send(self, message: str):
        """Sends a message

        Args:
            message (str): The message you want to send
        """

        try:
            chat = self.driver.find_element_by_css_selector(
                '#main > footer > div.vR1LG._3wXwX.copyable-area > div._2A8P4 > div > div._2_1wd.copyable-text.selectable-text')

            if message.find('\n'):
                for line in message.split('\n'):
                    chat.send_keys(line)
                    chat.send_keys(Keys.SHIFT + Keys.ENTER)
                chat.send_keys(Keys.ENTER)
            else:
                chat.send_keys(message)
        except:
            print('Something gone wrong')

    
    def reply(self, message: str):
        """Replies to the last message

        Args:
            message (str): The message you want to send
        """
        
        self.driver.execute_script('''
            var a = document.querySelectorAll('.message-in');
            var elem = a[a.length -1]
            var clickEvent = document.createEvent('MouseEvents');
            clickEvent.initEvent('dblclick', true, true);
            elem.dispatchEvent(clickEvent);
        ''')
        self.send(message)


    def send_file(self, file_path: str):
        """Sends a file

        Args:
            file_path (str/absolute path): The file of the path you want to send
        """

        regex = re.compile(r'(\w+\.(\w+))')
        file_name = file_path.split('\\')[-1]
        isZip = False

        if regex.findall(file_name):
            if regex.findall(file_name)[0] in ['png', 'jpg', 'mp4', '3gpp']:
                type = 1
            else:
                type = 3

        else:
            shutil.make_archive(file_name, 'zip', file_name)

            file_path = path.abspath(file_name + '.zip')
            isZip = True

            type = 3

        self.driver.execute_script('''
            document.querySelector("#main > footer > div.vR1LG._3wXwX.copyable-area > div.EBaI7._23e-h > div._2C9f1 > div > div").click()
        ''')

        sleep(0.7)

        img_box = self.driver.find_element_by_css_selector(
            f'#main > footer > div.vR1LG._3wXwX.copyable-area > div.EBaI7._23e-h > div._2C9f1 > div > span > div > div > ul > li:nth-child({type}) > button > input[type=file]')
        
        img_box.send_keys(file_path)

        while True:
            try:
                self.driver.find_element_by_css_selector(
                    '#app > div > div > div.Akuo4 > div._1Flk2._1sFTb > span > div > span > div > div > div._36Jt6.tEF8N > span > div > div > span').click()
                break
            except:
                pass


        if isZip:
            send2trash(file_name + '.zip')


    # FIXME: close group info after finishing
    def change_group_description(self, description: str):
        """Changes the group description

        Args:
            description (str): New group description
        """

        try:

            self.driver.find_element_by_css_selector(
                '#main > header > div._2uaUb > div.z4t2k > div > span').click()

            sleep(1)

            try:
                self.driver.find_element_by_css_selector(
                    '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div')

            except:
                print('You are not a group admin!')
                return

            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div').click()

            description_dom = self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div._3rhi1 > div > div._2_1wd.copyable-text.selectable-text')

            description_dom.clear()

            if description.find('\n'):
                for line in description.split('\n'):
                    description_dom.send_keys(line)
                    description_dom.send_keys(Keys.SHIFT + Keys.ENTER)
                description_dom.send_keys(Keys.ENTER)

            else:
                description_dom.send_keys(description)
                
        except:
            print('Something gone wrong')


    # FIXME: close group info after finishing
    def change_group_name(self, name: str):
        """Changes the group name

        Args:
            name (str): New group name
        """

        try:

            self.driver.find_element_by_css_selector(
                '#main > header > div._2uaUb > div.z4t2k > div > span').click()

            sleep(1)

            try:
                self.driver.find_element_by_css_selector(
                    '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div')

            except:
                print('You are not a group admin!')
                return

            self.driver.find_element_by_class_name('_1JAUF').click()

            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt.bRenh > div._2O6GW._3Ss_B._1lemF._3Ihuv > div._3rhi1.e1K_H._1nQew > span._2zDdK > div').click()

            group_name_dom = self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt.bRenh > div._2O6GW._3Ss_B._1lemF._1fB8E._3Ihuv > div._3rhi1 > div > div._2_1wd.copyable-text.selectable-text')

            group_name_dom.clear()
            group_name_dom.send_keys(name + Keys.ENTER)


        except:
            print('Something gone wrong')


    def leave_group(self):
        """Leaves the group you are"""

        self.driver.find_element_by_css_selector(
            '#main > header > div._2uaUb > div.z4t2k > div > span').click()

        self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(6) > div').click()

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > div > div > div > div > div > div._1uJw_ > div._1dwBj._3xWLK').click()


    # FIXME: close group info after finishing
    def add_to_group(self, contact_name: str):
        """Add a new participant to the group

        Args:
            contact_name (str): The contact name of who you want to add
        """

        try:

            self.driver.find_element_by_css_selector(
                '#main > header > div._2uaUb > div.z4t2k > div > span').click()

            try:
                self.driver.find_element_by_css_selector(
                    '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div')

            except:
                print('You are not a group admin!')
                
            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div:nth-child(2) > div.TbtXF').click()

            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text').send_keys(contact_name)
            
            sleep(0.5)
            
            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text').send_keys(Keys.ENTER)
                
            sleep(0.5)

            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div > span._3IGMG > div > div > div').click()

            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div._1uJw_ > div._1dwBj._3xWLK').click()

        except:
            print('Something gone wrong')
    

    # FIXME: close group info after finishing
    def remove_from_group(self, participant_name: str):
        """Removes a participant from the group

        Args:
            participant_name (str): The contact name or number of who you want to remove
        """

        try:

            self.driver.find_element_by_css_selector(
                '#main > header > div._2uaUb > div.z4t2k > div > span').click()

            try:
                self.driver.find_element_by_css_selector(
                    '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div')

            except:
                print('You are not a group admin!')
                return

            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div.-ZdaK > div > div > div._3TVPy').click()

            sleep(0.5)

            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text').send_keys(participant_name)

            sleep(0.5)
            
            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div._1C2Q3._36Jt6 > div:nth-child(1) > div > div > div > div > div').click()

            sleep(0.5)

            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(4) > div > ul > li:nth-child(2)').click()

            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > header > div > div._215wZ > button').click()
        
        except:
            print('Something gone wrong')


    # FIXME: close group info after finishing
    def make_group_admin(self, participant_name: str):
        """Makes someone a group admin

        Args:
            participant_name (str): [The contact name or number of who you want to make admin
        """

        try:

            self.driver.find_element_by_css_selector(
                '#main > header > div._2uaUb > div.z4t2k > div > span').click()

            try:
                self.driver.find_element_by_css_selector(
                    '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div')

            except:
                print('You are not a group admin!')
                return

            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div.-ZdaK > div > div > div._3TVPy').click()

            sleep(0.5)

            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text').send_keys(participant_name)

            sleep(0.5)
            
            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div._1C2Q3._36Jt6 > div:nth-child(1) > div > div > div > div > div').click()

            sleep(0.5)

            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(4) > div > ul > li:nth-child(1)').click()

            self.driver.find_element_by_css_selector(
                '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > header > div > div._215wZ > button').click()
        
        except:
            print('Something gone wrong')
    
    # TODO: get group invite link

    # TODO: invite by number

    # TODO: private answer

    # TODO: Get group info (maybe turn it into a class)

    # TODO: Decent error message



whatsapp = Whatsapp()