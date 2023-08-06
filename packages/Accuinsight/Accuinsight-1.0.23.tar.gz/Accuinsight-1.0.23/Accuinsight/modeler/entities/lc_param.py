import sys

from Accuinsight.modeler.entities._modeler_object import _ModelerObject
from Accuinsight.modeler.protos.service_pb2 import Param as ProtoParam


class Param(_ModelerObject):
    """
    Parameter object.
    """

    def __init__(self, key, value):
        if "pyspark.ml" in sys.modules:
            import pyspark.ml.param
            if isinstance(key, pyspark.ml.param.Param):
                key = key.name
                value = str(value)
        self._key = key
        self._value = value

    @property
    def key(self):
        """String key corresponding to the parameter name."""
        return self._key

    @property
    def value(self):
        """String value of the parameter."""
        return self._value

    def to_proto(self):
        param = ProtoParam()
        param.key = self.key
        param.value = self.value
        return param

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.key, proto.value)
