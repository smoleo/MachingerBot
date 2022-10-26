import streamlit as st
from PIL import Image
import numpy as np
from numpy import median as npmdn
import time
from statistics import median as mdn


st. set_page_config(layout="wide")

def main():
    initSessionState()
    file=st.file_uploader("Select Image", type=None, accept_multiple_files=False, disabled=False, label_visibility="visible")
    if(file!=None):
        if(file.type!='image/png' and file.type!='image/jpeg'):
            file=None
            st.write("please use png or jpg")
        if st.session_state['file']!=file:
            st.session_state['file']=file
            red, green, blue, grayscale, img=calculate(file)
            st.session_state['red']=red
            st.session_state['green']=green
            st.session_state['blue']=blue
            st.session_state['grayscale']=grayscale
            st.session_state['img']=img
            st.session_state['redgreen']=np.add(red,green)
            st.session_state['redblue']=np.add(red,blue)
            st.session_state['bluegreen']=np.add(blue,green)
            st.session_state['median']=img
        drawpage()
        

                    
        
def drawpage():
    with st.container():
        left,c1,c2,c3=st.columns([4,1,1,1])
        with left:
            st.image(st.session_state['img'],width=750)
        with c1:
            st.image(Image.fromarray(np.uint8(st.session_state['red'])),caption='Red')
            st.image(Image.fromarray(np.uint8(st.session_state['redgreen'])),caption='Red and Green')
            
        with c2:
            st.image(Image.fromarray(np.uint8(st.session_state['green'])),caption='Green')
            st.image(Image.fromarray(np.uint8(st.session_state['redblue'])),caption='Red and Blue')
            st.image(Image.fromarray(np.uint8(st.session_state['grayscale'])),caption='Grayscale')
        with c3:
            st.image(Image.fromarray(np.uint8(st.session_state['blue'])),caption='Blue')
            st.image(Image.fromarray(np.uint8(st.session_state['bluegreen'])),caption='Blue and Green')
    """---"""        
    with st.container():
        c1,c2=st.columns([4,3])
        with c1:
            st.image(st.session_state['median'],width=750,caption='Calculation Time='+str(st.session_state['time'])+' seconds')
        with c2:
            medianx=st.slider('filter x',1,151,1,step=2)
            mediany=st.slider('filter y',1,151,1,step=2)
            if st.button("Median Filter"):
                st.session_state['median']=Image.fromarray(np.uint8(filterMedian(medianx,mediany)))
                st.experimental_rerun()
            

@st.cache
def calculate(file):
    if file!=None:
        print(file)
    img=Image.open(file)
    print(img.size)
    pixels=np.array(img)
    height,width=img.size
    depth=len(pixels[0,0])
    red=np.zeros(shape=(width,height,depth))
    green=np.zeros(shape=(width,height,depth))
    blue=np.zeros(shape=(width,height,depth))
    grayscale=np.zeros(shape=(width,height,depth))

    i=0
    for lines in pixels:
        rLine,gLine,bLine,grLine=[],[],[],[]
        for p in lines:
            try:
                r,g,b,o=p
                rLine.append([r,0,0,o])
                gLine.append([0,g,0,o])
                bLine.append([0,0,b,o])
                avg=(int(r)+int(b)+int(g))/3
                grLine.append((avg,avg,avg,o))
            except:
                r,g,b=p
                rLine.append([r,0,0])
                gLine.append([0,g,0])
                bLine.append([0,0,b])
                avg=(int(r)+int(b)+int(g))/3
                grLine.append((avg,avg,avg))

        red[i]=rLine
        green[i]=gLine
        blue[i]=bLine
        grayscale[i]=grLine
        i+=1
        
    return red, green, blue, grayscale, img

def filterMedian(mx, my):
    useNP=False
    if (my*mx)>169:
        useNP=True
    pixels=np.array(st.session_state['img'])
    xradius=int((mx-1)/2)
    yradius=int((my-1)/2)
    print(xradius,yradius)
    width,height=st.session_state['img'].size
    median=np.zeros(shape=(width,height,len(pixels[0][0])))
    y=0
    x=0
    bar=st.progress(0)
    start =time.time()
    for lines in pixels:
        x=0
        for p in lines:
            try:
                pixelsInArea=pixels[int(y-yradius):int(y+yradius+1),int(x-xradius):int(x+xradius+1)]
                reshaped=pixelsInArea.reshape(my*mx,len(pixels[0][0]))
                if useNP:
                    if(len(pixels[0][0])==3):
                        median[y][x]=([npmdn(reshaped[:,0]),npmdn(reshaped[:,1]),npmdn(reshaped[:,2])])
                    else:
                        median[y][x]=([npmdn(reshaped[:,0]),npmdn(reshaped[:,1]),npmdn(reshaped[:,2]),p[3]])
                else:
                    if(len(pixels[0][0])==3):
                        median[y][x]=([mdn(reshaped[:,0]),mdn(reshaped[:,1]),mdn(reshaped[:,2])])
                    else:
                        median[y][x]=([mdn(reshaped[:,0]),mdn(reshaped[:,1]),mdn(reshaped[:,2]),p[3]])
            except Exception as e:
                pass
            x+=1
        y+=1
        bar.progress(int(y/height*100))
    bar.empty()
    end=time.time()
    print('done')
    st.session_state['time']=end-start
    #print(median)
    return median      
            
def initSessionState():

    if 'file' not in st.session_state:
        st.session_state['file'] = 'value'
    if 'img' not in st.session_state:
        st.session_state['img'] = 'value'
    if 'red' not in st.session_state:
        st.session_state['red'] = 'value'
    if 'green' not in st.session_state:
        st.session_state['green'] = 'value'
    if 'blue' not in st.session_state:
        st.session_state['blue'] = 'value'
    if 'redgreen' not in st.session_state:
        st.session_state['redgreen'] = 'value'
    if 'redblue' not in st.session_state:
        st.session_state['redblue'] = 'value'
    if 'bluegreen' not in st.session_state:
        st.session_state['bluegreen'] = 'value'
    if 'grayscale' not in st.session_state:
        st.session_state['grayscale'] = 'value'
    if 'time' not in st.session_state:
        st.session_state['time'] = 'value'
main()