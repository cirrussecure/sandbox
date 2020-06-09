
# ---------------------------
import sys
# print(sys.version)
# ---------------------------
# source(8/2018):
# https://stackoverflow.com/questions/32000934/python-print-a-variables-name-and-value
# Usage: debug('expression')

def debug(expression):
  '''
  document/test me
  '''
  frame = sys._getframe(1)
  print(
      expression, '=',
      repr(eval(expression, frame.f_globals, frame.f_locals)
  ))
