import random


def get_processed_strings(str_raw):
    """
    the function gets a string, creates a new one from it only from numbers and letters. Returns it.
    :param str_raw: str
    :return: str
    """
    return "".join(filter(lambda x: x.isalpha() or x.isdigit(), str_raw)).lower()


def get_check(item):
    """
    the function gets an object from two strings, checks whether they are an anagram.
    :param item: object model Anagram
    :return: bool
    """
    str_1_pars = get_processed_strings(item.str_1)
    str_2_pars = get_processed_strings(item.str_2)

    flag = False
    if len(str_1_pars) == len(str_2_pars):
        for el in str_1_pars:
            flag = el in str_2_pars
            if flag is False:
                break
    return flag


def get_mac_address():
    """
    function creates random hex number(MAC address)
    :return: hex
    """
    x = random.randint(100000000000000, 199999999999999)
    mac_address = f'{x:x}'
    ############################################################
    # это второй вариант, более надежный, но более длинный.
    # "%02x%02x%02x%02x%02x%02x" % (random.randint(0, 255),
    #                               random.randint(0, 255),
    #                               random.randint(0, 255),
    #                               random.randint(0, 255),
    #                               random.randint(0, 255),
    #                               random.randint(0, 255))
    #############################################################
    return mac_address


def get_dev_type():
    """
    function returns random element from tuple
    :return: str
    """
    dev_types = ('emeter', 'zigbee', 'lora', 'gsm')
    idx = random.randint(0, 3)
    return dev_types[idx]


def get_devices(count):
    """
    function gets number of objects, creates and returns them
    :param count: int
    :return: list
    """
    list_devices = []
    for el in range(count):
        device = {}
        device['dev_id'] = get_mac_address()
        device['dev_type'] = get_dev_type()
        list_devices.append(device)
    return list_devices
