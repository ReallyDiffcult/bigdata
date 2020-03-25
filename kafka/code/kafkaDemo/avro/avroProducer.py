import os
from io import BytesIO
from kafka import KafkaProducer
from kafka.errors import KafkaError
import avro.schema
from avro.io import DatumReader, DatumWriter, BinaryDecoder, BinaryEncoder
import json


class AvroUtils(object):
    """avro序列化接口
    """

    REQUEST_SCHEMA = {}
    RESPONSE_SCHEMA = {}
    ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname('__file__'), '..'))
    REQUEST_AVSC = os.path.join(ROOT_PATH, 'avro', 'user.avsc')
    RESPONSE_AVSC = os.path.join(ROOT_PATH, 'avro', 'user.avsc')

    @classmethod
    def init_schma(cls, request_file='', response_file=''):
        request_file = request_file or cls.REQUEST_AVSC
        response_file = response_file or cls.RESPONSE_AVSC

        if os.path.exists(request_file) is False:
            raise Exception('File {} is not Exist!'.format(request_file))
        if os.path.exists(response_file) is False:
            raise Exception('File {} is not Exist!'.format(response_file))

        with open(request_file, 'r') as fp:
            cls.REQUEST_SCHEMA = avro.schema.parse(fp.read())
        with open(response_file, 'r') as fp:
            cls.RESPONSE_SCHEMA = avro.schema.parse(fp.read())

    @classmethod
    def avro_encode(cls, json_data, schema=None):
        """avro 序列化json数据为二进制
        :param json_data:
        :param schema:
        :return:
        """
        bio = BytesIO()
        binary_encoder = BinaryEncoder(bio)
        dw = DatumWriter(schema or cls.RESPONSE_SCHEMA)
        dw.write(json_data, binary_encoder)
        return bio.getvalue()

    @classmethod
    def avro_decode(cls, binary_data, schema=None):
        """avro 反序列化二进制数据为json
        :param binary_data:
        :param schema:
        :return:
        """
        bio = BytesIO(binary_data)
        binary_decoder = BinaryDecoder(bio)
        return DatumReader(schema or cls.REQUEST_SCHEMA).read(binary_decoder)

AvroUtils.init_schma()
producer = KafkaProducer(bootstrap_servers='hdp4.buptnsrc.com:6667')
import time
for i in range(100):
# while True:
#     value = "yangkun" + str(i)
    value = "yangkun"
    message = AvroUtils.avro_encode({"name":value})
    future = producer.send("test_first", message)
    # future = producer.send("test_first", bytes(value,encoding="utf-8"))
producer.flush()
producer.close()