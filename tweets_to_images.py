import textwrap
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from tqdm import tqdm
import pandas as pd
import os
import fire
import errno

def tweets_to_images(
file, 
tweet_image
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
        image.save('output/output_' + str(idx+1) + '.png')

if __name__ == "__main__":
    fire.Fire(tweets_to_images)
