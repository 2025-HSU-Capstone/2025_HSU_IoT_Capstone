import platform
import os
import sys
platform.node = lambda: "safe-host"

api_key = os.getenv("OPENAI_API_KEY")
print("✅ API Key Raw:", repr(api_key))  # ← 주석이 남아 있는지 눈으로 확인

for key in [
    "COMPUTERNAME",
    "HOSTNAME",
    "LOGONSERVER",
    "USERDOMAIN",
    "USERDOMAIN_ROAMINGPROFILE",
    "ONEDRIVE",
    "ONEDRIVECOMMERCIAL"
]:
    os.environ.pop(key, None)

from openai import OpenAI
from dotenv import load_dotenv

def detect_non_ascii(name, value):
    try:
        value.encode("ascii")
    except UnicodeEncodeError:
        print(f"⚠️ 비ASCII 헤더 의심 → {name}: {value}")

# 기본 시스템 값 검사
detect_non_ascii("platform.node()", platform.node())
detect_non_ascii("os.getcwd()", os.getcwd())
detect_non_ascii("sys.getdefaultencoding()", sys.getdefaultencoding())

# 환경변수 검사
for k, v in os.environ.items():
    detect_non_ascii(f"os.environ['{k}']", v)

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY가 .env에 설정되어 있지 않습니다.")

client = OpenAI(
    api_key=api_key,
     default_headers={
        "User-Agent": "smartparm-client/1.0",  # ASCII-only
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "테스트"},
        {"role": "user", "content": "안녕"}
    ]
)

print("✅ 응답:", response.choices[0].message.content)

# import platform
# import os

# print("platform.node():", platform.node())
# print("os.getcwd():", os.getcwd())
