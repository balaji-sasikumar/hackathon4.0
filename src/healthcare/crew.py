from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai.tasks.conditional_task import ConditionalTask

from healthcare.tools.custom_tool import BookAppointmentTool, CheckAvailabilityTool, ConversationLoggerTool, EmailTool, GenerateRoomLinkTool, PatientAPIPostTool
@CrewBase
class Healthcare():
    """Healthcare crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def intake_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['intake_agent'], # type: ignore[index]
            # verbose=True,
            tools=[PatientAPIPostTool()],
            allow_delegation=False,
            force_tool_usage=True,  # ⬅️ Force LLM to use tool
        )

    @agent
    def bot_doctor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['bot_doctor_agent'], # type: ignore[index]
            # verbose=True,
        )
    @agent
    def appointment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['appointment_agent'], # type: ignore[index]
            # verbose=True,
            tools=[GenerateRoomLinkTool(),CheckAvailabilityTool(), BookAppointmentTool()],

        )
    @agent
    def email_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['email_agent'], # type: ignore[index]
            # verbose=True,
            tools=[EmailTool(),GenerateRoomLinkTool()],
        )
    
    @task
    def patient_intake_task(self) -> Task:
        return Task(
            config=self.tasks_config['patient_intake_task'], # type: ignore[index]
            
        )

    @task
    def basic_diagnosis_task(self) -> Task:
        return Task(
            config=self.tasks_config['basic_diagnosis_task'], # type: ignore[index]
            
            
        )
    @task
    def appointment_booking_task(self) -> Task:
        return Task(
            config=self.tasks_config['appointment_booking_task'], # type: ignore[index]
        )
    
    @task
    def email_followup_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_followup_task'], # type: ignore[index]
        )
        
    def manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["manager_agent"],  # Ensure it's defined in your YAML
            verbose=True,
            allow_delegation=True,
        )
    @crew
    def diagnosis_crew(self) -> Crew:
        return Crew(
            agents=[self.intake_agent(), self.bot_doctor_agent()],
            tasks=[self.patient_intake_task(), self.basic_diagnosis_task()],
            process=Process.sequential,
            # verbose=True,
        )
    @crew
    def appointment_crew(self) -> Crew:
        return Crew(
            agents=[self.appointment_agent()],
            tasks=[self.appointment_booking_task()],
            process=Process.sequential,
            # verbose=True,
        )

    @crew
    def followup_crew(self) -> Crew:
        return Crew(
            agents=[self.email_agent()],
            tasks=[self.email_followup_task()],
            process=Process.sequential,
            verbose=True        
            )
