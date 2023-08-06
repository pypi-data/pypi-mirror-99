import datetime, json

from Accuinsight.modeler.entities.monitoring_deploy_log import DeployLog
from Accuinsight.modeler.entities.monitoring_deploy_alarm import DeployAlarm
from Accuinsight.modeler.clients.modeler_api import DeployLogRestApi
from Accuinsight.modeler.core.LcConst import LcConst


class AddDeployLog:
    """
        Object for adding deploy log.
    """

    def __init__(self):
        self.deploy_log = DeployLog()
        self.deploy_alarm = DeployAlarm()
        self.deploy_log_api = DeployLogRestApi(LcConst.BACK_END_API_URL,
                                               LcConst.BACK_END_API_PORT,
                                               LcConst.BACK_END_API_URI)
        self.swagger = False

    def set_request(self, request):
        self.deploy_log.start_time = datetime.datetime.now().timestamp()
        self.deploy_log.req_method = request.method
        self.deploy_log.req_url = request.url

        req_data = list()
        if request.data:
            req_data.append(request.data.decode('utf-8'))

        if request.files:
            req_data.append(dict(request.files))

        if request.form:
            req_data.append(dict(request.form))

        if len(req_data) == 1:
            req_str = str(req_data.pop())
        elif len(req_data) == 0:
            req_str = str()
        else:
            req_str = str(req_data)

        try:
            self.deploy_log.req_body = json.loads(req_str)
        except json.decoder.JSONDecodeError:
            self.deploy_log.req_body = req_str

        if "swagger" in request.url:
            self.swagger = True
        else:
            self.swagger = False

    def set_response(self, response):
        response.direct_passthrough = False

        self.deploy_log.end_time = datetime.datetime.now().timestamp()
        self.deploy_log.status_code = str(response.status_code)
        try:
            res_data = response.get_data().decode()
        except UnicodeDecodeError:
            res_data = response.get_data()

        try:
            self.deploy_log.response_data = json.loads(res_data)
        except json.decoder.JSONDecodeError:
            self.deploy_log.response_data = str(res_data)

    def add_log(self, messages, notifiers):
        if not self.swagger:
            if messages is not None:
                self.deploy_alarm.timestamp = datetime.datetime.now().timestamp()

                if 'slack' in notifiers.keys():
                    self.deploy_alarm.notifiers['slack'] = notifiers['slack']['hook_url']

                if 'mail' in notifiers.keys():
                    self.deploy_alarm.notifiers['mail'] = notifiers['mail']['address']

                for message in messages:
                    self.deploy_alarm.message = message
                    self.deploy_log_api.call_rest_api('POST', self.deploy_alarm.get_alarm_param(), "alarm")

            self.deploy_log_api.call_rest_api('POST', self.deploy_log.get_logging_param())

    def get_log_info(self):
        try:
            summary_data = json.loads(self.deploy_log_api.call_rest_api('GET', None, 'log_summary'))['data']
        except:
            summary_data = {'totalCall': 0, 'totalSuccessCall': 0}

        log_info = dict()
        log_info['total_call'] = summary_data['totalCall']
        log_info['total_success_call'] = summary_data['totalSuccessCall']
        log_info['latest_log'] = {
            'start_time': datetime.datetime.fromtimestamp(self.deploy_log.start_time),
            'end_time': datetime.datetime.fromtimestamp(self.deploy_log.end_time),
            'duration': round(self.deploy_log.end_time - self.deploy_log.start_time, 3),
            'url': self.deploy_log.req_url,
            'request_method': self.deploy_log.req_method,
            'request_body': self.deploy_log.req_body,
            'status_code': int(self.deploy_log.status_code),
            'response_data': self.deploy_log.response_data
        }

        return log_info
