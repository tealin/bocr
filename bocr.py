from tkinter import *
import tkinter.filedialog
import pprint
import requests
import base64
import threading

'''
def haha():
    print(e1.get(),e2.get())
'''
def ocr(url='',image=''):

    url = url
    image = image

    #get cookies
    headers_one = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    }
    url_one = 'https://cloud.baidu.com/product/ocr/general'
    rq = requests.get(url_one)
    cookies = rq.cookies

    apiurl = 'https://cloud.baidu.com/aidemo'
    headers = {
        'Accept':'*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        #Content-Length: 767039
        'Content-Type': 'application/x-www-form-urlencoded',
        #Cookie: BAIDUID=BE59F66B784D283956A9017B932D3DAA:FG=1; BIDUPSID=BE59F66B784D283956A9017B932D3DAA; PSTM=1557106299; H_PS_PSSID=1440_28939_21117_28723_28963_28833_28584; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=enusJeCCxG3tGzr9FZUQyzrsc_bd6Cj2KM7A3J; H_BDCLCKID_SF=tJFH_CKbJKI3fP36q4jWMt_eMU_X5-RLq5TJWx7ba-5KHnKZJt_bJjc-Jf5-D4LtjCrK8RDKjt5MDf7zbtOE5trKKUoLDJQJaGOJ04oEq65qM65pDK_WjIL8eeoKJDL8fPctLn67Kb7_fb5k55FqbjQ8-Gt-56K-5RP-3JKHKC0tftbzBPbHhJ8_MfJXfCQ-J4I8o5Kyt65qM55PeK_BDIK8BUR-hRby-Dn00I6Q2b5Bfn74b-rfaDK8BUR-hRby-Dn00I_BtCDaMC-4D6D5Dj5yeUoX-RJZ5m7mXp0bbp30qCTDWloG2JIXKUbd5t0q0KLHahC50COkbRO4-TFhDjjyDf5; delPer=0; PSINO=3; ZD_ENTRY=baidu; _ga=GA1.2.647427218.1557383872; _gid=GA1.2.1207606338.1557383872; Hm_lvt_28a17f66627d87f1d046eae152a1c93d=1557383873; Hm_lpvt_28a17f66627d87f1d046eae152a1c93d=1557383873; BAIDU_CLOUD_TRACK_PATH=https%3A%2F%2Fcloud.baidu.com%2Fproduct%2Focr%2Fgeneral
        'Host': 'cloud.baidu.com',
        'Origin': 'https://cloud.baidu.com',
        'Referer': 'https://cloud.baidu.com/product/ocr/general',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    }

    data = {
        'image': image,
        'image_url': url,
        'type': 'commontext',
        'detect_direction': 'false',
    }

    r = requests.post(apiurl,headers=headers,data=data,cookies=cookies)

    return r.json()

def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()

root = Tk()
root.title('OCR识别 --必须联网   开发:tealin')
root.grid()
l1 = Label(root, text="图片URL地址:").grid(row=0,column=0,padx=10, pady=5)
e1 = Entry(root, width=40)
e1.grid(row=0,column=1,padx=10, pady=5)

image = ''
def fileload():
    filetypes = ( ("image file", ("*.png","*.jpeg","jpg","bmp")), ("All files", "*.*") )
    filename = tkinter.filedialog.askopenfilename(filetypes=filetypes)
    e1.insert('0',filename)
    #print(filename)


b1 = Button(root, text="上传本地图片",command=fileload,width=8)
b1.grid(row=0,column=2,padx=5, pady=5)


def goocr():
    url = e1.get()
    if url[0:4] == 'http':
        text = ocr(url)
        t1.delete('1.0','end')
        for t in text['data']['words_result']:
            t1.insert(END,t['words']+'\n')
    else:
        filename = e1.get()
        ed =filename.split('.')[-1]
        s = 'data:image/'+ed+';base64,'
        #print(s+'\n\n\n')
        with open(filename,'rb') as f:
            base64_data = base64.b64encode(f.read()).__str__()[2:-1]
            base64_data = s+base64_data
            #print(base64_data)
            text = ocr(image=base64_data)
            #pprint.pprint(text)
            t1.delete('1.0','end')
            for t in text['data']['words_result']:
                t1.insert(END,t['words']+'\n')
            #t1.insert('1.0',text)

    #t1.insert('1.0',text)
    #pprint.pprint(text)

b2 = Button(root, text="识别",width=8,command=lambda :thread_it(goocr()))
b2.grid(row=0,column=3,padx=5, pady=5)
t1 = Text(root,highlightbackground='#cccccc',borderwidth = 1)
t1.grid(row=2,columnspan=4,padx=10, pady=10)
note = '图片文件类型支持PNG、JPG、JPEG、BMP，图片大小不超过2M。'
t1.insert('0.1',note)


root.mainloop()