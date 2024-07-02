from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Date, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime


Base = declarative_base()

class Utente(Base):
    __tablename__ = 'utenti'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    indirizzo_1 = Column(String)
    indirizzo_2 = Column(String)
    created_at = Column(Date, default=datetime.date.today)


class Destinatario(Base):
    __tablename__ = 'destinatari'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ragione_sociale = Column(String, nullable=False)
    indirizzo_1 = Column(String)
    indirizzo_2 = Column(String)
    created_at = Column(Date, default=datetime.date.today)

    def __str__(self):
        return self.ragione_sociale

class Destinazione(Base):
    __tablename__ = 'destinazioni'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ragione_sociale = Column(String, nullable=False)
    indirizzo_1 = Column(String)
    indirizzo_2 = Column(String)
    created_at = Column(Date, default=datetime.date.today)

    def __str__(self):
        return self.ragione_sociale

class Trasportatore(Base):
    __tablename__ = "trasportatori"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ragione_sociale = Column(String, nullable=False)
    indirizzo_1 = Column(String)
    indirizzo_2 = Column(String)
    created_at = Column(Date, default=datetime.date.today)

    def __str__(self):
        return self.ragione_sociale


class Cmr(Base):
    __tablename__ = "cmr"
    id = Column(Integer, primary_key=True, autoincrement=True)
    utente_id = Column(Integer, ForeignKey('utenti.id'))
    destinatario_id = Column(Integer, ForeignKey('destinatari.id'))
    destinazione_id = Column(Integer, ForeignKey('destinazioni.id'))
    luogo_presa_in_carico = Column(String, nullable=False)
    data_presa_in_carico = Column(Date, default=datetime.date.today)
    documenti_allegati = Column(String)
    istruzioni_mittente = Column(String)
    porto_franco = Column(Boolean)
    porto_assegnato = Column(Boolean)
    rimborso = Column(String)
    trasportatore_id = Column(Integer, ForeignKey('trasportatori.id'))
    osservazioni_trasporto = Column(String)
    convenzioni = Column(String)
    compilato_a = Column(String)
    data_compilazione = Column(Date, default=datetime.date.today)
    created_at = Column(Date, default=datetime.date.today)

    dettagli = relationship("DettaglioCmr", back_populates="cmr")

    def __str__(self):
        return (f'Cmr n. {self.id} del {self.data_presa_in_carico}')

        # Metodo per salvare i dati del CMR

    def save_cmr_data(self):
        try:
            # Aggiungi il nuovo CMR alla sessione
            session.add(self)
            session.commit()  # Commit delle modifiche al database
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio del CMR: {e}")
            session.rollback()  # Rollback delle modifiche in caso di errore
            return False

class DettaglioCmr(Base):
    __tablename__ = "dettaglio_cmr"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cmr_id = Column(Integer, ForeignKey('cmr.id'))
    u_misura = Column(String)
    n_colli = Column(Integer)
    imballaggio = Column(String)
    denominazione = Column(String)
    statistica = Column(String)
    peso_lordo_kg = Column(Integer)
    volume_mc = Column(Integer)

    cmr = relationship("Cmr", back_populates="dettagli")

    def save_dettaglio_cmr_data(self):
        try:
            if not self.id:
                self.id = self.generate_new_detail_id()

            session.add(self)
            session.commit()  # Commit delle modifiche al database
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio del Dettaglio Cmr: {e}")
            session.rollback()  # Rollback delle modifiche in caso di errore
            return False

    def generate_new_detail_id(self):
        # Query per trovare l'ID massimo attuale e incrementarlo di 1
        max_id = session.query(func.max(DettaglioCmr.id)).scalar() or 0
        return max_id + 1


DATABASE_URL = "sqlite:///app.db"

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()



