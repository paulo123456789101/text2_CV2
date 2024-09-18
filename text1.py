# import cv2
# import pytesseract

# # Ler a imagem usando o OpenCV
# img = cv2.imread(r"C:\Users\paulo\Downloads\teste_text_python\text2_CV2\foto.png", cv2.IMREAD_COLOR)

# # Verificar se a leitura da imagem foi bem-sucedida
# if img is not None:
#     # Realizar a tradução da imagem em texto
#     text = pytesseract.image_to_string(img)

#     # Imprimir o texto extraído
#     print("Texto extraído da imagem:")
#     print("\n")
#     print(text)

# else:
#     print("Erro ao ler a imagem. Verifique o caminho do arquivo.")

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import cv2
import pytesseract
from pynput import keyboard

# Caminho para o executável do Tesseract (geralmente é detectado automaticamente)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

# Diretório a ser monitorado
diretorio_monitorado = r'C:\Users\paulo\Downloads\text2_CV2'   #C:\Users\paulo\Downloads\teste_text_python\text2_CV2

# Flag para indicar se deve parar a execução
should_stop = False

# Função chamada quando uma tecla é pressionada
def on_press(key):
    global should_stop
    if hasattr(key, 'char') and (key.char == 'q' or key.char == 'Q'):
        should_stop = True
    elif key == keyboard.Key.esc:
        should_stop = True

# Classe para manipular eventos do sistema de arquivos
class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if any(event.src_path.lower().endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            process_image(event.src_path)

# Função para processar uma imagem e extrair texto
def process_image(imagem_path):
    # Aguarde 1 segundo após a criação do arquivo
    time.sleep(1)

    # Usar OpenCV para ler a imagem
    img = cv2.imread(imagem_path, cv2.IMREAD_COLOR)
    
    if img is not None:
        texto_extraido = pytesseract.image_to_string(img)

        # Limpar o terminal
        if os.name == 'posix':
            os.system('clear')  # Para sistemas Unix-like (Linux ou macOS)
        else:
            os.system('cls')    # Para sistemas Windows

        print(f"Texto extraído da imagem '{imagem_path}':")
        print("\n")
        print(texto_extraido)
        print("\n")
    else:
        print(f"Erro ao ler a imagem '{imagem_path}'")

# Inicializar o observador e definir o manipulador de eventos
observer = Observer()
event_handler = ImageHandler()

# Adicionar o diretório monitorado para observação de eventos
observer.schedule(event_handler, path=diretorio_monitorado)

# Iniciar o observador
observer.start()

# Adicionar listener para pressionar teclas
with keyboard.Listener(on_press=on_press) as listener:
    try:
        while not should_stop:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

observer.stop()
observer.join()

