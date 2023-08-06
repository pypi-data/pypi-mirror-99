"""
AMQP
"""

import pika

from gmpyinfr_amqp.utils import read_conf_file

class AMQP:
    """Classe wrapper para o pika, no protocolo AMQP."""

    def __init__(self, filepath, verbose=False):
        """
        Construtor.

        Params:
            - filepath : str arquivo contendo a configuração a ser lida.
        """

        self.verbose = verbose
        conf = read_conf_file(filepath)
        self.routingkey = conf['routingkey']

        self.exchange = '{}.exchange'.format(self.routingkey)
        self.queue = '{}.queue'.format(self.routingkey)

        # credenciais
        self.cred = pika.PlainCredentials(
            username=conf['user'], password=conf['pwd'],
            erase_on_connect=True)
        self.comms('Credenciais criadas')

        # parâmetros de conexão
        self.params = pika.ConnectionParameters(
            host=conf['host'], port=conf['port'],
            virtual_host=conf['virtualhost'], credentials=self.cred)
        self.comms('Parâmetros de conexão criados')

        # propriedades da URL
        self.props = pika.BasicProperties(
            content_type='text/plain', delivery_mode=2)
        # delivery mode 2 para mensagem ser persistente

        self.conn = None  # conexão
        self.chnn = None  # channel

    def comms(self, msg):
        """Printa mensagens."""

        if self.verbose:
            print('[Rabbit] - {}'.format(msg))

    def connect(self):
        """Estabelece conexão."""

        if self.conn is None:
            self.comms('Estabelecendo conexão')
            # conexão
            self.conn = pika.BlockingConnection(self.params)
            # canal
            self.chnn = self.conn.channel()

            if not self.chnn.is_open:
                raise ValueError("Não foi possível abrir canal")

            # declarações
            self.chnn.exchange_declare(exchange=self.exchange,
                exchange_type='direct', durable=True)
            self.chnn.queue_declare(queue=self.queue,
                durable=True)
            self.chnn.queue_bind(self.queue, self.exchange,
                routing_key=self.routingkey)

            # coloca o canal em modo de confirmação
            self.chnn.confirm_delivery()
        else:
            self.comms('Conexão estabelecida previamente')

    def close(self):
        """Encerra a conexão."""

        if self.conn is not None and self.conn.is_open:
            self.comms('Encerrando conexão')
            self.conn.close()

            self.conn = None  # conexão
            self.chnn = None  # channel
        else:
            self.comms('Conexão encerrada')

    def send(self, body, retries=3):
        """Faz o envio de um body para o rabbit."""

        def _send(_try=1, e=None):
            """Faz uma tentativa de envio."""

            if _try > retries:
                raise e

            self.comms('Tentativa entrega nº {}'.format(_try))
            try:
                self.chnn.basic_publish(exchange=self.exchange,
                    routing_key=self.routingkey, body=body,
                    properties=self.props, mandatory=True)
                self.comms('Mensagem enviada')
            except pika.exceptions.AMQPError as e:
                self.comms('Falha tentativa {}'.format(_try))
                _send(_try + 1, e)

        self.connect()
        _send()
