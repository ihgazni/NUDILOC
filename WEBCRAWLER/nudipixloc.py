import navegador5 as nv
import navegador5.url_tool as nvurl
import navegador5.head as nvhead
import navegador5.body as nvbody
import navegador5.cookie
import navegador5.cookie.cookie as nvcookie
import navegador5.cookie.rfc6265 as nvrfc6265
import navegador5.jq as nvjq
import navegador5.js_random as nvjr
import navegador5.file_toolset as nvft
import navegador5.shell_cmd as nvsh
import navegador5.html_tool as nvhtml
import navegador5.solicitud as nvsoli
import navegador5.content_parser
import navegador5.content_parser.amf0_decode as nvamf0
import navegador5.content_parser.amf3_decode as nvamf3

from lxml import etree
import lxml.html
import collections
import copy
import re
import urllib
import os
import json
import sys
import time

from xdict.jprint import  pdir
from xdict.jprint import  pobj
from xdict.jprint import  print_j_str
from xdict import cmdline
import hashlib
import xdict.utils


nudipix_base_url = 'http://www.nudipixel.net'
taxonomy_url = 'http://www.nudipixel.net/taxonomy/'
locs_url = 'http://www.nudipixel.net/locations/'

try:
    lns_dir = sys.argv[2]
except:
    #lns_dir = '/media/root/6d1de738-2a56-4564-ab92-0401c7fe0f68/NUDIPIXLOC/'
    lns_dir = '../LNS/'
else:
    pass

#nvft.mkdir(lns_dir+'Images')

try:
    work_dir = sys.argv[4]
except:
    work_dir = '/media/root/82EC-3DCC/NUDIPIXLOC/'
else:
    pass


try:
    images_dir = sys.argv[6]
except:
    images_dir = = '../Images/'
else:
    pass

try:
    infos_dir = sys.argv[8]
except:
    infos_dir = = '../Infos/'
else:
    pass

try:
    thumbs_dir = sys.argv[10]
except:
    thumbs_dir = = '../Thumbs/'
else:
    pass




#taxonomy_init
def taxonomy_init(base_url='http://www.nudipixel.net/'):
    info_container = nvsoli.new_info_container()
    info_container['base_url'] = base_url
    info_container['method'] = 'GET'
    req_head_str = '''Accept: application/json\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: en;q=1.0, zh-CN;q=0.8'''
    info_container['req_head'] = nvhead.build_headers_dict_from_str(req_head_str,'\r\n')
    info_container['req_head']['Connection'] = 'close'
    #### init records_container
    records_container = nvsoli.new_records_container()
    return((info_container,records_container))




def get_etree_root(info_container,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    html_text = info_container['resp_body_bytes'].decode(coding)
    root = etree.HTML(html_text)
    return(root)

#

def get_country_urls(locs_url,countries_xpath='//div[@id="content"]/div/div/a[@href]'):
    info_container,records_container = taxonomy_init()
    info_container['url'] = locs_url
    #info_container = nvsoli.walkon(info_container,records_container=records_container)
    #info_container = nvsoli.auto_redireced(info_container,records_container)
    ####
    sleep_cnt = 0
    while(1):
        sleep_cnt = sleep_cnt + 1
        if(sleep_cnt > 30):
            sleep_cnt = 30
        else:
            pass
        try:
            info_container = nvsoli.walkon(info_container,records_container=records_container)
            info_container = nvsoli.auto_redireced(info_container,records_container)
        except:
            time.sleep(10 * sleep_cnt)
        else:
            break
    #### 
    root = get_etree_root(info_container)
    eles = root.xpath(countries_xpath)
    country_urls =[]
    country_names = []
    for i in range(0,eles.__len__()):
        url = nudipix_base_url + eles[i].attrib['href']
        country_urls.append(url)
        name = eles[i].text
        country_names.append(name)
    return((country_urls,country_names))


def get_location_urls(country_url,locations_xpath='//ul[@class="country_dive_site_list"]/li/a[@href]'):
    info_container,records_container = taxonomy_init()
    info_container['url'] = country_url
    #info_container = nvsoli.walkon(info_container,records_container=records_container)
    #info_container = nvsoli.auto_redireced(info_container,records_container)
    ####
    sleep_cnt = 0
    while(1):
        sleep_cnt = sleep_cnt + 1
        if(sleep_cnt > 30):
            sleep_cnt = 30
        else:
            pass
        try:
            info_container = nvsoli.walkon(info_container,records_container=records_container)
            info_container = nvsoli.auto_redireced(info_container,records_container)
        except:
            time.sleep(10 * sleep_cnt)
        else:
            break
    #### 
    root = get_etree_root(info_container)
    eles = root.xpath(locations_xpath)
    location_urls =[]
    location_names = []
    for i in range(0,eles.__len__()):
        url = nudipix_base_url + eles[i].attrib['href']
        if('location' in url):
            location_urls.append(url)
            name = eles[i].text
            location_names.append(name)
    return((location_urls,location_names))


def creat_country_md(curls,cnames):
    country_md = {}
    for i in range (0,curls.__len__()):
        abbrev = os.path.basename(curls[i].rstrip('/'))
        country_md[abbrev] = cnames[i]
        country_md[cnames[i]] = abbrev
    return(country_md)


def creat_location_md(lurls,lnames):
    location_md = {}
    for i in range (0,lurls.__len__()):
        abbrev = os.path.basename(lurls[i].rstrip('/'))
        location_md[abbrev] = lnames[i]
        location_md[lnames[i]] = abbrev
    return(location_md)



def get_nav_urls(loc_url,nav_xpath='//p[@class="nav"]/a[@href]'):
    info_container,records_container = taxonomy_init()
    info_container['url'] = loc_url
    #info_container = nvsoli.walkon(info_container,records_container=records_container)
    #info_container = nvsoli.auto_redireced(info_container,records_container)
    ####
    sleep_cnt = 0
    while(1):
        #####
        #print('--------get_nav_urls--------')
        #print(sleep_cnt)
        #print(loc_url)
        #print('--------get_nav_urls--------')
        #####
        sleep_cnt = sleep_cnt + 1
        if(sleep_cnt > 30):
            sleep_cnt = 30
        else:
            pass
        try:
            info_container = nvsoli.walkon(info_container,records_container=records_container)
            info_container = nvsoli.auto_redireced(info_container,records_container)
        except:
            time.sleep(10 * sleep_cnt)
        else:
            break
    #### 
    root = get_etree_root(info_container)
    eles = root.xpath(nav_xpath)
    if(eles.__len__() == 0):
        nav_urls = []
    else:
        max_page = eles[-2].text
        max_page = int(max_page)
        nav_urls = [loc_url]
        tem = os.path.dirname(eles[-2].attrib['href'].rstrip('/'))
        for i in range(2,max_page + 1):
            url = nudipix_base_url + tem + '/' + str(i)
            nav_urls.append(url)
    return(nav_urls)

def get_locsp_urls(nav_url,locsp_xpah='//div[@class="thumbnail"]/div/a[@href]'):
    info_container,records_container = taxonomy_init()
    info_container['url'] = nav_url
    ####
    #info_container = nvsoli.walkon(info_container,records_container=records_container)
    #info_container = nvsoli.auto_redireced(info_container,records_container)
    ####
    sleep_cnt = 0
    while(1):
        #print('>>>>>>>>>>>>>>>>>>>>')
        #print(info_container['url'])
        #print('<<<<<<<<<<<<<<<<<<<<')
        sleep_cnt = sleep_cnt + 1
        if(sleep_cnt > 30):
            sleep_cnt = 30
        else:
            pass
        try:
            info_container = nvsoli.walkon(info_container,records_container=records_container)
            info_container = nvsoli.auto_redireced(info_container,records_container)
        except:
            time.sleep(10 * sleep_cnt)
        else:
            break
    #### 
    root = get_etree_root(info_container)
    eles = root.xpath(locsp_xpah)
    locsp_urls = []
    for i in range(0,eles.__len__()):
        url = nudipix_base_url + eles[i].attrib['href']
        if('location' in url):
            locsp_urls.append(url)
    return(locsp_urls)  


def get_img_urls(locsp_url,img_xpath='//div[@class="thumbnail"]/div/a[@href]'):
    ####
    #sys.stdout.flush()
    #print(locsp_url)
    #sys.stdout.flush()
    ####
    info_container,records_container = taxonomy_init()
    info_container['url'] = locsp_url
    ####
    #info_container = nvsoli.walkon(info_container,records_container=records_container)
    #info_container = nvsoli.auto_redireced(info_container,records_container)
    ####
    ####
    sleep_cnt = 0
    while(1):
        #print('-------------------')
        #print(locsp_url)
        #print('-------------------')
        sleep_cnt = sleep_cnt + 1
        if(sleep_cnt > 30):
            sleep_cnt = 30
        else:
            pass
        try:
            info_container = nvsoli.walkon(info_container,records_container=records_container)
            info_container = nvsoli.auto_redireced(info_container,records_container)
        except:
            time.sleep(10 * sleep_cnt)
        else:
            break
    #### 
    root = get_etree_root(info_container)
    eles = root.xpath(img_xpath)
    img_urls = []
    thumbnail_urls = []
    ####
    ####
    for i in range(0,eles.__len__()):
        url = nudipix_base_url + eles[i].attrib['href']
        if(('photo' in url) & ( not ('photographer' in url))):
            img_urls.append(url)
            ele = eles[i].xpath('img')[0]
            thumbnail_urls.append(nudipix_base_url +ele.attrib['src'])
    nav_xpath='//p[@class="nav"]/a[@href]'
    eles = root.xpath(nav_xpath)
    if(eles.__len__() == 0):
        pass
    else:
        max_page = eles[-2].text
        max_page = int(max_page)
        tem = os.path.dirname(eles[-2].attrib['href'].rstrip('/'))
        for i in range(2,max_page + 1):
            nav_url = nudipix_base_url + tem + '/' + str(i)
            info_container,records_container = taxonomy_init()
            info_container['url'] = nav_url
            ####
            sleep_cnt = 0
            while(1):
                sleep_cnt = sleep_cnt + 1
                if(sleep_cnt > 30):
                    sleep_cnt = 30
                else:
                    pass
                try:
                    info_container = nvsoli.walkon(info_container,records_container=records_container)
                    info_container = nvsoli.auto_redireced(info_container,records_container)
                except:
                    time.sleep(10 * sleep_cnt)
                else:
                    break
            #### 
            root = get_etree_root(info_container)
            eles = root.xpath(img_xpath)
            for j in range(0,eles.__len__()):
                url = nudipix_base_url + eles[j].attrib['href']
                if(('photo' in url) & ( not ('photographer' in url))):
                    img_urls.append(url)
                    ele = eles[j].xpath('img')[0]
                    thumbnail_urls.append(nudipix_base_url +ele.attrib['src'])
    return((img_urls,thumbnail_urls))   


def get_EXIF(EXIF_url):
    info_container,records_container = taxonomy_init()
    info_container['url'] = EXIF_url
    ####
    ####info_container = nvsoli.walkon(info_container,records_container=records_container)
    ####info_container = nvsoli.auto_redireced(info_container,records_container)
    ####
    ####
    sleep_cnt = 0
    while(1):
        sleep_cnt = sleep_cnt + 1
        if(sleep_cnt > 30):
            sleep_cnt = 30
        else:
            pass
        try:
            info_container = nvsoli.walkon(info_container,records_container=records_container)
            info_container = nvsoli.auto_redireced(info_container,records_container)
        except:
            time.sleep(10 * sleep_cnt)
        else:
            break
    #### 
    root = get_etree_root(info_container)
    eles = root.xpath('//table[@class="exif"]/tr')
    EXIF = {}
    for i in range(0,eles.__len__()):
        key = eles[i].xpath('td')[0].text.rstrip(':')
        EXIF[key] = eles[i].xpath('td')[1].text
    return(EXIF)


def init_KPCOFGS(rsltin='path',**kwargs):
    if('names' in kwargs):
        kpcofgs_names = kwargs['names']
    else:
        kpcofgs_names = ['Kingdom','Phylum','Class','Subclass','Infraclass','Order','Superfamily','Family','Genus','Species']
    pobj(kpcofgs_names)
    if(rsltin == 'path'):
        rslt = ''
        for i in range(1,kpcofgs_names.__len__()):
            rslt = rslt + '/' 
        return(rslt)      
    else:
        rslt = {}
        for each in kpcofgs_names:
            rslt[each] = ''
        return(rslt)


def get_KPCOFGS(tbodys,**kwargs):
    if('names' in kwargs):
        kpcofgs_name = kwargs['names']
    else:
        kpcofgs_names = ['Kingdom','Phylum','Class','Subclass','Infraclass','Order','Superfamily','Family','Genus','Species']    
    kpcofgs = tbodys[1].getchildren()
    ks = init_KPCOFGS(rsltin='dict',names=kpcofgs_names)
    for i in range(0,kpcofgs.__len__()):
        ks[kpcofgs[i].xpath('td')[0].text.rstrip(':')] = kpcofgs[i].xpath('td/a')[0].text
    if('rsltin' in kwargs):
        rsltin = kwargs['rsltin']
    else:
        rsltin = 'path'
    if(rsltin == 'path'):
        path = ks[kpcofgs_names[0]]
        for i in range(1,kpcofgs_names.__len__()):
            path = path + '/' + ks[kpcofgs_names[i]]
        return(path)  
    else:
        return(ks)


def get_img_info(img_url,thumbnail_url,country_abbrev,location,base_url = nudipix_base_url):
    info_container,records_container = taxonomy_init()
    info_container['url'] = img_url
    ####
    #sys.stdout.flush()
    #print('---------------')
    #print(img_url)
    #sys.stdout.flush()
    ####
    #info_container = nvsoli.walkon(info_container,records_container=records_container)
    #info_container = nvsoli.auto_redireced(info_container,records_container)
    ####
    sleep_cnt = 0
    while(1):
        sleep_cnt = sleep_cnt + 1
        if(sleep_cnt > 30):
            sleep_cnt = 30
        else:
            pass
        try:
            info_container = nvsoli.walkon(info_container,records_container=records_container)
            info_container = nvsoli.auto_redireced(info_container,records_container)
        except:
            time.sleep(10 * sleep_cnt)
        else:
            break
    #### 
    img_root = get_etree_root(info_container)
    tbodys = img_root.xpath('//table')
    sp = img_root.xpath('//div/div/h2/a')[0].attrib['href'].rstrip('/')
    sp_name = os.path.basename(sp)
    info_raw = tbodys[0].getchildren()
    info = {}
    for i in range(0,info_raw.__len__()):
        key = info_raw[i].xpath('td')[0].text.rstrip(':')
        if(key == 'Camera'):
            info[key] = info_raw[i].xpath('td')[1].text
            EXIF_url = nudipix_base_url + info_raw[i].xpath('td/span/a')[0].attrib['href']
            info['EXIF'] = get_EXIF(EXIF_url)
        elif(key == 'Taken on'):
            info[key] = info_raw[i].xpath('td')[1].text
        elif(key == 'Viewed'):
            info[key] = info_raw[i].xpath('td')[1].text
        elif(key == 'Posted'):
            info[key] = info_raw[i].xpath('td')[1].text
        elif(key == 'Updated'):
            info[key] = info_raw[i].xpath('td')[1].text
        else:
            info[key] = info_raw[i].xpath('td/a')[0].text
    kpcofgs = get_KPCOFGS(tbodys,rsltin='dict')
    info['kpcofgs'] = kpcofgs
    img_real_url = nudipix_base_url + img_root.xpath('//div/img')[0].attrib['src']
    try:
        img_verifier = img_root.xpath('//div/img')[1].attrib['title']
    except:
        img_verifier = ''
    else:
        pass
    sha1 = hashlib.sha1(img_real_url.encode('utf-8')).hexdigest()
    img_suffix = os.path.basename(img_real_url).split('.')[-1]
    img_name = sp_name + '_' + sha1 + '.' + img_suffix
    thumbnail_suffix = os.path.basename(thumbnail_url).split('.')[-1]
    thumbnail_name = sp_name + '_' + sha1 + '.thumbnail.' + thumbnail_suffix
    info_name = sp_name + '_' + sha1 + '.dict'
    info['img_url'] = img_real_url
    info['verifier'] =  img_verifier
    info['img_name'] = images_dir + img_name
    info['index'] = sha1
    info['thumbnail_url'] = thumbnail_url
    info['thumbnail_name'] = thumbs_dir + thumbnail_name
    info['info_name'] = infos_dir + info_name
    info['country'] = country_abbrev
    info['location'] = location
    ####
    #print(img_real_url)
    try:
        info['seq'] = int(os.path.basename(img_real_url).split('.')[0])
    except:
        info['seq'] = -1
    else:
        pass
    #print('-------------')
    return(info)


#####################

try:
    content = nvft.read_file_content(fn = '../seq.record',op='r')
except:
    istart = 0
    jstart = 0
    kstart = 0
    xstart = 0
    ystart = 0
else:
    istart = json.loads(content)['istart']
    jstart = json.loads(content)['jstart']
    kstart = json.loads(content)['kstart']
    xstart = json.loads(content)['xstart']
    ystart = json.loads(content)['ystart']

try:
    content_curls = nvft.read_file_content(fn = '../curls.dict',op='r')
    content_cnames = nvft.read_file_content(fn = '../cnames.dict',op='r')
except:
    curls,cnames =  get_country_urls(locs_url)
    nvft.write_to_file(fn='../curls.dict',content=json.dumps(curls),op='w+')
    nvft.write_to_file(fn='../cnames.dict',content=json.dumps(cnames),op='w+')
else:
    curls = json.loads(content_curls)
    cnames = json.loads(content_cnames)

try:
    content_country_md = nvft.read_file_content(fn = '../country.dict',op='r')
except:
    country_md = creat_country_md(curls,cnames)
    nvft.write_to_file(fn='../country.dict',content=json.dumps(country_md),op='w+')
else:
    country_md = json.loads(content_country_md)


total = 0

for i in range (istart,curls.__len__()):
    #
    sys.stdout.flush()
    print('curl i:')
    print(i)
    print(curls[i])
    print('curl i:')
    sys.stdout.flush()
    #
    country_dir = lns_dir + 'Images/' + cnames[i]
    country_abbrev = os.path.basename(curls[i].rstrip('/'))
    nvft.mkdir(country_dir)
    ####
    lurls,lnames = get_location_urls(curls[i])
    #
    #sys.stdout.flush()
    #print("all lurls")
    #print(lurls)
    #print("all lurls")
    #sys.stdout.flush()
    #
    ####
    try:
        content_location_md = nvft.read_file_content(fn='../'+country_abbrev+'.loc.dict',op='r')
    except:
        location_md = creat_location_md(lurls,lnames)
        nvft.write_to_file(fn='../'+country_abbrev+'.loc.dict',content=json.dumps(location_md),op='w+')
    else:
        location_md = json.loads(content_location_md)
    ####
    if(i == istart):
        pass
    else:
        jstart = 0
    for j in range(jstart,lurls.__len__()):
        #
        sys.stdout.flush()
        print('lurl j:')
        print(j)
        print(lurls[j])
        print('lurl j:')
        sys.stdout.flush()
        #
        loc_dir = country_dir + '/' + lnames[j]
        nav_urls =  get_nav_urls(lurls[j])
        nvft.mkdir(loc_dir)
        if(j == jstart):
            pass
        else:
            kstart = 0
        for k in range(kstart,nav_urls.__len__()):
            #
            sys.stdout.flush()
            print('nav_url k:')
            print(k)
            print(nav_urls[k])
            print('nav_url k:')
            sys.stdout.flush()
            #
            nav_url = nav_urls[k]
            locsp_urls = get_locsp_urls(nav_url)
            ####
            #sys.stdout.flush()
            #print(nav_url)
            #pobj(locsp_urls)
            #sys.stdout.flush()
            ####
            if(k == kstart):
                pass
            else:
                xstart = 0   
            for x in range(xstart,locsp_urls.__len__()):
                locsp_url = locsp_urls[x]
                img_urls,thumbnail_urls = get_img_urls(locsp_url)
                ####
                sys.stdout.flush()
                print('locsp_url x:')
                print(x)
                print(locsp_url)
                print('locsp_url x:')
                #pobj(img_urls)
                sys.stdout.flush()
                ####
                if(x == xstart):
                    pass
                else:
                    ystart = 0
                for y in range(ystart,img_urls.__len__()):
                    #
                    sys.stdout.flush()
                    print('img_url y:')
                    print(y)
                    print(img_urls[y])
                    print('img_url y:')
                    sys.stdout.flush()
                    #
                    img_url = img_urls[y]
                    thumbnail_url = thumbnail_urls[y]
                    location = os.path.basename(locsp_url)
                    info = get_img_info(img_url,thumbnail_url,country_abbrev,location)
                    nvft.write_to_file(fn='../phnum.record',content=str(info['seq']),op='w+')
                    if(info['seq'] > total):
                        total = info['seq']
                    nvft.write_to_file(fn=info['info_name'],content=json.dumps(info),op='w+')
                    info_container,records_container = taxonomy_init()
                    info_container['url'] = info['img_url']
                    ####
                    sleep_cnt = 0
                    while(1):
                        sleep_cnt = sleep_cnt + 1
                        if(sleep_cnt > 30):
                            sleep_cnt = 30
                        else:
                            pass
                        try:
                            info_container = nvsoli.walkon(info_container,records_container=records_container)
                            info_container = nvsoli.auto_redireced(info_container,records_container)
                        except:
                            time.sleep(10 * sleep_cnt)
                        else:
                            break
                    ####
                    #sys.stdout.flush()
                    #print(info['img_name'])
                    #print(info['seq'])
                    #print(info['index'])
                    #print(info['img_url'])
                    #print(info_container['resp_body_bytes'][:50])
                    #sys.stdout.flush()
                    ####
                    nvft.write_to_file(fn=info['img_name'],content=info_container['resp_body_bytes'],op='wb+')
                    
                    info_container,records_container = taxonomy_init()
                    info_container['url'] = info['thumbnail_url']
                    ####
                    #info_container = nvsoli.walkon(info_container,records_container=records_container)
                    #info_container = nvsoli.auto_redireced(info_container,records_container)
                    sleep_cnt = 0
                    while(1):
                        print("================")
                        print(info_container['url'])
                        print("================")
                        sleep_cnt = sleep_cnt + 1
                        if(sleep_cnt > 30):
                            sleep_cnt = 30
                        else:
                            pass
                        try:
                            info_container = nvsoli.walkon(info_container,records_container=records_container)
                            info_container = nvsoli.auto_redireced(info_container,records_container)
                        except:
                            time.sleep(10 * sleep_cnt)
                        else:
                            break
                    ####
                    try:
                        nvft.write_to_file(fn=info['thumbnail_name'],content=info_container['resp_body_bytes'],op='wb+')
                    except:
                        print(info_container['resp_body_bytes'])
                        exit()
                    else:
                        pass
                    nvft.write_to_file(fn='../seq.record',content=json.dumps({'istart':i,'jstart':j,'kstart':k,'xstart':x,'ystart':y}),op='w+')
                    shell_CMDs = {}
                    shell_CMDs[1] = 'ln -s ' + info['img_name'].replace('../',work_dir) + ' ' + loc_dir
                    nvsh.pipe_shell_cmds(shell_CMDs)

nvft.write_to_file(fn='../total.record',content=str(total),op='w+')

