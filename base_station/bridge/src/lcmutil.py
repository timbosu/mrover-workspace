import rover_msgs


def decode(lcm_type_str, data):
    lcm_type = getattr(rover_msgs, lcm_type_str)
    return lcm_type.decode(data)


def is_lcm_object(obj):
    return '_get_packed_fingerprint' in dir(obj)


def lcm_to_dict(message):
    res = {}
    for slot in message.__slots__:
        val = getattr(message, slot)
        if is_lcm_object(val):
            res[slot] = lcm_to_dict(val)
        else:
            res[slot] = val
    return res


def dict_to_lcm(message):
    lcm_type = getattr(rover_msgs, message['type'])
    msg = lcm_type()

    for k, v in message.items():
        if k not in msg.__slots__:
            continue
        if isinstance(v, dict):
            v = dict_to_lcm(v)
        setattr(msg, k, v)

    return msg
