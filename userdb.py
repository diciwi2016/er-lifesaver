import hashlib

def verify(u,p):
    d={}
    uname=str(u)
    pwd=str(p)
    f=open('database.txt','r').read().strip().split("\n")
    for i in range(len(f)):
        f[i] = f[i].split("|")
    for i in f:
        d[i[0]]=i[1]
    if uname in d:
        if d[uname]==password_hash(pwd):
            return True
        else:
            print 'wrong pass'
            return False
    else:
        print 'cant find uname'
        return False

def add(uname, pwd):
    f=open('database.txt','a')
    f.write(uname + "|" + password_hash(pwd) +  "\n")
    f.close()
    return True

def password_hash(password):
    # Hash alg:
    m = hashlib.md5()
    m.update(password)
    hashpass = m.hexdigest()
    return hashpass


if __name__ == "__main__":
    if str(raw_input("Add user? ")) == "YES":
        username = str(raw_input("New username: "))
        password = str(raw_input("New password: "))
        f = open("database.txt", 'a')
        add(username, password)
        f.close()
