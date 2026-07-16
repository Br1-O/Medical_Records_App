from tkinter import messagebox
from datetime import datetime
from infrastructure.gui import Graphic_user_interface
from application.services import Patient_service, Medical_record_service, Log_service
from domain.Enums import View
from domain.Enums.Operation import Operation
from domain.Patient import Patient
from domain.Medical_record import Medical_record
from domain.Log import Log

class Graphic_user_interface_handler:

    def __init__(
        self, 
        graphic_user_interface: Graphic_user_interface,
        patient_service: Patient_service,
        medical_record_service: Medical_record_service,
        log_service: Log_service
    ):
        self._graphic_user_interface = graphic_user_interface
        self._patient_service = patient_service
        self._medical_record_service = medical_record_service
        self._log_service = log_service
        self._current_patient_dni: str = ""
        self._editing_patient: bool = False

    def bind_methods_to_graphic_user_interface(self) -> None:
        self._graphic_user_interface.on_patient_search = self._on_patient_search_handler
        self._graphic_user_interface.on_patient_creation = self._on_patient_creation_handler
        self._graphic_user_interface.on_patient_update = self._on_patient_update_handler
        self._graphic_user_interface.on_patient_delete = self._on_patient_delete_handler

        self._graphic_user_interface.on_medical_record_search = self._on_medical_record_search_handler
        self._graphic_user_interface.on_medical_record_creation = self._on_medical_record_creation_handler
        self._graphic_user_interface.on_medical_record_delete = self._on_medical_record_delete_handler

        self._graphic_user_interface.on_log_search = self._on_log_search_handler
        self._graphic_user_interface.on_log_double_click = self._on_log_double_click_handler
        self._graphic_user_interface.on_patient_detail_view = self._on_patient_detail_view_handler
        self._graphic_user_interface.on_edit_patient = self._on_edit_patient_handler
        self._graphic_user_interface.on_patient_reactivate = self._on_patient_reactivate_handler
        self._graphic_user_interface.on_medical_record_detail_view = self._on_medical_record_detail_view_handler

    def _log_operation(self, operation: str, affected_record_id: int) -> None:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_log = Log(
                timestamp=now,
                operation=operation,
                affected_record_id=affected_record_id
            )
            self._log_service.create_log_use_case(new_log)
        except Exception as e:
            print(f"[WARN] No se pudo registrar log de auditoría: {e}")

    # --- Handlers de Pacientes ---
    def _on_edit_patient_handler(self) -> None:
        try:
            self._graphic_user_interface.set_editing_mode(True)
            self._graphic_user_interface._editing_patient_dni = self._current_patient_dni
            patient = self._patient_service.get_patient_by_dni_use_case(self._current_patient_dni)
            if patient:
                self._editing_patient = True
                self._graphic_user_interface.set_patient_data_for_update_form(patient)
        except Exception as e:
            print(f"[WARN] Error al cargar datos para edición: {e}")

    def _on_patient_detail_view_handler(self) -> None:
        try:
            dni = self._graphic_user_interface.get_selected_patient_dni()
            if dni:
                self._current_patient_dni = dni
                patient = self._patient_service.get_patient_by_dni_use_case(dni)
                if patient:
                    detail_view = self._graphic_user_interface.views[View.PATIENT_DETAIL]
                    detail_view.lbl_fullname.configure(text=f"{patient.name} {patient.last_name}")
                    detail_view.lbl_dni.configure(text=f"DNI: {patient.dni}")
                    detail_view.lbl_birth_date.configure(text=f"Nacimiento: {patient.birth_date or '-'}")
                    detail_view.lbl_gender.configure(text=f"Género: {patient.gender or '-'}")
                    detail_view.lbl_phone.configure(text=f"Teléfono: {patient.phone or '-'}")
                    detail_view.lbl_emergency.configure(text=f"Contacto Emergencia: {patient.emergency_contact or '-'}")
                    detail_view.lbl_insurance.configure(text=f"Obra Social: {patient.health_insurance_name or '-'}")
                    detail_view.lbl_insurance_num.configure(text=f"Nro Obra Social: {patient.health_insurance_number or '-'}")
                    detail_view.lbl_status.configure(text=f"Estado: {'Activo' if patient.isActive else 'Inactivo'}")
                    detail_view.set_active_status(patient.isActive)
                records = self._medical_record_service.get_all_active_medical_records_by_dni_use_case(dni)
                self._graphic_user_interface.set_all_medical_records_data_for_display(records)
        except Exception as e:
            print(f"[WARN] Error al cargar vista detallada: {e}")

    def _on_medical_record_detail_view_handler(self) -> None:
        try:
            record_id = self._graphic_user_interface.get_selected_medical_record_id()
            if not record_id:
                return
            record = self._medical_record_service.get_medical_record_by_id_use_case(record_id)
            if record:
                self._graphic_user_interface.set_medical_record_data_for_display(record)
        except Exception as e:
            print(f"[WARN] Error al cargar detalle de entrada: {e}")

    def _on_patient_search_handler(self) -> None:
        try:
            search_data = self._graphic_user_interface.get_search_text_from_patient_search_form()
            query = search_data.get("query", "")
            is_active = self._graphic_user_interface.get_patient_status_filter()
            search_type = self._graphic_user_interface.get_patient_search_type()

            if not query:
                patients = self._patient_service.get_all_active_patients_use_case() if is_active else self._patient_service.get_all_inactive_patients_use_case()
            else:
                all_patients = self._patient_service.get_all_active_patients_use_case() if is_active else self._patient_service.get_all_inactive_patients_use_case()
                q = query.lower()
                if search_type == "DNI":
                    patients = [p for p in all_patients if q in p.dni]
                elif search_type == "Apellido":
                    patients = [p for p in all_patients if q in p.last_name.lower()]
                elif search_type == "Nombre":
                    patients = [p for p in all_patients if q in p.name.lower()]
                elif search_type == "Obra Social":
                    patients = [p for p in all_patients if q in (p.health_insurance_name or "").lower()]
                else:
                    patients = all_patients

            self._graphic_user_interface.set_all_patients_data_for_display(patients)

        except Exception as e:
            messagebox.showerror("Error de Búsqueda", f"Ocurrió un error al buscar pacientes: {str(e)}")

    def _on_patient_creation_handler(self) -> None:
        try:
            data = self._graphic_user_interface.get_data_from_patient_creation_form()
            if not data.get("dni") or not data.get("last_name") or not data.get("name"):
                messagebox.showwarning("Atención", "Los campos DNI, Nombre y Apellido son obligatorios.")
                return

            new_patient = Patient(
                name=data["name"],
                last_name=data["last_name"],
                dni=data["dni"],
                birth_date=data.get("birth_date", ""),
                gender=data.get("gender", "Otro"),
                phone=data.get("phone", ""),
                emergency_contact=data.get("emergency_contact", ""),
                has_health_insurance=bool(data.get("health_insurance_name", "").strip()),
                health_insurance_name=data.get("health_insurance_name", ""),
                health_insurance_number=data.get("health_insurance_number", "")
            )

            existing = self._patient_service.get_patient_by_dni_use_case(new_patient.dni)
            if existing:
                messagebox.showerror("DNI Duplicado", "Ese DNI ya se encuentra registrado.")
                return

            success = self._patient_service.create_patient_use_case(new_patient)
            if success:
                patient_id = self._patient_service.get_patient_by_dni_use_case(new_patient.dni)
                if patient_id:
                    self._log_operation("Alta Paciente", patient_id.id)
                messagebox.showinfo("Operación Exitosa", "Paciente registrado correctamente.")
                self._graphic_user_interface.clear_fields(View.PATIENT_REGISTRATION)
                self._graphic_user_interface.set_view(View.MAIN_WINDOW)
                self._on_patient_search_handler()
            else:
                messagebox.showerror("Error", "No se pudo registrar el paciente en la base de datos.")

        except ValueError as e:
            messagebox.showerror("Error de Validación", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error de Sistema", f"No se pudo completar el registro: {str(e)}")

    def _on_patient_update_handler(self) -> None:
        try:
            data = self._graphic_user_interface.get_data_from_patient_update_form()
            if not data.get("dni") or not data.get("last_name") or not data.get("name"):
                messagebox.showwarning("Atención", "Los campos DNI, Nombre y Apellido son obligatorios.")
                return

            editing_dni = self._graphic_user_interface._editing_patient_dni
            original_patient = self._patient_service.get_patient_by_dni_use_case(editing_dni)
            if not original_patient:
                messagebox.showerror("Error", "No se encontró el paciente original.")
                return

            updated_patient = Patient(
                name=data["name"],
                last_name=data["last_name"],
                dni=data["dni"],
                birth_date=data.get("birth_date", ""),
                gender=data.get("gender", "Otro"),
                phone=data.get("phone", ""),
                emergency_contact=data.get("emergency_contact", ""),
                has_health_insurance=bool(data.get("health_insurance_name", "").strip()),
                health_insurance_name=data.get("health_insurance_name", ""),
                health_insurance_number=data.get("health_insurance_number", ""),
                id=original_patient.id
            )

            if updated_patient.dni != editing_dni:
                conflicting = self._patient_service.get_patient_by_dni_use_case(updated_patient.dni)
                if conflicting:
                    messagebox.showerror("DNI Duplicado", "Ese DNI ya se encuentra registrado.")
                    return

            success = self._patient_service.update_patient_use_case(updated_patient)
            if success:
                self._log_operation("Modificación Paciente", original_patient.id)
                self._current_patient_dni = updated_patient.dni
                self._graphic_user_interface._editing_patient_dni = ""
                messagebox.showinfo("Éxito", "Datos del paciente actualizados.")
                self._graphic_user_interface.set_view(View.MAIN_WINDOW)
                self._on_patient_search_handler()
            else:
                self._graphic_user_interface._editing_patient_dni = ""
                messagebox.showerror("Error", "No se pudieron actualizar los datos.")

        except ValueError as e:
            messagebox.showerror("Error de Validación", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al intentar actualizar datos: {str(e)}")

    def _on_patient_delete_handler(self) -> None:
        try:
            dni_to_delete = self._graphic_user_interface.get_selected_patient_dni()
            if not dni_to_delete:
                return

            patient = self._patient_service.get_patient_by_dni_use_case(dni_to_delete)
            success = self._patient_service.delete_patient_by_dni_use_case(dni_to_delete)
            if success:
                if patient:
                    self._log_operation("Baja Paciente", patient.id)
                messagebox.showinfo("Baja Confirmada", "El paciente ha sido dado de baja lógicamente.")
                self._graphic_user_interface.set_view(View.MAIN_WINDOW)
                self._on_patient_search_handler()
            else:
                messagebox.showerror("Error", "No se pudo realizar la baja del paciente.")

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo eliminar al paciente: {str(e)}")

    def _on_patient_reactivate_handler(self) -> None:
        try:
            dni = self._current_patient_dni
            if not dni:
                dni = self._graphic_user_interface.get_selected_patient_dni()
            if not dni:
                return

            patient = self._patient_service.get_patient_by_dni_use_case(dni)
            if not patient:
                messagebox.showerror("Error", "No se encontro el paciente.")
                return

            reactivated = Patient(
                name=patient.name,
                last_name=patient.last_name,
                dni=patient.dni,
                birth_date=patient.birth_date or "",
                gender=patient.gender or "Otro",
                phone=patient.phone or "",
                emergency_contact=patient.emergency_contact or "",
                has_health_insurance=patient.has_health_insurance,
                health_insurance_name=patient.health_insurance_name or "",
                health_insurance_number=patient.health_insurance_number or "",
                is_active=True,
                id=patient.id
            )

            success = self._patient_service.update_patient_use_case(reactivated)
            if success:
                self._log_operation("Reactivacion Paciente", patient.id)
                messagebox.showinfo("Operacion Exitosa", "El paciente ha sido reactivado.")
                detail_view = self._graphic_user_interface.views[View.PATIENT_DETAIL]
                detail_view.lbl_status.configure(text="Estado: Activo")
                detail_view.set_active_status(True)
                self._on_patient_search_handler()
            else:
                messagebox.showerror("Error", "No se pudo reactivar el paciente.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al reactivar paciente: {str(e)}")

    # --- Handlers de Historias Clínicas (Consultas) ---
    def _on_medical_record_search_handler(self) -> None:
        try:
            dni = self._current_patient_dni
            if not dni:
                dni = self._graphic_user_interface.get_selected_patient_dni()
            if not dni:
                return

            records = self._medical_record_service.get_all_active_medical_records_by_dni_use_case(dni)

            query = self._graphic_user_interface.get_search_record_query()
            search_type = self._graphic_user_interface.get_search_record_type()

            if query:
                query_lower = query.lower()
                if search_type == "Fecha":
                    records = [r for r in records if query_lower in r.date.lower()]
                elif search_type == "Diagnóstico":
                    records = [r for r in records if query_lower in r.diagnosis.lower()]
                elif search_type == "Tratamiento":
                    records = [r for r in records if query_lower in r.treatment_evolution.lower()]

            self._graphic_user_interface.set_all_medical_records_data_for_display(records)
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Fallo al recuperar el historial clínico: {str(e)}")

    def _on_medical_record_creation_handler(self) -> None:
        try:
            data = self._graphic_user_interface.get_data_from_medical_record_creation_form()

            dni = self._current_patient_dni
            if not dni:
                dni = self._graphic_user_interface.get_selected_patient_dni()
            if not dni:
                messagebox.showerror("Error", "No se pudo identificar al paciente.")
                return

            patient = self._patient_service.get_patient_by_dni_use_case(dni)
            if not patient:
                messagebox.showerror("Error", "No se encontró el paciente.")
                return

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_record = Medical_record(
                patient_id=patient.id,
                date=now,
                consultation_reason=data.get("consultation_reason", ""),
                diagnosis=data.get("diagnosis", ""),
                treatment_evolution=data.get("treatment_evolution", ""),
                observations=data.get("observations", "")
            )

            success = self._medical_record_service.create_medical_record_use_case(new_record)
            if success:
                created = self._medical_record_service.get_all_active_medical_records_by_dni_use_case(dni)
                record_id = created[-1].id if created else patient.id
                self._log_operation("Alta Historial", record_id)
                self._graphic_user_interface.clear_fields(View.MEDICAL_RECORD_DETAIL)
                self._on_medical_record_search_handler()
                self._graphic_user_interface.set_view(View.PATIENT_DETAIL)
            else:
                messagebox.showerror("Error", "No se pudo guardar la entrada.")
        except ValueError as e:
            messagebox.showerror("Error de Validación", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error de Registro", f"No se pudo guardar la entrada: {str(e)}")

    def _on_medical_record_delete_handler(self) -> None:
        try:
            record_id = self._graphic_user_interface.get_selected_medical_record_id()
            if record_id == 0:
                return

            success = self._medical_record_service.delete_medical_record_by_id_use_case(record_id)
            if success:
                self._log_operation("Anulación", record_id)
                messagebox.showinfo("Éxito", "Entrada anulada correctamente.")
                self._on_medical_record_search_handler()
            else:
                messagebox.showerror("Error", "No se pudo anular la entrada.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar la anulación: {str(e)}")

    # --- Handlers de Logs (Auditoría) ---
    def _on_log_search_handler(self) -> None:
        try:
            logs = self._log_service.get_all_logs_use_case()
            self._graphic_user_interface.set_all_logs_data_for_display(logs)
        except Exception as e:
            messagebox.showerror("Error de Auditoría", f"Error al cargar la bitácora de logs: {str(e)}")

    def _on_log_double_click_handler(self) -> None:
        try:
            operation, affected_id = self._graphic_user_interface.get_selected_log_data()
            if not operation or not affected_id:
                return

            patient = None
            if "Paciente" in operation:
                all_patients = self._patient_service.get_all_active_patients_use_case() + self._patient_service.get_all_inactive_patients_use_case()
                patient = next((p for p in all_patients if p.id == affected_id), None)
            elif "Historial" in operation or "Anulación" in operation:
                record = self._medical_record_service.get_medical_record_by_id_use_case(affected_id)
                if record:
                    all_patients = self._patient_service.get_all_active_patients_use_case() + self._patient_service.get_all_inactive_patients_use_case()
                    patient = next((p for p in all_patients if p.id == record.patient_id), None)

            if patient:
                self._current_patient_dni = patient.dni
                detail_view = self._graphic_user_interface.views[View.PATIENT_DETAIL]
                detail_view.lbl_fullname.configure(text=f"{patient.name} {patient.last_name}")
                detail_view.lbl_dni.configure(text=f"DNI: {patient.dni}")
                detail_view.lbl_birth_date.configure(text=f"Nacimiento: {patient.birth_date or '-'}")
                detail_view.lbl_gender.configure(text=f"Género: {patient.gender or '-'}")
                detail_view.lbl_phone.configure(text=f"Teléfono: {patient.phone or '-'}")
                detail_view.lbl_emergency.configure(text=f"Contacto Emergencia: {patient.emergency_contact or '-'}")
                detail_view.lbl_insurance.configure(text=f"Obra Social: {patient.health_insurance_name or '-'}")
                detail_view.lbl_insurance_num.configure(text=f"Nro Obra Social: {patient.health_insurance_number or '-'}")
                detail_view.lbl_status.configure(text=f"Estado: {'Activo' if patient.isActive else 'Inactivo'}")
                records = self._medical_record_service.get_all_active_medical_records_by_dni_use_case(patient.dni)
                self._graphic_user_interface.set_all_medical_records_data_for_display(records)
                self._graphic_user_interface.set_view(View.PATIENT_DETAIL)
            else:
                messagebox.showinfo("Información", "No se pudo encontrar la entidad asociada al registro.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir el detalle: {str(e)}")
