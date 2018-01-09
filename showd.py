import navegador5.file_toolset as nvft
import os
import json
import sys
from xdict.jprint import  pobj



filename = sys.argv[1]
content = nvft.read_file_content(fn=filename,op='r')
d = json.loads(content)
pobj(d)
