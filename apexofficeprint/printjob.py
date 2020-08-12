import json

STATIC_OPTS = {
    "tool": "python",
    "version": "18.2"
}

class PrintJob:
    def __init__(self):
        pass

    @property
    def json(self) -> str:
        result = STATIC_OPTS
        # add more stuff to result
        return json.dumps(result)
