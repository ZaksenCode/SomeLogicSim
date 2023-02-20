import pygame as pg

pg.font.init()
font = pg.font.Font(None, 15)


class SchemObject:
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.sizeX = 0
        self.sizeY = 0

    def draw(self, screen: pg.display):
        self.draw_no_cons(screen)
        self.draw_cons(screen)

    def draw_no_cons(self, screen: pg.display):
        pass

    def draw_cons(self, screen: pg.display):
        pass

    def remove_if_mouse(self, schem, pos):
        if self.check_if_mouse(pos):
            self.remove(schem)

    def remove(self, schem):
        schem.Schem_objects.pop(schem.Schem_objects.index(self))

    def check_if_mouse(self, pos: []):
        if self.posX - self.sizeX / 2 <= pos[0] <= self.posX + self.sizeX / 2 and \
                self.posY - self.sizeY / 2 <= pos[1] <= self.posY + self.sizeY / 2:
            return True
        return False


class Wire:
    def __init__(self):
        self.StartPoint = (0, 0)
        self.EndPoint = (0, 0)
        self.ShouldDrawing = True
        self.isActive = False
        self.color = (10, 10, 10)
        self.activeColor = (10, 200, 10)
        self.StrCon = Connector(False)
        # TODO change Start And End Point to Cons position
        # self.EndCon = Connector(False)

    def draw(self, screen: pg.display):
        if self.ShouldDrawing:
            if self.isActive:
                pg.draw.line(screen, self.activeColor, self.StartPoint, self.EndPoint)
            else:
                pg.draw.line(screen, self.color, self.StartPoint, self.EndPoint)
        else:
            self.StrCon.wires.remove(self)

    def draw_on_pos(self, screen: pg.display, pos: []):
        if self.ShouldDrawing:
            if self.isActive:
                pg.draw.line(screen, self.activeColor, self.StartPoint, pos)
            else:
                pg.draw.line(screen, self.color, self.StartPoint, pos)


class Connector(SchemObject):
    def __init__(self, isExit: bool):
        super().__init__()
        self.isActive = False
        self.isExit = isExit
        self.wires = []
        self.range = 5

    def logic(self):
        if self.isExit:
            for wire in self.wires:
                wire.isActive = self.isActive
        else:
            for wire in self.wires:
                if wire.isActive:
                    self.isActive = True
                    break
                else:
                    self.isActive = False

    def draw(self, screen: pg.display):
        if self.isActive:
            pg.draw.circle(screen, (30, 200, 30), [self.posX, self.posY], self.range, 0)
        else:
            pg.draw.circle(screen, (30, 30, 30), [self.posX, self.posY], self.range, 0)
        for wire in self.wires:
            wire.draw(screen)

    def check_if_mouse(self, pos: []):
        if self.posX - self.range <= pos[0] <= self.posX + self.range and \
                self.posY - self.range <= pos[1] <= self.posY + self.range:
            return True
        return False

    def remove(self, schem):
        for wire in self.wires:
            wire.ShouldDrawing = False

    def connect(self, pos: [], newWire):
        if self.check_if_mouse(pos):
            if isinstance(newWire, Wire):
                newWire.EndPoint = (self.posX, self.posY)
                self.wires.append(newWire)
                newWire.StrCon.wires.append(newWire)
                return None
            else:
                newWire = Wire()
                newWire.StartPoint = (self.posX, self.posY)
                newWire.StrCon = self
        return newWire


class LogicElement(SchemObject):
    def __init__(self):
        super().__init__()
        self.enterConnectors = [Connector(False)]
        self.exitConnectors = [Connector(True)]
        self.rect = pg.rect.Rect(50, 50, 15, 15)
        self.sizeX = 40
        self.sizeY = 20
        self.name = font.render("logic", True, (200, 200, 200))

    def logic(self):
        for connector in self.enterConnectors:
            connector.logic()
        for connector in self.exitConnectors:
            connector.logic()

    def draw_no_cons(self, screen: pg.display):
        pg.draw.rect(screen, (60, 60, 60), self.rect, 2, 0)
        screen.blit(self.name, (self.posX - self.sizeX / 4, self.posY - self.sizeY / 4))

    def draw_cons(self, screen: pg.display):
        for connector in self.enterConnectors:
            connector.draw(screen)
        for connector in self.exitConnectors:
            connector.draw(screen)

    def check_connectors(self, pos: [], wire):
        for connector in self.enterConnectors:
            wire = connector.connect(pos, wire)
        for connector in self.exitConnectors:
            wire = connector.connect(pos, wire)
        return wire

    def setup_draw(self):
        self.rect = pg.rect.Rect(self.posX - self.sizeX / 2, self.posY - self.sizeY / 2, self.sizeX, self.sizeY)
        for i in range(len(self.enterConnectors)):
            self.enterConnectors[i].posX = self.posX - self.sizeX / 2
            self.enterConnectors[i].posY = self.posY + i * 10
        for i in range(len(self.exitConnectors)):
            self.exitConnectors[i].posX = self.posX + self.sizeX / 2
            self.exitConnectors[i].posY = self.posY + i * 10


class Button(SchemObject):
    def __init__(self):
        super().__init__()
        self.sizeX = 36
        self.sizeY = 20
        self.isActive = False
        self.exitConnectors = [Connector(True)]
        self.rect = pg.rect.Rect(50, 50, 15, 15)
        self.name = font.render("Btn", True, (200, 200, 200))

    def check_if_click(self, pos: []):
        if super().check_if_mouse(pos):
            self.isActive = not self.isActive

    def logic(self):
        for connector in self.exitConnectors:
            connector.isActive = self.isActive
            connector.logic()

    def draw_no_cons(self, screen: pg.display):
        pg.draw.rect(screen, (60, 60, 60), self.rect, 2, 0)
        screen.blit(self.name, (self.posX - self.sizeX / 4, self.posY - self.sizeY / 4))

    def draw_cons(self, screen: pg.display):
        for connector in self.exitConnectors:
            connector.draw(screen)

    def setup_draw(self):
        self.rect = pg.rect.Rect(self.posX - self.sizeX / 2, self.posY - self.sizeY / 2, self.sizeX, self.sizeY)
        for i in range(len(self.exitConnectors)):
            self.exitConnectors[i].posX = self.posX + self.sizeX / 2
            self.exitConnectors[i].posY = self.posY + i * 10

    def check_connectors(self, pos: [], wire):
        for connector in self.exitConnectors:
            wire = connector.connect(pos, wire)
        return wire

    def remove(self, schem):
        schem.Schem_objects.pop(schem.Schem_objects.index(self))


class Lamp(LogicElement):
    def __init__(self):
        super().__init__()
        self.name = font.render("Not", True, (200, 200, 200))
        self.sizeX = 30
        self.sizeY = 30
        self.isActive = False
        self.color = (200, 20, 200)

    def logic(self):
        super().logic()
        self.exitConnectors[0].isActive = self.enterConnectors[0].isActive
        if self.enterConnectors[0].isActive:
            self.isActive = True
        else:
            self.isActive = False

    def draw_no_cons(self, screen: pg.display):
        pg.draw.rect(screen, (60, 60, 60), self.rect, 2, 0)
        if self.isActive:
            pg.draw.circle(screen, self.color, [self.posX, self.posY], 10, 0)
        else:
            pg.draw.circle(screen, (20, 20, 20), [self.posX, self.posY], 10, 2)
            pg.draw.circle(screen, (40, 40, 40), [self.posX, self.posY], 8, 0)

    def draw_cons(self, screen: pg.display):
        for connector in self.enterConnectors:
            connector.draw(screen)
        for connector in self.exitConnectors:
            connector.draw(screen)


class NotElement(LogicElement):
    def __init__(self):
        super().__init__()
        self.name = font.render("Not", True, (200, 200, 200))

    def logic(self):
        super().logic()
        self.exitConnectors[0].isActive = not self.enterConnectors[0].isActive


class AndElement(LogicElement):
    def __init__(self):
        super().__init__()
        self.enterConnectors = [Connector(False), Connector(False)]
        self.exitConnectors = [Connector(True)]
        self.name = font.render("&", True, (200, 200, 200))

    def logic(self):
        super().logic()
        activ_cons = []
        for connector in self.enterConnectors:
            if connector.isActive:
                activ_cons.append(connector)
            else:
                break
        if len(activ_cons) == len(self.enterConnectors):
            self.exitConnectors[0].isActive = True
        else:
            self.exitConnectors[0].isActive = False


class OrElement(LogicElement):
    def __init__(self):
        super().__init__()
        self.enterConnectors = [Connector(False), Connector(False)]
        self.exitConnectors = [Connector(True)]
        self.name = font.render("1", True, (200, 200, 200))

    def logic(self):
        super().logic()
        activ_cons = []
        for connector in self.enterConnectors:
            if connector.isActive:
                activ_cons.append(connector)
            pass
        if len(activ_cons) >= 1:
            self.exitConnectors[0].isActive = True
        else:
            self.exitConnectors[0].isActive = False


class XorElement(LogicElement):
    def __init__(self):
        super().__init__()
        self.enterConnectors = [Connector(False), Connector(False)]
        self.exitConnectors = [Connector(True)]
        self.name = font.render("Xor", True, (200, 200, 200))

    def logic(self):
        super().logic()
        activ_cons = []
        for connector in self.enterConnectors:
            if connector.isActive:
                activ_cons.append(connector)
            pass
        if len(activ_cons) >= 1 and len(activ_cons) != len(self.enterConnectors):
            self.exitConnectors[0].isActive = True
        else:
            self.exitConnectors[0].isActive = False


class Schem:
    def __init__(self):
        self.background = (50, 50, 50)
        self.Schem_objects = []
