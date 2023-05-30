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
<p />
