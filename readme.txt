streamlit run app.py

streamlit run app.py --server.runOnSave false

【テスト実行方法】
1. 依存パッケージをインストール
   pip install -r requirements.txt
2. テスト実行
   pytest

【対応ファイル形式】
- Excelファイル（.xlsx）
- PDFファイル（.pdf）- テキストと画像の説明文を自動抽出

【PDF処理について】
- UnstructuredPDFLoaderを使用してPDFを解析
- 画像内の文字はOCR解析せず、画像の説明文のみを抽出
- テキストと画像の説明文を統一的にナレッジベースに保存