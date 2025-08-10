from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import sys
import os


load_dotenv()

# Define LiteLlm models
myModel = LiteLlm(model="openai/gpt-5-mini") # Must specify the model name


root_agent = LlmAgent(
        model=myModel,
        name="hr_agent",
        description="HR-менеджер оценивает запросы на отпуск с учетом доступных дат.",
        instruction=f"""
        Роль: HR-менеджер.
        Тебя подключают для оценки запросов на отпуск сотрудников.       

        ПРИМЕРЫ АНАЛИЗА:
        
        1. Запрос на отпуск:
           - Проверить доступность запрошенных дат
           - Учесть доступные даты в конфигурации
           - Предложить альтернативные даты при необходимости
        """,
        output_key="hr_decision"
    )
