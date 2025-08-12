from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

def ask_deepseek(system_prompt: str, user_prompt: str, model: str = "deepseek-chat") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            timeout=30  # タイムアウト設定追加
        )

        content = getattr(response.choices[0].message, "content", None)
        if content is not None:
            return content.strip()
        else:
            return "API応答にcontentが含まれていません"
    except TimeoutError:
        return "APIの応答がタイムアウトしました。しばらく経ってから再試行してください。"      
    except Exception as e:
        return f"エラーが発生しました: {e}"

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

def ask_deepseek(system_prompt: str, user_prompt: str, model: str = "deepseek-chat") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            timeout=30  # タイムアウト設定追加
        )

        content = getattr(response.choices[0].message, "content", None)
        if content is not None:
            return content.strip()
        else:
            return "API応答にcontentが含まれていません"
    except TimeoutError:
        return "APIの応答がタイムアウトしました。しばらく経ってから再試行してください。"      
    except Exception as e:
        return f"エラーが発生しました: {e}"

