
from direct.interval.LerpInterval import LerpFunc
from direct.gui.OnscreenImage import OnscreenImage
from direct.particles.ParticleEffect import ParticleEffect
from Spacejamclasses import Missile
import re
from collideObjectBase import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionHandlerEvent
from direct.task import Task
from typing import Callable


class Player(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, task, render, accept: Callable[[str, Callable], None]):
        super(Player, self).__init__(loader, modelPath, parentNode, nodeName, 0, 2)
        self.taskManager = task
        self.render = render
        self.accept = accept
        self.loader = loader

        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.SetKeyBindings()

        self.reloadTime = .25
        self.missileDistance= 4000
        self.missileBay = 1

        self.cntExplode = 0
        self.explodeIntervals = {}

        self.traverser = CollisionTraverser()
        self.handler = CollisionHandlerEvent()

        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)

        self.taskManager.add(self.CheckIntervals, 'checkMissiles', 34)
        self.EnableHUD()

    def EnableHUD(self):
        self.hud = OnscreenImage(image = "./Assets/Hud/Reticle3b.png", pos = Vec3(0, 0, 0), scale = 0.1)
        self.hud.setTransparency(TransparencyAttrib.MAlpha)

    def CheckIntervals(self, task):
        for i in Missile.Intervals:
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print (i + ' has reached the end of its fire solution.')
                break
        return Task.cont




    def Thrust(self, Keydown):
        if Keydown:
            self.taskManager.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskManager.remove('forward-thrust')

    def ApplyThrust(self, task):
        rate = 5
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def SetKeyBindings(self):
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('a', self.LeftTurn, [1])
        self.accept('a-up', self.LeftTurn, [0])
        self.accept('d', self.RightTurn, [1])
        self.accept('d-up', self.RightTurn, [0])
        self.accept('w', self.LookUp, [1])
        self.accept('w-up', self.LookUp, [0])
        self.accept('s', self.LookDown, [1])
        self.accept('s-up', self.LookDown, [0])
        self.accept('q', self.RollLeft, [1])
        self.accept('q-up', self.RollLeft, [0])
        self.accept('e', self.RollRight, [1])
        self.accept('e-up', self.RollRight, [0])
        self.accept('f', self.Fire)
    
    def LeftTurn(self, KeyDown):
        if KeyDown:
            self.taskManager.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskManager.remove('left-turn')

    def ApplyLeftTurn(self, task):
        rate = .5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    
    def RightTurn(self, KeyDown):
        if KeyDown:
            self.taskManager.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskManager.remove('right-turn')

    def ApplyRightTurn(self, task):
        rate = .5
        self.modelNode.setH(self.modelNode.getH() - rate)
        return Task.cont
    
    def LookUp(self, KeyDown):
        if KeyDown:
            self.taskManager.add(self.ApplyLookUp, 'look-up')
        else:
            self.taskManager.remove('look-up')

    def ApplyLookUp(self, task):
        rate = .5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def LookDown(self, KeyDown):
        if KeyDown:
            self.taskManager.add(self.ApplyLookDown, 'look-down')
        else:
            self.taskManager.remove('look-down')

    def ApplyLookDown(self, task):
        rate = .5
        self.modelNode.setP(self.modelNode.getP() - rate)
        return Task.cont
    
    def RollLeft(self, KeyDown):
        if KeyDown:
            self.taskManager.add(self.ApplyRollLeft, 'roll-left')
        else:
            self.taskManager.remove('roll-left')

    def ApplyRollLeft(self, task):
        rate = .5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def RollRight(self, KeyDown):
        if KeyDown:
            self.taskManager.add(self.ApplyRollRight, 'roll-right')
        else:
            self.taskManager.remove('roll-right')

    def ApplyRollRight(self, task):
        rate = .5
        self.modelNode.setR(self.modelNode.getR() - rate)
        return Task.cont
    
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            if self.missileBay > 1:
                self.missileBay = 1
                print("Reload complete.")
                return Task.done
        elif task.time <= self.reloadTime:
            print("Reload proceeding...")
            return Task.cont
    def Fire(self):
        if self.missileBay:
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())

            aim.normalize()

            fireSolution = aim * travRate
            InFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag ='Missile' + str(Missile.missileCount)

            posVec = self.modelNode.getPos() + InFront 

            currentMissile = Missile(self.loader, './Assets/phaser/phaser.egg', self.render, tag, posVec, 4.0)

            self.traverser.addCollider(currentMissile.collisionNode, self.handler)

            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.Intervals[tag].start()
        else:
            if not self.taskManager.hasTaskNamed('reload'):
                print('initializing reload...')
                self.taskManager.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        print("fromNode: " + fromNode)
        intoNode = entry.getintoNodePath().getName()
        print("intoNode: " + intoNode)
        intoPosition = Vec3(entry.getSurfacePoint(self.render))
        tempVar = fromNode.split('_')
        shooter = tempVar[0]
        tempVar = intoNode.split('-')
        tempVar = intoNode.split('_')
        victim = tempVar[0]
        pattern = r'[0-9]'
        strippedString = re.sub(pattern, '', victim)
        if (strippedString == "Drone"):
            print(shooter + ' is DONE.')
            Missile.Intervals[shooter].finish()
            print(victim, ' hit at ', intoPosition)
            self.DroneDestroy(victim, intoPosition)

        else:
            Missile.Intervals[shooter].finish()
    
    def DroneDestroy(self, hitID, hitPosition):
        nodeID = self.render.find(hitID)
        nodeID.detachNode()

        self.explodeNode.setPos(hitPosition)
        self.Explode(hitPosition)
    
    def Explode(self, impactPoint):
        self.cntExplode += 1
        tag = 'particles-' + str(self.cntExplode)

        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, fromData = 0, toData = 0, duration = 4.0, extraArgs = [impactPoint])
        self.explodeIntervals[tag].start()

    def ExplodeLight(self, t, explosionPosition):
        if t == 1.0 and self.explodeEffect:
            self.explodeEffect.disable()

        elif t == 0:
            self.explodeEffect.start(self.explodeNode)

    def SetParticles(self):
        base.enableParticles()
        self.explodeEffect = ParticleEffect()
        self.explodeEffect.loadConfig("./Assets/Particles/explosion.ptf")
        self.explodeEffect.setScale(20)
        self.explodeNode = self.render.attachNewNode('ExplosionEffects')