import time
import requests
from lxml import etree, html
import urllib3
import random
import json

procedurals=['analizy-kostanay',
             'komputernaya-tomografiya-kostanay',
             'mrt-kostanay',
             'procedurniy-kabinet-kostanay'
             ]
def get_links():
    """
    Represent function for loading information from 'https://vrachi-kostanay.kz
    website , links for button.

    Фунция загружает c 'https://vrachi-kostanay.kz информацию о ссылках,
    она используется в меню бота.

    """
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(headers=user_agent, url='https://vrachi-kostanay.kz')
    h = html.fromstring(r.text)
    body = h.getchildren()[1]
    blok = body.find_class('blk blk_button')
    links = []
    num = 0
    for bl in blok[2:43]:
        d = {}
        link = bl.find_class('btn-new block-content')[0]
        url = urllib3.util.parse_url(link.attrib.get('href'))
        d['path'] = url.path.strip('/')
        d['text'] = link.text
        d['num'] = num
        links.append(d)
        num = num+1
    return links

def get_info (line_str,link):
    doc_dict={}

    elem_str = etree.tostring(line_str, encoding='UTF-8')
    blok_list=elem_str.decode('UTF-8').replace(u'</b>', '').replace('<b class="">','').replace(u'<b>', '').split(u'<br/>')
    #etree.dumps(blok_list)
    for_delete=[]
    #human=elem_str.decode('UTF-8').lower().find(u'опыт')
    #filter

    for el in blok_list:
        if len(el)==1:
            print (ord (el))
            if (ord (el)==8203):
                for_delete.append(el)
        elif len(el)==0:
            for_delete.append(el)
    for el in for_delete:
        blok_list.remove(el)
    blok_list2=[]
    for el in blok_list:
        if el[0].startswith('<'):
            print(el)
            filt_html=html.fromstring(el)
            blok_list2.append(filt_html.text )

        else:
            blok_list2.append(el)
    blok_list=blok_list2
    for_delete=[]
    el=blok_list[0]
    if link.get('path') in procedurals:
        doc_dict['name']=el.strip()
        blok_list.remove(el)

        el=blok_list[0]
        doc_dict['spec']=el[:el.find('в ')].strip()
        blok_list.remove(el)
    else:
        doc_dict['name']=el.strip()
        blok_list.remove(el)

        el=blok_list[0]
        doc_dict['spec']=el[:el.find('в ')].strip()
        blok_list.remove(el)


        for el in blok_list:
            if el.lower().find('катег')>=0:
                doc_dict['grade']=el.strip()
                for_delete.append(el)
            elif el.lower().find('опыт')>=0:
                doc_dict['work_years']=el.lower().replace(u'опыт','').replace(u'лет','').replace(u'года','').replace(u'год','').strip()
                for_delete.append(el)
            elif el.lower().find('акад')>=0:
                doc_dict['sci_grade']=el.strip()
                for_delete.append(el)
        for el in for_delete:
            blok_list.remove(el)



    schedule=[]
    for el in blok_list:
        if len(el)>2:
            if ord(el[0])>=48 and  ord(el[0])<=57:
                 if ord(el[1])>=48 and  ord(el[1])<=57:
                    schedule.append(el)
            elif el.startswith('ПН'):
                schedule.append(el)
            elif el.startswith('ВТ'):
                schedule.append(el)
            elif el.startswith('СР'):
                schedule.append(el)
            elif el.startswith('ЧТ'):
                schedule.append(el)
            elif el.startswith('СБ'):
                schedule.append(el)
            elif el.startswith('ВС'):
                schedule.append(el)
            elif el.lower().strip().startswith('перерыв'):
                schedule.append(el)
            elif el.lower().strip().startswith('по записи'):
                schedule.append(el)
    for el in schedule:
        blok_list.remove(el)
    doc_dict['schedule']=schedule



    el=blok_list[0]
    doc_dict['city']=el.strip()
    blok_list.remove(el)

    el=blok_list[0]
    doc_dict['address']=el.strip()
    blok_list.remove(el)
    print(doc_dict)
    return doc_dict

def get_doctor(link):

    user_agent = {'User-agent': 'Mozilla/5.0'}
    # user_agent = {'User-agent': 'Mozilla/5.0'}
    # user_agent = {'User-agent':'Yandex browser 13'}
    url='https://vrachi-kostanay.kz/{}'.format(link.get('path'))
    print (url)
    count=0
    blok=[]
    sec=3
    while len(blok)==0:
        if len(blok)==0:

            print ('Списка нет ждемс {} секунд'.format(sec) )
            time.sleep(sec)
            r = requests.get(headers=user_agent, url=url)
            h = html.fromstring(r.text)
            body = h.getchildren()[1]
            blok = body.find_class('blk_box_self')
            #etree.dump(body)
            #print(etree.tostring(body  ) )

        else:
            print ('Список ')
        sec=random.randrange(3,10)
    doc_list=[]
    print(blok)
    if len (blok)>0:
        for el in blok:
            elem = el.find_class('blk_text')[0].getchildren()[0].getchildren()[0].getchildren()[0]
            info=get_info(elem,link)
            #info['link']=link
            print(info)
            doc_list.append(info)
    return doc_list
        # print(doc_list)

root=etree.Element('db')


#links=[get_links()[-1]]
links=get_links()
print (links)
for link in links:
# link=links[0]
    sub_el=etree.SubElement(root,link.get('path'))
    sub_el.attrib['button']=link.get('text')


    doctors=get_doctor(link)
    print (doctors)

    for doctor in doctors:
        sub_sub=etree.SubElement(sub_el,'doctor')
        print (doctor)
        if len (doctor.keys())>0:
            for key,value in doctor.items():

                if key !='schedule':
                    subb=etree.SubElement(sub_sub,key)
                    subb.text=value
                else:
                    subb=etree.SubElement(sub_sub,'scheduler')
                    for schedule in value:
                        subb2=etree.SubElement(subb,'schedule')
                        subb2.text=schedule
# time.sleep(30) # Сон в 3 секунды

f=open('db.xml','w+b')
f.write (etree.tostring(root,encoding='UTF-8',pretty_print=True ))

# f.write ( )

f.close()


# time.sleep(3) # Сон в 3 секунды
