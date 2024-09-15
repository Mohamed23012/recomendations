from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from chatbot.llm import llm
from crewai_tools import NL2SQLTool
from chatbot.config import config

@CrewBase
class EcommerceChatbotCrew:
    """E-commerce Chatbot Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.nl2sql_tool = NL2SQLTool(
            db_uri=config.DB_URI
        )

    @agent
    def shop_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['shop_assistant'],
            tools=[self.nl2sql_tool],
            verbose=True,
            allow_delegation=False,
            memory=True,
            llm=llm
        )

    @task
    def personalized_recommendations(self) -> Task:
        return Task(
            config=self.tasks_config['personalized_recommendations'],
            tools=[self.nl2sql_tool]
        )
    
    @task
    def answer_faq(self) -> Task:
        return Task(
            config=self.tasks_config['answer_faq'],
            tools=[self.nl2sql_tool]
        )
    
    @task
    def track_order(self) -> Task:
        return Task(
            config=self.tasks_config['track_order'],
            tools=[self.nl2sql_tool]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.agents],
            tasks=[
                self.tasks
            ],
            process=Process.sequential,
            verbose=True
        )