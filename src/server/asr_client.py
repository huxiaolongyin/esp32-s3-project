import os

import dashscope


# 16kHz 单声道音频识别示例
def transcribe_asr(audio_file_path: str):
    messages = [
        {
            "role": "system",
            "content": [
                # 此处用于配置定制化识别的Context
                {"text": ""},
            ],
        },
        {
            "role": "user",
            "content": [
                {"audio": audio_file_path},
            ],
        },
    ]
    response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY", "sk-09986c3ceb3842569f0b22cb158f34f2"),
        model="qwen3-asr-flash",
        messages=messages,
        result_format="message",
        asr_options={
            # "language": "zh", # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
            "enable_lid": True,
            "enable_itn": False,
        },
    )
    if response.status_code == 200:  # type:ignore
        return (
            response.output.choices[0].message.content[0].get("text", "")  # type:ignore
        )
    else:
        return "语音识别错误"


if __name__ == "__main__":
    result = transcribe_asr(
        r"C:\Users\Administrator\code\esp32-s3-project\src\server\welcome.mp3"  # 绝对地址
    )
    print(result)
