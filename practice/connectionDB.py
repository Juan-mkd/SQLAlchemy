#connection string format: driver+postgressql://user:pass@host:port/dbname
from sqlalchemy import create_engine

# username = 'root'
# password = '147'
# host = 'localhost'  
# port = '5433'  
# database = 'datadb'

# # Crear el motor de conexión
# engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}', echo=True)
# print(engine)


"""
connection con NullPool

from sqlalchemy.pool import NullPool
engine = create_engine("mysql+mysqldb://user:pass@host/dbname", poolclass=NullPool)

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from datetime import date


#declarative models
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Float, Integer, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

# Definición de la clase base
class Base(DeclarativeBase):
    pass

# Clase para la tabla Tipo Transaccion
class TipoTransaccion(Base):
    __tablename__ = "tipo_transaccion"
    
    id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"TipoTransaccion(id={self.id!r}, descripcion={self.descripcion!r})"


# Clase para la tabla Fecha
class Fecha(Base):
    __tablename__ = "Fecha"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)  # Cambia aquí
    dia: Mapped[int] = mapped_column(nullable=False)
    mes: Mapped[int] = mapped_column(nullable=False)
    anio: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"Fecha(id={self.id!r}, fecha={self.fecha!r})"


# Clase para la tabla Transacciones
class Transacciones(Base):
    __tablename__ = "Transacciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_id: Mapped[int] = mapped_column(ForeignKey("Fecha.id"))
    transaccion_tipo_id: Mapped[PGUUID] = mapped_column(ForeignKey("tipo_transaccion.id"))
    simbolo: Mapped[str] = mapped_column(String(255))
    precio: Mapped[float] = mapped_column(Float)
    valor: Mapped[float] = mapped_column(Float)

    # Relaciones
    fecha: Mapped[Fecha] = relationship("Fecha")
    tipo_transaccion: Mapped[TipoTransaccion] = relationship("TipoTransaccion")

    def __repr__(self) -> str:
        return (f"Transacciones(id={self.id!r}, fecha_id={self.fecha_id!r}, "
                f"transaccion_tipo_id={self.transaccion_tipo_id!r}, simbolo={self.simbolo!r}, "
                f"precio={self.precio!r}, valor={self.valor!r})")






# Datos de conexión
username = 'root'
password = '147'
host = 'localhost'  
port = '5433'  
database = 'datadb'

class Connection:
    #contructor
    def __init__(self):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def connection(self):
        engine = create_engine(
                f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}',
                poolclass=NullPool  
                )
        
        return engine
    



# Uso de la clase Connection
if __name__ == "__main__":
    conn = Connection()
    engine = conn.connection()
    
    # Crear las tablas en la base de datos
    Base.metadata.create_all(engine)

    # Crear una sesión
    Session = sessionmaker(bind=engine)
    with Session() as session:
        # Aquí puedes realizar operaciones, como agregar registros
        # Ejemplo de adición de una transacción:
        new_transaction = Transacciones(
            fecha_id=1,  # Debes asegurarte de que esta ID exista en la tabla Fecha
            transaccion_tipo_id=1,  # Debes definir esto en algún lugar
            simbolo="AAPL",
            precio=150.0,
            valor=15000.0
        )
        session.add(new_transaction)
        session.commit()