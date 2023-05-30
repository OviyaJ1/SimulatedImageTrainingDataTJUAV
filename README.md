# Simulated Image Training Data for TJ UAV
Oviya Jeyaprakash <br />
May 23, 2022 <br />
Yilmaz - Period 6 <br />

## Blender File Setup
<p> If you don't already have Blender installed on your desktop, make sure to do so (https://www.blender.org/download/). <br/>
  
Download the appropriate Blender file. The most recent Blender file I made is UAVrender.blend. It should be relatively straight 
forward to open on Blender when downloading. <br /> 
  
It should already be set up with the camera, light source, two field objects, five target shapes, and five target letters. 
If you would like to add more targets to the scene, then copy and paste a shape object within the scene. Rename the new object 
within the scene collection and its material index within its material properties appropriately. Similarly when making a new shape 
object, copy and paste a text object within the scene. Rename the text object within the scene collection and its material index 
within its material properties appropriately.<p/>

## Blender Script
<p> There are two main relevant scripts: default_changes.py and render_images.py. <br />

The former, default_changes.py, when run changes the scene once. Basically, it's a quick way to show the user what changes are made
with one call. It doesn't render or export any images. It just changes the scene. <br />
  
The latter, render_images.py, when run displays a UI tab for the user to interact with. It allows for the user to render and 
export as many images as needed to a certain file directory of the user's chosing. To clarify, the content of default_changes.py is 
used in render_images.py, but instead of only being called once, it will be called several times and each scene will be rendered 
and exported each time it changes. 

There are comments throughout both scripts that go into more detail about the actual code. However, some important things to know
if you don't feel like going through the comments...
  
```
#writes data to a CSV file and renders images
def write_some_data(context, filepath, self):
    csv_file = "C:/Users/Oviya/Documents/Blender/out.csv" 
    f = open(csv_file, 'w')
    f.writelines("Image Name, Color of Shape, Color of Letter, Shape, Letter, X1, X2, Y1, Y2, Shape Rotation, Altitude" + "\n")
    for index in range(1000): #number within range is the amount of images that will be rendered in the end!!!
        initial = call()
        bpy.context.scene.render.filepath = os.path.join(filepath, 'render%' + str(index) + '.jpg')
        bpy.ops.render.render(write_still = True)
        
        for i in initial:
            string_result = ", ".join(i)
            f.writelines('render%' + str(index) + '.jpg, ' + string_result + '\n')
    f.close()
```
This function within render_images.py creates, renders, and exports the generated images. Most importantly, the number within the 
range of the for loop is the number of images that will be generated. In addition, a CSV file with data regarding each target is created, 
so make sure to change the file directory for csv_file appropriately. 

```
class ExportSomeData(Operator, ExportHelper):
  bl_idname = "export_test.data"  # important since its how bpy.ops.import_test.some_data is constructed
  bl_label = "Export Data"
  
  filename_ext = "/TestImages/render%d.jpg"
  
  def execute(self, context): 
      #folder where user chooses to export images!!!
      return write_some_data(context, "C:/Users/Oviya/Documents/Blender/TestImages", self)
```
Similarly, there's another function within render_images.py that helps export all the generated images to a certain file directory. Change 
the file directory within the write_some_data method appropriately. 

```
def shapeChoice(shape_name, text_name, altitude):
  ...
  shapedir = "C:/Users/Oviya/Documents/Blender/Shapes" #folder of shape possibilities
  shapefile = random.choice(os.listdir(shapedir)) #chooses a random shape from the folder
  bpy.ops.image.open(filepath = os.path.join(shapedir, shapefile))
  new_shape = bpy.data.images[shapefile]
...
  
def call():
  ...
  #similar to shape selection, there are two fields in the scene, each one is selected randomly from a 
  folder of fields and uses a shader node to change the color of each field object in the scene
  #if you find better field images, replace and/or add images in the folder
  
  imgdir = "C:/Users/Oviya/Documents/Blender/Fields/"
  imgfile = random.choice(os.listdir(imgdir))
  bpy.ops.image.open(filepath = os.path.join(imgdir, imgfile))
  new_image = bpy.data.images[imgfile]
...
```  
Speaking of file directories, within both default_changes.py and render_images.py each field and target shape is randomly chosen from a 
folder of fields and shapes. Make sure to change the file directories appropriately. <br />
  
Again, this is the bare minimum that is needed to make the scripts run properly. However, if you want to change some of the optional variables,
like altitude range, lighting, camera focal length, number of targets per image, etc., take a look at the comments within the scripts.
<p />

## CV File Setup
<p> Pretty straightforward. Make sure to install the OpenCV library on your IDE. Manually choose the image you want or do so with the command line. 
The only variables you might need to play around with is within the threshold method. 

```
#might need to change threshold variables depending on the image
thresh = cv2.threshold(blurred, 145, 255, cv2.THRESH_BINARY)[1]
```
More details regarding the code content can be found within the comments of the script itself. 
