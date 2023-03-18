from turtle import width
from PIL import Image

image=Image.open('index.jpeg')
image=image.resize((1920,1080),Image.NEAREST)
width, height = image.size
pixels=image.load()

def prepare(Iwidth,Iheight):
    width='1fr '*Iwidth
    height='1fr '*Iheight
    f=open('image.css','w')
    f.write(".container {\n")
    f.write('    display: grid; \n')
    f.write('    width:'+str(Iwidth)+'px;\n')
    f.write('    height:'+str(Iheight)+'px;\n')
    f.write('    grid-template-columns: '+width+';\n')
    f.write('    grid-template-rows: '+height+';\n')
    f.write('    gap: 0px 0px; \n')
    f.write('    grid-template-areas: \n')

    line=' . '*Iwidth
    for i in range(0,Iheight):
        f.write('   "'+line+'"\n')
    f.write(';\n\n')
    f.write('}')
    
def genHTML():
    test="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="image.css" />
</head>
<body>
<div class="container">"""
    
    f=open('image.html', 'w')
    f.write(test)
    print(width, height)
    for i in range(height):
        for j in range(width):
            r, g, b = pixels[j, i]
            f.write(f'   <div style="background-color:rgb({r},{g},{b}); height:1px; width:1px;"></div>\n')
   
        
    f.write('</div>\n</body>\n</html>')
    

prepare(width,height)
genHTML()


