from vector_class import vector
import pygame


class env_vars():
    G = 6.67 *10**(-1)

class point_mass():
    def __init__(self,mass,radius,position,screen,name,velocity=None,force = None, charge = 0):
        self.mass = mass
        self.radius = radius
        self.position = position
        self.screen = screen
        self.name = name
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
        self.put_text_on_screen(self.name+" "+str(round(self.velocity.magnitude(),2))+"m/s")

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

    def put_text_on_screen(self,text):
        myfont = pygame.font.SysFont('Comic Sans MS', 15)
        textsurface = myfont.render(text, False, (0, 0, 0))
        self.screen.blit(textsurface,(self.position.x+self.radius,self.position.y))
        
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
    
    def compute_forces(self,others):
        self.force = vector(0,0)
        self.compute_force_due_to_gravity(others)
        
    def compute_force_due_to_gravity(self,others):
        for other in others:
            radius_vector = other.position - self.position
            force = radius_vector.unit_vec() * (env_vars.G * self.mass*other.mass )/(radius_vector.magnitude()**2)
            self.force += force

    def test_for_collision(self,others):
        for other in others:
            radius_sum = self.radius + other.radius
            radius_vector = other.position - self.position
            if radius_sum >= radius_vector.magnitude():
               self.handle_collision_elastically(other)
                
        
    def handle_collision_elastically(self,other):
        final_v_x = ((self.mass-other.mass)/(self.mass+other.mass))*self.velocity.x + ((2*other.mass)/(self.mass+other.mass))*other.velocity.x
        final_v_y = ((self.mass-other.mass)/(self.mass+other.mass))*self.velocity.y + ((2*other.mass)/(self.mass+other.mass))*other.velocity.y
        final_v_x_o = ((other.mass-self.mass)/(self.mass+other.mass))*other.velocity.x + ((2*self.mass)/(self.mass+other.mass))*self.velocity.x
        final_v_y_o = ((other.mass-self.mass)/(self.mass+other.mass))*other.velocity.y + ((2*self.mass)/(self.mass+other.mass))*self.velocity.y
        self.velocity = vector(final_v_x,final_v_y)
        other.velocity = vector(final_v_x_o,final_v_y_o)

                
    def do_all(self,others):
        self.compute_forces(others)
        self.update_me()
        self.draw_me()
    
            
class all_masses():
    def __init__(self,masses_list):
        self.masses_list = masses_list

    def execute(self):
        copy_others = self.masses_list.copy()
        for item in self.masses_list:
            copy_others.remove(item)
            item.test_for_collision(copy_others)
            
        for item in self.masses_list:
            others = self.masses_list.copy()
            others.remove(item)
            item.do_all(others)
