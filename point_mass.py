from vector_class import vector
import pygame

class env_vars():
    G = 6.67 *10**(-1)

class point_mass():
    def __init__(self,mass,radius,position,screen,velocity=None,force = None, charge = 0):
        self.mass = mass
        self.radius = radius
        self.position = position
        self.screen = screen
        if velocity is None:
            self.velocity = vector(0,0)
        else:
            self.velocity = velocity
        if force is None:
            self.force = vector(0,0)
        else:
            self.force = force
        self.charge = charge
        self.afterimages = []
        self.traces = []

    def draw_me(self):
        self.draw_after_images()
        #pygame.draw.circle(self.screen,(0,0,0),(int(self.position.x),int(self.position.y)),self.radius)

    def draw_after_images(self):
        for pos in self.afterimages:
            pygame.draw.circle(self.screen,(255,255,0),(int(pos.x),int(pos.y)),self.radius)
        pygame.draw.circle(self.screen,(255,0,0),(int(pos.x),int(pos.y)),self.radius)
        self.trace_me()
        
    def trace_me(self):
        points = []
        for point in self.traces:
            points.append((point.x,point.y))
        for i in range(1,len(points)):
            pygame.draw.line(self.screen,(0,0,255),(points[i-1][0],points[i-1][1]),(points[i][0],points[i][1]))
            
    def update_me(self):
        acceleration = self.force/self.mass
        self.velocity += acceleration
        self.position += self.velocity
        
        if len(self.afterimages)>5:
            self.afterimages.pop(0)
        self.afterimages.append(self.position)
        if len(self.traces)>400:
            self.traces.pop(0)
        self.traces.append(self.position)
    

    def compute_force_due_to_gravity(self,others):
        self.force = vector(0,0)
        for other in others:
            radius_vector = other.position - self.position
            force = radius_vector.unit_vec() * (env_vars.G * self.mass*other.mass )/(radius_vector.magnitude()**2)
            self.force += force

    def test_for_collision(self,others):
        for other in others:
            radius_sum = self.radius + other.radius
            radius_vector = other.position - self.position
            if radius_sum >= radius_vector.magnitude():
                self.velocity = vector(0,0)
                self.force  = vector(0,0)
                
    def do_all(self,others):
        self.compute_force_due_to_gravity(others)
        self.test_for_collision(others)
        self.update_me()
        self.draw_me()
    
            
class all_masses():
    def __init__(self,masses_list):
        self.masses_list = masses_list

    def execute(self):
        for item in self.masses_list:
            others = self.masses_list.copy()
            others.remove(item)
            item.do_all(others)
