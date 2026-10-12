# W4 命令行学科问答机器人（API 版）
# 依赖: pip install openai python-dotenv
# 运行: python week4_api_bot.py "把字句的教学难点有哪些"

import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# 加载.env
load_dotenv()

BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
MODEL = "doubao-seed-2-1-pro-260915"

_client = None

def get_client():
    """按需创建客户端: 这样"没配密钥"能在 __main__ 里被友好提示,
    而不是在 import 阶段就抛出看不懂的 OpenAIError。"""
    global _client
    if _client is None:
        key = os.getenv("ARK_API_KEY")
        if not key:
            raise RuntimeError("未配置 ARK_API_KEY")
        _client = OpenAI(base_url=BASE_URL, api_key=key)
    return _client

def ask(question, temperature=0.7, max_tokens=800):
    r = get_client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return r.choices[0].message.content

if __name__ == "__main__":
    if not os.getenv("ARK_API_KEY"):
        print("错误: 未设置 ARK_API_KEY。")
        print(" 处理: 在.env填入ARK_API_KEY密钥，重启终端后重试。")
        sys.exit(1)

    # 从命令行取问题，没有传参就默认问题
    q = " ".join(sys.argv[1:]) or "把字句的教学难点有哪些"
    try:
        ans = ask(q)
    except Exception:
        print("错误: 请求超时，请检查网络。")
        sys.exit(1)
    print(ans)

    # 追加写入日志 chat_log.txt
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"Q: {q}\nA: {ans}\n\n")