import bpy
import bpy_extras
import os
import random
import colorsys
import math

ft_m_conv = 3.28 #feet to meter conversion
in_m_conv = 39.37 #inch to meter conversion
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
color_options = ["white", "black", "gray", "brown", "red", "orange", "yellow", "green", "blue", "purple"]

def colorChoice(color):
    if color == 0:
        return colorsys.hsv_to_rgb(random.uniform(0.00, 1.00), random.uniform(0.00, 1.00), random.uniform(0.95, 1.00))
    elif color == 1:
        return colorsys.hsv_to_rgb(random.uniform(0.00, 1.00), random.uniform(0.00, 1.00), random.uniform(0.00, 0.08))
    elif color == 2:
        return colorsys.hsv_to_rgb(random.uniform(0.00, 1.00), random.uniform(0.00, 0.07), random.uniform(0.5, 0.85))
    elif color == 3:
        return colorsys.hsv_to_rgb(random.uniform(20/360, 35/360), random.uniform(0.5, 1.00), random.uniform(0.3, 0.5))
    elif color == 4:
        return colorsys.hsv_to_rgb(random.uniform(.98, 1.00), random.uniform(0.85, 1.00), random.uniform(0.5, 1.00))
    elif color == 5:
        return colorsys.hsv_to_rgb(random.uniform(.016, .054), random.uniform(0.85, 1.00), random.uniform(0.5, 1.00))
    elif color == 6:
        return colorsys.hsv_to_rgb(random.uniform(.094, .141), random.uniform(0.85, 1.00), random.uniform(0.5, 1.00))
    elif color == 7:
        return colorsys.hsv_to_rgb(random.uniform(.221, .355), random.uniform(0.85, 1.00), random.uniform(0.5, 1.00))
    elif color == 8:
        return colorsys.hsv_to_rgb(random.uniform(.464, .666), random.uniform(0.85, 1.00), random.uniform(0.5, 1.00))
    elif color == 9:
        return colorsys.hsv_to_rgb(random.uniform(.680, .731), random.uniform(0.85, 1.00), random.uniform(0.5, 1.00))
    
def coorChoice():
    #9m width 13m length
    return random.uniform(-7.0, 7.0), random.uniform(-11.0, 11.0)

def shapeChoice(shape_name, text_name, altitude):
    #colors
    text_num = random.choice(range(0, 10)) #choosing random letter color
    shape_num = random.choice(range(0, 10)) #choosing random shape color
    random_rotation = math.radians(random.uniform(0.0, 360.0)) #choosing random rotation amount
    
    while text_num == shape_num: #if the shape and letter have the same color, change it
        shape_num = random.choice(range(0, 10))
        
    color_text_random = colorChoice(text_num)
    color_shape_random = colorChoice(shape_num)
    
    #shape
    shapedir = "C:/Users/Oviya/Documents/Blender/Shapes" #folder of shape possibilities
    shapefile = random.choice(os.listdir(shapedir)) #chooses a random shape from the folder
    bpy.ops.image.open(filepath = os.path.join(shapedir, shapefile))
    new_shape = bpy.data.images[shapefile]
    
    mat_shape = bpy.data.materials[shape_name]
    mat_shape.use_nodes = True
    
    #shape is a transparent png, "Alpha" input only uses the non-transparent part of the image
    #creates a new shader node that uses the prior selected shape and then changes the color to the random color we selected ("Principled BSDF")
    node_tex_shape = mat_shape.node_tree.nodes.new("ShaderNodeTexImage")
    node_tex_shape.image = new_shape
    principled_shape = mat_shape.node_tree.nodes["Principled BSDF"]
    mat_shape.node_tree.links.new(principled_shape.inputs["Alpha"], node_tex_shape.outputs["Alpha"])
    mat_shape.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (color_shape_random[0], color_shape_random[1], color_shape_random[2], 1)
    
    #apply random coordinates and rotation
    new_shape_coor = coorChoice()
    shape_location = bpy.data.objects[shape_name]
    shape_location.location[0] = new_shape_coor[0]
    shape_location.location[1] = new_shape_coor[1]
    shape_location.location[2] = 0.001
    shape_location.rotation_euler[2] = random_rotation
    
    #make sure that the target is visible in the scene
    bpy.data.objects[shape_name].hide_render = False
    bpy.data.objects[shape_name].hide_viewport = False
    
    #using world to camera view to get the bounding boxes for each target
    bpy.data.objects[shape_name].update_tag()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    
    min_x = 1
    max_x = 1
    min_y = 0
    max_y = 0
    
    obj = bpy.data.objects[shape_name].evaluated_get(depsgraph)
    for vert in obj.data.vertices:
        positions = [(obj.matrix_world @ v.co) for v in obj.data.vertices]
        for pos in positions:
            coord = bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, bpy.data.objects["Camera"], pos)
            min_x = min(min_x, coord[0])
            max_y = max(max_y, coord[1])
            #max_x = max(max_x, coord[0]) #idk why these two lines don't work
            #min_y = min(min_y, coord[1])
            max_x = min_x + 0.028
            min_y = max_y - 0.04
            
            #render = bpy.context.scene.render #to understand visually using render regions
            #render.use_border = True
            #render.border_min_x = min_x
            #render.border_max_x = min_x + 0.028
            #render.border_min_y = max_y - 0.04
            #render.border_max_y = max_y

    #text; location, rotation, color; very similar to shape of the target
    text = bpy.data.curves[text_name]
    bpy.data.objects[text_name].location[0] = new_shape_coor[0]
    bpy.data.objects[text_name].location[1] = new_shape_coor[1]
    bpy.data.objects[text_name].location[2] = 0.002
    bpy.data.objects[text_name].rotation_euler[2] = random_rotation
    text.text_boxes[0].width = 11/in_m_conv
    text.text_boxes[0].height = 8.5/in_m_conv
    text.text_boxes[0].x = -(11/in_m_conv)/2
    text.text_boxes[0].y = -0.16
    text.align_x = 'CENTER'
    text.align_y = 'CENTER'
    text.size = 0.27
    letter = alphabet[random.choice(range(0, 26))]
    text.body = letter
    
    text_color = bpy.data.materials[text_name]
    text_color.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (color_text_random[0], color_text_random[1], color_text_random[2], 1)
    
    bpy.data.objects[text_name].hide_render = False
    bpy.data.objects[text_name].hide_viewport = False
    
    #color of shape, color of text, name of shape, name of text, shape coors (4), shape_rotation, altitude (for csv)
    return (color_options[shape_num], color_options[text_num], shapefile[:len(shapefile) - 4], letter, str(min_x), str(max_x), str(min_y), str(max_y), str(math.degrees(random_rotation)), str(altitude))

def call():
    #report({'INFO'}, "Text Color:" + color_options[text_num])
    #report({'INFO'}, "Shape Color:" + color_options[shape_num])
    
    #camera_rotation_random = math.radians(random.uniform(0.0, 360.0))
    result_return = []
    altitude = random.uniform(75.0, 125.0)
    
    #render region
    render = bpy.context.scene.render
    render.use_border = True
    render.border_min_x = 0
    render.border_max_x = 1
    render.border_min_y = 0
    render.border_max_y = 1
    #render.border_min_x = .46
    #render.border_max_x = .54
    #render.border_min_y = .46
    #render.border_max_y = .54

    #light source
    light_source = bpy.data.lights["Light"]
    light_source.type = 'SUN'
    light_source.energy = random.uniform(0.0, 20.0)

    #camera
    cam_pos = bpy.data.objects["Camera"]
    cam_pos.location[0] = cam_pos.location[1] = 0.0 
    cam_pos.location[2] = altitude/ft_m_conv
    cam_pos.rotation_euler[0] = cam_pos.rotation_euler[1] = 0.0 
    #cam_pos.rotation_euler[2] = camera_rotation_random 

    #implementing focal length is a bit annoying if you make it random
    #focal length will change how the field looks in relation to the camera, which messes with field size
    #you can use a ratio to determine how to scale the field (scaling to fit camera makes things a bit more efficeint when rendering), but the ration changes based on the camera's focal length
    
    cam_specific = bpy.data.cameras["Camera"] 
    #cam_specific.lens = random.uniform(30.0, 50.0)
    
    #field size
    bpy.data.objects["Field"].scale[0] = altitude * 0.2
    bpy.data.objects["Field"].scale[1] = altitude * 0.296
    bpy.data.objects["Field_Extra"].scale[0] = altitude * 0.2
    bpy.data.objects["Field_Extra"].scale[1] = altitude * 0.296
    
    
    #shape and text
    #if you want a larger range of targets per image, feel free to make more objects in the scene collection
    #then add the names of each object the lists below and increase the range in num_shapes
    shape_list = ["Shape", "Shape1", "Shape2", "Shape3", "Shape4"] 
    text_list = ["Text", "Text1", "Text2", "Text3", "Text4"]
    num_shapes = random.choice(range(1, 5))
    
    for i in range(len(shape_list)):
        bpy.data.objects[shape_list[i]].hide_render = True
        bpy.data.objects[shape_list[i]].hide_viewport = True
        bpy.data.objects[text_list[i]].hide_render = True
        bpy.data.objects[text_list[i]].hide_viewport = True
    
    for j in range(num_shapes):
        result_return.append(shapeChoice(shape_list[j], text_list[j], altitude))

    #fields
    #similar to shape selection, there are two fields in the scene, each one is selected randomly from a folder of fields and uses a shader node to change the color of each field object in the scene
    #if you find better field images, replace and/or add images in the folder
    imgdir = "C:/Users/Oviya/Documents/Blender/Fields/"
    imgfile = random.choice(os.listdir(imgdir))
    bpy.ops.image.open(filepath = os.path.join(imgdir, imgfile))
    new_image = bpy.data.images[imgfile]
    
    mat = bpy.data.materials["Field"]
    mat.use_nodes = True
    
    node_tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
    node_tex.image = new_image
    principled = mat.node_tree.nodes["Principled BSDF"]
    #link = principled.inputs["Base Color"].links[0]
    #mat.node_tree.links.remove(link)
    mat.node_tree.links.new(principled.inputs["Base Color"], node_tex.outputs["Color"])
    
    imgdir = "C:/Users/Oviya/Documents/Blender/Fields/"
    imgfile = random.choice(os.listdir(imgdir))
    bpy.ops.image.open(filepath = os.path.join(imgdir, imgfile))
    new_image_extra = bpy.data.images[imgfile]
    
    mat_extra = bpy.data.materials["Field_Extra"]
    mat_extra.use_nodes = True
    #mat_extra.node_tree.nodes.remove(mat_extra.node_tree.nodes["BSDF_PRINCIPLED"].inputs["Base Color"].links[0].from_node)
    
    node_tex_extra = mat_extra.node_tree.nodes.new("ShaderNodeTexImage")
    node_tex_extra.image = new_image_extra
    principled_extra = mat_extra.node_tree.nodes["Principled BSDF"]
    #bpy.data.materials["Field_Extra"].node_tree.nodes["Principled BSDF"].inputs[0].show_expanded = True
    #link_extra = principled_extra.inputs["Base Color"].links[0]
    #mat_extra.node_tree.links.remove(link_extra)
    mat_extra.node_tree.links.new(principled_extra.inputs["Base Color"], node_tex_extra.outputs["Color"])
    
    field_pos = bpy.data.objects["Field"]
    field_extra_pos = bpy.data.objects["Field_Extra"]
    
    #field_pos.rotation_euler[2] = camera_rotation_random + math.radians(90)
    #field_extra_pos.rotation_euler[2] = camera_rotation_random + math.radians(90)
    field_pos.location[0] = 0
    field_extra_pos.location[0] = 0
    field_pos.location[1] = 0
    field_extra_pos.location[1] = 0
    
    #mat = bpy.data.materials["Field"]
    #principled = mat.node_tree.nodes["Principled BSDF"]
    #principled.inputs["Base Color"] = bpy.data.images[os.path.join(imgdir, imgfile)].name #new_image
    
    print(result_return)
    return result_return
    
call()