import pandas as pd
import json
import requests
from holotools.ostools import getparent
import boto3
from boto3 import client

def s3_download(file_name,bucket,s3_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket, s3_name, file_name)
def s3_upload(file_name,bucket,s3_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket, s3_name)

root ='https://us.elabjournal.com/api/v1/'
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
def api_key():
    df = pd.read_csv(getparent()+'/.api.tsv', sep = '\t')
    api_key = df['password'][0]
    return api_key
def api(request, api_key=api_key(), root=root):
    try:
        return json.loads(requests.get(root+request, headers={'Authorization': api_key, 'Accept': 'application/json'}).text)
    except:
        return requests.get(root+request, headers={'Authorization': api_key}).text
def parse_excel(expJournalID):
    #needs openpyxl not xlrd
    import pandas as pd
    data = requests.get('https://us.elabjournal.com/api/v1/experiments/sections/%i/excel'%expJournalID, headers={'Authorization': api_key()})
    out = open('ex.xlsx','wb')
    for i in list(data):
        out.write(i)
    out.close()
    dfs = []
    i=0
    go = True
    while go == True:
        try:
            dfs.append(pd.read_excel('ex.xlsx',engine='openpyxl',sheet_name=i))
            i+=1
        except:
            go=False
    return dfs, data
def fill_passport(mymodels):
    # mini = mymodels[0].objects.filter(ministock_name='HD4_9G2')
    mini = mymodels[1].objects.all()
    # wgs  = mymodels[2].objects.all()
    # connect ministocks
    for i in mini:
        if i.ministock_name is not None:
            try:
                p = mymodels[3].objects.get(identity=i.ministock_name)
                print('found')
            except:
                p = mymodels[3].objects.create(identity=i.ministock_name,
                                        hb = i.hb,
                                        holobiome_owned=True)
                p.consensus.add(i)
        else:
            if i.hb is not None:
                try:
                    p = mymodels[3].objects.get(identity='HB-'+str(i.hb))
                    print('found')
                except:
                    p = mymodels[3].objects.create(identity='HB-'+str(i.hb),
                                            hb = i.hb,
                                            holobiome_owned=True)
                    p.consensus.add(i)
            print('except')
            print(p)
        # # try connect cons
        # if p.hb is not None:
        #     try:
        #         q= mymodels[1].objects.filter(hb=p.hb)
        #         if len(q)>0:
        #             for mq in q:
        #                 print(type(mq))
        #                 p.consensus.add(mq)
        #                 'con has been added'
        #     except:
        #         print('no con')
        # else:
        #     try:
        #         q= mymodels[1].objects.filter(ministock_name=p.identity)
        #         if len(q)>0:
        #             for mq in q:
        #                 p.consensus.add(mq)
        #                 print(mq)
        #     except:
        #         print('no con')
        # connect to wgs
        if p.hb is not None:
            try:
                q= mymodels[2].objects.filter(hb=p.hb)
                if len(q)>0:
                    for mq in q:
                        p.wgs.add(mq)
            except:
                print('no wgs')
        else:
            try:
                print('here b')
                q= mymodels[2].objects.filter(ministock_name=p.identity)
                print(q)
                if len(q)>0:
                    for mq in q:
                        p.wgs.add(mq)
                        print(mq)
            except:
                print('no wgs')
        p.save()
        print(p)
    d = {'passports':mymodels[3].objects.all()}
    return d
def sync(tmp):
    # sync experiments
    exp = api('experiments')
    exp = exp['data']
    for i in exp:
        # get or create our experiments in our own database
        q = Experiment.objects.get(experiment_id=i['experimentID'])
        if len(q)>0:
            expobj = Experiment.objects.get(experiment_id=i['experimentID'])[0]
        else:
            expobj = Experiment.create(experiment_id = i['experimentID'])
        # now go through the sections
        sections = api('experiments/'+str(i['experimentID'])+'/sections')
        for section in sections['data']:
            # get or create section in our own database
            q = Section.objects.get(section_id=section['expJournalID'])
            if len(q)>0:
                secobj = Experiment.objects.get(experiment_id=section['expJournalID'])[0]
            else:
                secobj = Section.create(section_id = section['expJournalID'])
            secobj.order = section['order']
            secobj.stype = section['sectionType']
            stype = section['sectionType']
            # each section will be handled slightly differently
            if stype == 'PARAGRAPH' or stype == 'PROCEDURE':
                # get html
                html = api('experiments/sections/%i/html'%section['expJournalID'])
                # source images
                eln_src ="https://us.elabjournal.com/members/experiments/journal/authloader.ashx?fileID="
                if eln_src in html:
                    sp = html.split()
                    r = []
                    for j in sp:
                        #get image id
                        if eln_src in j:
                            start = j.index('fileID')+7
                            start = j[start:]
                            new = ''
                            for m in start:
                                if m.isnumeric():
                                    new+=m
                                else:
                                    break
                            r.append('<img src="https://holotools.s3.amazonaws.com/static/passport/images/eln/%s">'%new)
                        else:
                            r.append(j)
                        html = ' '.join(r)
                        secobj.html = html
                        #download image
                        if new!='':
                            im = requests.get(eln_src+'/'+str(new), headers = {'Authorization': api_key(), 'Accept': 'application/json'}, stream=True).raw
                            out = open(tmp+'/'+new,'wb')
                            for i in list(im):
                                out.write(i)
                            out.close()
                            #put image in s3
                            file = open(tmp+'/'+str(section['expJournalID'],'r'))
                            fileobj = Image.create(str(section['expJournalID']),File(file))
                            secobj.images.add(fileobj)
                            os.remove(tmp+'/'+new)
                # try to add samples that are hb or hd
                for t in (strip_tags(html)).split():
                    t = t.lower()
                    if 'hb' in t.lower():
                        pasobj = Passport.objects.get(hb=int(j.replace('hb').replace('-')))
                    elif 'hd' in t.lower():
                        pasobj = Passport.objects.get(ministock__name=j)
                    try:
                        if len(pasobj)>0:
                            expobj.add(pasobj[0])
                    except:
                        print('no go')
            if stype == 'SAMPLESIN' or stype =='SAMPLESOUT':
                sam = api('sections/%i/samples'%section['expJournalID'])
                for i in sam:
                    sp = i['name'].split()
                    for j in sp:
                        j = sp.lower()
                        if 'hb' in j:
                            pasobj = Passport.objects.get(hb=int(j.replace('hb').replace('-')))
                        elif 'hd' in j:
                            pasobj = Passport.objects.get(ministock__name=j)
                        elif len(Passport.objects.get(altnames__name=j))>0:
                            pasobj = Passport.objects.get(altnames__name=j)
                        else:
                            pasobj = Passport.objects.get(identity=j)
                    if len(pasobj)>0:
                        expobj.samples.add(pasobj[0])
            if stype == 'EXCEL':
                from django.core.files import File
                data = requests.get('https://us.elabjournal.com/api/v1/experiments/sections/%i/excel'%section['expJournalID'], headers={'Authorization': api_key()})
                out = open(tmp+'/'+str(section['expJournalID']),'wb')
                for i in list(data):
                    out.write(i)
                out.close()
                file = open(tmp+'/'+str(section['expJournalID'],'r'))
                fileobj = Excel_File.create(str(section['expJournalID']),File(file))
                secobj.files.add(fileobj)
                os.remove(tmp+'/'+new)
            if stype == 'FILE':
                data = api('experiments/sections/%i/files/'%section['expJournalID'])['data']
                for d in data:
                    data = requests.get('https://us.elabjournal.com/api/v1/experiments/sections/%i/files/%i'%(section['expJournalID'],d['experimentFileID']), headers={'Authorization': api_key()})
                    out = open(tmp+'/'+str(section['experimentFileID']),'wb')
                    for i in list(data):
                        out.write(i)
                    out.close()
                    file = open(tmp+'/'+str(d['experimentFileID'],'r'))
                    fileobj = Section_File.create(str(d['experimentFileID']),File(file))
                    secobj.files.add(fileobj)
                    os.remove(tmp+'/'+new)
            if stype == 'IMAGE':
                data = api('experiments/sections/%i/images/'%section['expJournalID'])['data']
                for d in data:
                    data = requests.get('https://us.elabjournal.com/api/v1/experiments/sections/%i/files/%i'%(section['expJournalID'],d['experimentFileID']), headers={'Authorization': api_key()})
                    out = open(tmp+'/'+str(section['experimentFileID']),'wb')
                    for i in list(data):
                        out.write(i)
                    out.close()
                    file = open(tmp+'/'+str(d['experimentFileID'],'r'))
                    fileobj = Image.create(str(d['experimentFileID']),File(file))
                    secobj.files.add(fileobj)
                    os.remove(tmp+'/'+new)
            if stype == 'DATATABLE':
                print('not done yet')
            if stype == 'COMMENT':
                print('not done yet')
            secobj.save()
        expobj.save()
    # next up samples
