from functions import* 
import tkinter as tk
import time
import numpy as np




WIDTH = 500
HEIGHT = 500

ROTATION = [-1, 0, +1] 
MOTION = [-1, 0, +1]

class VehicleSimulator:
    def __init__(self, shema_loic=False, shema_eliott=False):
        self.window = tk.Tk()
        self.window.title("Simulator")
        self.window.iconbitmap("car.ico")
        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        # variable de test/runing
        self.step = 0
        self.random_motion, self.random_rotation = False, False
        self.constant_speed = False
        self.slow = False
        self.shema_loic, self.shema_eliott = shema_loic, shema_eliott

        self.x = WIDTH*3/5

        if self.shema_eliott:
            # Draw rails
            self.rails_thickness = 35
            self.init_rails(HEIGHT/2, self.rails_thickness)

            # Draw roads
            self.road_L_thickness = self.road__R_thickness = 40
            self.init_roads(WIDTH*2/5, self.road_L_thickness)
            self.init_roads(WIDTH*3/5, self.road__R_thickness)

        if self.shema_loic:
            # Draw rails
            self.canvas.create_line(340, 140, 500, 140, width=4)
            self.canvas.create_line(340, 188, 500, 188, width=4)

            self.canvas.create_line(0, 130, 150, 130, width=4)
            self.canvas.create_line(0, 198, 150, 198, width=4)

            self.canvas.create_line(340, 230, 500, 230, width=4)
            self.canvas.create_line(340, 280, 500, 280, width=4)

            # vertical road
            #up
            self.canvas.create_line(210, 120, 210, 0, width=2)
            self.canvas.create_line(288, 120, 288, 0, width=2)

            #down
            self.canvas.create_line(210, 300, 210, 500, width=2)
            self.canvas.create_line(288, 300, 288, 500, width=2)

            self.canvas.create_line(150, 120, 340, 120, width=1)
            self.canvas.create_line(150, 300, 340, 300, width=1)
            self.canvas.create_line(150, 120, 150, 300, width=1)
            self.canvas.create_line(340, 120, 340, 300, width=1)
            self.canvas.create_line(150, 210, 340, 210, width=1)
            self.x = 248


        # # droite modèles 30 degre
        # self.canvas.create_line(750, 0, 0, 375, width=4)
        # self.canvas.create_line(300, 0, 0, 600, width=4)


        # # Draw platform
        # self.platform_width, self.platform_height = 300, 200
        # self.canvas.create_polygon(*get_4points(WIDTH/2, HEIGHT/2, self.platform_width, self.platform_height), fill='', outline='blue')

        # Draw vehicle
        self.y = HEIGHT-50
        self.motion = MOTION[1]
        self.speed = 0
        self.rotation = ROTATION[1]
        self.vehicle_angle = 0
        self.v_width, self.v_height = 40, 70
        self.vehicle = self.canvas.create_polygon(*get_4points(self.x, self.y, self.v_width, self.v_height), fill="green")


        # Create buttons on grid(frame)
        self.frame = tk.Frame(self.window)
        self.frame.pack()

        label = tk.Label(self.frame, text="MOTION")
        label.grid(row=0, column=0)
        button1 = tk.Button(self.frame, text="backward", command=lambda: self.button_motion(0))
        button2 = tk.Button(self.frame, text="still", command=lambda: self.button_motion(1))
        button3 = tk.Button(self.frame, text="forward", command=lambda: self.button_motion(2))
        button1.grid(row=0, column=1)
        button2.grid(row=0, column=2)
        button3.grid(row=0, column=3)

        label = tk.Label(self.frame, text="ROTATION")
        label.grid(row=1, column=0)
        button4 = tk.Button(self.frame, text="left", command=lambda: self.button_rotation(0))
        button5 = tk.Button(self.frame, text="still", command=lambda: self.button_rotation(1))
        button6 = tk.Button(self.frame, text="right", command=lambda: self.button_rotation(2))
        button4.grid(row=1, column=1)
        button5.grid(row=1, column=2)
        button6.grid(row=1, column=3)

        button_reset = tk.Button(self.frame, text="RESET", command=self.reset)
        button_reset.grid(row=0, column=4)
        button_quit = tk.Button(self.frame, text="QUIT", command=self.button_quit)
        button_quit.grid(row=1, column=4)

        # Text creation
        space_between_text = 15
        text_position_x = WIDTH/6
        self.text_x_y = self.canvas.create_text(text_position_x, space_between_text, text="(x,y) = ({},{})".format(round(self.x,1),round(self.y,1)), font=('Arial', 10))
        self.text_vehicle_angle = self.canvas.create_text(text_position_x, space_between_text*2, text="vehicle_angle = {}".format(round(self.vehicle_angle,1)), font=('Arial', 10))
        self.text_motion = self.canvas.create_text(text_position_x, space_between_text*3, text="motion = {}".format(round(self.motion,1)), font=('Arial', 10))
        self.text_step = self.canvas.create_text(text_position_x, space_between_text*4, text="step = {}".format(self.step), font=('Arial', 10))

    # Buttons functions
    def button_motion(self, number):
    	if number==0:
    		self.motion = MOTION[0]
    	elif number==1:
    		self.motion = MOTION[1]
    	elif number==2:
        	self.motion = MOTION[2]
        
    def button_rotation(self, number):
    	if number==0:
    		self.rotation = ROTATION[0]
    	elif number==1:
    		self.rotation = ROTATION[1]
    	elif number==2:
    		self.rotation = ROTATION[2]

    def button_quit(self):
        self.window.destroy()

    # Draw roads function
    def init_roads(self, width, thickness):
      self.canvas.create_line(width-thickness, 0, width-thickness, HEIGHT, width=2)
      self.canvas.create_line(width+thickness, 0, width+thickness, HEIGHT, width=2)

    # Draw rails function
    def init_rails(self, height, thickness):
      self.canvas.create_line(0, height-thickness, WIDTH, height-thickness, width=5)
      self.canvas.create_line(0, height+thickness, WIDTH, height+thickness, width=5)

    # implémentation d'une accélération et décélération
    def update_speed(self):
        if self.motion != 0:
            self.speed += self.motion
        elif self.speed < 0:
            self.speed += 1
        elif self.speed > 0:
            self.speed -= 1

    # Update position function
    def update_position(self):
        rotate(self.vehicle, self.rotation, self.canvas)
        self.vehicle_angle += self.rotation

        if self.constant_speed:
            self.speed = 1
            movement = move_forward(self.vehicle, self.speed*self.motion, self.vehicle_angle)
        else:
            self.update_speed()
            movement = move_forward(self.vehicle, self.speed, self.vehicle_angle)

        self.canvas.move(self.vehicle, movement[0], movement[1])
        # maj de self.x, self.y
        x0, y0, _, _, x2, y2, _, _ = self.canvas.coords(self.vehicle)
        self.x, self.y = get_2center(x0, y0, x2, y2)
        self.update_display()

    # Update text
    def update_display(self):
        self.canvas.itemconfig(self.text_x_y, text="(x,y) = ({},{})".format(round(self.x,1),round(self.y,1)))
        self.canvas.itemconfig(self.text_vehicle_angle, text="vehicle_angle = {}".format(round(self.vehicle_angle,1)))
        self.canvas.itemconfig(self.text_motion, text="motion = {}".format(round(self.motion,1)))
        self.canvas.itemconfig(self.text_step, text="step = {}".format(self.step))

    def action_rng_motion(self):
        number = np.random.randint(3)
        if number==0:
            self.motion = MOTION[0]
        elif number==1:
            self.motion = MOTION[1]
        elif number==2:
            self.motion = MOTION[2]
        
    def action_rng_rotation(self):
        number = np.random.randint(3)
        if number==0:
            self.rotation = ROTATION[0]
        elif number==1:
            self.rotation = ROTATION[1]
        elif number==2:
            self.rotation = ROTATION[2]

    # Step
    def one_step(self):
        self.update_position()
        if self.random_motion:
            self.action_rng_motion()
        if self.random_rotation:
            self.action_rng_rotation()
        # Angle  reset
        self.vehicle_angle %= 360
        self.step += 1

    # Start episode
    def start_episode(self):
        t = time.time()
        tick, in_canvas = 0, True
        while in_canvas:
            # print(tick)

            self.one_step()

            # Display settings
            if self.slow:
                time.sleep(0.001)
            self.window.update()

            # Condition de fin
            if self.x > WIDTH or self.y > HEIGHT or self.x < 0 or self.y < 0:
                in_canvas = False

            tick += 1
        self.window.destroy()
        return round(time.time() - t,2) # le temps par épisode

    # Reset the vehicle
    def reset(self):
        self.x = WIDTH * 3 / 5
        self.y = HEIGHT - 50
        self.motion = MOTION[1]
        self.speed = 0
        self.rotation = ROTATION[1]
        self.vehicle_angle = 0
        self.canvas.delete(self.vehicle)
        self.vehicle = self.canvas.create_polygon(*get_4points(self.x, self.y, self.v_width, self.v_height), fill="green")
        self.update_display()
        self.start_episode()



def run_episode(nb):
    times = []
    for i in range(nb):
        sim = VehicleSimulator(shema_loic=True, shema_eliott=False)

        # constante pour parametrer l'execution
        sim.random_motion, sim.random_rotation = False, False
        sim.constant_speed = False # sinon accélération pour chaque tick
        sim.slow = True # time.sleep dans le main
        sim.shema_loic, sim.shema_eliott = True, False # differents modèle de shéma

        times.append(sim.start_episode())
        sim.window.mainloop()
    return times



if __name__ == "__main__":

    times = run_episode(2)
    print(times)