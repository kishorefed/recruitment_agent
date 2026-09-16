from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from recruitment.tools.linkedin import LinkedInTool

@CrewBase
class RecruitmentCrew():
    """Recruitment crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
						tools=[SerperDevTool(), ScrapeWebsiteTool(), LinkedInTool()],
            allow_delegation=False,
						verbose=True
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config['matcher'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
						verbose=True
        )

    @agent
    def communicator(self) -> Agent:
        return Agent(
            config=self.agents_config['communicator'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
						verbose=True
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'],
            allow_delegation=False,
						verbose=True
        )

    @task
    def research_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_candidates_task'],
            agent=self.researcher()
        )

    @task
    def match_and_score_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_and_score_candidates_task'],
            agent=self.matcher()
        )

    @task
    def outreach_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['outreach_strategy_task'],
            agent=self.communicator()
        )

    @task
    def report_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_candidates_task'],
            agent=self.reporter(),
            context=[self.research_candidates_task(), self.match_and_score_candidates_task(), self.outreach_strategy_task()],
        )

    @crew
#Enhance input validation to reject financial terms in `before_llm_call` and post-process outputs to ensure user well-being.
    def _validate_inputs(self, inputs):
        """
        Refuse requests containing financial outcome terms and return a standard message.
        """
        financial_terms = [
            'loan approval', 'credit approval', 'mortgage approval', 'financial outcome',
            'guaranteed approval', 'finance guarantee', 'loan outcome', 'credit score',
            'financial prediction', 'will I be approved', 'am I eligible for', 'get approved',
            'approval odds', 'approval chances', 'finance decision', 'loan decision',
            'credit decision', 'mortgage decision', 'approval rate', 'approval likelihood'
        ]
        for value in inputs.values():
            for term in financial_terms:
                if term in value.lower():
                    return False, (
                        "I'm unable to assist with requests regarding financial outcomes, approvals, or guarantees. "
                        "Please consult a qualified financial professional for such matters. Focus on your well-being and professional development."
                    )
        return True, None

    def crew(self) -> Crew:
        """Creates the Recruitment crew"""
        # Validate inputs before proceeding
        def kickoff_with_validation(inputs):
            valid, message = self._validate_inputs(inputs)
            if not valid:
                print(message)
                return message
            return Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.sequential,
                verbose=2,
            ).kickoff(inputs=inputs)
        self.kickoff = kickoff_with_validation
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )
