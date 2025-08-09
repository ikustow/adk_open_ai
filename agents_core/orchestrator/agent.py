from dotenv import load_dotenv
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# Define LiteLlm models
myModel = LiteLlm(model="openai/gpt-5-mini") # Must specify the model name

# Import sub-agent objects
from .sub_agents.hr_manager.agent import root_agent as hr_agent
from .sub_agents.office_manager.agent import root_agent as office_agent
from .sub_agents.ceo.agent import root_agent as ceo_agent

# 1) Capture user's request into state.user_request
capture_request_agent = LlmAgent(
    model=myModel,
    name="capture_user_request",
    description="Сохраняет исходный запрос пользователя в state.user_request.",
    instruction="""
    Верни дословно входной пользовательский запрос без изменений. Никакого дополнительного текста.
    """,
    output_key="user_request",
)

# Intent classifier: decide whether to trigger approval flow or keep small talk
intent_classifier_agent = LlmAgent(
    model=myModel,
    name="intent_classifier",
    description="Классифицирует намерение пользователя: approval_request | small_talk.",
    instruction="""
    Дан пользовательский запрос:
    {user_request}

    Простая классификация:
    - "small_talk" - приветствия, общие вопросы, простое общение об офисной жизни
    - "approval_request" - конкретные запросы (отпуск, повышение, командировка, изменение графика)
    
    Верни СТРОГО одно слово: approval_request | small_talk
    """,
    output_key="intent",
)

# Office culture agent - отвечает на общие вопросы об офисной жизни и корпоративной культуре
office_culture_agent = LlmAgent(
    model=myModel,
    name="office_culture_handler",
    description="Обрабатывает простые диалоги и общение об офисной жизни и корпоративной культуре.",
    instruction="""
    Ты - представитель компании, отвечающий за культуру и атмосферу в офисе. Отвечай на общие вопросы об офисной жизни, культуре компании, рабочей атмосфере.
    
    Если intent == "small_talk", ответь дружелюбно на запрос пользователя.
    Если intent != "small_talk", верни SKIP.
    
    Будь естественным, дружелюбным, говори от имени компании.
    Общайся на темы офисной жизни, корпоративной культуры, рабочей атмосферы.
    """,
    output_key="office_culture_response"
)

# Approval workflow orchestrator - запускает под-агентов для approval requests
approval_workflow_agent = SequentialAgent(
    name="approval_workflow",
    description="Запускает последовательность HR → Office → CEO для approval requests.",
    sub_agents=[
        hr_agent,           # HR оценка рисков
        office_agent,       # Office оценка ресурсов
        ceo_agent,          # CEO финальное решение
    ],
)

# Conditional approval workflow - запускается только для approval requests
conditional_approval_workflow = LlmAgent(
    model=myModel,
    name="conditional_approval_workflow",
    description="Условно запускает approval workflow только для approval requests.",
    instruction="""
    Твоя задача - решить, нужно ли запускать approval workflow.
    
    Входные данные:
    - intent: {intent}
    
    ЛОГИКА:
    
    1. Если intent == "small_talk":
        - НЕ запускай approval workflow
        - Верни "SKIP_APPROVAL"
    
    2. Если intent == "approval_request":
        - Нужно запустить approval workflow
        - Верни "RUN_APPROVAL"
    
    Верни СТРОГО: "SKIP_APPROVAL" | "RUN_APPROVAL"
    """,
    output_key="approval_decision"
)

# Parallel workflow executor - запускает approval workflow параллельно с office culture
parallel_workflow_executor = ParallelAgent(
    name="parallel_workflow_executor",
    description="Параллельно выполняет office culture и approval workflow на основе intent.",
    sub_agents=[
        conditional_approval_workflow,  # Решает нужно ли запускать approval
        approval_workflow_agent,        # HR → Office → CEO workflow
    ],
)

# Smart workflow orchestrator - умно выбирает между office culture и approval workflow
smart_workflow_orchestrator = LlmAgent(
    model=myModel,
    name="smart_workflow_orchestrator",
    description="Умно выбирает какой workflow использовать и формирует финальный ответ.",
    instruction="""
    Ты - УМНЫЙ ОРКЕСТРАТОР. Твоя задача - проанализировать все данные и сформировать финальный ответ.
    
    Входные данные:
    - user_request: {user_request}
    - intent: {intent}
    - office_culture_response: {office_culture_response}
    - approval_decision: {approval_decision}
    - hr_decision: {hr_decision}
    - office_decision: {office_decision}
    - ceo_decision: {ceo_decision}
    
    ЛОГИКА:
    
    1. Если intent == "small_talk":
        - Используй {office_culture_response} как основу
        - Сделай ответ дружелюбным и естественным
        - Отвечай от имени компании
        - approval_decision должен быть "SKIP_APPROVAL"
        - hr_decision, office_decision, ceo_decision могут быть пустыми или "SKIP"
        - НЕ используй данные от approval workflow
    
    2. Если intent == "approval_request":
        - approval_decision должен быть "RUN_APPROVAL"
        - Проверь результаты всех под-агентов (hr_decision, office_decision, ceo_decision)
        - Сформируй понятный ответ на основе решения CEO
        - Объясни результат простым языком
    
    В любом случае:
    - Сделай ответ понятным и дружелюбным
    - Не добавляй технические детали о внутренней работе системы
    - Обращайся к пользователю от первого лица (мы, наш офис)
    - Если это approval request, четко укажи результат (одобрено/отклонено) и краткое обоснование
    """,
    output_key="final_response"
)

# Main orchestrator - объединяет все компоненты
root_agent = SequentialAgent(
    name="orchestrator",
    description="Главный оркестратор: обрабатывает запросы через классификацию и соответствующие workflows.",
    sub_agents=[
        capture_request_agent,      # 1. Захватывает запрос
        intent_classifier_agent,    # 2. Классифицирует намерение
        office_culture_agent,       # 3. Обрабатывает office culture (может вернуть SKIP)
        parallel_workflow_executor, # 4. ПАРАЛЛЕЛЬНЫЙ EXECUTOR: условно запускает approval workflow
        smart_workflow_orchestrator, # 5. УМНЫЙ ОРКЕСТРАТОР: выбирает workflow и формирует ответ
    ],
)