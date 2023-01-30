from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, create_engine, inspect, select, func, text

Base = declarative_base()


class Cliente(Base):
    """
    Criando tabela com sqlalchemy atráves das classes
    """
    __tablename__ = 'cliente'
    # atributos
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9),unique=True)
    endereco = Column(String(9))
    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'User (id = {self.id}), nome = {self.nome}, cpf = {self.cpf}, conta = {self.conta})'


class Conta(Base):
    __tablename__ = 'conta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String, nullable=False)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    cliente = relationship("Cliente", back_populates='conta')

    def __repr__(self):
        return f"conta (id = {self.id}), tipo = {self.tipo}, agencia = {self.agencia} "


print(Cliente.__tablename__)

print(Conta.__tablename__)

# conexão com o banco de dado
engine = create_engine("sqlite:///:memory")

# Criando as tabelas no banco de dados atráves das classes

Base.metadata.create_all(engine)

# Criando inspect

inspetor_engine = inspect(engine)


with Session(engine) as session:
    juliana = Cliente(
        nome= 'Juliana',
        cpf= '123456789',
        endereco = 'San Martin',
        conta = [Conta(tipo='poupança',agencia='BB',num=1)]
    )
    joao = Cliente(
        nome= 'João',
        cpf= '987654321',
        endereco = 'Caxangá',
        conta = [Conta(tipo='Salário',agencia='Santander',num=2)]
    )

    patric = Cliente(
        nome= 'Patric',
        cpf= '123987654',
        endereco='Peixe',
        conta=[Conta(tipo='corrente', agencia='Itau', num=3)]

    )
    # Persistindo o banco de dados
    session.add_all([juliana, joao, patric])
    session.commit()




connection = engine.connect()



sql = text('SELECT cliente.id, cliente.nome, cliente.cpf, conta.tipo, conta.agencia, conta.num '
           'FROM cliente '
           'JOIN conta ON cliente.id = conta.id_cliente')

result = connection.execute(sql)

for row in result:
    print(row.id, row.nome, row.cpf, row.tipo, row.agencia, row.num)