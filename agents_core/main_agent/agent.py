from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# Define LiteLlm models
myModel = LiteLlm(model="openai/gpt-5-mini") # Must specify the model name

# We have created a single agent using LiteLlm
root_agent = LlmAgent(
    model=myModel,
    name="main_agent",
    description="Агент маршрутизации запросов",
    instruction="""
   Твоя задача определить какой тип диалога идет, нужно выделить это просто смолл толк о жизни в офисе.
   Если это смолл толк о жизни в офисе, то верни path: 'office_culture'.
   Если это запрос на отпуск, повышение, командировку, изменение графика, то верни path: 'approval_request'.
   Если это что-то другое, то верни path: 'other'.
    """,
    output_key="route_path"
)