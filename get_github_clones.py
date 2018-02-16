import requests
from requests.auth import HTTPBasicAuth
import json
import pickle 
import sys
import os
from urllib import FancyURLopener

def initialize_repo(repo):
    if os.path.exists(repo+'_clones.pkl'):
        os.remove(repo+'_clones.pkl')
    g={}
    pickle.dump(g,open(repo+'_clones.pkl','w'))
 
user='apmechev'
#repo="GRID_picastools"

print(sys.argv)
if len(sys.argv)>1:
    repo=sys.argv[1]
else:
    repo="GRID_picastools"

def get_creds(creds_file='git_creds'):
    creds=[]
    with open(creds_file,'r') as auth_file:
        for l in auth_file:
            creds.append(l.strip())
    return creds

if not os.path.exists(repo+'_clones.pkl'):
    initialize_repo(repo)

def get_git_clones(user='apmechev',repo=''):
    creds=get_creds()
    url="https://api.github.com/repos/"+user+"/"+repo+"/traffic/clones"
    output=requests.get(url,auth=HTTPBasicAuth(creds[0],creds[1]))
    if output.__getstate__()['status_code'] != 200:
        if output.__getstate__()['status_code'] == 401:
            print("Invalid Username/Password!")
        elif output.__getstate__()['status_code'] == 403: 
            print("Empty Password!")
        output.raise_for_status()
    return output

glrtc=pickle.load(open(repo+'_clones.pkl','r'))
o=get_git_clones(user,repo)
for i in o.json()['clones']:
    glrtc[i['timestamp']]=i['count']

def count_clones(clonedict):
    s=0
    for i in clonedict.keys():
        s+=clonedict[i]
    if s==0:
        return(str(0),"red")
    if s<10:
        return(str(s),"orange")
    if s<100:
        return(str(s),"yellow")
    if s<1000:
        return(str(s),"yellowgreen")
    elif s<1000000:
        return(str(s/1000)+"K+","green")
    elif s<1000000000:
        return(str(s/1000)+"M+","brightgreen")
    


class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def download_badge(repo,numclones,color='green'):
    mopen = MyOpener()    
    mopen.retrieve("https://img.shields.io/badge/clones-"+str(numclones)+"-"+color+".svg","/var/www/html/apmechev.com/public_html/img/git_repos/"+repo+"_clones.svg")

c,col=count_clones(glrtc)
download_badge(repo,c,col)


pickle.dump(glrtc,open(repo+'_clones.pkl','w'))
