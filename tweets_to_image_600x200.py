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
date = False, #adding date dramatically decreases performance due to addition of computer vision
character_color = False
):
    image = Image.open(tweet_image)
    base_width, base_height = image.size
    #if base_width != 600 & base_height != 200: raise ValueError#base_width / base_height != 5: raise
    #else: pass

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
        font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=15)
        tweet = "\n".join(textwrap.wrap(tweet, width=75))
        x_text,y_text = draw.textsize(tweet, font=font)
        y_text = y_text + 45
        if character_color == True: line_by_line(tweet=tweet, font=font, draw=draw)
        else:
            draw.text ((75,36-6), tweet, font = font, fill = (0,0,0))
            x_text,y_text = draw.textsize(tweet, font=font)
            y_text = y_text + 45
        if bar == True: bar_info(image, draw, x_text, y_text)
        if date == True: date_info(image, draw, tweet_image)
        image.save('output/output_' + str(idx+1) + '.png')


def testing_function (tweet_image, date = True, bar = True, character_color=True):
    image = Image.open(tweet_image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=15)
    tweet = "The Democrats, together #correup #media with #help the corrupt Fake News Media, have launched a massive Disinformation Campaign the likes of which has never been seen before. They will say anything, like their recent lies about me and the Military, and hope that it sticks... But #MAGA gets it!"
    tweet = "\n".join(textwrap.wrap(tweet, width=75))
    x_text,y_text = draw.textsize(tweet, font=font)
    y_text = y_text + 45
    if character_color == True: line_by_line(tweet=tweet, font=font, draw=draw)
    else: 
        draw.text ((75,36-6), tweet, font = font, fill = (0,0,0))
        x_text,y_text = draw.textsize(tweet, font=font)
        y_text = y_text + 45
    if date == True: date_info(image, draw, tweet_image)
    if bar == True: bar_info(image, draw, x_text, y_text)
    image.save(r'D:\Github\Projects\Tweet-to-image\output_test.png')


def bar_info(image, draw, x_text, y_text):
    box = Image.open(r'resources\bar_no_data_600.png')
    font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeui.ttf', size=14)
    image.paste(box, box=(75, y_text))
    draw.text((104, y_text-2), str(random.randrange(0,100)), font=font, fill = (101,119,134))
    draw.text((231, y_text-2), str(random.randrange(0,1000)), font=font, fill = (101,119,134))
    draw.text((368, y_text-2), str(random.randrange(0,1000)), font=font, fill = (101,119,134))


def date_info(image, draw, tweet_image): #have to utilize cv2 due to variable name length
    img = cv2.imread(tweet_image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15)) 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    cnt = contours[1]
    x,y,w,h = cv2.boundingRect(cnt)
    
    font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeui.ttf', size=15)
    draw.text((x+w-6,y+5), ' · '+str(random.randrange(1,23)) + 'h', font = font, fill = (101,119,134))
    
    

def line_by_line(tweet, font, draw):
    tweet_list = tweet.splitlines()
    ybase = 36-6
    for tweet_line in tweet_list:
        #print(tweet_line)
        xbase = 75
        character_instance = False
        space_instance = False
        start_index=0
        for i, c  in enumerate(tweet_line):
            if c == '#' or c=='@':
                #print('Character true')
                character_instance = True #Shows that a character is in that line
                character_index = i
                draw.text((xbase,ybase), tweet_line[start_index:character_index],font=font, fill=(0,0,0)) #words before hashtag
                x,y = draw.textsize(tweet_line[start_index:character_index],font=font)
                xbase = xbase + x
                for n,c in enumerate(tweet_line[i:], character_index):
                    if c == ' ' or c== ')' or c== ']':
                        space_instance = True
                        space_index = n
                        word = tweet_line[character_index:space_index] #the hashtag
                        print(word)
                        draw.text((xbase,ybase), word, font=font, fill =(27, 149, 224))
                        x,y = draw.textsize(word, font=font)
                        xbase = xbase + x
                        start_index = space_index
                        break
                    else: pass
                if space_instance == False:
                    draw.text((xbase,ybase), tweet_line[i:], font = font, fill = (27, 149, 224))
            else: pass
        if character_instance == False: # if character is not in a line after reading it, then it pastes it as default
            #print('no character')
            draw.text((xbase,ybase), tweet_line, font = font, fill = (0,0,0))
        if character_instance == True & space_instance == True:
            draw.text((xbase,ybase), tweet_line[space_index:], font=font,fill=(0,0,0))
        x,y = draw.textsize(tweet_line, font=font)
        ybase = ybase + y #goes down the line.
        
# if __name__ == "__main__":
#     fire.Fire(tweets_to_images)

testing_function(tweet_image = r"D:\Github\Projects\Tweet-to-image\templates\Trump_600x200_blank.png", date = True, bar = True, character_color=True)
#tweets_to_images(file=r"D:\Github\Projects\Tweet-to-image\realDonaldTrump_tweets.csv",  tweet_image=r"D:\Github\Projects\Tweet-to-image\templates\Trump_600x200_blank.png", bar = True, date = True, character_color = True)