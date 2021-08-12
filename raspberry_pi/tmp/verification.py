import global_var

def verify(client_sock):
    # verified
    global_var.verified = 1
    global_var.verified_sock = client_sock
    return True