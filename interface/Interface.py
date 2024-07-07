import tkinter as tk
from tkinter import filedialog

import requests
from PIL import Image, ImageTk
import tkintermapview as tkmv
from utils import *


class Interface:

    def __init__(self):
        self.LAT = -29.7131
        self.LONG = -52.4316
        self.URL = "http://127.0.0.1:8000/posts"
        self.root = tk.Tk()
        self.rua = tk.StringVar()
        self.numero = tk.StringVar()
        self.bairro = tk.StringVar()
        self.gravidade = tk.StringVar()
        self.description = tk.StringVar()
        self.evidencia = tk.StringVar()
        self.problema = tk.StringVar()
        self.map_widget = None
        self.widgets = []
        self.problemas = []

    def fechar_widgets(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []

    def abrir_mapa(self):
        self.fechar_widgets()  # Fechar todos os widgets antes de executar a função
        if self.map_widget is not None:
            self.map_widget.destroy()  # Destroy the existing map widget
        self.map_widget = tkmv.TkinterMapView(self.root, width=450, height=650)
        self.map_widget.set_position(self.LAT, self.LONG)
        self.map_widget.set_zoom(14)
        self.map_widget.pack()
        self.widgets.append(self.map_widget)
        self.carregar_problemas()

        for problema in self.problemas:
            lat = problema["latitude"]
            lon = problema["longitude"]
            titulo = problema["title"]
            gravidade = problema["level"]
            imagem_caminho = "../" + problema["images_url"][0]
            likeNumero = 0

            if lat and lon:
                # Calcular tamanho do ícone com base nos likes
                tamanho_icone = 25 + (likeNumero // 5) * 5
                marker_icon = None
                if gravidade == "Baixo":
                    marker_icon = carregar_icone("source/marker_green.png", tamanho_icone)
                elif gravidade == "Médio":
                    marker_icon = carregar_icone("source/marker_yellow.png", tamanho_icone)
                elif gravidade == "Alto":
                    marker_icon = carregar_icone("source/marker_red.png", tamanho_icone)

                marker = self.map_widget.set_marker(lat, lon, text=titulo, icon=marker_icon)

                if imagem_caminho:
                    try:
                        imagem = Image.open(imagem_caminho)
                        imagem.thumbnail((50, 50))  # Ajustar o tamanho da imagem
                        imagem_tk = ImageTk.PhotoImage(imagem)
                        marker.image = imagem_tk  # Adicionar a imagem ao marcador
                    except Exception as e:
                        print(f"Erro ao carregar imagem: {e}")

    def carregar_problemas(self):
        self.problemas = requests.get(self.URL).json()

    def mostrar_problemas(self):
        self.fechar_widgets()  # Fechar todos os widgets antes de executar a função
        self.carregar_problemas()
        if not self.problemas:
            texto_sem_problemas = tk.Label(self.root, text="Nenhum problema foi adicionado.", bg='black', fg='white')
            texto_sem_problemas.pack(side="top", padx=5, pady=5)
            self.widgets.append(texto_sem_problemas)  # Adicionar o widget à lista
        else:
            problemas_ordenados = sorted(self.problemas, key=lambda x: x["likes"], reverse=True)

            canvas = tk.Canvas(self.root, bg='black')
            scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='black')

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            self.widgets.append(canvas)
            self.widgets.append(scrollbar)
            self.widgets.append(scrollable_frame)

            for index, problema in enumerate(problemas_ordenados, start=1):
                problema_id = problema["id"]
                latitude = problema["latitude"]
                titulo = problema["title"]
                longitude = problema["longitude"]
                description = problema["description"]
                gravidade = problema["level"]
                likes = problema["likes"]
                imagem_caminho = "../" + problema["images_url"][0]

                frame_problema = tk.Frame(scrollable_frame, bg='purple', padx=10, pady=10)
                frame_problema.pack(pady=5, anchor="center", fill=tk.X)
                self.widgets.append(frame_problema)  # Adicionar o widget à lista

                frame_problema.columnconfigure(0, weight=1)  # Permitir que a coluna 0 expanda

                # Botão de Like
                botao_like = tk.Button(frame_problema, text="Like", bg='purple', fg='white',
                                       command=lambda p_id=problema_id: self.incrementar_likes(p_id))
                botao_like.grid(row=5, column=0, padx=85, pady=5, sticky='w')
                self.widgets.append(botao_like)  # Adicionar o widget ao botão de like à lista

                # Texto de Likes
                texto_likes = tk.Label(frame_problema, text=f"Likes: {likes}", bg='purple', fg='white')
                texto_likes.grid(row=4, column=0, padx=78, pady=1, sticky='w')
                self.widgets.append(texto_likes)  # Adicionar o widget à lista

                # Textos de Problema, Descrição e Gravidade
                texto_problema = tk.Label(frame_problema, text=f"Problema: {titulo}", bg='purple',
                                          fg='white')
                texto_problema.grid(row=0, column=0, columnspan=4, padx=5, pady=2)
                self.widgets.append(texto_problema)  # Adicionar o widget à lista

                texto_description = tk.Label(frame_problema, text=f"Comentários: {description}", bg='purple', fg='white')
                texto_description.grid(row=1, column=0, columnspan=4, padx=5, pady=2)
                self.widgets.append(texto_description)  # Adicionar o widget à lista

                texto_gravidade = tk.Label(frame_problema, text=f"Gravidade: {gravidade}", bg='purple', fg='white')
                texto_gravidade.grid(row=2, column=0, columnspan=4, padx=5, pady=2)
                self.widgets.append(texto_gravidade)  # Adicionar o widget à lista

                texto_abrir_mapa = tk.Label(frame_problema, text="Clique na seta para ir ao \n local do problema",
                                            bg='purple', fg='white')
                texto_abrir_mapa.grid(row=4, column=2, padx=40, pady=5, sticky='e')
                self.widgets.append(texto_abrir_mapa)  # Adicionar o widget ao botão de abrir o mapa à lista

                # Botão de abrir mapa
                botao_abrir_mapa = tk.Button(frame_problema, text="➡️", bg='purple', fg='white',
                                             command=lambda lat=latitude, lon=longitude: self.centrar_mapa_no_marcador(lat,
                                                                                                                  lon))
                botao_abrir_mapa.grid(row=5, column=2, padx=85, pady=5, sticky='e')
                self.widgets.append(botao_abrir_mapa)  # Adicionar o widget ao botão de abrir o mapa à lista

                if imagem_caminho:
                    try:
                        imagem = Image.open(imagem_caminho)
                        imagem.thumbnail((200, 200))  # Ajustar o tamanho da imagem
                        imagem_tk = ImageTk.PhotoImage(imagem)
                        imagem_label = tk.Label(frame_problema, image=imagem_tk, bg='purple')
                        imagem_label.image = imagem_tk  # Manter referência da imagem
                        imagem_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
                        self.widgets.append(imagem_label)  # Adicionar o widget de imagem à lista
                    except Exception as e:
                        print(f"Erro ao carregar imagem: {e}")

    def entrada_dados(self):
        self.fechar_widgets()  # Fechar todos os widgets antes de executar a função

        # Reset input fields
        self.rua.set("")
        self.numero.set("")
        self.bairro.set("")
        self.gravidade.set("Baixa")  # Reset to default value
        self.description.set("")
        self.evidencia.set("")
        self.problema.set("")

        frame_form = tk.Frame(self.root, bg='black')
        frame_form.pack(padx=10, pady=10)

        self.widgets.append(frame_form)

        # Criado para criar uma validação de 40 caracteres no máximo
        vcmd = (self.root.register(limitar_caracteres), '%P')

        # Rua
        texto_rua = tk.Label(frame_form, text="Rua", bg='black', fg='white')
        texto_rua.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.widgets.append(texto_rua)  # Adicionar o widget à lista
        caixa_texto_rua = tk.Entry(frame_form, width=50, textvariable=self.rua)
        caixa_texto_rua.grid(row=0, column=1, padx=5, pady=5)
        self.widgets.append(caixa_texto_rua)  # Adicionar o widget à lista
        caixa_texto_rua.focus()

        # Número
        texto_numero = tk.Label(frame_form, text="Número", bg='black', fg='white')
        texto_numero.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.widgets.append(texto_numero)  # Adicionar o widget à lista
        caixa_texto_numero = tk.Entry(frame_form, width=50, textvariable=self.numero)
        caixa_texto_numero.grid(row=1, column=1, padx=5, pady=5)
        self.widgets.append(caixa_texto_numero)  # Adicionar o widget à lista

        # Bairro
        texto_bairro = tk.Label(frame_form, text="Bairro", bg='black', fg='white')
        texto_bairro.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.widgets.append(texto_bairro)  # Adicionar o widget à lista
        caixa_texto_bairro = tk.Entry(frame_form, width=50, textvariable=self.bairro)
        caixa_texto_bairro.grid(row=2, column=1, padx=5, pady=5)
        self.widgets.append(caixa_texto_bairro)  # Adicionar o widget à lista

        # Problema
        texto_problema = tk.Label(frame_form, text="Problema", bg='black', fg='white')
        texto_problema.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.widgets.append(texto_problema)  # Adicionar o widget à lista
        caixa_texto_problema = tk.Entry(frame_form, width=50, textvariable=self.problema)
        caixa_texto_problema.grid(row=3, column=1, padx=5, pady=5)
        self.widgets.append(caixa_texto_problema)  # Adicionar o widget à lista
        caixa_texto_problema.config(validate='key', validatecommand=vcmd)  # Seta a regra de limitar caracteres

        # Descrição
        texto_descricao = tk.Label(frame_form, text="Descrição do problema", bg='black', fg='white')
        texto_descricao.grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.widgets.append(texto_descricao)  # Adicionar o widget à lista
        caixa_texto_descricao = tk.Entry(frame_form, width=50, textvariable=self.description)
        caixa_texto_descricao.grid(row=4, column=1, padx=5, pady=5)
        self.widgets.append(caixa_texto_descricao)  # Adicionar o widget à lista
        caixa_texto_descricao.config(validate='key', validatecommand=vcmd)  # Seta a regra de limitar caracteres

        # Gravidade
        texto_gravidade = tk.Label(frame_form, text="Selecione a gravidade do problema", bg='black', fg='white')
        texto_gravidade.grid(row=5, column=0, sticky='w', padx=5, pady=5)
        self.widgets.append(texto_gravidade)  # Adicionar o widget à lista
        self.gravidade.set("Baixa")  # Set default value
        menu_gravidade = tk.OptionMenu(frame_form, self.gravidade, "Baixo", "Médio", "Alto")
        menu_gravidade.grid(row=5, column=1, padx=5, pady=5)
        self.widgets.append(menu_gravidade)  # Adicionar o widget à lista

        # Evidência
        texto_evidencia = tk.Label(frame_form, text="Insira evidências (arquivos)", bg='black', fg='white')
        texto_evidencia.grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.widgets.append(texto_evidencia)  # Adicionar o widget à lista
        botao_evidencia = tk.Button(frame_form, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        botao_evidencia.grid(row=6, column=1, padx=5, pady=5)
        self.widgets.append(botao_evidencia)  # Adicionar o widget à lista

        # Botões de confirmação e não confirmação
        botao_confirmar = tk.Button(frame_form, text="Confirmar", bg='green', fg='white', command=self.confirmar)
        botao_confirmar.grid(row=7, column=0, padx=5, pady=5, sticky='e')
        self.widgets.append(botao_confirmar)  # Adicionar o widget à lista

        botao_nao_confirmar = tk.Button(frame_form, text="Não Confirmar", bg='red', fg='white',
                                        command=self.nao_confirmar)
        botao_nao_confirmar.grid(row=7, column=1, padx=5, pady=5, sticky='w')
        self.widgets.append(botao_nao_confirmar)  # Adicionar o widget à lista

    def confirmar(self):

        lat = None
        long = None

        lat, long = geocode_address(self.rua.get(), self.numero.get(), self.bairro.get(), 'RS', 'Santa Cruz do Sul')

        if lat == self.LAT and long == self.LONG:
            self.nao_encontrado()
        else:
            data = {
                "title": self.problema.get(),
                "description": self.description.get(),
                "latitude": lat,
                "longitude": long,
                "category_name": "undefined",
                "post_level": self.gravidade.get(),
            }
            files = [
                ('files', open(self.evidencia.get(), 'rb')),
            ]

            response = requests.post(self.URL, data=data, files=files)
            if response.status_code != 200:
                print(f"Erro: {response.status_code}, {response.text}")
                return

            self.fechar_widgets()  # Fechar todos os widgets anteriores

            frame_confirmacao = tk.Frame(self.root, bg='black')
            frame_confirmacao.pack(padx=10, pady=10)
            self.widgets.append(frame_confirmacao)

            texto_confirmacao = tk.Label(frame_confirmacao,
                                         text=f"Informações armazenadas:\nProblema: {self.problema.get()}\nRua: {self.rua.get()}"
                                              f"\nNúmero: {self.numero.get()}\nBairro: {self.bairro.get()}"
                                              f"\nGravidade: {self.gravidade.get()}\nDescrição: {self.description.get()}"
                                              f"\nEvidência:",
                                         bg='black', fg='white')
            texto_confirmacao.pack(side="top", padx=5, pady=5)
            self.widgets.append(texto_confirmacao)  # Adicionar o widget de confirmação à lista

            if self.evidencia.get():
                try:
                    imagem = Image.open(self.evidencia.get())
                    imagem.thumbnail((400, 400))  # Ajustar o tamanho da imagem
                    imagem_tk = ImageTk.PhotoImage(imagem)
                    imagem_label = tk.Label(frame_confirmacao, image=imagem_tk, bg='black')
                    imagem_label.image = imagem_tk  # Manter referência da imagem
                    imagem_label.pack(side="top", padx=5, pady=5)
                    self.widgets.append(imagem_label)  # Adicionar o widget de imagem à lista
                except Exception as e:
                    print(f"Erro ao carregar imagem: {e}")

    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename()
        if arquivo:
            self.evidencia.set(arquivo)
            # tem q ver

    def configurar(self):
        self.root.title("CleanApp")
        self.root.geometry("450x650")  # Set the size of the window
        self.root.configure(background="black")
        self.root.resizable(width=False, height=False)

    def execute(self):
        self.configurar()
        bottom_bar = tk.Frame(self.root, bg='purple')
        bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Load and resize the images
        try:
            home_image = Image.open("source/home_icon.png").resize((35, 35))
            add_image = Image.open("source/add_icon.png").resize((35, 35))
            map_image = Image.open("source/map_icon.png").resize((35, 35))
        except Exception as e:
            print(f"Error loading images: {e}")
            home_image = add_image = map_image = Image.new('RGB', (35, 35), color='purple')  # Placeholder

        home_photo = ImageTk.PhotoImage(home_image)
        add_photo = ImageTk.PhotoImage(add_image)
        map_photo = ImageTk.PhotoImage(map_image)

        # Create buttons with images
        home_button = tk.Button(bottom_bar, image=home_photo, bg='purple', borderwidth=0,
                                command=self.mostrar_problemas)
        add_button = tk.Button(bottom_bar, image=add_photo, bg='purple', borderwidth=0, command=self.entrada_dados)
        map_button = tk.Button(bottom_bar, image=map_photo, bg='purple', borderwidth=0, command=self.abrir_mapa)

        # Arrange buttons in the bottom bar
        home_button.pack(side=tk.LEFT, padx=56)
        add_button.pack(side=tk.LEFT, padx=56)
        map_button.pack(side=tk.LEFT, padx=56)
        self.root.mainloop()

    def nao_encontrado(self):
        self.fechar_widgets()  # Fechar todos os widgets anteriores
        frame_nao_encontrado = tk.Frame(self.root, bg='black')
        frame_nao_encontrado.pack(anchor='center', padx=10, pady=10)
        self.widgets.append(frame_nao_encontrado)

        texto_nao_confirmacao = tk.Label(frame_nao_encontrado,
                                         text="As informações não foram Validadas \n Não encontramos o endereço digitado, tente novamente.",
                                         bg='black', fg='white')
        texto_nao_confirmacao.pack(anchor='center', padx=5, pady=5)
        self.widgets.append(texto_nao_confirmacao)  # Adicionar o widget de não confirmação à lista

    def nao_confirmar(self):
        self.fechar_widgets()  # Fechar todos os widgets anteriores
        frame_nao_confirmacao = tk.Frame(self.root, bg='black')
        frame_nao_confirmacao.pack(padx=10, pady=10)
        self.widgets.append(frame_nao_confirmacao)

        texto_nao_confirmacao = tk.Label(frame_nao_confirmacao, text="As informações não foram confirmadas.",
                                         bg='black', fg='white')
        texto_nao_confirmacao.pack(side="top", padx=5, pady=5)
        self.widgets.append(texto_nao_confirmacao)  # Adicionar o widget de não confirmação à lista

    def centrar_mapa_no_marcador(self, latitude, longitude):
        """Centraliza o mapa no marcador com base na latitude e longitude fornecidas."""
        self.fechar_widgets()  # Fechar todos os widgets antes de executar a função
        if self.map_widget is not None:
            self.map_widget.destroy()  # Destroy the existing map widget
        self.map_widget = tkmv.TkinterMapView(self.root, width=450, height=650)
        self.map_widget.set_position(latitude, longitude)
        self.map_widget.set_zoom(14)
        self.map_widget.pack()
        self.widgets.append(self.map_widget)

        for problema in self.problemas:
            lat = problema["latitude"]
            lon = problema["longitude"]
            titulo = problema["title"]
            gravidade = problema["level"]
            imagem_caminho = "../" + problema["images_url"][0]
            likes = problema["likes"]

            if lat and lon:
                # Calcular tamanho do ícone com base nos likes
                tamanho_icone = 25 + (likes // 5) * 5
                marker_icon = None
                if gravidade == "Baixo":
                    marker_icon = carregar_icone("source/marker_green.png", tamanho_icone)
                elif gravidade == "Médio":
                    marker_icon = carregar_icone("source/marker_yellow.png", tamanho_icone)
                elif gravidade == "Alto":
                    marker_icon = carregar_icone("source/marker_red.png", tamanho_icone)

                marker = self.map_widget.set_marker(lat, lon, text=titulo, icon=marker_icon)

                if imagem_caminho:
                    try:
                        imagem = Image.open(imagem_caminho)
                        imagem.thumbnail((50, 50))  # Ajustar o tamanho da imagem
                        imagem_tk = ImageTk.PhotoImage(imagem)
                        marker.image = imagem_tk  # Adicionar a imagem ao marcador
                    except Exception as e:
                        print(f"Erro ao carregar imagem: {e}")

    def incrementar_likes(self, id):
        requests.post(self.URL+"/like/"+str(id))
        self.mostrar_problemas()
