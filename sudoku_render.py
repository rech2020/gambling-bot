from PIL import Image, ImageDraw, ImageFont
import random
import os
import math

def drawsudoku(width:int=9,height:int=9,cell_size:int=60,skin:dict=None,numbers_grid:list[list]=None,user_numbers_grid:list[list]=None)-> Image.Image:
    if (len(numbers_grid)<height or len(numbers_grid[0])<width)and(len(numbers_grid)<height or len(numbers_grid[0])<width):
        print("WARNING: numbers grid is... both longer and shorter than the given height and width???????")
    elif len(numbers_grid)<height or len(numbers_grid[0])<width:
        print("WARNING: numbers grid is shorter than given width/height. im not sure if that was some optimization or not")
    elif len(numbers_grid)<height or len(numbers_grid[0])<width:
        print("WARNING: numbers grid is longer than given width/height.")
    
    image_width=width*cell_size
    image_height=height*cell_size
    default_skin={
            "background": "#e6eef2",
            "border1": "#34495e",
            "border2": "#cfdbe4",
            "font1": "#34495e",
            "font2": "#2980b9",
            "select":"#3cd3ff",
    }
    if skin==None:
        skin=default_skin
    else:
        if not skin['background']or not skin['border1'] or not skin["border2"] or not skin['font1'] or not skin['font2'] or not skin['select']:
            print('skin missing certain values')
            return
    
    # attempt to load the funny papyrus font
    try:
        font = ImageFont.truetype("papyrus-pixel.ttf", size=cell_size)
    except: # aw man it didnt load
        try: # try to load the sands font
            font = ImageFont.truetype("Comic Sans MS Pixel.ttf", size=cell_size)
        except: # aw man it didnt load either
            # load the default font
            font = ImageFont.load_default(size=cell_size//1.25)

    # make a BLANK image
    img = Image.new('RGB',size=[image_width,image_height],color=skin['background'])
    draw = ImageDraw.Draw(img)
    # draw a small grid
    for i in range(width): # draw the horizontal lines
        draw.line([image_width-(cell_size*i),0,image_width-(cell_size*i),image_height],fill=skin['border2'],width=2)
    for i in range(height): # draw the vertical lines
        draw.line([0,image_height-(cell_size*i),image_width,image_height-(cell_size*i)],fill=skin['border2'],width=2)
    # if the grid is either: 9x9, 6x6 or 4x4: draw the big grid
    if (width==height==9):
        for i in range(width//3): # draw the horizontal lines
            draw.line([image_width-(cell_size*3*i),0,image_width-(cell_size*3*i),image_height],fill=skin['border1'],width=2)
        for i in range(width//3): # draw the vertical lines
            draw.line([0,image_height-(cell_size*3*i),image_width,image_height-(cell_size*3*i)],fill=skin['border1'],width=2)
    elif (width==height==6):
        pass # i will implement this later trust

    # draw the big border
    draw.rectangle([0,0,image_width,image_height],outline=skin['border1'],width=3)

    # draw the og numbers
    for y in range(height):
        for x in range(width):
            if numbers_grid!=None:
                if numbers_grid[y][x]!=None:
                    if numbers_grid[y][x]>0:
                        cell_x = x * cell_size
                        cell_y = y * cell_size
                        number = str(numbers_grid[y][x])
                
                        # Get text size using textbbox (replacement for getsize)
                        bbox = draw.textbbox((0, 0), number, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                
                        # Calculate text position (centered in cell)
                        text_x = cell_x + (cell_size - text_width) // 2
                        text_y = cell_y + (cell_size - text_height) // 2 - 10
                
                        draw.text((text_x, text_y), number, fill=skin['font1'], font=font)
    # draw the user's numbers
    for y in range(height):
        for x in range(width):
            if user_numbers_grid!=None:
                if user_numbers_grid[y][x]>0 and not numbers_grid[y][x]>0 and user_numbers_grid[y][x]!=None:
                    cell_x = x * cell_size
                    cell_y = y * cell_size
                    number = str(user_numbers_grid[y][x])

                    # Get text size using textbbox (replacement for getsize)
                    bbox = draw.textbbox((0, 0), number, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]

                    # Calculate text position (centered in cell)
                    text_x = cell_x + (cell_size - text_width) // 2
                    text_y = cell_y + (cell_size - text_height) // 2 - 10

                    draw.text((text_x, text_y), number, fill=skin['font2'], font=font)

    return img

def drawsudokuv2(width:int=3,height:int=None,cell_size:int=60,skin:dict=None,board:list[list]=None,user_board:list[list]=None)-> Image.Image:
    """
    draws the given board
    :param width: the board's width, e.g. a standard sudoku has a width of 3
    :param height: the board's height, e.g. a standard sudoku has a width of 3
    :param cell_size: the size of the cells on the image
    :param skin: a dictionary containing hex color values for background, borders, and fonts
    :param board: a matrix containing the sudoku board obviously
    :param user_board: a matrix containing the numbers that the user wrote
    :return: an image
    """
    if height==None:
        height=width
    # calculate the base image height and width
    image_width=width*height*cell_size
    image_height=height*width*cell_size
    # default skin that i totally didnt steal
    default_skin={
        "background": "#e6eef2",
        "border1": "#34495e",
        "border2": "#cfdbe4",
        "font1": "#34495e",
        "font2": "#2980b9",
        "select":"#3cd3ff",
    }
    # safeguards in case someone doesnt pass a skin or passes a skin thats missing some values
    if skin==None:
        skin=default_skin
    else:
        if not skin['background']or not skin['border1'] or not skin["border2"] or not skin['font1'] or not skin['font2']:
            print('skin missing certain values, defaulting to the default skin')
            skin=default_skin
    
    # attempt to load the funny papyrus font
    try:
        font = ImageFont.truetype("papyrus-pixel.ttf", size=cell_size)
    except: # aw man it didnt load
        try: # try to load the sands font
            font = ImageFont.truetype("Comic Sans MS Pixel.ttf", size=cell_size)
        except: # aw man it didnt load either
            # load the default font
            font = ImageFont.load_default(size=cell_size)
    
    # make a BLANK image
    img = Image.new('RGB',size=[image_width,image_height],color=skin['background'])
    draw = ImageDraw.Draw(img)

    # draw a small grid
    for i in range(width*height): # draw the horizontal lines
        draw.line([image_width-(cell_size*i),0,image_width-(cell_size*i),image_height],fill=skin['border2'],width=2)
    for i in range(height*width): # draw the vertical lines
        draw.line([0,image_height-(cell_size*i),image_width,image_height-(cell_size*i)],fill=skin['border2'],width=2)
    # draw the BIG grid
    for i in range(width): # draw the horizontal lines
        draw.line([image_width-(cell_size*height*i),0,image_width-(cell_size*height*i),image_height],fill=skin['border1'],width=2)
    for i in range(height): # draw the vertical lines
        draw.line([0,image_height-(cell_size*width*i),image_width,image_height-(cell_size*width*i)],fill=skin['border1'],width=2)

    # draw the big border
    draw.rectangle([0,0,image_width,image_height],outline=skin['border1'],width=3)

    # draw the og numbers
    for y in range(height*width):
        for x in range(width*height):
            if board!=None:
                if board[y][x]!=None:
                    if board[y][x]>0:
                        cell_x = x * cell_size
                        cell_y = y * cell_size
                        number = str(board[y][x])
                
                        # Get text size using textbbox (replacement for getsize)
                        bbox = draw.textbbox((cell_x, cell_y), number, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                
                        # Calculate text position (centered in cell)
                        text_x = cell_x + (cell_size - text_width) // 2
                        text_y = cell_y + (cell_size - text_height) // 2 - (cell_size//4)

                        #draw.rectangle((bbox[0],bbox[1],bbox[2],bbox[3]),outline="red") # debug stuff nothing important
                        draw.text((text_x, text_y), number, fill=skin['font1'], font=font)

    # draw the user numbers
    for y in range(height*width):
        for x in range(width*height):
            if user_board!=None:
                if user_board[y][x]!=None:
                    if user_board[y][x]>0 and ((not board[y][x]>0)if board[y][x] is not None else True):
                        cell_x = x * cell_size
                        cell_y = y * cell_size
                        number = str(user_board[y][x])
                
                        # Get text size using textbbox (replacement for getsize)
                        bbox = draw.textbbox((cell_x, cell_y), number, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                
                        # Calculate text position (centered in cell)
                        text_x = cell_x + (cell_size - text_width) // 2
                        text_y = cell_y + (cell_size - text_height) // 2 - (cell_size//4)

                        #draw.rectangle((bbox[0],bbox[1],bbox[2],bbox[3]),outline="red") # debug stuff nothing important
                        draw.text((text_x, text_y), number, fill=skin['font2'], font=font)

    
    # return the image
    return img