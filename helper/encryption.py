import time

def new_token(user_id: int):
    t = str(hex(int(str(time.time()).replace(".", ""))))
    i = str(hex(user_id))
    return (i + t)
