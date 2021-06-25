import random


def get_mac_address():
    '''
    functions create random hex number(MAC address)
    :return: hex
    '''
    x = random.randint(100000000000000, 199999999999999)
    mac_address = f'{x:x}'

    # "%02x%02x%02x%02x%02x%02x" % (random.randint(0, 255),
    #                               random.randint(0, 255),
    #                               random.randint(0, 255),
    #                               random.randint(0, 255),
    #                               random.randint(0, 255),
    #                               random.randint(0, 255))

    return mac_address


def get_dev_type():
    '''
    function return random element from tuple
    :return: str
    '''
    dev_types = ('emeter', 'zigbee', 'lora', 'gsm')
    idx = random.randint(0, 3)
    return dev_types[idx]


def get_devices(count):
    list_devices = []
    for el in range(count):
        device = {'dev_id': '', 'dev_type': ''}
        device['dev_id'] = get_mac_address()
        device['dev_type'] = get_dev_type()
        list_devices.append(device)
    return list_devices
