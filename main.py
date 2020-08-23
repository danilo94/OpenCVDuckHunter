# import win32gui
import webbrowser
import numpy as np
import cv2
import time
import pyautogui
#from PIL import ImageGrab
import pyscreenshot as ImageGrab

JogarJogo = True
VerMascaras = False
VerRetangulos = False
cor_pato_preto = np.array([0,0,0])
cor_minima_pato_vermelho = np.array([170,50,50]) # Range mínimo para a cor vermelha
cor_maxima_pato_vermelho = np.array([180,255,255]) # Range máximo para a cor vermelha

toplist, winlist = [], []

webbrowser.register('firefox',None,webbrowser.BackgroundBrowser("firefox"))
webbrowser.get('firefox').open('https://duckhuntjs.com/')

valores_desejados = [16,25,34,12,11,30]

bbox = (0,0,800,600)

while True:
    try:
        img = ImageGrab.grab(bbox)
        imgcv = np.array(img)
        imgcv = imgcv[:,:,::-1].copy()
        hsv = cv2.cvtColor(imgcv,cv2.COLOR_BGR2HSV)
        hsv = cv2.rectangle(hsv,(0,0),(800,250),(0,0,0),-1)
        hsv = cv2.rectangle(hsv,(0,550),(802,864),(0,0,0),-1)
        mascara_cor_preta = cv2.inRange(hsv, cor_pato_preto, cor_pato_preto)
        mascara_cor_vermelha = cv2.inRange(hsv,cor_minima_pato_vermelho,cor_maxima_pato_vermelho)

        mascaras_combinadas = cv2.bitwise_or(mascara_cor_vermelha,mascara_cor_preta)
        contornos, hierarquia = cv2.findContours(mascaras_combinadas,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contorno in contornos:
            x, y, w, h = cv2.boundingRect(contorno)
            if ( h  in valores_desejados):
                if (JogarJogo and not VerMascaras and not VerRetangulos):
                    middlex = int(x + w / 2)
                    middley = int(y + h / 2)
                    pyautogui.click(middlex, middley)
                    print ("Atirou na posição: (",middlex,middley,")")
                    time.sleep(1.3)
                    break
                if (VerRetangulos):
                    cv2.rectangle(imgcv, (x, y), (x + w, y + h), (0, 0, 255), 2)

            if (VerMascaras):
                cv2.imshow('Mascara Pato',mascaras_combinadas)

            elif(VerRetangulos):
                cv2.imshow('Retangulo Pato',imgcv)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(e)
        exit()


cv2.destroyAllWindows()
