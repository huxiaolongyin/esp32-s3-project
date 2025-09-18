from typing import Any, Generator

from openai import OpenAI

# OpenAI API 配置（推荐使用环境变量，避免泄露）


OPENAI_API_KEY = "sk-wedekzslvzzgekpxgqepyrebwklmysvsphdubyffmurjxkjj"
OPENAI_BASE_URL = "https://api.siliconflow.cn/v1"
OPENAI_MODEL = "Qwen/Qwen2.5-32B-Instruct"
llm_client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)


def get_response(query: str) -> Generator[str | None, Any, Any]:
    response = llm_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": query}],
        stream=True,
    )
    for chunk in response:
        yield chunk.choices[0].delta.content


if __name__ == "__main__":
    for part in get_response("介绍一下你自己"):
        print(part, end="", flush=True)
