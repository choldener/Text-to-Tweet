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

def tweets_to_images(
file, 
tweet_image,
bar = False,
date = False
):
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

def testing_function (file, tweet_image, info = True, date = True, bar = True):
    image = Image.open(tweet_image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=37)
    tweet = ""
    tweet = "\n".join(textwrap.wrap(tweet, width=75))
    draw.text ((185,80), tweet, font = font, fill = (0,0,0))
    x_text,y_text = draw.textsize(tweet, font=font)
    x_text,y_text = x_text + 85,y_text + 85
    # if date == True:
    #     date_info()
    if bar == True:
        bar_info(image, draw, x_text, y_text)
    image.save(r'D:\Github\Projects\Tweet-to-image\output4.png')

def bar_info(image, draw, x_text, y_text):
    box = Image.open(r'resources\bar_no_data.png')
    font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=35)
    image.paste(box, box=(185, y_text))
    date = random.randrange(0,1)
    print('parmas set')
    print(draw) 
    ######## Still need to figure out coords on image
    draw.text((250, y_text+19), str(random.randrange(0,100)), font=font, fill = (101,119,134))
    draw.text((565, y_text+19), str(random.randrange(0,1000)), font=font, fill = (101,119,134))
    draw.text((865, y_text+19), str(random.randrange(0,1000)), font=font, fill = (101,119,134))
    draw.text((950, 25), str(date), font=font, fill = (101,119,134))
    ########

# def date_info(image, draw):
#     box = Image.open(r'resources\date_dot.png')
#     font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=35)
#     image.paste(box, box=(950, 25))
#     draw.text((950,25), str(random.randrange(1,23)) + 'h', font = font, fill = (101,119,134))
    
if __name__ == "__main__":
    fire.Fire(tweets_to_images)
