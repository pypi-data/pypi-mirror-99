
class BaseIFlowlyException(Exception): pass

class APIKeyMissing(BaseIFlowlyException): pass

class TriggerError(BaseIFlowlyException): pass