import string, secrets


def make_password(count):
    special = "!@#$%^&*"
    all_chars = string.ascii_letters + string.digits + special
    return "".join(secrets.choice(all_chars) for _ in range(count))


print(make_password(10))
