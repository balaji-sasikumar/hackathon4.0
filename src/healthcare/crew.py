from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

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
            verbose=True,
            tools=[PatientAPIPostTool()],
            allow_delegation=False,
            force_tool_usage=True,  # ⬅️ Force LLM to use tool
        )

    @agent
    def bot_doctor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['bot_doctor_agent'], # type: ignore[index]
            verbose=True,
            
        )
    @agent
    def appointment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['appointment_agent'], # type: ignore[index]
            verbose=True,
            tools=[GenerateRoomLinkTool(),CheckAvailabilityTool(), BookAppointmentTool()],
        )
    # @agent
    # def email_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['email_agent'], # type: ignore[index]
    #         verbose=True,
    #         tools=[EmailTool()],
    #     )
    
    @task
    def patient_intake_task(self) -> Task:
        return Task(
            config=self.tasks_config['patient_intake_task'], # type: ignore[index]
        )

    @task
    def basic_diagnosis_task(self) -> Task:
        return Task(
            config=self.tasks_config['basic_diagnosis_task'], # type: ignore[index]
            tools=[GenerateRoomLinkTool()],
        )
    @task
    def appointment_booking_task(self) -> Task:
        return Task(
            config=self.tasks_config['appointment_booking_task'], # type: ignore[index]
        )
    # @task
    # def email_followup_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['email_followup_task'], # type: ignore[index]
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the Healthcare crew"""
        
        
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True, # ⬅️ Return intermediate steps for debugging
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
