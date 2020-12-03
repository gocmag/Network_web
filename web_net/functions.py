def binary(object):
    for address in object:
        network_binary = bin(int(address))
        finaly_network_bynary = int(network_binary, 2)
        break
    return finaly_network_bynary