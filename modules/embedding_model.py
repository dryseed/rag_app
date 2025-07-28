from langchain_huggingface import HuggingFaceEmbeddings

# 使用支持日语的多语言Embedding模型
def get_embedding():
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large",
        model_kwargs={"device": "cpu"}  # 有 GPU 可改为 "cuda"
    )
