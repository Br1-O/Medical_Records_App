from domain.Entity import Entity
from domain.Value_objects import Id, Datetime, Text_with_range;

class Medical_record(Entity):
    def __init__(self, 
                 patient_id, 
                 date, 
                 consultation_reason, 
                 diagnosis,
                 treatment_evolution, 
                 observations="",
                 is_active=True, 
                 id=None):
        super().__init__(id=id, is_active=is_active)
        
        # Clave foránea referencial
        self._patient_id = Id(patient_id)
        if self._patient_id.value is None:
            raise ValueError("El 'patient_id' es obligatorio en el historial médico.")
            
        # Formato con hora para la evolución médica
        self._date = Datetime(date)
        
        # Textos de entrada en historia clinica
        self._consultation_reason = Text_with_range(consultation_reason, "Motivo de consulta", 1, 500, required=True)
        self._diagnosis = Text_with_range(diagnosis, "Diagnóstico", 1, 1000, required=True)
        self._treatment_evolution = Text_with_range(treatment_evolution, "Evolución/Tratamiento realizado", 1, 5000, required=True) # Sin límite práctico pero estricto
        self._observations = str(observations).strip() if observations else ""

    @property
    def patient_id(self): return self._patient_id.value
    
    @property
    def date(self): return self._date.value
    
    @property
    def consultation_reason(self): return self._consultation_reason.value
    
    @property
    def diagnosis(self): return self._diagnosis.value
    
    @property
    def treatment_evolution(self): return self._treatment_evolution.value
    
    @property
    def observations(self): return self._observations