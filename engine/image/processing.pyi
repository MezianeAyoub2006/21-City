import os, pygame
from typing import *
from PIL import Image
from engine.image.slicer import Slicer, convert_PIL_pygame

def set_path(path:str) -> None:
    """
nebulix.image.processing.set_path

Modify image folder path.

Args:
    path : path to your image folder
    """
    ...

def load_image(path:str) -> pygame.Surface:
    """
nebulix.image.processing.load_image

Get pygame surface from image path.

Args:
    path : relative path from the image folder to get the image
    """
    ...

def load_images(path:str) -> List[pygame.Surface]:
    """
nebulix.image.processing.load_images

Get images all images from a folder.

Args:
    path : relative path from the image folder to the folder
    """
    ...

def set_alpha(image:pygame.Surface, alpha:int) -> pygame.Surface:
    """
nebulix.image.processing.set_alpha

Return modifed image with different alpha values.

Args:
    image : surface to modify 
    alpha : alpha value to apply

    """
    ...

def scale_image_list(images:List[pygame.Surface], scaling:Tuple[int, int]) -> List[pygame.Surface]:
    """
nebulix.image.processing.scale_image_list

Scale an image list.

Args:
    images  : list of images
    scaling : size of new images
    """
    ...

def scale_animations(animations:List[List[pygame.Surface]], scaling:Tuple[int, int]) -> List[List[pygame.Surface]]:
    """
nebulix.image.processing.scale_animations

Scale animation matrix.

Args:
    animations : animation matrix
    scaling    : size of new frames
    """
    ...
 
def get_outline(image:pygame.Surface, color:Tuple[int, int, int]=(0,0,0)) -> pygame.Surface:
    """
nebulix.image.processing.get_outline

Return the outline of an image.

Args:
    image : image to get the outline from
    color : color of the outline
    """
    ...
  
def load_sprite(path:str, slicing:Tuple[int, int]) -> List[pygame.Surface]:
    """
nebulix.image.processing.load_sprite

Load a sprite sheet.

Args:
    path    : path to the sprite sheet image
    slicing : size of every frame
    """
    ...
  
def load_animation(path:str, slicing:Tuple[int, int], frames:int) -> List[List[pygame.Surface]]:
    """
nebulix.image.processing.load_animation

Load animation.

Args:
    path    : path to the animation image
    slicing : size of every frame
    """
    ...
  
def organise_into_animation(sprite, slicing, frames):
    ...