from PIL import Image, ImageDraw, ImageFont
import math
import streamlit as st
import numpy as np

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?+~<>i!lI;:,\"^`'. "[::-1]
#chars = "#Wo- "[::-1]
#chars="01"[::1]
charArray = list(chars)
charArray.reverse()
charLength = len(charArray)
interval = charLength/256

st.session_state['scale'] = 0.1
st.session_state['bgBrightness']=0
oneCharWidth = 10
oneCharHeight = 18
count=0

st.set_page_config(layout="wide")

def main():
    initSessionState()
    file=st.file_uploader("Select Image", type=None, accept_multiple_files=False, disabled=False, label_visibility="visible")
    st.session_state['bgBrightness']=st.slider('Brightness',min_value=0, max_value=255, value=st.session_state['bgBrightness'], step=1, label_visibility="visible")
    st.session_state['scale']=st.slider('scalefactor',min_value=0.01, max_value=0.5, value=st.session_state['scale'], step=0.001, label_visibility="visible")
    if(file!=None):
        if(file.type!='image/png' and file.type!='image/jpeg'):
            file=None
            st.write("please use png or jpg")
        st.session_state['file']=file
        st.session_state['img']=Image.open(file)
        st.session_state['idimg']+=1
        print(file)
        st.session_state['output']=asciiArt(st.session_state['img'],st.session_state['scale'])
 
        drawpage()
          
def initSessionState():
    if 'file' not in st.session_state:
        st.session_state['file'] = 'value'
    if 'img' not in st.session_state:
        st.session_state['img'] = 'value'
    if 'idimg' not in st.session_state:
        st.session_state['idimg']=0
    if 'saved' not in st.session_state:
        st.session_state['saved']=False


def drawpage():
    with st.container():
        left,mid,right=st.columns([4,1,4])
        with left:
            st.image(st.session_state['img'],use_column_width=True)
        with right:
            try:
                st.image(Image.fromarray(np.uint8(st.session_state['output'])),use_column_width=True)
            except:
                pass

def getChar(inputInt):
    return charArray[math.floor(inputInt*interval)]

def asciiArt(im,scaleFactor):
    fnt = ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf', 20)
    width, height = im.size
    print(width,height)
    im = im.convert('RGBA')
    #st.session_state['img'].save("bin/"+str(len(os.listdir("bin")))+".png")
    #Image.fromarray(im).save("bin/"+str(len(os.listdir("bin")))+".png")
    im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))),Image.Resampling.NEAREST)
    
    width, height = im.size
    pix = im.load()
    
    outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = (st.session_state['bgBrightness'], st.session_state['bgBrightness'], st.session_state['bgBrightness']))
    d = ImageDraw.Draw(outputImage)

    for i in range(height):
        for j in range(width):
            
            try:
                    r, g, b = pix[j, i]
                    h = int((r/3 + g/3 + b/3))
                    d.text((j*oneCharWidth, i*oneCharHeight), getChar(h), font = fnt, fill = (r, g, b))

            except:
                r, g, b, _ = pix[j, i]
                if((r,g,b)==(71,112,76)):
                     r,g,b=255,255,255
                h = int((r/3 + g/3 + b/3))
                d.text((j*oneCharWidth, i*oneCharHeight), getChar(h), font = fnt, fill = (r, g, b))  
    outputImage.save("output.png")  
    return outputImage
    
main()
