from turtle import *

def snow(a, order):
  if order >0:
     for d in [60, -120, 60, 0]:
         forward(a/3)
         left(d)

snow(100,0)
pensize(4)
snow(100,1)