#To Help Understand These Errors
#Visit The Error Documentation

class ArgError(Exception):
    pass

class SocketError(Exception):
    pass

class ServerHostingError(Exception):
    pass

class ClientConnectionError(Exception):
    pass

class MessageError(Exception):
    pass

class FileRemovalError(Exception):
    pass

class LinkerReadError(Exception):
    pass

class LinkerBuildError(Exception):
    pass

class InterfaceInstallError(Exception):
    pass

class NotOnlineError(Exception):
    pass

class SocketClosed(Warning):
    pass