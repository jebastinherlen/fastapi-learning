import bcrypt

password = "mypassword"

hased_password = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())

print(hased_password)