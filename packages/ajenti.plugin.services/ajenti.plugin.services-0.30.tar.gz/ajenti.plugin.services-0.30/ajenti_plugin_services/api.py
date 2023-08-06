from jadi import interface


class Service():
    """
    Basic class to store service informations.
    """

    def __init__(self, manager):
        self.id = None
        self.name = None
        self.manager = manager
        self.state = None
        self.running = None


class ServiceOperationError(Exception):
    """
    Exception class for services.
    """

    def __init__(self, inner):
        self.inner = inner

    def __unicode__(self):
        return '[ServiceOperationError %s]' % self.inner


@interface
class ServiceManager():
    """
    Abstract interface for all managers.
    """

    id = None
    name = None

    def list(self):
        raise NotImplementedError

    def get_service(self, _id):
        raise NotImplementedError

    def start(self, _id):
        raise NotImplementedError

    def stop(self, _id):
        raise NotImplementedError

    def restart(self, _id):
        raise NotImplementedError
