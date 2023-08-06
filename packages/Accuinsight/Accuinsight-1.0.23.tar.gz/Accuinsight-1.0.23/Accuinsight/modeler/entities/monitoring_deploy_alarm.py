from Accuinsight.modeler.entities._modeler_object import _ModelerObject


class DeployAlarm(_ModelerObject):
    """
        Deploy alarm parameter object.
    """
    def __init__(self):
        self._message = None
        self._notifiers = dict()

    @property
    def message(self):
        """alarm message to send"""
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    @property
    def notifiers(self):
        """alarm notifier list"""
        return self._notifiers

    @notifiers.setter
    def notifiers(self, notifiers):
        self._notifiers = notifiers

    @classmethod
    def from_proto(cls, proto):
        pass

    def get_alarm_param(self):
        """Create and return backend API parameter"""
        import json

        if self.message is None:
            raise Exception("message cannot be None")

        data = dict()

        data['message'] = self.message
        data['notifiers'] = self.notifiers

        return json.dumps(data)
