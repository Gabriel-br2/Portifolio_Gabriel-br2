# To do: 
# animação ->  start/ stop
# Ferramentas: Linha, quadrado, quadrado preenchido, circulo, circulo preenchido
# texts
# aplicar funcs
# export animação

import pygame
from color_select import *

pygame.init()

def genRectMatriz(dx,dy,tamX,tamY,t,e,data):
    rects_m = []
    x,y = dx,dy
    for colun in range(tamY):
        Line = []
        for line in range(tamX):
            if data: Line.append((0,0,0))
            else: Line.append(pygame.Rect(x,y,t,t))
            x += t+e
        rects_m.append(Line)
        y +=t+e
        x = dx
    return rects_m

def drawMatrizColor(tamX,tamY,color_mat,screen,Mat,limX,b):
    for colun in range(tamY):
        for line in range(limX-tamX,limX):
            if color_mat[colun][line] != (0,0,0) or b:
                pygame.draw.rect(screen, color_mat[colun][line], Mat[colun][line-(limX-tamX)])

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def concate_tu(t1,t2):
    t1 = list(t1)
    t1.append(t2)
    return tuple(t1)

def drawPrevMatrizColor(tamX,tamY,color_mat,screen,Mat):
    for colun in range(tamY):
        for line in range(tamX):
            if color_mat[colun][line] != (0,0,0):
                draw_rect_alpha(screen,concate_tu(color_mat[colun][line],75),Mat[colun][line])
            
def testMatrizClick(mat,tamX,tamY,m,et_mouse):
    for a in range(tamY):
        for b in range(tamX):
            if testButton(mat[a][b],m) and et_mouse: 
                return True,b,a
    return False,0,0
    
def doubleFrame(main_mat):
    Ret = []
    for a in range(len(main_mat)):
        ret_l = []
        for b in range (len(main_mat[a])):
            ret_l.append(main_mat[a][b])
        Ret.append(ret_l)
    return Ret

def dataSavedProcessing(dataReaded):
    dataReaded = dataReaded.split(',')
    dataReaded = dataReaded[0].split('(') + dataReaded[1:]
    dataReaded = dataReaded[1:len(dataReaded)-1] + dataReaded[len(dataReaded)-1].split(')')
    dataReaded = list(map(int,dataReaded[0:len(dataReaded)-1]))
    return dataReaded 

def readDataSaved(tamX, tamY):
    matriz,cont,arqName = [], 0, "color_saved.txt"
    file = open(arqName,'r')
    lines = file.readlines()
    for Y in range(tamY):
        colun = []
        for X in range(tamX):
            try: 
                dataReaded = lines[0]
                lines.pop(0)
            except: dataReaded = '(0,0,0)\n'
            dataReaded = dataSavedProcessing(dataReaded)
            colun.append((dataReaded[0],dataReaded[1],dataReaded[2]))
            cont += 1
        matriz.append(colun)

    while len(lines) > 0:
        for ncolor in range(tamY):
            try:
                dataReaded = lines[0]
                lines.pop(0)
            except: dataReaded = '(0,0,0)\n'
            dataReaded = dataSavedProcessing(dataReaded)
            matriz[ncolor].append((dataReaded[0],dataReaded[1],dataReaded[2]))
    return matriz

def main():
    running, main_matriz,indexC = True,[],3
    current_frame,tam = -1,-1
    tamX, tamY, tamXC, tamYC = 30, 12, 3, 6

    screen = pygame.display.set_mode((818,373))
    pygame.display.set_caption('Animation Generator')

    # createRect
    main_color = pygame.Rect(728, 31, 58, 58)
    main_colorborder = pygame.Rect(727, 30, 60, 60)
    button_colorselect = pygame.Rect(727, 105, 60, 60)
    button_new_frame = pygame.Rect(30, 313, 100, 30)
    but_duplicateframe = pygame.Rect(135,313,100,30)
    but_back = pygame.Rect(240,313,30,30)
    but_front = pygame.Rect(275,313,30,30)
    but_backC = pygame.Rect(727,313,28,30) 
    but_frontC = pygame.Rect(760,313,28,30)
    but_rmFrame = pygame.Rect(310,313,100,30)

    rects_m = genRectMatriz(30,30,tamX,tamY,20,3,False)
    rects_sc = genRectMatriz(728,178,tamXC,tamYC,17,4.5,False) 
        
    font = [25, 20, 15]
    font = fontVector(font)

    r,g,b = 0,0,0
    c = False

    while running:
        save_mat = readDataSaved(tamXC,tamYC)
        m = pygame.mouse.get_pos()

        for event in pygame.event.get():
            et_mouse = (event.type == pygame.MOUSEBUTTONDOWN)

            if (event.type == pygame.QUIT) or (c): 
                running = False

            if testButton(button_colorselect,m) and et_mouse:
                r1,g1,b1,s,c = selectColor(r,g,b,screen,font,388,105)
                if s: r,g,b = r1,g1,b1
                
            if (testButton(button_new_frame,m) and et_mouse) or tam == -1:
                main_matriz.insert(current_frame+1,genRectMatriz(0,0,tamX,tamY,0,0,True))
                current_frame += 1
                tam+=1

            if testButton(but_duplicateframe,m) and et_mouse:
                main_matriz.insert(current_frame+1,doubleFrame(main_matriz[current_frame]))
                current_frame += 1
                tam+=1

            if testButton(but_back,m) and et_mouse:
                if current_frame == 0: current_frame = tam
                else: current_frame -= 1

            if testButton(but_front,m) and et_mouse:
                if current_frame == tam: current_frame = 0
                else: current_frame += 1

            if testButton(but_rmFrame,m) and et_mouse:
                if len(main_matriz) > 1:
                    tam -=1
                    main_matriz.pop(current_frame)
                    if current_frame>tam: current_frame=0
                else:
                    main_matriz.pop(current_frame)
                    main_matriz.append(genRectMatriz(0,0,tamX,tamY,0,0,False))

            if testButton(but_frontC,m) and et_mouse and indexC < len(save_mat[0]):  indexC+=1
            if testButton(but_backC,m) and et_mouse and indexC > tamXC: indexC -= 1 

            test,changed_X,changed_Y = testMatrizClick(rects_m,tamX,tamY,m,et_mouse)
            if test: 
                if(event.button == 3): main_matriz[current_frame][changed_Y][changed_X] = (0, 0, 0)
                else: main_matriz[current_frame][changed_Y][changed_X] = (r, g, b)

            testC,changed_XC,changed_YC = testMatrizClick(rects_sc,tamXC,tamYC,m,et_mouse)
            if testC:
                color_to_change = save_mat[changed_YC] [changed_XC+(indexC-tamXC)]             
                r,g,b = color_to_change[0],color_to_change[1],color_to_change[2]

        if c: break
        screen.fill((50, 50, 50))

        # text
        str_to_txt = str(current_frame+1) + ' of ' + str(tam+1) 
        txt = font[1].render(str_to_txt,True,(255,255,255))
        screen.blit(txt, (30,7))
        
        drawMatrizColor(tamX,tamY,main_matriz[current_frame],screen,rects_m,30,True) 
        
        if len(main_matriz) > 1: 
            if (current_frame != 0):drawPrevMatrizColor(tamX,tamY,main_matriz[current_frame-1],screen,rects_m)
            else: drawPrevMatrizColor(tamX,tamY,main_matriz[-1],screen,rects_m)

        drawMatrizColor(tamX,tamY,main_matriz[current_frame],screen,rects_m,30,False)    
        drawMatrizColor(tamXC,tamYC,save_mat,screen,rects_sc,indexC,True)

        #drawRect
        pygame.draw.rect(screen, (0 , 0, 0), main_colorborder)
        pygame.draw.rect(screen, (r, g, b), main_color)
        pygame.draw.rect(screen, (70, 70, 70), button_colorselect)
        pygame.draw.rect(screen, (70, 70, 70), but_front)
        pygame.draw.rect(screen, (70, 70, 70), but_back)
        pygame.draw.rect(screen, (70, 70, 70), but_duplicateframe)
        pygame.draw.rect(screen, (70, 70, 70), button_new_frame)
        pygame.draw.rect(screen, (70, 70, 70), but_backC)
        pygame.draw.rect(screen, (70, 70, 70), but_frontC)
        pygame.draw.rect(screen, (70, 70, 70), but_rmFrame)
        
        pygame.display.update()

main()