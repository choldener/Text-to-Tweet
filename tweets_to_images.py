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
info = False
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
        if info == True:
            random_info(image, draw, x_text, y_text)
        image.save('output/output_' + str(idx+1) + '.png')

def random_info(image, draw, x_text, y_text):
    box = Image.open(r'\'resources\box_no_info.png')
    font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=30)
    image.paste(box, box=(185, y_text))
    likes = random.randrange(0,1000)
    retweets = random.randrange(0,1000)
    comments = random.randrange(0,100)
    date = random.randrange(0,1)
    ######## Still need to figure out coords on image
    # draw.text((), likes, font=font, fill = (101,119,134))
    # draw.text((), retweets, font=font, fill = (101,119,134))
    # draw.text((), comments, font=font, fill = (101,119,134))
    # draw.text((), date, font=font, fill = (101,119,134))
    ########

def testing_function (file, tweet_image, info = True):
    image = Image.open(tweet_image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r'C:\Windows\Fonts\Segoeuisl.ttf', size=37)
    tweet = "We are getting the Commercial Fishing Industry in Maine back on track (will be better than ever) after suffering years of stupidity and abuse from the previous administration. Already got 5000 square miles back and available to fish. China & E.U. told to drop their Tariffs now!!!"
    tweet = "\n".join(textwrap.wrap(tweet, width=75))
    draw.text ((185,80), tweet, font = font, fill = (0,0,0))
    x_text,y_text = draw.textsize(tweet, font=font)
    x_text,y_text = x_text + 85,y_text + 85
    if info == True:
        random_info(image, draw, x_text, y_text)
    image.save(r'D:\Github\Projects\Tweet-to-image\output5.png')
    
if __name__ == "__main__":
    fire.Fire(tweets_to_images)
