import pygame
import sys
import random

pygame.init()

display_width = 900
display_height = 900

gameDisplay = pygame.display.set_mode( ( display_width,display_height ) )
pygame.display.set_caption( 'Sudoku' )
clock = pygame.time.Clock()

hrubaSirka = 5
tenkaSirka = 2

thismodule = sys.modules[ __name__ ]
thismodule.tempR = 200
thismodule.tempG = 200
thismodule.tempB = 200

fontSize0 = display_width // 22
fontSize1 = display_width // 12
fontSize2 = display_width // 9
fontSize3 = display_width // 5

thismodule.pocetVolnychMiest = 35

word = []
thismodule.hlavnaPlocha = []
thismodule.plocha = []

lahka = 45
stredna = 40
tazka = 35

cierna = ( 0,0,0 )
cervena = ( 130,0,20 )
zelena = ( 50,150,60 )

thismodule.koniec2 = False #treba referencovat na zaciatku aby PollEvents nevyhadzoval chybu, ze koniec 2 nie je referencovany

def TextObjects( string,font,color ):
    textSurface = font.render( string,True,color )
    return textSurface,textSurface.get_rect()

def ZobrazText( string,fontSizeX,color,x,y ):
    text = pygame.font.SysFont( "timesnewroman",fontSizeX )
    TextSurf, TextRect = TextObjects( string,text,color )
    TextRect.center = ( x,y )
    gameDisplay.blit( TextSurf,TextRect )

def Normalizacia( x ):
    x.clear()
    for i in range( 81 ):
        x.append( 0 )

def Tlacidlo( borderXStart,borderYStart,width,height,borderWidth,borderColor,text,textSize,textColorDefault,textColorHover,actions ):
    def avg( a,b ):
        return ( a + b ) / 2

    pygame.draw.rect( gameDisplay,borderColor,( borderXStart,borderYStart,width,height ),borderWidth )
    mouse = pygame.mouse.get_pos()

    if borderXStart + width > mouse[ 0 ] > borderXStart:
        if borderYStart + height > mouse[ 1 ] > borderYStart:
            ZobrazText( text,textSize,textColorHover,avg( borderXStart,borderXStart + width ),borderYStart + height / 2 )
            if pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[ 0 ]:
                    if actions:
                        for i in actions:
                            i()
                    pygame.event.wait()
        else:
            ZobrazText( text,textSize,textColorDefault,avg( borderXStart,borderXStart + width ),borderYStart + height / 2 )
    else:
        ZobrazText( text,textSize,textColorDefault,avg( borderXStart,borderXStart + width ),borderYStart + height / 2 )

def ZakladnaObrazovka():
    thismodule.koniec1 = True
    while thismodule.koniec1:
        gameDisplay.fill( ( 255,255,255 ) )
        ZobrazText( "SUDOKU",fontSize3,cervena,display_width / 2,0.4 * ( display_height / 2 ) )
        ZobrazText( "Marek Borik",fontSize1,cierna,display_width / 2,0.7 * ( display_height / 2 ) )

        Tlacidlo( display_width * 0.1,display_height * 0.68,display_width * 0.8,display_height * 0.1,2,cierna,"ZAČNI HRU",fontSize1,cierna,zelena,[ HlavnaObrazovka ] )
        Tlacidlo( display_width * 0.1,display_height * 0.8,display_width * 0.8,display_height * 0.1,2,cierna,"NASTAVENIA",fontSize1,cierna,zelena,[ Nastavenia ] )

        PollEvents()
        pygame.display.update()
        clock.tick( 60 )

def HlavnaObrazovka():
    VygenerujPlochu()
    thismodule.koniec2 = True
    while thismodule.koniec2:
        gameDisplay.fill( ( 255,255,255 ) )

        if not Vyhral():
            MouseHoverOver()
            ZobrazCislaNaPloche()
            ZobrazGrid()
        else:
            ZobrazText( "VYHRAL SI",fontSize2,zelena,display_width / 2,display_height / 2 )

        PollEvents()

        pygame.display.update()
        clock.tick( 60 )

def Pauza():
    thismodule.koniec3 = True
    while thismodule.koniec3:
        gameDisplay.fill( ( 255,255,255 ) )

        ZobrazText( "Hra je pozastavená",fontSize2,zelena,display_width / 2,display_height / 2 )
        Tlacidlo( display_width * 0.15,display_height * 0.75,display_width * 0.7,display_height * 0.1,3,cierna,"Nová hra",fontSize1,cierna,cervena,[ VygenerujPlochu,HlavnaObrazovka ] )

        PollEvents()

        pygame.display.update()
        clock.tick( 60 )

def Nastavenia():
    thismodule.koniec4 = True

    def Negan():
        thismodule.koniec4 = False

    def NastavObtiaznostLahka():
        thismodule.pocetVolnychMiest = 81 - lahka #31
    def NastavObtiaznostStredna():
        thismodule.pocetVolnychMiest = 81 - stredna #36
    def NastavObtiaznostTazka():
        thismodule.pocetVolnychMiest = 81 - tazka #41

    NastavObtiaznostLahka()

    while thismodule.koniec4:
        gameDisplay.fill( ( 255,255,255 ) )

        ZobrazText( "NASTAVENIA",fontSize2,cierna,display_width / 2,display_height * 0.1 )
        ZobrazText( "OBTIAŽNOSŤ",fontSize1,cierna,display_width / 2,display_height * 0.5 )


        Tlacidlo( display_width * 0.15,display_height * 0.8,display_width * 0.7,display_height * 0.1,3,cierna,"HLAVNÉ MENU",fontSize1,cierna,zelena,[ Negan ] )

        if thismodule.pocetVolnychMiest is 81 - lahka:
            Tlacidlo( display_width / 21,display_height * 0.57,( display_width / 21 ) * 5,display_height * 0.1,3,cierna,"ĽAHKÁ",fontSize0,zelena,zelena,[ NastavObtiaznostLahka ] )
            Tlacidlo( ( display_width / 21 ) * 8,display_height * 0.57,( display_width / 21 ) * 5,display_height * 0.1,3,cierna,"STREDNÁ",fontSize0,cervena,cervena,[ NastavObtiaznostStredna ] )
            Tlacidlo( ( display_width / 21 ) * 15,display_height * 0.57,( display_width / 21 ) * 5,display_height * 0.1,3,cierna,"ŤAŽKÁ",fontSize0,cervena,cervena,[ NastavObtiaznostTazka ] )
        elif thismodule.pocetVolnychMiest is 81 - stredna:
            Tlacidlo( display_width / 21,display_height * 0.57,( display_width / 21 ) * 5,display_height * 0.1,3,cierna,"ĽAHKÁ",fontSize0,cervena,cervena,[ NastavObtiaznostLahka ] )
            Tlacidlo( ( display_width / 21 ) * 8,display_height * 0.57,( display_width / 21 ) * 5,display_height * 0.1,3,cierna,"STREDNÁ",fontSize0,zelena,zelena,[ NastavObtiaznostStredna ] )
            Tlacidlo( ( display_width / 21 ) * 15,display_height * 0.57,( display_width / 21 ) * 5,display_height * 0.1,3,cierna,"ŤAŽKÁ",fontSize0,cervena,cervena,[ NastavObtiaznostTazka ] )
        elif thismodule.pocetVolnychMiest is 81 - tazka:
            Tlacidlo( display_width / 21,display_height * 0.57,( display_width / 21 ) * 5,display_height * 0.1,3,cierna,"ĽAHKÁ",fontSize0,cervena,cervena,[ NastavObtiaznostLahka ] )
            Tlacidlo( ( display_width / 21 ) * 8,display_height * 0.57,( display_width / 21 ) * 5,display_height * 0.1,3,cierna,"STREDNÁ",fontSize0,cervena,cervena,[ NastavObtiaznostStredna ] )
            Tlacidlo( ( display_width / 21 ) * 15,display_height * 0.57,( display_width / 21 ) * 5,display_height * 0.1,3,cierna,"ŤAŽKÁ",fontSize0,zelena,zelena,[ NastavObtiaznostTazka ] )

        PollEvents()

        pygame.display.update()
        clock.tick( 60 )

    ZakladnaObrazovka()

def VygenerujPlochu(): #kod na generaciu vyriesenych sudoku z internetu

    Normalizacia( thismodule.plocha )
    Normalizacia( thismodule.hlavnaPlocha )

    maxAttempts = 1000
    count = 9999
    solCount = 0

    while count > maxAttempts:
        solCount += 1
        thismodule.puzzle = []
        for i in range( 9 ):
            row = []
            for j in range( 9 ):
                row.append( 0 )
            thismodule.puzzle.append( row )

        for row in range( 9 ):
            for col in range( 9 ):
                thisRow = thismodule.puzzle[ row ]
                thisCol = []
                for h in range( 9 ):
                    thisCol.append( thismodule.puzzle[ h ][ col ] )

                subCol = int( col / 3 )
                subRow = int( row / 3 )
                subMat = []
                for subR in range( 3 ):
                    for subC in range( 3 ):
                        subMat.append( thismodule.puzzle[ subRow * 3 + subR ][ subCol * 3 + subC ] )
                randVal = 0
                count = 0
                while randVal in thisRow or randVal in thisCol or randVal in subMat:
                    randVal = random.randint( 1,9 )
                    count += 1

                    if count > maxAttempts:
                        break
                thismodule.puzzle[ row ][ col ] = randVal

                if count > maxAttempts:
                    break
            if count > maxAttempts:
                break

    thismodule.hlavnaPlocha.clear()
    for i in thismodule.puzzle: #rozhranie
        for j in range( 9 ):
            thismodule.hlavnaPlocha.append( i[ j ] )

    matte = random.sample( range( 81 ),thismodule.pocetVolnychMiest ) #nahodne dane prec nejake cisla
    for i in range( thismodule.pocetVolnychMiest ):
        thismodule.hlavnaPlocha[ matte[ i ] ] = 0

    thismodule.plocha = list( thismodule.hlavnaPlocha )

def PridajDoPlochy( x,riadok,stlpec ):
    if thismodule.hlavnaPlocha[ riadok * 9 + stlpec ] is 0:
        thismodule.plocha[ riadok * 9 + stlpec ] = x

def ZobrazCislaNaPloche():
    for i in range( 9 ):
        for j in range( 9 ):
            if thismodule.plocha[ i * 9 + j ] is not 0:
                if thismodule.hlavnaPlocha[ i * 9 + j ] is not 0:
                    ZobrazText( str( thismodule.plocha[ i * 9 + j ] ),fontSize1,cervena,( 2 * ( j + 1 ) - 1  ) * display_width / 18,( 2 * ( i + 1 ) - 1  ) * display_height / 18 )
                else:
                    ZobrazText( str( thismodule.plocha[ i * 9 + j ] ),fontSize1,cierna,( 2 * ( j + 1 ) - 1  ) * display_width / 18,( 2 * ( i + 1 ) - 1  ) * display_height / 18 )

def ZobrazGrid():
    pygame.draw.line( gameDisplay,cierna,( display_width / 3,0 ),( display_width / 3,display_height ),hrubaSirka )
    pygame.draw.line( gameDisplay,cierna,( 2 * display_width / 3,0 ),( 2 * display_width / 3,display_height ),hrubaSirka )
    pygame.draw.line( gameDisplay,cierna,( 0,display_height / 3 ),( display_width,display_height / 3 ),hrubaSirka )
    pygame.draw.line( gameDisplay,cierna,( 0,2 * display_height / 3 ),( display_width,2 *display_height / 3 ),hrubaSirka )

    for i in range( 1,9 ):
        pygame.draw.line( gameDisplay,cierna,( i * display_width / 9,0 ),( i * display_width / 9,display_height ),tenkaSirka )

    for i in range( 1,9 ):
        pygame.draw.line( gameDisplay,cierna,( 0,i * display_height / 9 ),( display_width,i * display_height / 9 ),tenkaSirka )

def MouseHoverOver():
    mouse = pygame.mouse.get_pos()
    x1 = mouse[ 0 ] // ( display_width / 9 )
    y1 = mouse[ 1 ] // ( display_height / 9 )

    if pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[ 0 ]:
            thismodule.tempR = 90
            thismodule.tempG  = 250
            thismodule.tempB = 30

            pygame.draw.rect( gameDisplay,( thismodule.tempR,thismodule.tempG,thismodule.tempB ),( x1 * display_width / 9,y1 * display_height / 9,display_width / 9 + tenkaSirka,display_height / 9 + tenkaSirka ) )

            ZobrazGrid()
            ZobrazCislaNaPloche()
            pygame.display.update()

            word.clear()
            while not word:
                PollEvents()

            if word[ 0 ] == '[0]' or word[ 0 ] == '[1]' or word[ 0 ] == '[2]' or word[ 0 ] == '[3]' or word[ 0 ] == '[4]' or word[ 0 ] == '[5]' or word[ 0 ] == '[6]' or word[ 0 ] == '[7]' or word[ 0 ] == '[8]' or word[ 0 ] == '[9]':
                PridajDoPlochy( int( word[ 0 ][ 1 ] ),int( y1 ),int( x1 ) )

    thismodule.tempR = 200
    thismodule.tempG = 200
    thismodule.tempB = 200

    pygame.draw.rect( gameDisplay,( thismodule.tempR,thismodule.tempG,thismodule.tempB ),( x1 * display_width / 9,y1 * display_height / 9,display_width / 9 + tenkaSirka,display_height / 9 + tenkaSirka ) )

def Vyhral():
    vyhral1 = False
    vyhral2 = False

    for i in range( 9 ):
        listRiadok = [ 1,2,3,4,5,6,7,8,9 ]
        listStlpec = [ 1,2,3,4,5,6,7,8,9 ]
        for j in range( 9 ):
            for k in listRiadok: #pre kazde cislo v riadku loopujem listom cisel 1-9, ked najdem, tak ho vyhodim z listu, na konci riadka musi zostat prazdny list, ak je tam kazde cislo prave raz
                if k == thismodule.plocha[ i * 9 + j ]: #riadky
                    listRiadok.remove( k )
                    break
            for l in listStlpec:
                if l == thismodule.plocha[ j * 9 + i ]: #stlpce
                    listStlpec.remove( l )
                    break

        if not listRiadok: #je v kazdom riadku kazde cislo prave raz?
            vyhral1 = True
        else:
            vyhral1 = False #ak je aspon v jednom riadku nejaka duplicita, netreba ist dalej
            break

        if not listStlpec:
            vyhral2 = True
        else:
            vyhral2 = False
            break

    return vyhral1 and vyhral2

thismodule.counter = 0
def PollEvents():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name( event.key )
            word.append( key )
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and thismodule.counter % 2 is 0 and thismodule.koniec2:
                thismodule.counter += 1
                Pauza()
            if event.key == pygame.K_ESCAPE and thismodule.counter % 2 is 1 and thismodule.koniec3:
                thismodule.counter += 1
                HlavnaObrazovka()

Normalizacia( thismodule.plocha )
ZakladnaObrazovka()
