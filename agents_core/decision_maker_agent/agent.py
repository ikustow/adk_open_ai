from dotenv import load_dotenv
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm

from .sub_agents.hr_agent.agent import root_agent as hr_agent
from .sub_agents.payroll_agent.agent import root_agent as payroll_agent


load_dotenv()

# Define LiteLlm models
myModel = LiteLlm(model="openai/gpt-5-mini") # Must specify the model name

# Parallel workflow executor - запускает approval workflow 
parallel_workflow_executor = ParallelAgent(
    name="parallel_workflow_executor",
    description="Параллельно выполняет office culture и approval workflow на основе intent.",
    sub_agents=[
        hr_agent,  # Решает нужно ли запускать approval
        payroll_agent,        # HR → Office → CEO workflow
    ],
)


ceo_agent = LlmAgent(
        model=myModel,
        name="ceo_agent",
        description="CEO компании принимает решение на основе рекомендаций HR и Office менеджеров.",
        instruction=f"""
       Твоя задача принять решение на основе рекомендаций HR и Office менеджеров. Для этого запускай parallel_workflow_executor
       
       Ответ от hr_agent и payroll_agent будет в state.hr_decision и state.payroll_decision соответственно.
       
       Структура ответов:
       - state.hr_decision: содержит решение HR по отпуску (в ответе называй это мнение HR)
       - state.payroll_decision: содержит решение Payroll по зарплате (в ответе называй это мнение Payroll)
       
       Твоя задача:
       1. Проанализировать оба решенияы
       2. Принять финальное решение как CEO
       3. Объяснить логику принятия решения
       4. Предложить план действий
       
       Ты генеральный директор компании, отвечающий за культуру и атмосферу в офисе. Отвечай на общие вопросы об офисной жизни, культуре компании, рабочей атмосфере.
    
        """,
        output_key="ceo_answer"
        )



root_agent = SequentialAgent(
    name="decision_maker_agent",
    sub_agents=[parallel_workflow_executor,ceo_agent],
    description="Executes a sequence of code writing, reviewing, and refactoring.",
    # The agents will run in the order provided: Writer -> Reviewer -> Refactorer
)

