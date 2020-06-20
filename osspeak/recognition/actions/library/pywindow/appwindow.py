class ApplicationWindow:

    def __init__(self, implementation):
        self._implementation = implementation

    @property
    def title(self):
        return self._implementation.title

    def minimize(self):
        self._implementation.minimize()
        
    def maximize(self):
        self._implementation.maximize()
        
    def close(self):
        self._implementation.close()
        
    def focus(self):
        self._implementation.focus()

    @property
    def coords(self):
        return self._implementation.coords