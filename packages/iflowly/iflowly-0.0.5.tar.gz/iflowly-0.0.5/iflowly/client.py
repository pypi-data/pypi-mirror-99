import requests
from .utils import RequestConstructor
from .exceptions import TriggerError
from .constants import BASE_API_URL, LATEST_API_VERSION

class IFlowly():

    def __init__(self, api_key):
        self.requester = RequestConstructor(api_key)

    def get_flow(self, flow_name, version='latest'):
        return Flow(flow_name, self.requester, version)


class State():

    def __init__(self, id, name, label, active, initial, mark_completed):
        self.id = id
        self.name = name
        self.label = label
        self.active = active
        self.initial = initial
        self.mark_completed = mark_completed

    @classmethod
    def initialize(cls, data):
        return cls(
            data.get('id'),
            data.get('name'),
            data.get('label'),
            data.get('active'),
            data.get('initial'),
            data.get('mark_completed')
        )

class Trigger():

    def __init__(self, id, name, label, active, source, destination):
        self.id = id
        self.name = name
        self.label = label
        self.active = active
        self.source = State.initialize(source)
        self.destination = State.initialize(destination)

    @classmethod
    def initialize(cls, data):
        return cls(
            data.get('id'),
            data.get('name'),
            data.get('label'),
            data.get('active'),
            data.get('source'),
            data.get('destination')
        )


class Version():

    def transform_url(self):
        return self.flow.requester.transform_url('flows', self.flow.id) + 'versions/'

    def __init__(self, flow, version):
        self.flow = flow
        self.__get_version(version)

    def __set_attrs_from_response(self, response):
        self.id = response.get('id')
        self.locked = response.get('locked')
        self.version = response.get('version')
        self.latest = response.get('latest')

    def __get_version(self, version):
        url = self.transform_url()
        params = {
            'version': version
        }
        response = self.flow.requester.request('get', url, params=params)
        if response.status_code == 200:
            self.__set_attrs_from_response(response.json())


class Flow():

    def __init__(self, flow_name, requester, version='latest'):
        self.requester = requester
        self.states = []
        self.triggers = []
        self.__get_flow(flow_name)
        self.version = Version(self, version)
        self.__get_flow_details()

    def __set_attrs_from_response(self, response):
        self.id = response.get('id')
        self.name = response.get('name')
        self.deleted = response.get('deleted')
        self.active = response.get('active')

    def __get_flow(self, flow_name):
        url = self.requester.transform_url('flows', flow_name)
        response = self.requester.request('get', url)
        if response.status_code == 200:
            self.__set_attrs_from_response(response.json())

    def __get_flow_details(self):
        url = self.requester.transform_url('flows', self.id) + 'advanced/options/' + self.version.id + '/'
        params = {
            'type': 'FlowVersion'
        }
        response = self.requester.request('get', url, params=params, json=False)
        if response.status_code == 200:
            json_response = response.json()
            for state_relation in json_response.get('states', []):
                self.states.append(State.initialize(state_relation.get('state')))

            for trigger_relation in json_response.get('triggers', []):
                self.triggers.append(Trigger.initialize(trigger_relation.get('trigger')))


    def run_event(self, event_name, context={}):
        PATH = '{flow_id}/execute-event/{event_name}'.format(flow_id=self.id, event_name=event_name)
        URL = self.requester.transform_url('flows', PATH)
        PARAMS = {
            'version': self.version.version
        }
        self.requester.request('post', URL, params=PARAMS, data=context)
        return 'Success'

    def run_trigger(self, trigger_name, context={}):
        PATH = '{flow_id}/execute-trigger/{trigger_name}'.format(flow_id=self.id, trigger_name=trigger_name)
        URL = self.requester.transform_url('flows', PATH)
        PARAMS = {
            'version': self.version.version
        }
        try:
            self.requester.request('post', URL, params=PARAMS, data=context)
            return 'Success'
        except requests.exceptions.HTTPError as e:
            response_json = e.response.json()
            detail = response_json.get('detail')
            raise TriggerError(detail) from None
