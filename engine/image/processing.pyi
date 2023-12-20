import os, pygame
from typing import *
from PIL import Image
from engine.image.slicer import Slicer, convert_PIL_pygame

def set_path(path:str):
    """
nebulix.image.processing.set_path

Modify image folder path.

Args:
    path str : path to your image folder
    """
    ...

def load_image(path:str):
    """
nebulix.image.processing.load_image

Get pygame surface from image path.

Args:
    path str : relative path from the image folder to get the image
    """
    ...

def load_images(path:str):
    """
nebulix.image.processing.load_images

Get images all images from a folder.

Args:
    path str : relative path from the image folder to the folder
    """
    ...

def set_alpha(image:pygame.Surface, alpha:int):
    """
nebulix.image.processing.set_alpha

Return modifed image with different alpha values.

Args:
    image pygame.Surface : image to modify 
    alpha 0 < int < 255  : alpha value to apply

    """
    ...

def scale_image_list(images:List[pygame.Surface], scaling:Tuple[int, int]):
    """
nebulix.image.processing.scale_image_list

Scale an image list.

Args:
    images [pygame.Surface]    : list of images
    scaling (int > 0, int > 0) : size of new images
    """
    ...

def scale_animations(animations:List[List], scaling:Tuple[int, int]):
    """
nebulix.image.processing.scale_animations

Scale animation matrix.

Args:
    animations [list]          : animation matrix
    scaling (int > 0, int > 0) : size of new frames
    """
    ...
 
def get_outline(image:pygame.Surface, color:Tuple[int, int, int]=(0,0,0)):
    """
nebulix.image.processing.get_outline

Return the outline of an image.

Args:
    image pygame.Surface  : 
    color (int, int, int) : color of the outline
    """
    ...
  
def load_sprite(path:str, slicing:Tuple[int, int]):
    """
nebulix.image.processing.load_sprite

Load a sprite sheet.

Args:
    path str                   : path to the sprite sheet image
    slicing (int > 0, int > 0) : size of every frame
    """
    ...
  
def load_animation(path:str, slicing:Tuple[int, int], frames:int):
    """
nebulix.image.processing.load_animation

Load animation.

Args:
    path str                   : path to the animation image
    slicing (int > 0, int > 0) : size of every frame
    """
    ...
  