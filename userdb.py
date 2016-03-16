import hashlib

def verify(username, password):
    credentials = list(open("known_users"))
    for user in credentials:
        _user = user.strip().split("|||")
        if _user[0] == username and _user[1] == password_hash(password):
            return True
    return False

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
        f = open("known_users", 'a')
        f.write(username + "|||" + password_hash(password) + "\n")
        f.close()
