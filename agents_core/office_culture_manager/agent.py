from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm



load_dotenv()

# Define LiteLlm models
myModel = LiteLlm(model="openai/gpt-5-mini") # Must specify the model name

# We have created a single agent using LiteLlm

root_agent = LlmAgent(
        model=myModel,
        name="office_culture_manager",
        description="Office-culture менеджер отвечает на вопросы об офисной культуре и атмосфере в офисе.",
        instruction=f"""
       Твоя задача ответить на вопросы об офисной культуре и атмосфере в офисе.
       Ты представитель компании, отвечающий за культуру и атмосферу в офисе. Отвечай на общие вопросы об офисной жизни, культуре компании, рабочей атмосфере.
      
       Будь естественным, дружелюбным, говори от имени компании.
       Общайся на темы офисной жизни, корпоративной культуры, рабочей атмосферы.
        """,
        output_key="office_culture_answer"
        )

