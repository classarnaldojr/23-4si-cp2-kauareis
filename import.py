import cv2
import matplotlib.pyplot as plt
import numpy as np

pontuacao_direita = 0
pontuacao_esquerda = 0
cont = 0


def gray_and_blur(img):
    # Blur na Imagem para facilitar a detecção pois vai ficar mais clara
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    k_size = (35, 35)
    filtro_blur = cv2.GaussianBlur(img_gray, k_size, 0)

    _, thresh = cv2.threshold(filtro_blur, 127, 255,
                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return thresh


def area(contours):
    max_area = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > max_area:
            aux = contours[i]
            max_area = area

    cnt = aux

    M = cv2.moments(cnt)

    if M["m00"] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    else:
        M["m00"] == 0.1
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

    return max_area


def contornos(thresh):
    contours, _ = cv2.findContours(thresh.copy(),
                                   cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours


def jogadas(area):
    if area > 14500 and area < 17000:
        jogada = "Papel"
        return jogada
    elif area > 11500 and area < 14000:
        jogada = "Pedra"
        return jogada
    elif area < 11500 and area > 6000:
        jogada = "Tesoura"
        return jogada

# Jogador 1 = esquerda
# Jogador 2 = direita


def vencedor(jogada_esquerda, jogada_direita):

    if jogada_esquerda == jogada_direita:
        resultado = "Empate!"
        return resultado

    elif (jogada_esquerda == "Tesoura" and jogada_direita == "Papel"):
        resultado = "Jogador 1 venceu!"
        return resultado
    elif (jogada_esquerda == "Papel" and jogada_direita == "Tesoura"):
        resultado = "Jogador 2 venceu!"
        return resultado
    elif (jogada_esquerda == "Pedra" and jogada_direita == "Tesoura"):
        resultado = "Jogador 1 venceu!"
        return resultado
    elif (jogada_esquerda == "Tesoura" and jogada_direita == "Pedra"):
        resultado = "Jogador 2 venceu!"
        return resultado
    elif (jogada_esquerda == "Papel" and jogada_direita == "Pedra"):
        resultado = "Jogador 1 venceu!"
        return resultado
    elif (jogada_esquerda == "Pedra" and jogada_direita == "Papel"):
        resultado = "Jogador 2 venceu!"
        return resultado


def placarEsquerda(vitorioso, pontuacao_mao_esquerda):
    if vitorioso == "Jogador 1 venceu!":
        pontuacao_mao_esquerda = pontuacao_mao_esquerda + 1
    return pontuacao_mao_esquerda


def placarDireita(vitorioso, pontuacao_mao_direita):
    if vitorioso == "Jogador 2 venceu!":
        pontuacao_mao_direita = pontuacao_mao_direita + 1
    return pontuacao_mao_direita


video = cv2.VideoCapture('pedra-papel-tesoura.mp4')  # Captura do Vídeo


while video.isOpened():

    ret, img = video.read()

    video_final = cv2.resize(img, (800, 600))

    crop_video_esquerda = video_final[100:600, 100:450]
    crop_video_direita = video_final[100:600, 350:800]

    imagem_gray1 = gray_and_blur(crop_video_esquerda)
    imagem_gray2 = gray_and_blur(crop_video_direita)

    contorno_mao_esquerda = contornos(imagem_gray1)
    contorno_mao_direita = contornos(imagem_gray2)

    # Cauculo da área das duas mãos
    area_mao_esquerda = area(contorno_mao_esquerda)
    area_mao_direita = area(contorno_mao_direita)

    # Define o que foi jogado por cada jogador (PEDRA, PAPEL e TESOURA)
    jogada_mao_esquerda = jogadas(area_mao_esquerda)
    jogada_mao_direita = jogadas(area_mao_direita)

    ganhador = vencedor(jogada_mao_esquerda, jogada_mao_direita)

    cont += 1
    if cont >= 90:
        cont = 0
        pontuacao_esquerda = placarEsquerda(ganhador, pontuacao_esquerda)
        pontuacao_direita = placarDireita(ganhador, pontuacao_direita)

    # Jogada da Mão Esquerda
    (cv2.putText(video_final,
                 ("Jogador 1: " + str(jogada_mao_esquerda)),
                 (30, 50),  # Jogada da Mão Esquerda
                 cv2.FONT_HERSHEY_SIMPLEX,
                 0.8, (0, 0, 0), 1, cv2.LINE_AA))
    # Jogada da Mão Direita
    (cv2.putText(video_final,
                 ("Jogador 2: " + str(jogada_mao_direita)),
                 (425, 50),
                 cv2.FONT_HERSHEY_SIMPLEX,  # Jogada da Mão Direita
                 0.8, (0, 0, 0), 1, cv2.LINE_AA))
    # Placar
    (cv2.putText(video_final,
                 "Jogador 1: " + str(pontuacao_esquerda),
                 (30, 500),
                 cv2.FONT_HERSHEY_SIMPLEX,  # Vencedor da Rodada
                 0.8,
                 (0, 0, 0), 1, cv2.LINE_AA))

    (cv2.putText(video_final,
                 "Jogador 2: " + str(pontuacao_direita),
                 (525, 500),
                 cv2.FONT_HERSHEY_SIMPLEX,  # Vencedor da Rodada
                 0.8,
                 (0, 0, 0), 1, cv2.LINE_AA))
    # Resultado da Jogada
    (cv2.putText(video_final,
                 str(ganhador),
                 (300, 560),
                 cv2.FONT_HERSHEY_SIMPLEX,  # Vencedor da Rodada
                 0.8,
                 (70, 168, 50), 1, cv2.LINE_AA))

    # Ajustando o tamanho do vídeo

    cv2.imshow("Video final", video_final)

    k = cv2.waitKey(10)
    if k == 27:
        break

video.release()

cv2.destroyAllWindows()
