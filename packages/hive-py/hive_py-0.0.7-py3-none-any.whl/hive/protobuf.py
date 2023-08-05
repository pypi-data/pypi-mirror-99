def protobuf_encoder(_, obj):
    return obj.SerializeToString()


def protobuf_decoder(cls, bytes):
    obj = cls()
    obj.ParseFromString(bytes)
    return obj
