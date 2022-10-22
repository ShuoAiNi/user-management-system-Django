import random
from PIL import Image,ImageDraw,ImageFont,ImageFilter

def check_code(width=128,height=30,char_length=5,font_file="BOD_R.TTF",font_size=28):
    code=[]

    #画布长128，宽30
    img = Image.new(mode="RGB",size=(width,height),color=(255,255,255))
    #函数声明，在img上绘图
    draw = ImageDraw.Draw(img,mode="RGB")

    def rndChar():
        """生成随机字母"""
        return chr(random.randint(65,90))

    def rndColor():
        """生成随机颜色"""
        return (random.randint(0,255),random.randint(10,255),random.randint(64,255))

    #写文字
    font = ImageFont.truetype(font_file,font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(1,3)
        x=  int(i * width / char_length)
        #(x,h)为字符在图片上的坐标
        draw.text((x,h),char,font=font,fill=rndColor())

    #写干扰点
    for i in range(50):
        draw.point((random.randint(0,width),random.randint(0,height)),fill=rndColor())

    #写干扰圆圈
    for i in range(40):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=rndColor())
        x = random.randint(0,width)
        y = random.randint(0,height)
        draw.arc((x,y,x+4,y+4),0,90,fill=rndColor())

    for i in range(6):
        x1 = random.randint(0,width)
        y1 = random.randint(0,height)
        x2 = random.randint(0,width)
        y2 = random.randint(0,height)
        draw.line((x1,y1,x2,y2),fill=rndColor())

    #边界增强版加强滤镜EDGE_ENHANCE_MORE
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return img, ''.join(code)











