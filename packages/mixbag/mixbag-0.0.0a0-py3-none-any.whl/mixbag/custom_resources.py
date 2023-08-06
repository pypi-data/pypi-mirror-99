class CustomResourceEventHandler:
    def __init__(self, physical_id=None):
        self._id = physical_id

    def __call__(self, event, context):
        request_type = event["RequestType"]
        if request_type == "Create":
            return self.handle_event(self.on_create, event, context)
        if request_type == "Update":
            return self.handle_event(self.on_update, event, context)
        if request_type == "Delete":
            return self.handle_event(self.on_delete, event, context)
        raise ValueError("Invalid request type: %s" % request_type)

    @property
    def id(self):
        if self._id is None:
            self._id = hash(f"{__file__}::{self.__class__.__name__}")
        return self._id

    def on_create(self, event, context):
        raise NotImplementedError()

    def on_update(self, event, context):
        raise NotImplementedError()

    def on_delete(self, event, context):
        raise NotImplementedError()

    def handle_event(self, method, event, context):
        try:
            data = method(event, context)
            response = self.success(event, data=data)
        except Exception as exc:
            response = self.failure(event, str(exc))
        return response

    def get_response(self, status, event, reason=None, data=None):
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html
        return {
            "Status": status,
            "Reason": reason,
            "PhysicalResourceId": self.id,
            "RequestId": event["RequestId"],
            "StackId": event["StackId"],
            "LogicalResourceId": event["LogicalResourceId"],
            "Data": data,
        }

    def success(self, event, data=None):
        return self.get_response("SUCCESS", event, data=data)

    def failure(self, event, reason: str):
        return self.get_response("FAILED", event, reason=reason)
