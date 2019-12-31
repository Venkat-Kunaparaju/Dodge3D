from direct.showbase.ShowBase import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.actor.Actor import Actor
from core import CollisionPolygon, Vec3
from random import shuffle
from direct.gui.OnscreenText import OnscreenText
import math



ConfigVariableBool("show-frame-rate-meter").setValue(1)


class Player:
    def __init__(self):
        self.keys = {"w":False, "s":False, "a":False, "d":False}
        self.vel = .2
        self.wOn= self.aOn=self.sOn= self.dOn = True
        
        self.dum= self.render.attachNewNode("dum")
        self.player = Actor("Models/Character/Ralph.egg", {"walk":"Models/Character/Ralph-Run.egg", "idle":"Models/Character/Ralph-Idle.egg"})
        self.player.reparentTo(self.render)
        self.player.setScale(1.2)
        self.player.setPos(0,0, 0)
        self.walk = self.player.getAnimControl('walk')
        self.idle = self.player.getAnimControl('idle')
        self.temp = self.player.getMat().getRow3(1)
        self.Vecvel = Vec3(0,-self.vel,0)
        
        
        self.cnode = CollisionNode("player")
        self.cnode.addSolid(CollisionBox(Point3(0,0,0), .2, .2, 1))
        self.player_collision = self.player.attachNewNode(self.cnode)
        #self.player_collision.show()
        
        self.accept("w", self.setKeys, ["w", True])
        self.accept("w-up", self.setKeys, ["w", False])
        self.accept("s", self.setKeys, ["s", True])
        self.accept("s-up", self.setKeys, ["s", False])
        self.accept("a", self.setKeys, ["a", True])
        self.accept("a-up", self.setKeys, ["a", False])
        self.accept("d", self.setKeys, ["d", True])
        self.accept("d-up", self.setKeys, ["d", False])
        
    def setKeys(self, key, value):
        self.keys[key] = value
    def Move(self, task):

        if not(self.keys["w"] or self.keys["s"] or self.keys["a"] or self.keys["d"]) or (self.keys["w"] and self.keys["s"]) or (self.keys["a"] and self.keys["d"] and not(self.keys["w"] or self.keys["s"])):
            if not(self.idle.isPlaying()):
                self.idle.play()
                self.walk.stop()
        else:
            if not(self.walk.isPlaying()):
                self.walk.play()
                self.idle.stop()
        if (self.keys["w"] and not(self.keys["s"] or self.keys["d"] or self.keys["a"])) or (self.keys["w"] and self.keys["d"] and self.keys["a"]):
            self.player.setH(180)
            if self.wOn:
                self.player.setPos(self.player, self.Vecvel)
        if (self.keys["s"] and not(self.keys["w"] or self.keys["d"] or self.keys["a"])) or (self.keys["s"] and self.keys["d"] and self.keys["a"]):
            self.player.setH(0)
            if self.sOn:
                self.player.setPos(self.player, self.Vecvel)
        if self.keys["d"] and not(self.keys["s"] or self.keys["w"] or self.keys["a"]):
            self.player.setH(90)
            if self.dOn:
                self.player.setPos(self.player, self.Vecvel)
        if self.keys["a"]  and not(self.keys["s"] or self.keys["d"] or self.keys["w"]):
            self.player.setH(270)
            if self.aOn:
                self.player.setPos(self.player, self.Vecvel)
        if self.keys["w"] and self.keys["a"] and not(self.keys["d"]):
            self.player.setH(225)
            if self.wOn and self.aOn:
                self.player.setPos(self.player, self.Vecvel)
        if self.keys["w"] and self.keys["d"] and not(self.keys["a"]):
            self.player.setH(135)
            if self.wOn and self.dOn:
                self.player.setPos(self.player, self.Vecvel)
        if self.keys["s"] and self.keys["a"] and not(self.keys["d"]):
            self.player.setH(315)
            if self.sOn and self.aOn:
                self.player.setPos(self.player, self.Vecvel)
        if self.keys["s"] and self.keys["d"] and not(self.keys["a"]):
            self.player.setH(45)
            if self.sOn and self.dOn:
                self.player.setPos(self.player, self.Vecvel)

            
        return Task.cont
class Walls:
    def __init__(self):
        self.topD = 11
        self.leftD = -14
        self.rightD = 14
        self.botD = -7
        self.angle = 14
        

        
        self.wall_top = CollisionNode("Twall")
        self.wall_top.addSolid(CollisionPolygon(Point3(self.leftD,self.topD,0), Point3(self.leftD,self.topD,1), Point3(self.rightD,self.topD,1), Point3(self.rightD,self.topD,0)))
        self.Twall = self.render.attachNewNode(self.wall_top)
        #self.Twall.show()
        
        self.wall_right = CollisionNode("Rwall")
        self.wall_right.addSolid(CollisionPolygon(Point3(self.rightD,self.topD,0), Point3(self.rightD, self.topD, 1), Point3(self.angle, self.botD, 1), Point3(self.angle, self.botD, 0)))
        self.Rwall = self.render.attachNewNode(self.wall_right)
        #self.Rwall.show()
        
        self.wall_left = CollisionNode("Lwall")
        self.wall_left.addSolid(CollisionPolygon(Point3(self.leftD,self.topD,0), Point3(self.leftD,self.topD,1), Point3(-self.angle, self.botD, 1), Point3(-self.angle, self.botD, 0)))
        self.Lwall = self.render.attachNewNode(self.wall_left)
        #self.Lwall.show()
        
        self.wall_bot = CollisionNode("Bwall")
        self.wall_bot.addSolid(CollisionPolygon(Point3(self.leftD,self.botD,0), Point3(self.leftD,self.botD,1), Point3(self.rightD,self.botD,1), Point3(self.rightD,self.botD,0)))
        self.Bwall = self.render.attachNewNode(self.wall_bot)
        #self.Bwall.show()
        
        self.wallB = loader.loadModel("Models/Cube.egg")
        self.wallB.reparentTo(self.render)
        self.wallB.setY(self.botD)
        self.wallB.setScale(16, .1,.6)
        self.wallB.setColor(0,.2,.5,1)
        
        self.wallT = loader.loadModel("Models/Cube.egg")
        self.wallT.reparentTo(self.render)
        self.wallT.setY(self.topD)
        self.wallT.setScale(16, .1,.6)
        self.wallT.setColor(0,.2,.5,1)

class Road:
    def __init__(self):
        self.roads = []
        for i in range(0,9):
            self.roads.append(loader.loadModel("Models/Cube.egg"))
            self.roads[i].reparentTo(self.render)
            self.roads[i].setScale(16, .05, .55)
            self.roads[i].setPos(0,(i-3)*2,-.05)
            self.roads[i].setP(90)
            self.roads[i].setColor(.12,.12,.12,1)
        self.barriers = []
        for i in range(0,8):
            self.barriers.append(loader.loadModel("Models/Cube.egg"))
            self.barriers[i].reparentTo(self.render)
            self.barriers[i].setScale(16,.05,.06)
            self.barriers[i].setPos(0,(i-3)*2+1,-.05)
            self.barriers[i].setP(90)
            self.barriers[i].setColor(.5,.5,.5,1)
        
class Car:
    def __init__(self, speed, startX, startY, number):
        self.speed = speed
        self.startX = startX
        self.startY = startY
        self.startZ = .5
        self.car_num = number
        self.name = "car" + number
        
        self.x = startX
        
        self.car = loader.loadModel("Models/Car.egg")
        self.car.reparentTo(render)
        self.car.setPos(self.startX, self.startY, self.startZ)
        self.car.setScale(.2)
        
        self.carNode = CollisionNode(self.name)
        self.carNode.addSolid(CollisionBox(Point3(0,0,0), 4, 8, 2))
        self.carNode = self.car.attachNewNode(self.carNode)
        
        if self.startX > 0:
            self.car.setH(90)
            self.speed = -self.speed
        else: 
            self.car.setH(-90)
            self.speed = self.speed
        
        taskMgr.add(self.Move, "move_car" + self.car_num)
    def Move(self, task):
        self.car.setX(self.car.getX() + self.speed)
        self.x = self.car.getX()
        return Task.cont
        

class Game(ShowBase, Player, Walls):
    def __init__(self):
        ShowBase.__init__(self)
        Player.__init__(self)
        Walls.__init__(self)
        Road.__init__(self)
        
        self.all_car = []
        self.carN = 1
        self.car_y = [-6,-4,-2,0,2,4,6,8,10]
        self.car_x = [-25,25]
        self.speed = [.1,.2,.3,.4]
        self.score = 0
        self.highscore = 0 
        self.output = "Score: " + str(self.score)
        self.difficulty = .3
        self.font = loader.loadFont('Fonts/SigmarOne-Regular.ttf')
        self.collision = False
        
        self.env = loader.loadModel("Models/env.egg.pz")
        self.env.reparentTo(self.render)
        self.env.setScale(30)  
        
        self.traverser = CollisionTraverser('traverser')
        base.cTrav = self.traverser
        self.colEvent = CollisionHandlerEvent()
        self.traverser.addCollider(self.player_collision, self.colEvent)
        self.colEvent.addInPattern("into-%in")
        self.colEvent.addOutPattern("out-%in")
        
        for name in ["Twall","Bwall","Rwall","Lwall"]:
            self.accept(f"into-{name}", self.Check)
            self.accept(f"out-{name}", self.Out)
            
        base.setBackgroundColor(.1,.1,.1)
        base.disableMouse()
        camera.setPosHpr(0,-35,20,0,-30,0)
        
        taskMgr.add(self.Move, "move_player")
        taskMgr.add(self.car_check, "car_check")
        self.carSeq = Sequence(Func(self.MakeCar), Wait(self.difficulty))
        self.carSeq.loop()
        
        self.text = OnscreenText(text = self.output, pos = (1, .9), scale =.1, mayChange = 1, font = self.font, fg = (1,.5,0,1))
        self.idle.play()
        self.pause(False)
       
    def Check(self, coll):
        if coll.getIntoNodePath().getName() == "Twall":
            self.wOn = False
        if coll.getIntoNodePath().getName() == "Rwall":
            self.dOn = False
        if coll.getIntoNodePath().getName() == "Bwall":
            self.sOn = False
        if coll.getIntoNodePath().getName() == "Lwall":
            self.aOn = False
    def Out(self, coll):
        if coll.getIntoNodePath().getName() == "Twall":
            self.wOn = True
        if coll.getIntoNodePath().getName() == "Rwall":
            self.dOn = True
        if coll.getIntoNodePath().getName() == "Bwall":
            self.sOn = True
        if coll.getIntoNodePath().getName() == "Lwall":
            self.aOn = True
    def MakeCar(self):
        shuffle(self.car_y)
        shuffle(self.car_x)
        shuffle(self.speed)
        self.all_car.append(Car(self.speed[0], self.car_x[0], self.car_y[0], str(self.carN)))
        self.carN += 1
    def car_check(self, task):
        for car in self.all_car:
            if car.x < -25 or car.x > 25:
                self.all_car.remove(car)
                car.car.removeNode()
                taskMgr.remove('move_car' + car.car_num)
                self.score += 1
                self.output = "Score: " + str(self.score)
                self.text.setText(self.output)
            if not(self.collision):
                self.accept(f"into-{car.name}", self.collide_car)
        
        return Task.cont
    def collide_car(self, coll):
        for car in self.all_car:
            if car.carNode != coll.getIntoNodePath():
                car.car.removeNode()
            taskMgr.remove('move_car' + car.car_num)
        self.collision = True
        self.pause()
            
    def pause(self, coll=True):
        self.carSeq.pause()
        self.walk.stop()
        taskMgr.remove("move_player")
        if self.score > self.highscore:
            self.highscore = self.score
        self.text.setPos(10,10)
        if coll:
            self.dead_text = OnscreenText(text = f"You Have Been Hit \n Score: {self.score} \n Highscore:  {self.highscore} \n \n \n Press R to play again \n Press F to exit", pos = (0, .4), scale =.1, mayChange = 1, fg = (.1,.7,.1,1 ), 
            font = self.font)
        else:
            self.dead_text = OnscreenText(text = f"Dodge the Cars! \n \n Press R to start", pos = (0, .4), scale =.1, mayChange = 1, fg = (0,.6,1,1 ), font = self.font)
        self.accept("r", self.un_pause)
        self.accept("f", self.exit)
    def un_pause(self):
        for car in self.all_car:
            car.car.removeNode()
        for car in  self.all_car:
            self.all_car.remove(car)
            
        taskMgr.remove("pause")
        taskMgr.add(self.Move, "move_player")
        self.carSeq.resume()
        self.ignore("r")
        self.ignore("f")
        
        self.score = 0
        self.dead_text.remove_node()
        self.output = "Score: " + str(self.score)
        self.text.setText(self.output)
        self.text.setPos(1.1,.9)
        self.collision = False
        
    def exit(self):
        finalizeExit()
        
 
Game=Game()
Game.run()
