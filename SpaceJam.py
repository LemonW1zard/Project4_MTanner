from direct.showbase.ShowBase import ShowBase
import Spacejamclasses as Spacejamclasses
import DefensePaths as DefensePaths
from panda3d.core import *
from collideObjectBase import PlacedObject
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from direct.particles.ParticleEffect import ParticleEffect
from Player import myPlayer

# Space Jam.py
# Micah Tanner
# 02/11/2024
# Space Jam Game Primary Program

class myApp(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)
        self.traverser = CollisionTraverser()
        self.cTrav = self.traverser
        self.traverser.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.cTrav.showCollisions(self.render)
        self.Scene()
        self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
        self.traverser.addCollider(self.Player.collisionNode, self.pusher)
    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Player.modelNode)
        self.camera.setFluidPos(0, 1, 0)

    def DrawCloudDefense(self, centralObject, droneName): 
        unitVec = DefensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()  
        Spacejamclasses.Drone(self.loader, "./Assets/Drones/DroneDefender.x", self.render, droneName, "./Assets/Drones/Drones.jpg", position, 10)


    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1): 
        unitVec = DefensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 300 + centralObject.modelNode.getPos()  
        Spacejamclasses.Drone(self.loader, "./Assets/Drones/DroneDefender.x", self.render, droneName, "./Assets/Drones/Drones.jpg", position, 5)


    def DrawAxisDronesXY (self, centralObject, droneName):
        unitVec = DefensePaths.axisDronesXY ()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()  
        Spacejamclasses.Drone(self.loader, "./Assets/Drones/DroneDefender.x", self.render, droneName, "./Assets/Drones/Drones.jpg", position, 5)


    def DrawAxisDronesXZ (self, centralObject, droneName):
        unitVec = DefensePaths.axisDronesXZ ()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()  
        Spacejamclasses.Drone(self.loader, "./Assets/Drones/DroneDefender.x", self.render, droneName, "./Assets/Drones/Drones.jpg", position, 5)


    def DrawAxisDronesYZ (self, centralObject, droneName):
        unitVec = DefensePaths.axisDronesYZ ()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()  
        Spacejamclasses.Drone(self.loader, "./Assets/Drones/DroneDefender.x", self.render, droneName, "./Assets/Drones/Drones.jpg", position, 5)


    
    
    
    def Scene(self):
    
    

        #########################Universe Rendering################################################ 
        self.Universe = Spacejamclasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, 'Universe', "./Assets/Universe/Universe.jpg", (0, 0, 0), 10000)
        
        #########################Planet Rendering##################################################

        self.Planet1 = Spacejamclasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet1', "./Assets/Planets/starfield-in-blue.jpg", (1000, 5000, 67), 350)
        self.Planet2 = Spacejamclasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet2', "./Assets/Planets/moon-planet.jpg", (2000, 4000, 67), 350)
        self.Planet3 = Spacejamclasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet3', "./Assets/Planets/lava-planet.jpg", (3000, 3000, 67), 350)
        self.Planet4 = Spacejamclasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet4', "./Assets/Planets/consumed-planet.jpg", (4000, 2000, 67), 350)
        self.Planet5 = Spacejamclasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet5', "./Assets/Planets/frozen-planet.jpg", (5000, 1000, 67), 350)
        self.Planet6 = Spacejamclasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet6', "./Assets/Planets/neutron-star.jpg", (-5000, -1000, 67), 350)
        self.Player =  myPlayer(self.loader, "./Assets/Player/hornetMini.x", self.render, 'Player', "./Assets/Player/hornetMini.jpg", (0, 0, 0), 50, self.task_mgr, self.render, self.accept, self.traverser)
        self.Station = Spacejamclasses.Station(self.loader, "./Assets/Space-Station/spaceStation.x", self.render, 'Station', "./Assets/Space-Station/SpaceStation.png", (-3000, -3000, 67), 50)

        fullCycle = 60
        self.SetCamera()
        for j in range(fullCycle):
            Spacejamclasses.Drone.droneCount += 1
            nickName = "Drone" + str(Spacejamclasses.Drone.droneCount)
            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.Planet2, nickName, j, fullCycle, 2)
            self.DrawAxisDronesXY(self.Planet3, nickName)
            self.DrawAxisDronesXZ(self.Planet3, nickName)
            self.DrawAxisDronesYZ(self.Planet3, nickName)




app = myApp()
app.Player.SetKeyBindings()
app.run()