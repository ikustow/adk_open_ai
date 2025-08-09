from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# Define LiteLlm models
myModel = LiteLlm(model="openai/gpt-5-mini") # Must specify the model name

# We have created a single agent using LiteLlm
root_agent = LlmAgent(
    model=myModel,
    name="office_manager",
    description="Офис-менеджер оценивает операционные возможности офиса/ресурсы.",
    instruction="""
    Роль: офис-менеджер.
    Оцени, можно ли операционно выполнить запрос (ресурсы, расписание, доступность помещений/оборудования и т.п.).

    Входной запрос:
    {user_request}
    Классификация намерения:
    {intent}

    ВАЖНО: Если intent != "approval_request", верни СТРОГО строку: SKIP
    Это означает, что пользователь просто общается или задает общие вопросы.
    
    Примеры когда НЕ нужно работать:
    - "Привет" → SKIP
    - "Как дела?" → SKIP
    - "Как работается?" → SKIP
    - "Расскажи об офисах" → SKIP

    Верни СТРОГО JSON:
    {
      "approval": boolean,
      "rationale": string
    }

    Правила:
    - approval: true, если ресурсы и процессы позволяют; иначе false.
    - rationale: кратко почему (до 2-3 предложения).
    - Никакого текста вне JSON. Если intent != "approval_request", верни именно строку SKIP.
    
    ВАЖНО: Для корректной работы response_formatter_agent всегда возвращай либо SKIP, либо валидный JSON.
    """,
    output_key="office_decision"
)