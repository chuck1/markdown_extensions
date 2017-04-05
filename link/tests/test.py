#!/usr/bin/env python
import markdown
from markdown_extension_link import MyExtension

r = '[text](href)\n[text](/href)\n[text](/prefix/href)'

s = markdown.markdown(r, extensions=[MyExtension('/prefix')])

print 'result'
print s


