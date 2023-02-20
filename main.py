from object import *

pg.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720

screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
icon = pg.image.load("sprites/icon.png")

pg.display.set_caption("Simulator :3")
pg.display.set_icon(icon)

cursor_color = (20, 20, 200)
rem_cursor_color = (200, 20, 20)
cursorShouldDraw = True
current_schem = Schem()
running = True
current_object = None
remove_mode = False
while running:
    screen.fill(current_schem.background)

    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if not remove_mode:
                if current_object is None or isinstance(current_object, Wire):
                    if len(current_schem.Schem_objects) >= 1:
                        for i in range(len(current_schem.Schem_objects)):
                            if isinstance(current_schem.Schem_objects[i], LogicElement):
                                current_object = current_schem.Schem_objects[i].check_connectors(pos, current_object)
                            if isinstance(current_schem.Schem_objects[i], Button):
                                current_schem.Schem_objects[i].check_if_click(pos)
                                current_object = current_schem.Schem_objects[i].check_connectors(pos, current_object)
            else:
                for i in range(len(current_schem.Schem_objects)):
                    current_schem.Schem_objects[i - 1].remove_if_mouse(current_schem, pos)

        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            if not remove_mode:
                if isinstance(current_object, LogicElement):
                    current_object.posX = pos[0]
                    current_object.posY = pos[1]
                    current_object.setup_draw()
                    current_schem.Schem_objects.append(current_object)
                if isinstance(current_object, Button):
                    current_object.posX = pos[0]
                    current_object.posY = pos[1]
                    current_object.setup_draw()
                    current_schem.Schem_objects.append(current_object)

            if not isinstance(current_object, Wire):
                current_object = None

        if event.type == pg.KEYDOWN:
            key = event.key
            if key == pg.K_0:
                current_object = None
            elif key == pg.K_1:
                current_object = NotElement()
            elif key == pg.K_2:
                current_object = AndElement()
            elif key == pg.K_3:
                current_object = OrElement()
            elif key == pg.K_4:
                current_object = XorElement()
            elif key == pg.K_5:
                current_object = Button()
            elif key == pg.K_6:
                current_object = Lamp()

            if key == pg.K_r:
                remove_mode = not remove_mode

        if event.type == pg.QUIT:
            running = False

    if len(current_schem.Schem_objects) >= 1:
        for i in range(len(current_schem.Schem_objects)):
            if isinstance(current_schem.Schem_objects[i], LogicElement):
                current_schem.Schem_objects[i].logic()
            if isinstance(current_schem.Schem_objects[i], Button):
                current_schem.Schem_objects[i].logic()

    if len(current_schem.Schem_objects) >= 1:
        for i in range(len(current_schem.Schem_objects)):
            current_schem.Schem_objects[i].draw(screen)

    if cursorShouldDraw:
        pos = pg.mouse.get_pos()
        if remove_mode:
            pg.draw.circle(screen, rem_cursor_color, pos, 8, 2)
        else:
            if current_object is not None:
                if isinstance(current_object, Wire):
                    current_object.draw_on_pos(screen, pos)
                elif isinstance(current_object, LogicElement):
                    current_object.posX = pos[0]
                    current_object.posY = pos[1]
                    current_object.setup_draw()
                    current_object.draw_no_cons(screen)
                elif isinstance(current_object, Button):
                    current_object.posX = pos[0]
                    current_object.posY = pos[1]
                    current_object.setup_draw()
                    current_object.draw_no_cons(screen)

    pg.display.update()

pg.quit()
