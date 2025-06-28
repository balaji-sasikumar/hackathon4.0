from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Type
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