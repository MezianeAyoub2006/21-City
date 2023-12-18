import os, pygame
from typing import *
from PIL import Image
from nebulix.image.slicer import Slicer, convert_PIL_pygame

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
    ...

def scale_image_list(images:List[pygame.Surface], scaling:Tuple[int, int]):
    ...

def scale_animations(animations:List[List], scaling:Tuple[int, int]):
    ...
 
def get_outline(image:pygame.Surface, color:Tuple[int, int, int]=(0,0,0)):
    ...
  
def load_sprite(path:str, slicing:Tuple[int, int]):
    ...
  
def load_animation(path:str, slicing:Tuple[int, int], frames:int):
    ...
  