from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from openai import OpenAI
import os
from dotenv import load_dotenv


def response(message):
    try:
        llm = ChatOpenAI(
            api_key="a04976dc-1b1a-589f-8588-2c77203c0de5",
           base_url="https://arvancloudai.ir/gateway/models/Gemini-2.0-Flash-001/ZsL6R_G-v1BtQX0BBwmjt_SXIyGNYEQ8yGnrTH1JBa_wl58uFZ_6F7NWxRkotfxpj7K80b9qMy2O2xKeKfLN1dcVnSZR9x5_" \
           "k5ipYY13WQjh5QWI07tDlLOZx1y1lS9aHfB6d5Q1OOLRs36YkYTvdYpCmnDpCD_73ebtDRMNbEurUT8V0xp0t2POTkY1BygYL-" \
           "ROhbtkllMEwU4-zRqbTlslUyN03VzVYh9EbG62TFqS8ABD78OhR9WhMJ_FSj5vBB-n1Q/v1",
           model="Gemini-2.5-Pro",
           max_tokens=10000,
           temperature=0.8,
           )
        ms = [
            SystemMessage(
                content="You are a helpful assistant, your name is paul"
                ),
                HumanMessage(
                    content=message
                    )
            ]
        rp = llm.invoke(ms)
        return rp.content
    except:
        return "not response"
    

load_dotenv()

client = OpenAI(
  api_key=os.getenv('API_KEY'),
  base_url= os.getenv('BASE_URL')
)

response = client.chat.completions.create(
    model=os.getenv('MODEL'),
    messages=[
        {"role": "user", "content": "Tell me a joke about developers."}
    ],
    temperature=0.9,      # Controls creativity
    max_tokens=400,     # Limits the length of the response
)

print(response.choices[0].message.content)

