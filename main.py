import music
import speech
import audio
import radio
import math
from machine import time_pulse_us
from time import sleep_us
from microbit import *

radio.off()
radio.config(channel=43)  # Adresse radio
radio.config(length=251)  # Longueur max du message
radio.on()


class Robot():

    def __init__(self):
        self.address_robot = 0x10
        self.dir_moteur_gauche = 0x0
        self.dir_moteur_droite = 0x02
        self.vit_moteur_gauche = 0x01
        self.vit_moteur_droite = 0x03
        self.R = 21
        self.L = 100
        self.angle = 0
        self.vitesse_lineaire = 0
        self.vitesse_angulaire = 0  
        self.trig = pin0
        self.echo = pin1
        self.P = 1
        self.I = 0
        self.D = 0
    
    def x(self, last_time, new_time):

        return self.vitesse_lineaire*math.cos(self.angle)*(new_time-last_time)
    
    def y(self, last_time, new_time):

        return self.vitesse_lineaire*math.sin(self.angle)*(new_time-last_time)
    
    def tour_roue_gauche(self):
        
        i2c.write(self.address_robot,bytearray([0x04]))
        return int.from_bytes(i2c.read(self.address_robot, 2),'big')/80

    def tour_roue_droite(self):

        i2c.write(self.address_robot,bytearray([0x06]))
        return int.from_bytes(i2c.read(self.address_robot, 2),'big')/80

    
    def get_vitesse_lineaire(self, last_time, new_time):

        phi_roue_gauche = self.compute_phi_roue(self.tour_roue_gauche(),last_time, new_time)
        phi_roue_droite =self.compute_phi_roue( self.tour_roue_droite(),last_time, new_time)

        self.vitesse_lineaire = self.R/2 *( phi_roue_gauche + phi_roue_droite)

    def compute_phi_roue(self, n_tours, last_time, new_time):

        return 2*n_tours*math.pi/(new_time - last_time)
    
        
    def get_vitesse_angulaire(self, last_time, new_time):

        phi_roue_gauche = self.compute_phi_roue(self.tour_roue_gauche(),last_time, new_time)
        phi_roue_droite =self. compute_phi_roue( self.tour_roue_droite(),last_time, new_time)

        self.vitesse_angulaire = self.R/self.L * ( phi_roue_gauche - phi_roue_droite)


    def regler_vitesse(self, vitesse_roue_gauche, vitesse_roue_droite):

        i2c.write(self.address_robot, bytearray([self.vit_moteur_gauche,vitesse_roue_gauche]))
        i2c.write(self.address_robot, bytearray([self.vit_moteur_droite,vitesse_roue_droite]))

    def avancer(self, initial_vit):

        i2c.write(self.address_robot, bytearray([self.dir_moteur_droite, 0x01]))
        i2c.write(self.address_robot, bytearray([self.dir_moteur_gauche, 0x01]))

        self.regler_vitesse(initial_vit, initial_vit)

    def stop(self):
        i2c.write(self.address_robot, bytearray([self.dir_moteur_droite, 0x00]))
        i2c.write(self.address_robot, bytearray([self.dir_moteur_gauche, 0x00]))
        self.regler_vitesse(0,0)

    def reculer(self,speed:int):
        i2c.write(self.address_robot, bytearray([self.dir_moteur_droite, 0x02]))
        i2c.write(self.address_robot, bytearray([self.dir_moteur_gauche, 0x02]))
        self.regler_vitesse(speed,speed)


    def convert_w_to_v(self, w):
        return int(self.R * w)
    
    def tourner(self,speed:int):
        pass
    
    def compute_distance(self, last_time, new_time):
        return round(self.vitesse_lineaire * (new_time - last_time),2)
        
    def distance_ultrason(self):

        self.trig.write_digital(0)
        sleep(2)
        self.trig.write_digital(1)
        sleep_us(30)
        self.trig.write_digital(0)

        self.echo.read_digital()
        micros = time_pulse_us(self.echo, 1)

        t_echo = micros / 1000000

        distance = (t_echo / 2)*34300

        return distance
    
    def phi_roue_gauche(self):
        return self.vitesse_lineaire/self.R - self.L * self.vitesse_angulaire/2
    
    def phi_roue_droite(self):
        return self.vitesse_lineaire/self.R + self.L * self.vitesse_angulaire/2
    
    def pdi(self, e_prev,last_time,new_time, integral, mesure, commande):
        
        # PID calculations
        e = commande - mesure
            
        P = self.P*e
        integral = integral + self.I*e*(new_time - last_time)
        D = self.D*(e - e_prev)/(new_time - last_time)

        # calculate manipulated variable - MV 
        MV = P + integral + D
        
        # update stored data for next iteration
        return e, MV
    
    def send_message(self,message):

        encoded_message = message.encode()  # Encodage du message en bytes
        radio.send_bytes(encoded_message)  # Envoi du message sous forme de bytes
        display.scroll("sent")
    
    def receive_message(self):
        message = radio.receive_bytes()  # Réception du message sous forme de bytes
        if message:
            # Décodage du message reçu
            try:
                decoded_message = message.decode()
                display.scroll(decoded_message)
            except UnicodeError:
                # En cas d'erreur de décodage
                display.show(Image.NO)
                sleep(1000)


robot = Robot()
first = True
v0 = 50



while True:
    new_time = running_time()

    # display.scroll(robot.distance_ultrason())

    robot.receive_message()

    if pin_logo.is_touched():
        message = "Are you okay baby girl?"
        robot.send_message(message)

    # robot.avancer(v0)

    # if not first:
    #     robot.get_vitesse_lineaire(last_time, new_time)
    #     display.scroll(str(robot.compute_distance(last_time, new_time)))
    

    # last_time = new_time
    # first = False

    sleep(100)

    # robot.stop()

    # sleep(1000)




    #robot.avancer(50)
    #sleep(1000)
    #robot.stop()
    #sleep(100)
    #robot.reculer(50)
    #sleep(300)
    #robot.stop()

    # if button_a.was_pressed():
    #     display.show(Image.HEART)
    #     set_volume(255)
    #     speech.say("Hello, sexy lady!")
    #     music.play(music.PYTHON)

    # elif button_b.was_pressed():
    #     display.show(Image.ANGRY)
    #     set_volume(255)
    #     speech.say("Hello, bad bitch!")
    #     music.play(music.FUNERAL)

    
