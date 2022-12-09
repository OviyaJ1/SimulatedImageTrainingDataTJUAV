import bpy
import os
import random

ft_m_conv = 3.28 #feet to meter conversion

light_source = bpy.data.lights["Light"]
light_source.type = 'SUN'
light_source.energy = random.uniform(0.0, 20.0)

cam_pos = bpy.data.objects["Camera"]
cam_pos.location[0] = cam_pos.location[1] = 0.0 
cam_pos.location[2] = random.uniform(75.0/ft_m_conv, 125.0/ft_m_conv) 
cam_pos.rotation_euler[0] = cam_pos.rotation_euler[1] = 0.0 
cam_pos.rotation_euler[2] = random.uniform(0.0, 360.0) 

cam_specific = bpy.data.cameras["Camera"]
cam_specific.lens = random.uniform(30.0, 50.0)
