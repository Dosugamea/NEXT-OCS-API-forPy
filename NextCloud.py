import requests

class Req():
    #WrapRequests
    def rtn(self,resp):
        return resp.json()
    def get(self,ur):
        res = requests.get(ur,auth=self.auth_pk,headers=self.h_get)
        return self.rtn(res)
    def post(self,ur,dt=None):
        if dt == None: res = requests.post(ur,auth=self.auth_pk,headers=self.h_post)
        else: res = requests.post(ur,auth=self.auth_pk,data=dt,headers=self.h_post)
        return self.rtn(res)
    def put(self,ur,dt=None):
        if dt == None: res = requests.put(ur,auth=self.auth_pk,headers=self.h_post)
        else: res = requests.put(ur,auth=self.auth_pk,data=dt,headers=self.h_post)
        return self.rtn(res)
    def delete(self,ur,dt=None):
        if dt == None: res = requests.delete(ur,auth=self.auth_pk,headers=self.h_post)
        else: res = requests.delete(ur,auth=self.auth_pk,data=dt,headers=self.h_post)
        return self.rtn(res)
        
class GroupFolders():
    #/ocs/v2.php/apps/groupfolders/folders
    def getGroupFolders(self):
        print(GroupFolders.url+self.tojs)
        return self.get(GroupFolders.url+self.tojs)
    def createGroupFolder(self,mountpoint):
        return self.post(GroupFolders.url+self.tojs,{"mountpoint":mountpoint})
    def deleteGroupFolder(self,fid):
        return self.delete(GroupFolders.url+"/"+str(fid)+self.tojs)
    def giveAccessToGroupFolder(self,fid,gid):
        return self.post(GroupFolders.url+"/"+fid+"/"+gid+self.tojs)
    def deleteAccessToGroupFolder(self,fid,gid):
        return self.delete(GroupFolders.url+"/"+fid+"/"+gid+self.tojs)
    def setAccessToGroupFolder(self,fid,gid,permissions):
        return self.post(GroupFolders.url+"/"+fid+"/"+gid+self.tojs,{"permissions":permissions})
    def setQuotaOfGroupFolder(self,fid,quota):
        return self.post(GroupFolders.url+"/"+fid+"/quota"+self.tojs,{"quota":quota})
    def renameGroupFolder(self,fid,mountpoint):
        return self.post(GroupFolders.url+"/"+fid+"/mountpoint"+self.tojs,{"mountpoint":mountpoint})        

class Share():
    #/ocs/v2.php/apps/files_sharing/api/v1
    def getShares(self):
        return self.get(Share.url + "/shares" + self.tojs)
    def getSharesFromPath(self,path=None,reshares=None,subfiles=None):
        if path == None: return False
        url = Share.url + "/shares/" + path
        added = False
        if reshares != None:
            if added == False:
                url += "?"
                added = True
            url += "reshares=true"
        if subfiles != None:
            if added == False: url += "?"
            else: url += "&"
            url += "subfiles=true"
        return self.get(url+self.tojs)
    def getShareInfo(self,sid):
        return self.get(Share.url+"/shares/"+sid+self.tojs)
    def createShare(self,path,shareType,shareWith=None,publicUpload=None,password=None,permissions=None):
        url = Share.url + "/shares"+self.tojs
        if publicUpload == True: publicUpload = "true"
        if (path == None or isinstance(shareType, int) != True) or (shareType in [0,1] and shareWith == None): return False
        msg = {"path":path,"shareType":shareType}
        if shareType in [0,1]: msg["shareWith"] = shareWith
        if publicUpload == True: msg["publicUpload"] = publicUpload
        if shareType == 3 and password != None: msg["password"] = str(password)
        if permissions != None: msg["permissions"] = permissions
        return self.post(url,msg)
    def deleteShare(self,sid):
        return self.delete(Share.url+"/shares/"+sid+self.tojs)
    def updateShare(self,sid,permissions=None,password=None,publicUpload=None,expireDate=None):
        if permissions == None and password==None and publicUpload == None and expireDate == None: return False
        msg = {}
        if permissions != None: msg["permissions"] = permissions
        if password != None: msg["password"] = str(password)
        if publicUpload == True: msg["publicUpload"] = "true"
        if publicUpload == False: msg["publicUpload"] = "false"
        if expireDate != None: msg["expireDate"] = expireDate
        return self.put(Share.url+"/shares/"+sid+self.tojs,msg)
    def listAcceptedFederatedCloudShares(self):
        return self.get(Share.url+"/remote_shares"+self.tojs)
    def getKnownFederatedCloudShare(self,sid):
        return self.get(Share.url+"/remote_shares/"+str(sid)+self.tojs)
    def deleteAcceptedFederatedCloudShare(self,sid):
        return self.delete(Share.url+"/remote_shares/"+str(sid)+self.tojs)
    def listPendingFederatedCloudShares(self,sid):
        return self.get(Share.url+"/remote_shares/pending"+self.tojs)
    def acceptPendingFederatedCloudShare(self,sid):
        return self.post(Share.url+"/remote_shares/pending/"+str(sid)+self.tojs)
    def declinePendingFederatedCloudShare(self,sid):
        return self.delete(Share.url+"/remote_shares/pending/"+str(sid)+self.tojs)

class Apps():
    #/ocs/v1.php/cloud/apps
    def getApps(self,filter=None):
        if filter == True:  return self.get(Apps.url + "?filter=enabled"+self.tojs)
        elif filter == False:  return self.get(Apps.url + "?filter=disabled"+self.tojs)
        return self.get(Apps.url+self.tojs)
    def getApp(self,aid):
        return self.get(Apps.url + "/" + aid+self.tojs)
    def enableApp(self,aid):
        return self.post(Apps.url + "/" + aid+self.tojs)
    def disableApp(self,aid):
        return self.delete(Apps.url + "/" + aid+self.tojs)       
        
class Group():
    #/ocs/v1.php/cloud/groups
    def getGroups(self,search=None,limit=None,offset=None):
        url = Group.url
        if search != None or limit != None or offset != None:
            url+= "?"
            added = False
            if search != None:
                url+="search="+search
                added = True
            if limit != None:
                if added == False: url += "&"
                url+="limit="+limit
                added = True
            if offset != None:
                if added == False: url += "&"
                url+="offset="+offset
                added = True
        url += self.tojs
        return self.get(url)
    def addGroup(self,gid):
        url = Group.url + self.tojs
        msg = {"groupid":gid}
        return self.post(url,msg)
    def getGroup(self,gid):
        return self.get(Group.url + "/"+ gid + self.tojs)
    def getSubAdmins(self,gid):
        return self.get(Group.url + "/" + gid + "/subadmins")
    def deleteGroup(self,gid):
        return self.delete(Group.url + "/" + gid)

class User():
    #/ocs/v1.php/cloud/users
    def addUser(self,uid,passwd):
        msg = {'userid':uid,'password':passwd}
        return self.post(User.url + self.tojs,msg)
    def getUsers(self,search=None,limit=None,offset=None):
        url = User.url
        if search != None or limit != None or offset != None:
            url+= "?"
            added = False
            if search != None:
                url+="search="+search
                added = True
            if limit != None:
                if added == False: url += "&"
                url+="limit="+limit
                added = True
            if offset != None:
                if added == False: url += "&"
                url+="offset="+offset
                added = True
        url+= self.tojs
        return self.get(url)
    def getUser(self,uid):
        return self.get(User.url + "/" + uid + self.tojs)
    def editUser(self,uid,email=None,quota=None,displayname=None,phone=None,address=None,website=None,twitter=None,password=None):
        url = User.url + "/" + uid + self.tojs
        msg = {}
        if email != None:
            msg = {'key':"email",'value':email}
            self.put(url,msg)
        if quota != None:
            msg = {'key':"quota",'value':quota}
            self.put(url,msg)
        if phone != None:
            msg = {'key':"phone",'value':phone}
            self.put(url,msg)
        if address != None:
            msg = {'key':"address",'value':address}
            self.put(url,msg)
        if website != None:
            msg = {'key':"website",'value':website}
            self.put(url,msg)
        if twitter != None:
            msg = {'key':"twitter",'value':twitter}
            self.put(url,msg)
        if displayname != None:
            msg = {'key':"displayname",'value':displayname}
            self.put(url,msg)
        if password != None:
            msg = {'key':"password",'value':password}
            self.put(url,msg)
        if msg != {}:
            return True
        else:
            return False
    def disableUser(self,uid):
        return self.put(User.url + "/" + uid + "/disable" + self.tojs)
    def enableUser(self,uid):
        return self.put(User.url + "/" + uid + "/enable" + self.tojs)
    def deleteUser(self,uid):
        return self.delete(User.url + "/" + uid + self.tojs)
    def addToGroup(self,uid,gid):
        url = User.url + "/" + uid + "/groups" + self.tojs
        msg = {'groupid':gid}
        return self.post(url,msg)
    def removeFromGroup(self,uid,gid):
        url = User.url + "/" + uid + "/groups" + self.tojs
        msg = {'groupid':gid}
        return self.delete(url,msg)
    def createSubAdmin(self,uid,gid):
        url = User.url + "/" + uid + "/subadmins" + self.tojs
        msg = {'groupid':gid}
        return self.post(url,msg)
    def removeSubAdmin(self,uid,gid):
        url = User.url + "/" + uid + "/subadmins" + self.tojs
        msg = {'groupid':gid}
        return self.delete(url,msg)
    def getSubAdminGroups(self,uid):
        return self.get(User.url + "/" + uid + "/subadmins" + self.tojs)
    def resendWelcomeMail(self,uid):
        return self.post(User.url + "/" + uid + "/welcome" + self.tojs)

class NextCloud(Req,User,Group,Apps,Share,GroupFolders):
    '''
    OCS StatusCode
        100 - successful
        996 - server error
        997 - not authorized
        998 - not found
        999 - unknown error
    Parameters
        uid -> UserID(UserName)
        gid -> GroupID(GroupName)
        aid -> AppID(ApplicationName)
        sid -> ShareID
        fid -> FolderID
        
        Quota
            -3 -> Unlimited
        ShareType
            0 -> user
            1 -> group
            3 -> publicLink
            6 -> federated cloud share
        Permissions
            1  -> read
            2  -> update
            4  -> create
            8  -> delete
            16 -> share
            31 -> all
        expireDate -> String e.g "YYYY-MM-DD"
    '''
    def __init__(self,endpoint,user,passwd,js=False):
        if js == True: self.tojs = "?format=json"
        else: self.tojs = ""
        self.endpoint = endpoint
        User.url = endpoint + "/ocs/v1.php/cloud/users"
        Group.url = endpoint + "/ocs/v1.php/cloud/groups"
        Share.url = endpoint + "/ocs/v2.php/apps/files_sharing/api/v1"
        Apps.url = endpoint + "/ocs/v1.php/cloud/apps"
        GroupFolders.url = endpoint + "/ocs/v2.php/apps/groupfolders/folders"
        self.h_get = {"OCS-APIRequest": "true"}
        self.h_post = {"OCS-APIRequest":"true","Content-Type":"application/x-www-form-urlencoded"}
        self.auth_pk = (user, passwd)
