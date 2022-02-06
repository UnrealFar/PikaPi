import random, string, base64, time

def new_token(userid: int):
    u = str(base64.b64encode(str(userid).encode()))[2:-1]
    e = str(base64.b64encode(str().join(random.sample(string.ascii_letters, 4)).encode()))[2:-1]
    v = str(base64.b64encode(str(time.time()).encode()))[2:-1]
    return ".".join([u, e, v])
