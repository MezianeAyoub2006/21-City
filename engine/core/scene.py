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
    
    def get_objects(self):
        return self.objects

    def get_objects_by_tags(self, *tags):
        objs = []
        for obj in self.objects:
            if set(tags).intersection(set(obj.tags)):
                objs.append(obj)
        return objs
    
    def get_objects_by_tag(self, tag):
        return list(filter(lambda obj : tag in obj.tags, self.objects))