from logging import root
from tkinter import *
from tkinter import messagebox
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re


def login():
    _username = username_entry.get()
    _password = pass_entry.get()
    # 2a. Điền thông tin vào ô user và pass
    txtUser = browser.find_element_by_id("email")
    txtUser.send_keys(_username) 
    txtPass = browser.find_element_by_id("pass")
    txtPass.send_keys(_password)
    txtPass.send_keys(Keys.ENTER)
def on_press():
    loop = True
    while loop:
        element = browser.find_element_by_tag_name("body")
        if element != None :
            element.send_keys(Keys.ARROW_DOWN + "j" + Keys.ENTER)
            loop = False
        sleep(1)    
    return None

def print_result():
    print(link_text.get())
    browser.get(link_text.get())
    on_press()

    data = []
    i = int(from_text.get())
    count = 0
    while i < int(to_text.get()):
        print(i)
        try:
            article = browser.find_element_by_css_selector(f'div[aria-posinset="{i}"]') 
            if article != None :
                i+=1 
                actions = ActionChains(browser)
                actions.move_to_element(article).perform()  

                info = {}
                info['id'] = i
                dir = article.find_element_by_css_selector('div[dir="auto"]')
                if dir != None :
                    button = dir.find_elements_by_xpath("//*[text()='Xem thêm']")
                    if button != None: 
                        print("click")
                        for j in button:
                            try:
                                j.click()
                            except:
                                print('miss click')
                text = article.text

                index = text.find("\n")
                info["name"] = text[:index]
                text = text.replace(' ', '').replace('.','') 
                phone =  re.search(r'(84|0[3|5|7|8|9])+([0-9]{8})\b', text, flags=0)
                if phone != None : 
                    info["phone"] = phone.group(0)
                    data.append(info) 
                    print(info['phone']) 
                    

            else:    
                print('Not found',)
        except:    
            print('feild')
            count+=1
            if count == 10 :
                print('press j')
                on_press()
    result = ''
    for i in data:
        result += str(i['id']) +'-'+i['phone']+'-'+ i['name'] + '\n'
    left.insert(END, result)


# 1. Khai bao bien browser
_username = 'admin'
_password = "123456"
_number_from = "1"
_number_to = "10"
_url =""

# Create window object
app = Tk()
# username
username_text = StringVar()
username_label = Label(app, text='username', font=('bold', 14))
username_label.grid(row=0, column=0, sticky=W)
username_entry = Entry(app, textvariable=username_text)
username_entry.grid(row=0, column=1)
username_entry.insert(0, _username)

# pass
pass_text = StringVar()
pass_label = Label(app, text='password', font=('bold', 14))
pass_label.grid(row=0, column=2, sticky=W)
pass_entry = Entry(app, textvariable=pass_text)
pass_entry.grid(row=0, column=3)
pass_entry.insert(5, _password)
# number 1
from_text = StringVar()
from_label = Label(app, text='from', font=('bold', 14))
from_label.grid(row=1, column=0, sticky=W)
from_entry = Entry(app, textvariable=from_text)
from_entry.grid(row=1, column=1)
from_entry.insert(0, _number_from)
#number 2
to_text = StringVar()
to_label = Label(app, text='to', font=('bold', 14))
to_label.grid(row=1, column=2, sticky=W)
to_entry = Entry(app, textvariable=to_text)
to_entry.grid(row=1, column=3)
to_entry.insert(0, _number_to)


# link
link_text = StringVar()
link_label = Label(app, text='link group  ', font=('bold', 14))
link_label.grid(row=2, column=0, sticky=W)
link_entry = Entry(app, textvariable=link_text, width= 62)

link_entry.grid(row=2, column=1, columnspan=3)

# usernames List (Listbox)
left = Text(app, height=20, width=40, border=0)


left.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
# right = Text(app)
# right.grid(row=3, column=4)
# Set scroll to listbox


# Buttons
add_btn = Button(app, text='Đăng nhập', width=12, command=login)
add_btn.grid(row=0, column=5, padx=20)

remove_btn = Button(app, text='Tìm kiếm', width=12, command=print_result)
remove_btn.grid(row=2, column=5)

browser  = webdriver.Chrome(executable_path="./chromedriver")
browser.get("http://facebook.com")
# browser.set_window_position(0, 0)
# browser.set_window_size(0, 0)

app.title('Facebook tool')
app.geometry('700x500')



# Start program
app.mainloop()