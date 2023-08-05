import msgpack

packer = msgpack.Packer(default=lambda o: o.__dict__)


def msgpack_encoder(cls, obj):
    return packer.pack(obj)


def msgpack_decoder(cls, msg_bytes):
    d = msgpack.unpackb(msg_bytes)
    if type(d) == cls:
        return d

    obj = cls()
    for k, v in d.items():
        setattr(obj, k, v)
    return obj
