from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from  models import Summary, FeatureExtractionResult,  CompetitorAnalysis, TimelineAnalysis



@CrewBase
class RedditMind():
	"""RedditMind crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def summarizer(self) -> Agent:
		return Agent(
			config=self.agents_config['summarizer'],
			verbose=True
		)

	@agent
	def features_extraction(self) -> Agent:
		return Agent(
			config=self.agents_config['features_extraction'],
			verbose=True
		)

	@agent
	def comparison_analysis(self) -> Agent:
		return Agent(
			config=self.agents_config['comparison_analysis'],
			verbose=True
		)

	@agent
	def timeline_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['timeline_analyzer'],
			verbose=True
		)

	# To learn more about structured task outputs,
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def summarize_task(self) -> Task:
		return Task(
			config=self.tasks_config['summarize_task'],
			output_json=Summary,
			output_file='review.json'
		)

	@task
	def features_extraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['features_extraction_task'],
			output_json=FeatureExtractionResult,
			output_file='features.json'
		)

	@task
	def comparison_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['comparison_analysis_task'],
			output_json=CompetitorAnalysis,
			output_file='competition.json'
		)

	@task
	def timeline_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['timeline_analysis_task'],
			output_json=TimelineAnalysis,
			output_file='timeline_analysis.json'
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the RedditMind crew"""

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
