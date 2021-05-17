from imdb import IMDb
import imdb
from PIL import Image, ImageDraw, ImageColor, ImageFont
import requests
from io import BytesIO
from colour import Color
import sys


class CreatePicture():
    def __init__(self, name, hexcode='#ffffe4'):
        self.ia = IMDb()
        self.dims = (800, 800)
        self.font = ImageFont.truetype("NotoSans-Condensed.ttf", 60)
        self.name = name
        try:
            self.rgb = ImageColor.getrgb(hexcode)
        except ValueError:
            print('Enter a valid colour / hexcode next time.')
            self.rgb = ImageColor.getrgb('#ffffe4')

    def getMovieByID(self, movieID):
        try:
            return self.ia.get_movie(movieID)
        except IndexError:

            print("This movie does not exist.")
            raise RuntimeError

    def getMovieIDFromName(self, movieName):
        try:
            return self.ia.search_movie(movieName)[0].movieID
        except IndexError:
            print("This movie does not exist.")

    def episodes(self, ID):
        try:
            series = self.ia.get_movie(ID)
            self.ia.update(series, 'episodes')
            seasons = series['episodes']
            seasons = {x: seasons.get(x) for x in sorted(seasons.keys())}
            try:
                x = {season: {episode: round(series['episodes'][season][episode]['rating'], 2)
                              for episode in series['episodes'][season]}
                     for season in seasons}
                return x
            except:
                x = {season: {} for season in seasons.keys()}
                for season, value in seasons.items():
                    dictionary = x.get(season)
                    for episode in series['episodes'][season]:
                        try:
                            val = round(series['episodes'][season][episode]['rating'], 2)
                            dictionary[episode] = val
                        except KeyError:
                            val = 0
                            dictionary[episode] = val
                    x[season] = dictionary
                return x
        except KeyError as e:
            print('Please enter a valid series 1.')
            return None
        except TypeError as e:
            print('Please enter a valid series 2.')
            return None
        except imdb._exceptions.IMDbDataAccessError:
            return None

    def getImage(self, ID):
        series = self.ia.get_movie(ID)
        try:
            image_url = series['full-size cover url']
        except KeyError:
            image_url = series['cover url']

        response = requests.get(image_url)
        im = Image.open(BytesIO(response.content))
        im = im.resize((200, 300))
        return im

    def drawBackground(self):
        image = Image.new("RGB", self.dims, color=self.rgb)

        return image

    def getText(self, ID):
        text = str(self.getMovieByID(ID))
        font = self.font
        txt = Image.new('RGB', (600, 100), self.rgb)

        draw = ImageDraw.Draw(txt)
        draw.text((0, 0), text, font=font, fill=(0, 0, 0))

        return txt

    def drawRatingBG(self):
        height = 600
        width = 400

        image = Image.new(mode='RGB', size=(width, height), color=self.rgb)

        return image

    def addRatings(self, ratings=None, grid=None):
        red = Color('red')
        green = Color('green')
        yellow = Color('yellow')
        cRange = list(green.range_to(yellow, 25)) + list(yellow.range_to(red, 75))

        epsLengths = [len(x) for x in ratings.values()]
        maxEps, maxIndex = max(epsLengths), epsLengths.index(max(epsLengths))

        W, H = int(400 / (len(ratings.values()) + 1)), int(600 / (maxEps + 1))
        boxSize = (W, H)
        font = ImageFont.truetype("NotoSans-Condensed.ttf", size=int((W / 10) + 5))

        for i, episodes in enumerate(ratings.values()):
            offset = (i + 1) * W, 0
            rgb = (169, 169, 169)
            image = Image.new(mode='RGB', size=boxSize, color=rgb)
            text = 'Season {}'.format(i + 1)

            draw = ImageDraw.Draw(image)
            w, h = draw.textsize(text, font=font)
            draw.text(((W - w) / 2, (H - h) / 2), text, fill=(0, 0, 0), font=font)
            grid.paste(image, offset)

            for j, rating in enumerate(episodes.values()):
                rating = rating if rating < 10.1 else 0
                if i == maxIndex:
                    offset = 0, (j + 1) * H
                    rgb = (169, 169, 169)
                    image = Image.new(mode='RGB', size=boxSize, color=rgb)
                    text = 'Episode {}'.format(j + 1)

                    draw = ImageDraw.Draw(image)
                    w, h = draw.textsize(text, font=font)
                    draw.text(((W - w) / 2, (H - h) / 2), text, fill=(0, 0, 0), font=font)
                    grid.paste(image, offset)

                text = str(rating)
                offset = (i + 1) * W, (j + 1) * H

                hexVal = cRange[100 - int(rating * 10) - 1] if rating != 10.0 else cRange[0]
                rgb = ImageColor.getrgb(str(hexVal.hex_l))
                image = Image.new(mode='RGB', size=boxSize, color=rgb)

                draw = ImageDraw.Draw(image)
                w, h = draw.textsize(text, font=font)
                draw.text(((W - w) / 2, (H - h) / 2), text, fill=(0, 0, 0), font=font)

                grid.paste(image, offset)

        return grid

    def combine(self, img, background, txt, grid, mode):
        img_offset = 50, 150
        txt_offset = 50, 25
        grid_offset = 300, 150
        background.paste(img, img_offset)
        background.paste(txt, txt_offset)
        background.paste(grid, grid_offset)
        if mode == 'show':
            background.show(title=self.name)
        else:
            background.save(self.name + '.png', format='png')

    def createImage(self, mode='save'):
        ID = self.getMovieIDFromName(self.name)
        ratings = self.episodes(ID)
        if ratings is not None:
            img = self.getImage(ID)
            bg = self.drawBackground()
            txt = self.getText(ID)
            grid = self.drawRatingBG()
            ratingsBG = self.addRatings(ratings=ratings, grid=grid)
            self.combine(img, bg, txt, ratingsBG, mode)


if len(sys.argv) > 1:
    name = str(sys.argv[1])
    savePos = 0
    hexcode = '#ffffe4'
    mode = 'show'
    if name == '--help':
        print('         -type the name of the show you want in quotes ("")')
        print('         -If you also want an alternative coloured background use a full hexcode')
        print('         or a basic colour also in quotes')
        print('         -If you want to save the photo to the directory that the python file is saved')
        print('         use --save at the end of the argument')
    else:
        if len(sys.argv) > 2:
            if '--save' in str(sys.argv):
                savePos = 2 if len(sys.argv) < 4 else 3
            hexcode = sys.argv[2] if savePos != 2 else '#ffffe4'
        self = CreatePicture(name, hexcode)
        mode = 'save' if savePos != 0 else 'show'
        self.createImage(mode=mode)
