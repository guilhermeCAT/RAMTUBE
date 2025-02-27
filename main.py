from pytubefix import YouTube, exceptions
from pytubefix.cli import on_progress
import json
import os
import time

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
JSON_FILE = os.path.join(BASE_DIR, "historico_baixados.json")


if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w") as file:
        json.dump([], file, indent=2)

p_videos = 'videos'
p_audios = 'audios'

class Download_De_Video:
    def __init__(self, link_do_download):
        try:
            self.yt = YouTube(link_do_download, on_progress_callback=on_progress)
            self.nome = self.yt.title
            self.baixando = False
        except exceptions.RegexMatchError:
            raise ValueError("URL inválida. Por favor, insira um link válido do YouTube.")
        except exceptions.VideoUnavailable:
            raise ValueError("O vídeo não está disponível.")
        except Exception as erros:
            raise ValueError(f"Erro inesperado: {erros}")

    def salvar_historico(self):
        historico = self.carregar_historico()
        if self.nome not in historico:
            historico.append(self.nome)
            with open(JSON_FILE, "w") as file:
                json.dump(historico, file, indent=2)

    def baixar(self, p_videos):
        if not self.baixando:
            self.baixando = True
            print(f'{self.nome} está baixando na melhor qualidade possível')
            ys = self.yt.streams.get_highest_resolution()
            ys.download(output_path=p_videos)
            self.salvar_historico()
        else:
            print(f'{self.nome} já está baixando')

    @staticmethod
    def carregar_historico():
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    @staticmethod
    def ver_historico():
        historico = Download_De_Video.carregar_historico()
        if historico:
            print("Histórico de vídeos baixados:")
            for i, video in enumerate(historico, 1):
                print(f"{i}. {video}")
        else:
            print("Nenhum vídeo baixado ainda.")

class Download_De_Audio(Download_De_Video):
    def __init__(self, link_do_download):
        super().__init__(link_do_download)
    
    def baixar(self, p_audios):
        print(f'{self.nome} está baixando o áudio...')
        self.yt.streams.filter(only_audio=True).first().download(output_path=p_audios)
        self.salvar_historico()

def menu():
    while True:
        try:
            print('===============================')
            print(10*' ',"RAMTUBE")
            print('===============================')
            print("0. Sair\n1. Baixar vídeo\n2. Baixar áudio\n3. Ver histórico")
            print('===============================')
            pergunta = int(input("ESCOLHA:  "))
            os.system('cls')
        except ValueError:
            print("Digite somente números!")
            time.sleep(3)
            os.system('cls')
            continue
        except Exception as e:
            print(f"Erro inesperado: {e}")
            time.sleep(3)
            os.system('cls')
            continue

        if pergunta == 1:
            try:
                link_do_download = input("Digite a URL do vídeo: ")
                dv = Download_De_Video(link_do_download)
                dv.baixar(p_videos)
                time.sleep(3)
                os.system('cls')
            except ValueError as erros:
                print(erros)
                time.sleep(3)
                os.system('cls')
        elif pergunta == 2:
            try:
                link_do_download = input("Digite a URL do áudio: ")
                da = Download_De_Audio(link_do_download)
                da.baixar(p_audios)
                time.sleep(3)
                os.system('cls')
            except ValueError as erros:
                print(erros)
                time.sleep(3)
                os.system('cls')
        elif pergunta == 3:
            Download_De_Video.ver_historico()
            print()
            time.sleep(6)
            os.system('cls')
        elif pergunta == 0:
            break
        else:
            print("Opção inválida, tente novamente.")
            time.sleep(3)
            os.system('cls')

menu()