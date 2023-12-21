z_pos_func = lambda obj : obj.z_pos

class Scene:
    
    def __init__(self):
        self.objects = []

    def update(self):
        for object in filter(z_pos_func, self.objects):
            try:
                object.update(self)
            except AttributeError:
                pass