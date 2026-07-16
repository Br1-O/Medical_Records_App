from domain.Entity import Entity
from domain.Value_objects import (
    Date, Dni, Email, Gender, Health_insurance, 
    Last_name, Name, Phone, Text_with_range
)

class Patient(Entity):
    def __init__(self, 
                 name, 
                 last_name, 
                 dni, 
                 birth_date, 
                 gender, 
                 phone,
                 emergency_contact, 
                 address="", 
                 secondary_phone="", 
                 email="",
                 city="Mar del Plata", 
                 country="Argentina",
                 has_health_insurance=False, 
                 health_insurance_name="",
                 health_insurance_number="", 
                 medical_observations="",
                 is_active=True, 
                 id=None):
        super().__init__(id=id, is_active=is_active)
        
        # Validaciones de Datos Personales delegadas a Value Objects
        self._name = Name(name, "Nombre")
        self._last_name = Last_name(last_name, "Apellido")
        self._dni = Dni(dni)
        self._birth_date = Date(birth_date, "Fecha de nacimiento", allow_future=False)
        self._gender = Gender(gender)
        
        # Campos de contacto[cite: 1]
        self._phone = Phone(phone, "Teléfono", required=True)
        self._secondary_phone = Phone(secondary_phone, "Teléfono secundario", required=False)
        self._email = Email(email)
        self._emergency_contact = Text_with_range(emergency_contact, "Contacto de emergencia", 1, 100, required=True)
        
        # Ubicación[cite: 1]
        self._address = Text_with_range(address, "Dirección", 0, 100, required=False)
        self._city = Text_with_range(city, "Ciudad", 2, 50, required=True)
        self._country = Text_with_range(country, "País", 2, 50, required=True)
        
        # Obra Social condicional[cite: 1]
        self._health_insurance = Health_insurance(
            has_health_insurance, health_insurance_name, health_insurance_number
        )
        
        # Observaciones[cite: 1]
        self._medical_observations = str(medical_observations).strip() if medical_observations else ""

    # --- Getters que exponen valores planos/primitivos para compatibilidad externa ---
    @property
    def name(self): return self._name.value
    
    @property
    def last_name(self): return self._last_name.value
    
    @property
    def dni(self): return self._dni.value
    
    @property
    def birth_date(self): return self._birth_date.value
    
    @property
    def gender(self): return self._gender.value
    
    @property
    def phone(self): return self._phone.value
    
    @property
    def secondary_phone(self): return self._secondary_phone.value
    
    @property
    def email(self): return self._email.value
    
    @property
    def emergency_contact(self): return self._emergency_contact.value
    
    @property
    def address(self): return self._address.value
    
    @property
    def city(self): return self._city.value
    
    @property
    def country(self): return self._country.value
    
    @property
    def has_health_insurance(self): return self._health_insurance.has_insurance
    
    @property
    def health_insurance_name(self): return self._health_insurance.name
    
    @property
    def health_insurance_number(self): return self._health_insurance.affiliate_number
    
    @property
    def medical_observations(self): return self._medical_observations