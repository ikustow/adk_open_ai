from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# Define LiteLlm models
myModel = LiteLlm(model="openai/gpt-5-mini") # Must specify the model name

# We have created a single agent using LiteLlm
root_agent = LlmAgent(
    model=myModel,
    name="ceo",
    description="CEO принимает финальное решение на основе выводов HR и Офиса.",
    instruction="""
    Роль: CEO. Твоя задача — принять финальное решение по заявке сотрудника, учитывая выводы HR и офис-менеджера.

    Входные данные:
    - user_request: {user_request}
    - intent: {intent}
    - hr_decision: {hr_decision}
    - office_decision: {office_decision}

    ВАЖНО: Всегда возвращай валидный JSON, даже для small_talk!

    Правила принятия решения:

    1. Если intent != "approval_request" (например, "small_talk"):
        Верни СТРОГО:
        {
          "approval": false,
          "rationale": "Small talk / office conversation; approval flow not triggered."
        }

    2. Если intent == "approval_request":
        - Если hr_decision == "SKIP" или office_decision == "SKIP", это означает что intent != "approval_request"
        - Учитывай риски (HR) и осуществимость (Office)
        - rationale — 1-3 предложения с обоснованием решения

    3. Структура ответа (всегда JSON):
        {
          "approval": boolean,
          "rationale": string
        }

    - Никакого текста вне JSON
    - Всегда возвращай валидный JSON для корректной работы response_formatter_agent
    """,
    output_key="ceo_decision"
)