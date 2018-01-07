from __future__ import division
import os
import sys
import re
import subprocess
from itertools import permutations

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *


import math
import functools

SEGMENTS = 48

def audioAmp(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  print(pos)
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0

  audioAmp = color(Blue)(                         
                        cube([15.25,24.34,3])    
                        )

  if flip is True:
    audioAmp = rotate([0,180,0])(audioAmp)

  if 1 <= rotate <= 3:
    audioAmp = rotate([0,0,90*rotate])(audioAmp) 

  return translate(pos)(audioAmp)
def camera(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0

  rp_width = 23.99
  rp_length = 23.99
  rp_height = 2.3
  rectangularPlate = color([0,0.5,0])(                        
                                 down(rp_height)(left(rp_length/2-2)(back(rp_width/2)(cube([rp_length,rp_width,rp_height]))))
                                 )
  se_length = 8.4
  se_height = 2.3
  cameraBody = color(Black)(                        
                           translate([-se_length/2,-se_length/2,0])(cube([se_length,se_length,2.3])),
                           up(se_height)(cylinder(h = 2.3, r1 = 4.0, r2 = 4.0))     
                           )
  camera = rectangularPlate + cameraBody
  if flip is True:
    camera = rotate([0,180,0])(camera)

  if 1 <= rotate <= 3:
    camera = rotate([0,0,90*rotate])(camera) 
  
  return translate(pos)(camera)
def powerBoost(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0
  rp_length = 36.17
  rp_width = 23.00
  rp_height = 2.33
  odd_component_height = 7.33
  rectangularPlate = color([0,0.5,0])(                        
                                 back(rp_width/2)(cube([rp_length,rp_width,odd_component_height]))
                                 )
  usb_width = 11.7
  usb_length = 14.8
  usb_height = 5.89
  usbPort = color([0.824,0.824,0.824])(
                                     left(8.97)(up(rp_height)(back(usb_width/2)(cube([usb_length,usb_width,usb_height]))))
                                      )
  powerBoost = rectangularPlate + usbPort

  if flip is True:
    powerBoost = rotate([0,180,0])(powerBoost)

  if 1 <= rotate <= 3:
    powerBoost = rotate([0,0,90*rotate])(powerBoost) 

  return translate(pos)(powerBoost)
def speaker(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0
  length = 21.62
  width = 18.00
  height = 7.77
  speaker = color([0.7,0.7,0.7])(                        
                                cube([length,width,height],center = True)
                                )

  if flip is True:
    speaker = rotate([0,180,0])(speaker)

  if 1 <= rotate <= 3:
    speaker = rotate([0,0,90*rotate])(speaker) 

  return translate(pos)(speaker)
def screen(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0
  lcd_length = 123.10
  lcd_width = 76.05
  lcd_height = 2.33 * 2      # guesstimate
  screenLCD = color([0.5,0.5,0])(                        
                                cube([lcd_length,lcd_width,lcd_height])
                                )
  plate_length = 123.10
  plate_width = 76.05
  plate_height = 2.33
  circuitPlate = color([0.824,0.824,0.824])(
                                           down(plate_height*2)(cube([plate_length,plate_width,plate_height]))
                                           )
  powerBoost = screenLCD + circuitPlate

  if flip is True:
    powerBoost = rotate([0,180,0])(powerBoost)

  if 1 <= rotate <= 3:
    powerBoost = rotate([0,0,90*rotate])(powerBoost) 

  return translate(pos)(powerBoost)
def screenDriver(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0

  length = 48.00
  width = 40.75
  height = 5.69
  screenDriver = color(Blue)(                        
                            cube([length,width,height],center = True)
                             )
  if flip is True:
    screenDriver = rotate([0,180,0])(screenDriver)

  if 1 <= rotate <= 3:
    screenDriver = rotate([0,0,90*rotate])(screenDriver) 


  return translate(pos)(screenDriver)
def piZero(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0
  rp_length = 66.00
  rp_width = 29.96
  rp_height = 1.33
  rectangularPlate = color([0,0.5,0])(                        
                                     down(rp_height)(cube([rp_length,rp_width,rp_height]))
                                     )
  usb1_width = 5.55
  usb1_length = 7.58
  usb1_height = 7.33/4
  usbPortTemplate1 = color([0.824,0.824,0.824])(
                                               cube([usb1_length,usb1_width,usb1_height])
                                               )
  
  usbPort1 = back(31.58-29.96)(right(37.54)(right(50.8 - 37.54)(usbPortTemplate1) + usbPortTemplate1))
  
  usb2_length = 11.24
  usb2_width = 7.58
  usb2_height = 7.33/4
  usbPortTemplate2 = color([0.824,0.824,0.824])(
                                               cube([usb2_length,usb2_width,usb2_height])
                                               )
  usbPort2 = back(31.58-29.96)(right(8.04)(usbPortTemplate2))
  
  usbPort = usbPort1 + usbPort2
  piZero = usbPort + rectangularPlate

  if flip is True:
    piZero = rotate([0,180,0])(piZero)

  if 1 <= rotate <= 3:
    piZero = rotate([0,0,90*rotate])(piZero) 

  return translate(pos)(piZero)
def battery(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0
  length = 65.00
  width = 51.00
  height = 8.00
  battery = color([0.95,0.95,0.95])(                        
                                   cube([length,width,height],center = True)
                                   )

  if flip is True:
    battery = rotate([0,180,0])(battery)

  if 1 <= rotate <= 3:
    battery = rotate([0,0,90*rotate])(battery) 

  return translate(pos)(battery)
def gsmChip(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0
  length = 45.62
  width = 34.00
  height = 8.00
  gsmChip = color([0.1,0.1,0.1])(                        
                                cube([length,width,height],center = True)
                                )
  if flip is True:
    gsmChip = rotate([0,180,0])(gsmChip)

  if 1 <= rotate <= 3:
    gsmChip = rotate([0,0,90*rotate])(gsmChip) 

  return translate(pos)(gsmChip)

def audioAmp(pos,flip,rotate):
  if pos is None:
    pos = [0,0,0]
  print(pos)
  if flip is None:
    flip = False
  if rotate is None:
    rotate = 0

  audioAmp = color(Blue)(                         
                        cube([15.25,24.34,3])    
                        )

  if flip is True:
    audioAmp = rotate([0,180,0])(audioAmp)

  if 1 <= rotate <= 3:
    audioAmp = rotate([0,0,90*rotate])(audioAmp) 

  return translate(pos)(audioAmp)

def boundingBox(openscadObject):

  def isanumber(a):

    try:
        float(a)
        bool_a = True
    except:
        bool_a = False

    return bool_a

  # Create space for an openscad file
  cwd = os.getcwd()
  code_filepath = os.path.join(cwd, "tempOpenSCADfile.scad")
  stl_filepath  = os.path.join(cwd, "tempOpenSCADfile.stl")
  # Convert object to valid openSCAD code
  code = scad_render_to_file(openscadObject,code_filepath)

  # Ask openSCAD to generate STL
  subprocess.call(["openscad","-o",stl_filepath,code_filepath])

  # Time to use admesh to find min/max values
  cmd = ['admesh',stl_filepath]
  proc = subprocess.Popen('admesh tempOpenSCADfile.stl',shell=True,stdout=subprocess.PIPE)

  for line in proc.stdout:
    if 'Min X' in line.decode("utf-8"):
      my_list = line.decode("utf-8").split()
      [minX,maxX] = [float(x.replace(",", "")) for x in my_list if isanumber(x.replace(",", "")) == True]

    if 'Min Y' in line.decode("utf-8"):
      my_list = line.decode("utf-8").split()
      [minY,maxY] = [float(x.replace(",", "")) for x in my_list if isanumber(x.replace(",", "")) == True]

    if 'Min Z' in line.decode("utf-8"):
      my_list = line.decode("utf-8").split()
      [minZ,maxZ] = [float(x.replace(",", "")) for x in my_list if isanumber(x.replace(",", "")) == True]

  return [minX,maxX,minY,maxY,minZ,maxZ]
      

#  for line in proc.stdout.readlines():
#    if "minX" in line:
#      print(line)

def intersectionAssertion(object1,object2):
  def isanumber(a):

    try:
        float(a)
        bool_a = True
    except:
        bool_a = False

    return bool_a

  openscadObject = object1 * object2

  # Create space for an openscad file
  cwd = os.getcwd()
  code_filepath = os.path.join(cwd, "tempOpenSCADfile_intersection.scad")
  png_filepath  = os.path.join(cwd, "tempOpenSCADfile_intersection.png")
  # Convert object to valid openSCAD code
  code = scad_render_to_file(openscadObject,code_filepath)

  # Ask openSCAD to generate STL
  subprocess.call(["openscad","-o",png_filepath,code_filepath])

  # Time to use admesh to find min/max values
  cmd = 'magick ' + png_filepath + ' -define histogram:unique-colors=true -format %c histogram:info:- | wc -l'
  proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)

  for line in proc.stdout:
    ans = isanumber(line.decode("utf-8"))

  if ans is True:
    return True
  else:
    return False

def intersectionList(*args):

  bool = False
  for p in permutations(items,2):
    bool = bool or intersectionAssertion(p[0],p[1])
  return bool

if __name__ == '__main__':

    list_of_bodies = [
    audioAmp(     [0,10,10],None,None),   
    camera(       [0,30,30],None,None),     
    powerBoost(   [0,50,50],None,None),  
    #speaker(      [0,70,70],None,None),    
    screen(       [0,90,90],None,None),   
    screenDriver( [0,110,110],None,None),
    piZero(       [0,130,130],None,None),      
    battery(      [0,150,150],None,None),     
    #gsmChip(      [0,170,170],None,None)
    ]

    body = functools.reduce(lambda x,y: x + y,list_of_bodies)
    a = body
    #print(intersectionAssertion(a,a))
    #print(boundingBox(a))
    print("poop")
    scad_render_to_file(a, file_header='$fn = %s;' % SEGMENTS, include_orig_code=False)
