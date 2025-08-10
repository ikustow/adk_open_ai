from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


load_dotenv()

# Define LiteLlm models
myModel = LiteLlm(model="openai/gpt-5-mini") # Must specify the model name

# We have created a single agent using LiteLlm

root_agent = LlmAgent(
        model=myModel,
        name="payroll_agent",
        description="Payroll-менеджер оценивает запросы на повышение зарплаты с учетом доступного бюджета.",
        instruction=f"""
        Роль: Payroll-менеджер.
        Тебя подключают для оценки запросов на повышение зарплаты сотрудников.
          
        ПРИМЕРЫ АНАЛИЗА:
        
        1. Запрос на повышение:
           - Проверить доступность бюджета
           - Учесть лимиты на сотрудника
           - Предложить альтернативные суммы при необходимости       
        """,
        output_key="payroll_decision"
    )

