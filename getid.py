import requests
import json
import pprint
import shutil
import os
import urllib.request


pp = pprint.PrettyPrinter(indent=2)
higData = {'user': "", 'id': 0, 'name': "", 'count': 0}


def chkErr(js):
    if'error' in js.keys():
        return 1
    else:
        return 0


def conn(user, comm):
    facebook_token = ""
    hd = {"Authorization": "OAuth " + facebook_token}
    url = "https://graph.facebook.com/v2.7/"+comm
    r = requests.get(url, headers=hd)
    res = json.loads(r.text, encoding='utf-8')
    if chkErr(res):
        print('Token Key Error or missing permission and Exit program')
        exit(0)
    else:
        return json.loads(r.text, encoding='utf-8')


def show_menu(type):
    print(" --------- Select Menu ---------- ")
    if type == 1:
        print("1. Download by username")
        print("2. Show Download links")
    else:
        print("1. Download by Album ID")
        print("2. Show Download links")
    print(" -------------------------------- ")


def select_menu():
    user = str(input("Input Page-name/Album Id: ")).strip()
    if user.isnumeric():
        show_menu(2)
    else:
        show_menu(1)

    mm = int(input("Enter number : "))
    return {'menu': mm, 'user': str(user)}


def menu():
    mm = select_menu()
    user = mm['user']
    mid = mm['menu']
    if user.isnumeric():
        if mid == 1:
            x = 1
            while x:
                x = menuB_01(user)
    else:
        if mid == 1:
            x = 1
            while x:
                x = menuA_01(user)
        elif mid == 2:
            x = 1
            while x:
                x = menuA_02(user)
        elif mid == 0:
            return False
        else:
            print("Type 0 for exit")

    return True


def menuA_01(user):
    alid = getAlbum(user)
    if alid:
        box = getPhotoInAlbum(user, alid)
        print(box)
        #downloadInlist(box)
        return 0
    else:
        print("Error Try agine")
        return 1


def menuA_02(user):
    alid = getAlbum(user)
    if alid:
        box = getPhotoInAlbum(user, alid)
        downloadInlist2(box)
        return 0
    else:
        print("Error Try agine")
        return 1


def menuB_01(aid):
    alid = getPhotobyId(aid)
    if alid:
        downloadInlist(alid)
        return 0
    else:
        print("Error Try agine")
        return 1


def getComm(node, field):
    return str(node)+"?fields="+str(field)


def getPhotobyId(id):
    comm = getComm(id, "photos.limit(9999){images,album}")
    js = conn(id, comm)
    albox = []
    try:
        for uu in js['photos']['data']:
            findMaxSize = []
            for ee in uu['images']:
                findMaxSize.append(ee['height']+ee['width'])
            num = findMaxSize.index(max(findMaxSize))
            albox.append([str(uu['id']),str(uu['images'][num]['source'])])
            higData['name'] = uu['album']['name']
    except:
        print("Json Error")
        exit(0)

    return albox


def getAlbum(user):
    comm = getComm(user, "albums.limit(999){count,name}")
    js = conn(user, comm)

    i = 0
    albumBox = {'name': [], 'id': [], 'count': []}
    print("------------ " + user + " album ------------")
    try:
        for uu in js['albums']['data']:
            if (uu['name'] != "Cover Photos" and uu['name'] != "Timeline Photos" and uu[
                'name'] != "Profile Pictures" and
                        uu['name'] != "Untitled Album" and uu['name'] != "Mobile Uploads"):
                i += 1
                albumBox['id'].append(uu['id'])
                albumBox['name'].append(uu['name'])
                albumBox['count'].append(uu['count'])
                print(str(i) + "  " + uu['name'] + " (" + str(uu['count']) + ")(" + str(uu['id']) + ")")
    except:
        print("Error: getAlbum not true")
        exit(0)

    print("------------",end='')
    print("-"*(len(user)+10), end='')
    print("------------")

    while(1):
        dla = int(input("Download album No. : "))
        if 0 < dla <= len(albumBox['id']):
            higData['name'] = albumBox['name'][dla-1]
            higData['id'] = albumBox['id'][dla-1]
            higData['count'] = albumBox['count'][dla-1]
            return albumBox['id'][dla-1]
        elif dla == 0:
            return 0
        else:
            print("Not in order. Try agin! or type 0 for exit")


def getPhotoInAlbum(user, aid):
    comm = getComm(aid+"/photos", "images&limit=9999")
    print("Select : "+str(higData['id'])+' '+higData['name'])
    data = conn("", comm)
    # Process
    listData = []
    for uu in data['data']:
        templist = []
        # find Maximum size
        for kk in uu['images']:
            templist.append(kk['height']+kk['width'])

        num = templist.index(max(templist))
        listData.append([uu['id'],uu['images'][num]['source']])
        # return id and url
    return listData


def getFileOnInternet(name,url):
    # Stream download for large files
    response = requests.get(url, stream=True)
    ty = response.headers['Content-Type'].split('/', 1)
    rt = {'jpeg': 'jpg', 'png': 'png'}
    ty = rt[ty[1]]
    print("downloading: "+name+'.'+ty)
    with open(str(name)+'.'+ty, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def getFileOnInternet2(name,url):
    # one shot downloads
    ty = url.split('/')[-1]
    ty = ty.split('?')[0]
    ty = ty.split('.')[-1]
    print("downloading: "+name+'.'+ty)
    urllib.request.urlretrieve(url, name+'.'+ty)


def downloadInlist(listA):
    # function download file build-in
    z = len(str(len(listA)))
    if not os.path.isdir(higData['name']):
        os.mkdir(higData['name'])
    os.chdir(higData['name'])
    for num in range(len(listA)):
        getFileOnInternet2(str(num).zfill(z)+'_'+str(listA[num][0]), listA[num][1])
    os.chdir('../')


def downloadInlist2(listA):
    # function show links download for another program
    z = len(str(len(listA)))
    for num in listA:
        print(num[1])


def main():
    active = True
    while(active):
        higData = {'user': "", 'id': 0, 'name': "", 'count': 0}
        active = menu()

if __name__ == "__main__":
    main()