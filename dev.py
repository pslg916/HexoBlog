import os
import sys

msg = sys.argv[1]

os.system('hexo g')
os.system('git add .')
os.system('git commit -m {}'.format(msg))
os.system('git push node master')
os.system('git push hub master')

