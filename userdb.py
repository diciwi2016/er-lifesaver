import hashlib

##############################
# takes params (username, password)               #
# to verify if username & password matches    #
##############################

def verify(u, p, fname):
    d = {} #dictionary for each user account
    uname = str(u)
    pwd = str(p)
    f = open(fname, 'r').read().strip().split("\n")
    for i in range(len(f)):
        f[i] = f[i].split("|")
    for i in f:
        if len(i) > 1:
            d[i[0]] = i[1] # key: username, value: password
    if uname in d: # match input with dictionary
        if d[uname] == password_hash(pwd):
            return True
        else:
            print 'wrong pass'
            return False
    else:
        print 'cant find uname'
        return False


#########################
# takes param (username, password)   # 
# add user account to database             #
#########################

def add(uname, pwd, fname):
    f = open(fname, 'a')
    f.write(uname + "|" + password_hash(pwd) + "\n")
    f.close()
    return True

def addHospital(uname, pwd, hname, fname):
    f = open(fname, 'a')
    f.write(uname + "|" + password_hash(pwd) + "|" + hname +"\n")
    f.close()
    return True

####################################################
# takes params (username, password, first, last, date of birth, address, state)           #
# updates user information to send to hospitals in database                                       #
####################################################

def update(uname, pwd, fname, lname, dob, loc, state):

    DATA = open('database.txt', 'r')
    File = DATA.read()
    DATA.close()

    index = File.find(uname + "|") + len(uname) + 1
    File = File[:index] + password_hash(pwd) + "|" + fname + "|" + lname + "|" + dob + "|" + loc + "|" + state + File[File[index:-2].find("\n"):]
    #if File[:-2]!="\n":
     #   File+="\n"
    FileW = open('database.txt', 'w')
    FileW.write(File)
    FileW.close()

def hSchedUpdate(uname, pwd, listt):
    DATA = open('hospitaldb.txt', 'r')
    File = DATA.read()
    DATA.close()

    index = File.find(uname + "|") + len(uname) + 1
    File = File[:index] + password_hash(pwd) + "|" + listt[0]+ "|" + listt[1] + "|" + listt[2] + "|" + listt[3]+ "|" +listt[4]+ "|" +listt[5]+ "|" +listt[6]+ "|" +listt[7] + File[File[index:-2].find("\n"):]
    #if File[:-2]!="\n":
     #   File+="\n"
    FileW = open('hospitaldb.txt', 'w')
    FileW.write(File)
    FileW.close()
 
#####################
# takes param (password)           #
# hashes password using md5    #
#####################

def password_hash(password):
    m = hashlib.md5()
    m.update(password)
    hashpass = m.hexdigest()
    return hashpass


#####################
# main method for testing lol     #
#####################
if __name__ == "__main__":
    if str(raw_input("Add user? ")) == "YES":
        username = str(raw_input("New username: "))
        password = str(raw_input("New password: "))
        f = open("database.txt", 'a')
        L =update(username, password, "KKK", "YYY", "03/14/16", "345 Chambers", "NY")
        f.close()
        print L
