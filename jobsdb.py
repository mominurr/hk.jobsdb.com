import re
import requests
from bs4 import BeautifulSoup as bs
import time
import PySimpleGUI as sg
import threading,queue
import json
import xlsxwriter

Flag_1,Flag_2=0,0

headers_2 = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "x-user-lan": "en-US",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": 'en-US',
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }




def scraping_1(new_url_1,currentPage_1,lastPage_1,queue1):
    info_list_1=[]
    global Flag_1
    for new_page_1 in range(currentPage_1,lastPage_1):
        page_url_1=f'{new_url_1}{new_page_1}'

        # print('Scraping 1 : ',new_page_1)
        try:
            res_1=requests.get(page_url_1,headers=headers_2,timeout=180)
        except:
            res_1=''

        try:
            soup_1=bs(res_1.content,'html.parser')
        except:
            soup_1=''

        try:
            json_str_1=soup_1.find_all('script')[1].text.strip().replace(";",'')
        except:
            json_str_1=''
        # print("len: ",len(json_str))
        try:
            json_str_1=json_str_1.split('window.REDUX_STATE =')[-1].strip()
        except:
            json_str_1=''
        try:
            datas_1=re.sub(
                r'(?<="description" : )"(.*?)"(?=,\s+")',
                lambda h: json.dumps(h.group(1)),
                json_str_1,
                flags=re.S,
            )
        except:
            datas_1=''
        try:
            data_1 = json.loads(datas_1)
        except:
            data_1=''

        try:
            jobs_1=data_1["result"]["jobs"]
        except:
            jobs_1=''

        # print("Search 1: jobs length: ",len(jobs_1))
        
        for job_1 in jobs_1:
            info_1=[]
            try:
                company_name_1=job_1["companyMeta"]["name"]
            except:
                company_name_1=''

            try:
                job_title_1=job_1["jobTitle"]
            except:
                job_title_1=''
            
            try:
                job_url_1=job_1["jobUrl"]
            except:
                job_url_1=''

            try:
                time_of_post_1=job_1["postingDuration"]
            except:
                time_of_post_1=''
            
            info_1.append(job_url_1)
            info_1.append(job_title_1)
            info_1.append(company_name_1)
            info_1.append(time_of_post_1)
            info_list_1.append(info_1)
    queue1.put(info_list_1)
    Flag_1=1
    # print("Complete 1")   



def scraping_2(new_url_2,currentPage_2,lastPage_2,queue2):
    info_list_2=[]
    global Flag_2
    for new_page_2 in range(currentPage_2,lastPage_2+1):
        page_url_2=f'{new_url_2}{new_page_2}'

        # print('Scraping 2 : ',new_page_2)
        try:
            res_2=requests.get(page_url_2,headers=headers_2,timeout=180)
        except:
            res_2=''
        # with open('source.html','w',encoding='utf-8') as f:
        #     f.write(res_2.text)
        try:
            soup_2=bs(res_2.content,'html.parser')
        except:
            soup_2=''

        try:
            json_str_2=soup_2.find_all('script')[1].text.strip().replace(";",'')
        except:
            json_str_2=''
        # print("len: ",len(json_str))
        try:
            json_str_2=json_str_2.split('window.REDUX_STATE =')[-1].strip()
        except:
            json_str_2=''
        try:
            datas_2=re.sub(
                r'(?<="description" : )"(.*?)"(?=,\s+")',
                lambda h: json.dumps(h.group(2)),
                json_str_2,
                flags=re.S,
            )
        except:
            datas_2=''
        try:
            data_2 = json.loads(datas_2)
        except:
            data_2=''

        try:
            jobs_2=data_2["result"]["jobs"]
        except:
            jobs_2=''
        # print("Search 2: jobs length: ",len(jobs_2))
        # data = json.loads(data)

        # print(json.dumps(data, indent=4))

        # with open("sample_1.json", "w") as outfile:
        #     json.dump(data_2, outfile)
        
        for job_2 in jobs_2:
            info_2=[]
            try:
                company_name_2=job_2["companyMeta"]["name"]
            except:
                company_name_2=''

            try:
                job_title_2=job_2["jobTitle"]
            except:
                job_title_2=''
            
            try:
                job_url_2=job_2["jobUrl"]
            except:
                job_url_2=''

            try:
                time_of_post_2=job_2["postingDuration"]
            except:
                time_of_post_2=''
            
            info_2.append(job_url_2)
            info_2.append(job_title_2)
            info_2.append(company_name_2)
            info_2.append(time_of_post_2)
            info_list_2.append(info_2)
    queue2.put(info_list_2)
    Flag_2=1
    # print("Complete 2")



def main(url):
    # url='https://hk.jobsdb.com/hk/search-jobs/sales/1'
    try:
        response=requests.get(url,headers=headers_2,timeout=180)
    except:
        pass

    try:
        soup=bs(response.content,'html.parser')
    except:
        soup=''

    try:
        json_str=soup.find_all('script')[1].text.strip().replace(";",'')
    except:
        json_str=''
    # print("len: ",len(json_str))
    try:
        json_str=json_str.split('window.REDUX_STATE =')[-1].strip()
    except:
        json_str=''
    try:
        datas=re.sub(
            r'(?<="description" : )"(.*?)"(?=,\s+")',
            lambda h: json.dumps(h.group(1)),
            json_str,
            flags=re.S,
        )
    except:
        datas=''
    try:
        data = json.loads(datas)
    except:
        data=''


    try:
        x=url.split("/")[-1]
    except:
        x=''

    try:
        new_url=url.replace(f"{x}",'').strip()
    except:
        new_url=''
    currentPage=data["result"]["currentPage"]
    lastPage=data["result"]["lastPage"]
    try:
        path=url.split("/")[-2].strip()
    except:
        path="_"

    if lastPage%2==0:
        first_half=int(lastPage//2)
    else:
        first_half=int(((lastPage-1)//2))
    paths=f"{path}.xlsx"
    print(currentPage,lastPage)
    
    queued_request1 = queue.Queue()
    queued_request2 = queue.Queue()
    threading.Thread(target=scraping_1, args=(new_url,currentPage,first_half,queued_request1)).start()
    threading.Thread(target=scraping_2, args=(new_url,first_half,lastPage,queued_request2)).start()

    while True:
        if Flag_1==1 and Flag_2==1:
            break
        time.sleep(10)

    details_value=[]
    details_value_1=queued_request1.get()
    details_value_2=queued_request2.get()
    details_value.append(details_value_1)
    details_value.append(details_value_2)
    # print("File creating......")
    user_file=xlsxwriter.Workbook(paths)
    user_sheet=user_file.add_worksheet()
    exel_titles=['Job URL','Job Title','Company Name','Time of Job Post']
    for excel_title in range(len(exel_titles)):
        user_sheet.write(0,excel_title,exel_titles[excel_title])
    row=1
    for product_values in details_value:
        for product_value in product_values:
            for title in range(len(product_value)):
                user_sheet.write(row,title,product_value[title])
            row+=1
    user_file.close()
    # print("Complete")
    window['-OUT-'].update("Complete")




sg.theme('LightBlue1')
layout = [[sg.Text('Web Scraping Tools for :- https://hk.jobsdb.com/',font='curiear 18', text_color='blue',justification='center')],[sg.Text('')],[sg.Text("Enter Url: ",size =(20, 1),font='curiear 14'), sg.InputText(size=(70,100))],[sg.Text('')],[sg.Text('',size=(30,1),font='curiear 14',key='-OUT-',text_color='green')],[sg.Text('')],[sg.Button("Search",auto_size_button=True, button_color='green'),sg.Button('Exit',auto_size_button=True, button_color='red')]]

window = sg.Window('Webscraping Window', layout, size=(770,240),resizable=True)
global f
f=0

while True:
    event,values=window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        f=1
        window.close()
        break
    if event=='Search':
        window['-OUT-'].update("Data processing.........")
		#print('Hello')
    if event == "Search":
        URL=values[0]
        if not URL:
            sg.popup_error('You did not enter anything')
            exit()
        else:
            threading.Thread(target=main, args=(URL,)).start()