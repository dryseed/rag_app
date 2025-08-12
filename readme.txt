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


【メモ：ChatGPTでAPI仕様書のMarkdownファイル化】
1，转为 Markdown 格式，进行格式美化（标题、列表、引用、代码块等）
2，完整提取（不漏字段、不省略段落），表格中的数据也需要提取，也不要改变文档的语言。
3，文档中有图片，该图片信息不能读取的话，可以略过。
4，分割成多个markdown格式文件，并提供下载链接。另外, 每个文件根据实际要分成多个层级，做到层次清晰（#，##，###，####）
  01_interface_overview.md ：インターフェース概要
  02_api_payment.md ：支払
  03_api_refund.md ： 返金
  04_api_reverse.md：取消
  05_api_order_query.md ：オーダ照会
  06_api_confirm.md ： 確認
  07_code_definitions.md ：コード定義