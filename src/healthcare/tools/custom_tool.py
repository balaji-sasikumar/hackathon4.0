import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import ClassVar, Dict, Any, Type
import random
import string

class PatientAPIPayload(BaseModel):
    patient_api: str = Field(..., description="The API endpoint to send the patient data to")
    patient_data: Dict[str, Any] = Field(..., description="The patient data to post, in structured JSON format")


class PatientAPIPostTool(BaseTool):
    name: str = "post_to_patient_api"
    description: str = "Posts structured patient data to the EHR system."
    args_schema: Type[PatientAPIPayload] = PatientAPIPayload  # ✅ Add proper type annotation

    def _run(self, patient_api: str, patient_data: Dict[str, Any]) -> str:
        import requests
        try:
            print(f"📦 Sending POST to: {patient_api}")
            print(f"🧾 Payload: {patient_data}")
            response = requests.post(patient_api, json=patient_data)
            return f"✅ POST to {patient_api} responded with {response.status_code}: {response.text}"
        except Exception as e:
            return f"❌ Error posting to EHR API: {e}"
        
class GenerateRoomLinkTool(BaseTool):
    name: str = "generate_live_consultation_link"
    description: str = "Generate a secure random live consultation room URL"

    def _run(self) -> str:
        room_id = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 12)))
        return f"https://jitsistoragewebapp.z30.web.core.windows.net/#{room_id}"

class ConversationLoggerInput(BaseModel):
    content: str = Field(..., description="Text content to write into the conversation log")

class ConversationLoggerTool(BaseTool):
    name: str = "log_conversation"
    description: str = "Logs messages to a session file that persists the conversation so far"
    args_schema: Type[ConversationLoggerInput] = ConversationLoggerInput

    log_file: ClassVar[str] = "session_log.txt"  # ✅ Annotated as ClassVar

    def _run(self, content: str) -> str:
        try:
            with open(self.log_file, "a") as f:
                f.write(content.strip() + "\n")
            return "📝 Conversation logged."
        except Exception as e:
            return f"❌ Failed to write conversation: {e}"

    @classmethod
    def read_log(cls) -> str:
        if os.path.exists(cls.log_file):
            with open(cls.log_file, "r") as f:
                return f.read()
        return ""

    @classmethod
    def clear_log(cls):
        if os.path.exists(cls.log_file):
            os.remove(cls.log_file)


class AvailabilityAPIPayload(BaseModel):
    availability_api: str = Field(..., description="The API endpoint to check availability")
    doctor_and_date: Dict[str, Any] = Field(..., description="The doctor ID and date to check availability for, in structured JSON format")


class CheckAvailabilityTool(BaseTool):
    name: str = "check_availability"
    description: str = "Checks the availability of a doctor on a specific date."
    args_schema: Type[AvailabilityAPIPayload] = AvailabilityAPIPayload  # ✅ Add proper type annotation

    def _run(self, availability_api: str, doctor_and_date: Dict[str, Any]) -> str:
        import requests
        try:
            print(f"🔍 Checking availability at: {availability_api}")
            print(f"📅 Doctor and Date: {doctor_and_date}")
            response = requests.post(availability_api, json=doctor_and_date)
            return f"✅ Availability check responded with {response.status_code}: {response.text}"
        except Exception as e:
            return f"❌ Error checking availability: {e}"


class BookAppointmentAPIPayload(BaseModel):
    appointment_api: str = Field(..., description="The API endpoint to book the appointment")
    appointment: Dict[str, Any] = Field(..., description="The appointment details to book, in structured JSON format")

class BookAppointmentTool(BaseTool):
    name: str = "book_appointment"
    description: str = "Books an appointment with a doctor."
    args_schema: Type[BookAppointmentAPIPayload] = BookAppointmentAPIPayload  # ✅ Add proper type annotation

    def _run(self, appointment_api: str, appointment: Dict[str, Any]) -> str:
        import requests
        try:
            print(f"📅 Booking appointment at: {appointment_api}")
            print(f"📝 Appointment details: {appointment}")
            response = requests.post(appointment_api, json=appointment)
            return f"✅ Appointment booking responded with {response.status_code}: {response.text}"
        except Exception as e:
            return f"❌ Error booking appointment: {e}"
