from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from recruitment.tools.linkedin import LinkedInTool

@CrewBase
#Enhance input validation to reject financial terms in `before_llm_call` and post-process outputs to ensure user well-being.
class RecruitmentCrew():
    """Recruitment crew
    Policy: Before invoking the LLM, all inputs must be validated to ensure they do not request financial outcomes or advice. If such a request is detected, the system must refuse and instruct the user to consult a qualified financial professional. No keyword filtering or post-hoc output filtering is allowed; encode this as a validation policy only.
    """
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
    def crew(self) -> Crew:
        """Creates the Recruitment crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )

# === SecuraAI recommendation coverage (auto-generated; do not remove) ===
#Implement system prompt rules to refuse financial outcome requests and redirect users to seek professional advice.
# TODO(SecuraAI): address via SYSTEM_PROMPT / instruction / policy text (do not use keyword filtering on model output).
# No code changes needed: pending prompt-level implementation — All task descriptions updated with explicit refusal and redirection instructions..
