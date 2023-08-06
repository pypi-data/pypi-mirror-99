from .dependencies import dependencies

class VariableTracker(dict):

    #---------------------------------------------------------------------------
    
    def __init__(self, *args, callback, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback
        
    #---------------------------------------------------------------------------

    def __getitem__(self, key):
        self.callback(key)
        return super().__getitem__(key)

    #---------------------------------------------------------------------------
