#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
单文件 + 容错版：转不了的 LaTeX 就跳过，只删 $$ 定界符
"""
import os
import re
import traceback
from pathlib import Path
import win32com.client as win32

TARGET_FILE = r"D:/18-李健成-3班.docx"   # ← 你的文件

app = win32.Dispatch("KWPS.Application")
app.Visible = False
app.DisplayAlerts = False

def latex_to_omml(latex: str) -> str:
    """返回空串表示转换失败"""
    try:
        tmp = app.Documents.Add()
        eq = tmp.OMaths.Add(tmp.Range())
        eq.Range.Text = latex
        eq.BuildUp()
        omml = eq.Range.WordOpenXML
        tmp.Close(SaveChanges=False)
        return omml
    except Exception:
        return ""

def process_one_doc(path: Path):
    doc = app.Documents.Open(str(path))
    rng = doc.Content
    pat = re.compile(r"\$\$(.*?)\$\$", re.S)
    match = pat.search(rng.Text)
    while match:
        latex = match.group(1).strip()
        omml = latex_to_omml(latex)
        start = rng.Start + match.start()
        end   = rng.Start + match.end()
        hit_range = doc.Range(start, end)

        if omml:                                    # 成功 → 插公式
            hit_range.Text = ""
            doc.Range(start, start).InsertXML(omml)
            print(f"[公式化]  {latex}")
        else:                                       # 失败 → 只删$$
            hit_range.Text = latex
            print(f"[跳过]    {latex}  （非法 LaTeX）")

        rng = doc.Content
        match = pat.search(rng.Text)

    new_name = path.with_name(path.stem + "_wpsFormula.docx")
    doc.SaveAs(str(new_name))
    doc.Close()
    print(f"已生成 → {new_name}")

def main():
    try:
        process_one_doc(Path(TARGET_FILE))
    except Exception as e:
        print("出错：", e)
        traceback.print_exc()
    finally:
        app.Quit()

if __name__ == "__main__":
    main()