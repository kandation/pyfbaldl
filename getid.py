import requests
import codecs
import json
import pprint
import shutil
import os

#
#!!! Important !!!! Don't forget create token
#
#--------- Setting ---------
facebook_token = ""
user = ""

pp = pprint.PrettyPrinter(indent=2)
higData = {'user':"", 'id':0, 'name':"", 'count':0}

def conn(user, comm):

    hd = {"Authorization": "OAuth " + facebook_token}
    url = "https://graph.facebook.com/v2.7/"+comm
    r = requests.get(url, headers=hd)
    return json.loads(r.text, encoding='utf-8')

def show_menu():
    print("Select Menu")
    print("1. scan ablum")

def menu(user):
    show_menu()
    mid = int(input())
    #mid = 1
    if(mid == 1):
        box = getPhotoInAlbum(user, getAlbum(user))
        #print(box)
        downloadInlist(box)
    else:
        pass

def getComm(node, field):
    return str(node)+"?fields="+str(field)


def getAlbum(user):

    comm = getComm(user, "albums.limit(999){count,name}")
    js = conn(user, comm)

    i = 0
    albumBox = {'name':[], 'id':[], 'count':[]}
    print("\n-------- " + user + " album ------------")
    for uu in js['albums']['data']:
        if (uu['name'] != "Cover Photos" and uu['name'] != "Timeline Photos" and uu['name'] != "Profile Pictures" and
                    uu['name'] != "Untitled Album" and uu['name'] != "Mobile Uploads"):
            i = i + 1
            albumBox['id'].append(uu['id'])
            albumBox['name'].append(uu['name'])
            albumBox['count'].append(uu['count'])
            print(str(i) + "  " + uu['name'] + " (" + str(uu['count']) + ")(" + str(uu['id']) + ")")

    print("----------------------------------------")


    dla = int(input("Download album No. : "))
    #dla = 1
    if(dla >0 and dla <= len(albumBox['id'])):
        higData['name'] = albumBox['name'][dla-1]
        higData['id'] =  albumBox['id'][dla-1]
        higData['count'] = albumBox['count'][dla-1]
        return albumBox['id'][dla-1]
    else:
        print("Not in order")
        return 0

def getPhotoInAlbum(user, aid):
    comm = getComm(aid+"/photos", "images&limit=9999")
    print("Select : "+str(higData['id'])+' '+higData['name'])
    data = conn("", comm)

    listData = []

    for uu in data['data']:
        templist = []
        #find Maximum size
        for kk in uu['images']:
            templist.append(kk['height']+kk['width'])

        num = templist.index(max(templist))
        listData.append([uu['id'],uu['images'][0]['source']])
        #return id and url
    return listData

def getFileOnInternet(name,url):
    response = requests.get(url, stream=True)
    ty = response.headers['Content-Type'].split('/', 1)
    rt = {'jpeg': 'jpg', 'png': 'png'}
    ty = rt[ty[1]]
    print("downloading: "+name+'.'+ty)
    with open(str(name)+'.'+ty, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    #del response

def downloadInlist(listA):
    z = len(str(len(listA)))
    os.mkdir(higData['name'])
    os.chdir(higData['name'])
    for num in range(len(listA)):
        getFileOnInternet(str(num).zfill(z)+'_'+str(listA[num][0]), listA[num][1])





menu(user)





#pp.pprint()