import urllib
import urllib2
import base64
class login:
    def __init__(self,Username,Password):
        self.Url = 'https://gw.buaa.edu.cn:803/include/auth_action.php'
        Password=base64.b64encode(Password)
        L=list(Password)
        for a in range(len(L)):
           if L[a]=='=':
               L[a]='%3D'
        Password=''.join(L)
        self.Data = 'action=login&username='+Username+'&password={B}'+Password+'&ac_id=4&user_ip=&nas_ip=&user_mac=&save_me=1&ajax=1'
    def auto_login(self):
        request = urllib2.Request(url=self.Url,data=self.Data)
        response = urllib2.urlopen(request)
        print response.read()

#####################################################
Buaa = login(Username='by1206148',Password='19880207')
Buaa.auto_login()
