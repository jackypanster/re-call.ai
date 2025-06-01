import httpx
import logging
from app.config import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.model = settings.preferred_model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"  # 示例，具体以 OpenRouter 文档为准

    async def summarize(self, content: str) -> str:
        prompt = f"请用一句话总结以下内容：{content}"
        try:
            response = await self._call_llm(prompt)
            return response
        except Exception as e:
            logging.error(f"LLM summarize error: {e}")
            raise

    async def extract_tags(self, content: str) -> list:
        prompt = f"请为以下内容提取3-5个关键词或标签，逗号分隔：{content}"
        try:
            response = await self._call_llm(prompt)
            return [tag.strip() for tag in response.split(",")]
        except Exception as e:
            logging.error(f"LLM extract_tags error: {e}")
            raise

    async def _call_llm(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.base_url, json=payload, headers=headers, timeout=30)
            await resp.raise_for_status()
            data = await resp.json()
            return data["choices"][0]["message"]["content"]

# 单例实例
llm_service = LLMService()

def get_llm_service():
    return llm_service
