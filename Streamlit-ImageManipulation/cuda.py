from __future__ import division
from numba import cuda, float32

import cupy
from PIL import Image
import numpy as np
import math

mx=25
my=25
pl=mx*my
pd=1
xradius=int((mx-1)/2)
yradius=int((my-1)/2)


@cuda.jit
def my_kernel_2D(i_array,o_array):
   
    x, y = cuda.grid(2)
    w,h,d = i_array.shape
    if x-xradius > 0 and y-yradius > 0 and x+xradius+1 < w and yradius+y+1 <h:
        pixelsInArea=cuda.local.array(shape=(my,mx), dtype=float32)
        pixelsInArea=i_array[int(y-yradius):int(y+yradius),int(x-xradius):int(x+xradius)]
        o_array[y,x]=[cupy.median(pixelsInArea[:,:,0]),cupy.median(pixelsInArea[:,:,1]),cupy.median(pixelsInArea[:,:,2])]

    
    
image=Image.open("colorwheel.png")

data = np.array(image)


c_inputArray = cuda.to_device( data )
c_outputArray = cuda.to_device(np.zeros(data.shape))
c_sortStack = cuda.to_device(np.zeros((my*mx,1)))

threadsperblock = (32, 32)
blockspergrid_x = math.ceil(data.shape[0] / threadsperblock[0])
blockspergrid_y = math.ceil(data.shape[1] / threadsperblock[1])
blockspergrid = (blockspergrid_x, blockspergrid_y)
my_kernel_2D[blockspergrid, threadsperblock](c_inputArray,c_outputArray)

image=c_outputArray.copy_to_host()
print(image)
i=Image.fromarray(np.uint8(image))
i.show()
