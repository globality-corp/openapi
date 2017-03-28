from . import load

import sys
with open (sys.argv [1]) as fileobj:
    swagger = load (fileobj)
swagger.validate ()
