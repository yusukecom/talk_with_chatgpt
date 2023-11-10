# talk_with_chatgpt

このプロジェクトは、音声を録音し、それをテキストに変換し、そのテキストに基づいて応答を生成し、その応答を音声に変換して再生する、という一連の流れを実現するものです。

## 必要なパッケージ

- keyboard
- os
- tempfile
- numpy
- openai
- sounddevice
- soundfile
- serpapi
- elevenlabs
- langchain
- dotenv

## 環境変数

以下の環境変数を設定する必要があります。

- `OPENAI_API_KEY`: OpenAIのAPIキー
- `SERPAPI_API_KEY`: SerpAPIのAPIキー

## 使用方法

1. まず、スペースキーを押して録音を開始します。
2. 録音が終了すると、録音された音声がテキストに変換されます。
3. そのテキストに基づいて応答が生成され、その応答が音声に変換されて再生されます。

## 注意事項

このプロジェクトはデモンストレーション用であり、実際の使用には適していません。また、音声認識や音声生成の精度は保証されていません。
