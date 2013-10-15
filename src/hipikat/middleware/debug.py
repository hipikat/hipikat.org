
class DebugOuterMiddleware(object):
    """
    Debug-mode middleware on the 'outermost' middleware layer, for the project.
    """
    def process_request(self, request):
        pass

class DebugInnerMiddleware(object):
    """
    Debug-mode middleware on the 'innermost' middleware layer, for the project.
    """
    def process_request(self, request):
        pass
