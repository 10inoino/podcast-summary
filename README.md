# What is this?

- Podcast の音声を読み込んで、要約するプログラムです。

# 準備

- ルートディレクトリに、`set_api_key_to_env.sh`という名前で、以下のようなファイルを作成してください。[api_key]には OpenAI の API キーが入ります

```sh
export OPENAI_API_KEY="[api_key]"
```

# 使い方

Podcast の音声データを、ルートディレクトリに配置し、以下のコマンドで実行できます。

```sh
python3 main.py [音声ファイル名]
```

# その他

- 音声データが長すぎると、GPT-3.5-turbo のトークンの上限に引っかかり、要約ができないことがあります。
- `prompt.txt`を書き換えると、Podcast の要約以外にも使えます。

# 参考資料

- https://platform.openai.com/docs/api-reference
- https://dev.classmethod.jp/articles/openai-api-whisper-about-data-limit/
- https://dev.classmethod.jp/articles/openai-api-chatgpt-tiktoken/
- https://blog.since2020.jp/ai/chatgpt_api_role/
- https://dev.classmethod.jp/articles/release-openai-apis-chatgpt-and-whisper/
