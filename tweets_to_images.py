import textwrap
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from tqdm import tqdm
import pandas as pd
import os
import fire
import errno
import random
import cv2 

def tweets_to_images(
file, 
tweet_image,
bar = False,
date = False #adding date dramatically decreases performance due to addition of computer vision
):
    image = Image.open(tweet_image)
    base_width, base_height = image.size
    if base_width != 1500 & base_height != 300: raise #base_width / base_height != 5: raise
    else: pass

    try:
        os.makedirs('output')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    user = pd.read_csv(file, encoding='utf-8')
    print(user.size)
    user = user.drop_duplicates()
    print(user.size)
    user = user.tweets.tolist()

    for idx, tweet in enumerate(tqdm(user)):
        image = Image.open(tweet_image)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=37)
        tweet = "\n".join(textwrap.wrap(tweet, width=75))
        draw.text ((185,80), tweet, font = font, fill = (0,0,0))
        x_text,y_text = draw.textsize(tweet, font=font)
        x_text,y_text = x_text + 85,y_text + 85
        if bar == True:
            bar_info(image, draw, x_text, y_text)
        image.save('output/output_' + str(idx+1) + '.png')

# def testing_function (tweet_image, date = True, bar = True):
#     image = Image.open(tweet_image)
#     draw = ImageDraw.Draw(image)
#     font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=37)
#     tweet = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."
#     tweet = "\n".join(textwrap.wrap(tweet, width=75))
#     draw.text ((185,80), tweet, font = font, fill = (0,0,0))
#     x_text,y_text = draw.textsize(tweet, font=font)
#     x_text,y_text = x_text + 85,y_text + 85
#     if date == True:
#         date_info(image, draw, tweet_image)
#     if bar == True:
#         bar_info(image, draw, x_text, y_text)
#     image.save(r'D:\Github\Projects\Tweet-to-image\output4.png')

def bar_info(image, draw, x_text, y_text):
    box = Image.open(r'resources\bar_no_data.png')
    font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeui.ttf', size=35)
    image.paste(box, box=(185, y_text))
    draw.text((250, y_text+19), str(random.randrange(0,100)), font=font, fill = (101,119,134))
    draw.text((565, y_text+19), str(random.randrange(0,1000)), font=font, fill = (101,119,134))
    draw.text((865, y_text+19), str(random.randrange(0,1000)), font=font, fill = (101,119,134))

def date_info(image, draw, tweet_image): #have to utilize cv2 due to variable name length
    img = cv2.imread(tweet_image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15)) 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    cnt = contours[1]
    x,y,w,h = cv2.boundingRect(cnt)
    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    # cv2.imshow("Wall Detection", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=35)
    draw.text((x+w-4,y+1), ' · '+str(random.randrange(1,23)) + 'h', font = font, fill = (101,119,134))
    
if __name__ == "__main__":
    fire.Fire(tweets_to_images)
