import microbit as mb
import music
import speech
import audio
from microbit import *


class Robot():

    def __init__(self):
        self.address_robot = 0x10
        self.dir_moteur_gauche = 0x0
        self.dir_moteur_droite = 0x02
        self.vit_moteur_gauche = 0x01
        self.vit_moteur_droite = 0x03
        # self.moteur_gauche = "0x0"
        # self.moteur_gauche = "0x0"
        # self.moteur_gauche = "0x0"
        # self.moteur_gauche = "0x0"
        # self.moteur_gauche = "0x0"
        # self.moteur_gauche = "0x0"

    def regler_vitesse(self, vit_roue_gauche, vit_roue_droite):
        
        i2c.write(self.address_robot, bytearray([self.vit_moteur_gauche,vit_roue_gauche]))
        i2c.write(self.address_robot, bytearray([self.vit_moteur_droite,vit_roue_droite]))

    def avancer(self,speed:int):
        i2c.write(self.address_robot, bytearray([self.dir_moteur_droite, 0x01]))
        i2c.write(self.address_robot, bytearray([self.dir_moteur_gauche, 0x01]))
        self.regler_vitesse(speed,speed)

    def stop(self):
        i2c.write(self.address_robot, bytearray([self.dir_moteur_droite, 0x00]))
        i2c.write(self.address_robot, bytearray([self.dir_moteur_gauche, 0x00]))
        self.regler_vitesse(0,0)

    def reculer(self,speed:int):
        i2c.write(self.address_robot, bytearray([self.dir_moteur_droite, 0x02]))
        i2c.write(self.address_robot, bytearray([self.dir_moteur_gauche, 0x02]))
        self.regler_vitesse(speed,speed)
    
    def tourner(self,speed:int):
        pass

        



while True:
    robot = Robot()
    display.show(Image.ANGRY)
    music.play(music.FUNERAL)
    robot.avancer(50)
    sleep(1000)
    robot.stop()
    sleep(100)
    robot.reculer(50)
    sleep(300)
    robot.stop()

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

    
