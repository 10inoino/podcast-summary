import openai
import os
import pathlib
import subprocess
import math
import datetime
import sys
import tiktoken

from pydub import AudioSegment
from tiktoken.core import Encoding

gpt_model = "gpt-3.5-turbo"
maxmum_tokens = 4096
converted_file_dir = "./converted"

os.system('source set_api_key_to_env.sh')
openai.api_key = os.getenv("OPENAI_API_KEY")
original_path = sys.argv[1]
print("Summirize " + original_path)

original_file = pathlib.Path(original_path)
target_path = original_path

TARGET_FILE_SIZE = 25000000

print(f"{original_file.stat().st_size=}")
if original_file.stat().st_size > TARGET_FILE_SIZE:
    print("This file needs to be converted.")
    audio_segment = AudioSegment.from_file(str(original_file))

    audio_length_sec = len(audio_segment)/1000

    target_kbps = int(math.floor(TARGET_FILE_SIZE * 8 /
                                 audio_length_sec / 1000 * 0.95))

    if target_kbps < 8:
        assert f"{target_kbps=} is not supported."

    dt_now = datetime.datetime.now()

    os.mkdir(converted_file_dir)
    converted_file = pathlib.Path(
        converted_file_dir + "/" + dt_now.strftime('%Y%m%d_%H%M%S')).with_suffix(".mp4")

    subprocess.run(["ffmpeg", "-i", str(original_file), "-codec:a", "aac", "-ar",
                    "16000", "-ac", "1", "-b:a", f"{target_kbps}k", str(converted_file)])
    target_path = converted_file

print("Transcribing...")
with open(str(target_path), "rb") as f:
    response = openai.Audio.transcribe(
        "whisper-1", f, prompt="こんにちは。今日は、いいお天気ですね。")
transcription = str(response["text"])
print("======Transcription Result======")
print(transcription)
print("================================")

print("Token Check...")
encoding: Encoding = tiktoken.encoding_for_model(gpt_model)
tokens = encoding.encode(transcription)
tokens_count = len(tokens)
if tokens_count > maxmum_tokens:
    print(
        f"This model's maximum context length is {maxmum_tokens=} tokens. However, your messages resulted in {tokens_count=} tokens. Please shorten the audio.")
    sys.exit(1)
print("Token Check OK")

print("Summary...")
prompt_text = open('./prompt.txt', 'r').read()
complete_prompt = prompt_text.replace("{{transcription}}", transcription)

completion = openai.ChatCompletion.create(
    model=gpt_model,
    messages=[
        {"role": "user", "content": complete_prompt}
    ]
)
print("======Summary Result======")
print(completion["choices"][0]['message']['content'])
print("==========================")
