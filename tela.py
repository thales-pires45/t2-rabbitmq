from threading import Thread
from tkinter import *
import pika


class Application_privado():
    def __init__(self):
        tela = Toplevel()
        self.tela = tela
        self.janela()
        self.mensagem_layout()
        self.receber_layout()
        self.enviar_layout()
        self.thread_receber()

    def janela(self):
        self.tela.remetente = remetente.get()
        self.tela.destinatario = destinatario.get()
        self.tela.title(f'WhatsApp_2 Privado - {self.tela.remetente}')
        self.tela.geometry("300x390+300+100")
        self.tela.configure(bg="#000000")
        self.tela.resizable(False, False)

    def mensagem_layout(self):
        self.tela.listbox = Frame(self.tela)
        self.tela.scrollbar = Scrollbar(self.tela.listbox)
        self.tela.mensagem_box = Listbox(
            self.tela.listbox,
            height=21,
            width=45,
            yscrollcommand=self.tela.scrollbar.set
        )
        self.tela.scrollbar.pack(side=RIGHT, fill=Y)
        self.tela.mensagem_box.pack(side=LEFT, fill=BOTH)
        self.tela.mensagem_box.pack()
        self.tela.listbox.pack()

    def receber_layout(self):
        self.tela.botao_box = Frame(self.tela)
        self.tela.botao_box.configure(bg="#000000")
        self.tela.texto_mensagem = Entry(
            self.tela.botao_box,
            width=30,
            bg='white',
            font=('Comic Sans MS', '10')
        )
        self.tela.texto_mensagem.pack(side=LEFT, anchor=SE, pady=13, padx=5)
        self.tela.texto_mensagem.pack()

    def enviar_layout(self):
        self.tela.botao_enviar = Button(
            self.tela.botao_box,
            text="Enviar",
            command=self.send,
            fg="#000000",
            bg="white",
            font=('Arial', '8'),
        )
        self.tela.botao_enviar.pack(side=LEFT, anchor=S, pady=11, padx=5)
        self.tela.botao_box.pack()

    def thread_receber(self):
        self.tela.receber = Thread(target=self.receiver)
        self.tela.receber.start()

    def receiver(self):
        def inserir(ch, method, propreties, body):
            self.tela.lista_mensagem.insert(END, f"{self.tela.destinatario} -> " + body.decode('utf-8'))

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=self.tela.remetente)
        channel.basic_consume(queue=self.tela.remetente, on_message_callback=inserir, auto_ack=True)
        channel.start_consuming()
        connection.close()

    def send(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=self.tela.destinatario)
        mensagem = self.tela.texto_mensagem.get()
        self.tela.lista_mensagem.insert(END, f"{self.tela.remetente} -> " + mensagem)
        channel.basic_publish(exchange='', routing_key=self.tela.destinatario, body=mensagem.encode('utf-8'))
        connection.close()


class Application_grupo():
    def __init__(self):
        tela2 = Toplevel(janela)
        self.tela2 = tela2
        self.janela()
        self.mensagem_layout()
        self.receber_layout()
        self.envia_layout()
        self.thread_receber()

    def janela(self):
        self.tela2.remetente = remetente.get()
        self.tela2.grupo = grupo.get()
        self.tela2.title(f'WhatsApp_2 Grupo - {self.tela2.remetente}')
        self.tela2.geometry("300x390+830+100")
        self.tela2.configure(bg="#000000")
        self.tela2.resizable(False, False)

    def mensagem_layout(self):
        self.tela2.listbox = Frame(self.tela2)
        self.tela2.scrollbar = Scrollbar(self.tela2.listbox)
        self.tela2.mensagem_box = Listbox(
            self.tela2.listbox,
            height=21,
            width=45,
            yscrollcommand=self.tela2.scrollbar.set
        )
        self.tela2.scrollbar.pack(side=RIGHT, fill=Y)
        self.tela2.mensagem_box.pack(side=LEFT, fill=BOTH)
        self.tela2.mensagem_box.pack()
        self.tela2.listbox.pack()

    def receber_layout(self):
        self.tela2.botao_box = Frame(self.tela2)
        self.tela2.botao_box.configure(bg="#000000")
        self.tela2.texto_mensagem = Entry(
            self.tela2.botao_box,
            width=30,
            bg='white',
            font=('Comic Sans MS', '10')
        )
        self.tela2.texto_mensagem.pack(side=LEFT, anchor=SE, padx=5, pady=13)
        self.tela2.texto_mensagem.pack()

    def envia_layout(self):
        self.tela2.botao_enviar = Button(
            self.tela2.botao_box,
            text="Enviar",
            command=self.send_grupo,
            fg="#000000",
            bg="white",
            font=('Arial', '8'),
        )
        self.tela2.botao_enviar.pack(side=LEFT, anchor=S, pady=11, padx=5)
        self.tela2.botao_box.pack()

    def thread_receber(self):
        self.tela2.receber = Thread(target=self.receiver_grupo)
        self.tela2.receber.start()

    def receiver_grupo(self):
        def inserir(ch, method, propreties, body):
            self.tela2.lista_mensagem.insert(END, body.decode('utf-8'))

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.tela2.grupo, exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=self.tela2.grupo, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=inserir, auto_ack=True)
        channel.start_consuming()
        connection.close()

    def send_grupo(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        mensagem = self.tela2.texto_mensagem.get()
        channel.exchange_declare(exchange=self.tela2.grupo, exchange_type='fanout')
        channel.basic_publish(exchange=self.tela2.grupo, routing_key='', body=f'{self.tela2.remetente} -> ' + mensagem)


janela = Tk()


# Propriedades da janela:
janela.resizable(width=False, height=False)
janela.configure(bg='#000000')
janela.title('WhatsApp_2')
janela.geometry('350x210+460+300')

# Janela Inicial:
titulo1 = Label(bg='#000000', font=('Arial', '14', 'bold'), fg='white', text='BEM VINDO ao WHATSAPP2')
titulo1.place(x='35', y='10')

remetente = Entry(width=25, bg='white', font=('Comic Sans MS', '10'))
remetente.place(x=130, y=50)
Info1 = Label(font=('Arial', '11', 'bold'), fg='white', bg='#000000', text='Remetente:')
Info1.place(x=10, y=50)

destinatario = Entry(width=25, bg='white', font=('Comic Sans MS', '10'))
destinatario.place(x=130, y=75)
Info2 = Label(font=('Arial', '11', 'bold'), fg='white', bg='#000000', text='Destinatario:')
Info2.place(x=10, y=75)

grupo = Entry(width=25, bg='white', font=('Comic Sans MS', '10'))
grupo.place(x=130, y=100)
Info3 = Label(font=('Arial', '11', 'bold'), fg='white', bg='#000000', text='Grupo:')
Info3.place(x=10, y=100)

proximo = Button(width='39', text='Grupo', font=('Arial', '10'), command=Application_grupo)
proximo.place(x=15, y=170)

proximo2 = Button(width='39', text='Privado', font=('Arial', '10'), command=Application_privado)
proximo2.place(x=15, y=140)

janela.mainloop()
