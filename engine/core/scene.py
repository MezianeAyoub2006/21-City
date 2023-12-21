z_pos_func = lambda obj : obj.z_pos

class Scene:
    
    def __init__(self):
        self.objects = []

    def update(self):
        for object in sorted(self.objects, key=z_pos_func):
            object.update(self)
    
    def link(self, *args):
        for arg in args:
            self.objects.append(arg)