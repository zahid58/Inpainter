<h1 align="center">
<p>Inpainter
</h1>
<h3 align="center">
<p>A python GUI application to inpaint images.
</h3>

*Inpainting* is a set of image processing algorithms where damaged, missing or unwanted parts of an image are filled in using the neighbouring pixels. It can also be used to 
remove forground objects. This is a GUI application that helps you do just that. It has an interactive and user-friendly GUI for marking the regions of the images. 

<p align="center">
 <img alt="cover" src="https://github.com/Zedd1558/Image-Inpainter/blob/master/demo/cover.jpg" height="50%" width="50%">
</p>


### Implementation
The frontend GUI is developed using PyQt. The backend inpainting operations are done using *OpenCV* library. Currently, *OpenCV* provides two algorithms for inpainting which are-
* cv2.INPAINT_TELEA: An image inpainting technique based on the fast marching method (Telea, 2004)
* cv2.INPAINT_NS: Navier-stokes, Fluid dynamics, and image and video inpainting (Bertalmío et al., 2001)

Later on, I'll try to incorporate recent deep learning methods that perform way better than these classical image processing algorithms.

<h4 align="center">
<p>let's see an exmaple
</h4>
<p align="center">
 <img alt="editing" src="https://github.com/Zedd1558/Image-Inpainter/blob/master/demo/editpage.jpg">
</p>
<h4 align="center">
<p>removes text quite well!
</h4>

### Here's how you can quickly incorporate other inpainting methods
Let's say you want to add the inpainting algorithm **Deepfill**. Here's how you can do it:
1. Open up *editpage.py*. Go to the method *setupUi()* of class *Editpage*. Add the following line at the very end of this method.
```python
self.addInpaintingMethod("Deepfill")
```
This will add your new method's name in the *dropdown selection list* of the GUI editing page.

2. Now, in *backend.py* you can add a method that will call your inpainting algorithm.
```python
def inpaint_deepfill(image, mask):
    # call your custom algorithm for inpainting here and pass your image and mask to your algorithm
    # return your output image with format numpy ndarray, for now I am just returning the input image
    return image    
```
3. Last thing you need to do is call your inpainting method from *editor.py*. Go to the method *inpaint()* of *editor.py*. Add and elif condition which checks `self._method` by your method's name and calls the corresponding inpainting method from *backend.py*
```python
    def inpaint(self):
        img = np.array(self._current_image)                   
        mask = rgb_view(self._mask)
      
        if self._method == "Navier-Stokes":
            output_rgb = backend.inpaint_cv2(img, mask,method="ns")
            
        elif self._method == "Telea":
            output_rgb = backend.inpaint_cv2(img, mask,method="telea")
         
        elif self._method == "Deepfill":                                  # add these lines 
            output_rgb = backend.inpaint_deepfill(img, mask)              # to call your inpainting algorithm
            
        else:
            raise Exception("this inpainting method is not recognized!")
        output = array2qimage(output_rgb)
```

### Required libraries
PyQt, Numpy, OpenCV3, qimage2ndarray
### How to run
open up console in the project directory and enter this 
```
python inpainter.py
```
<p align="center">
 <img alt="editing" src="https://github.com/Zedd1558/Image-Inpainter/blob/master/demo/inpaint_demo2.gif">
</p>

### Standalone Executable
You will get the application in just one exectuable file (.exe) in the following drive link.
https://drive.google.com/file/d/1ReiSmzh3T9DRLvMrtOJeaH2hWSJ9sE9a/view?usp=sharing

### Contribute
Feel free to fork the project and contribute. You can incorporate recent deep learning methods, make the GUI more easy to use, include relevant photo editing features. 

