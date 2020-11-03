# import bcrypt
# password = "super secret password"
# # Hash a password for the first time, with a randomly-generated salt

# st = bcrypt.gensalt()
# print st

# hashed = str(bcrypt.hashpw(password, st))
# print hashed
# # Check that an unhashed password matches one that has previously been
# # hashed
# if bcrypt.checkpw(password, hashed):
# 	print("It Matches!")
# else:
# 	print("It Does not Match :(")

# print "==============================================="


import hashlib
import bcrypt

password = 'a@pinto'
h = hashlib.md5(password.encode())
print (h.hexdigest())
print (type(h.hexdigest()))

dynamic_salt = bcrypt.gensalt()
static_salt="#ANTS@!%"
password = "d@user"
salted_password = static_salt + password
hashed = bcrypt.hashpw(salted_password.encode('utf8'),bcrypt.gensalt())
print ("hash is : ", hashed)
print (dynamic_salt)
