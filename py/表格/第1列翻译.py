import pandas as pd
import asyncio
from googletrans import Translator

async def main():
    df = pd.read_excel("springer_nature_link.xlsx")
    translator = Translator()
    col_name = df.columns[0]

    translated_texts = []
    for text in df[col_name]:
        if isinstance(text, str) and text.strip():
            try:
                result = await translator.translate(text, src="en", dest="zh-cn")
                translated_texts.append(result.text)
            except Exception as e:
                print(f"翻译失败：{text}，错误：{e}")
                translated_texts.append(text)
        else:
            translated_texts.append(text)

    df[col_name] = translated_texts
    df.to_excel("translated.xlsx", index=False)
    print("翻译完成，已保存为 translated.xlsx")

asyncio.run(main())
