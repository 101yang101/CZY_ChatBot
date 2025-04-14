from langchain_core.tools import Tool
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

class KnowledgeBase:
    """
    一个用于构建和管理产品知识库的类。
    """

    def __init__(self, filepath: str, api_key=None, chunk_size: int = 100, chunk_overlap: int = 10):
        """
        初始化知识库。

        :param filepath: 知识库文件路径。
        :param chunk_size: 文本分割的块大小，默认为 100。
        :param chunk_overlap: 文本分割的重叠部分大小，默认为 10。
        """
        self.filepath = filepath
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.api_key = api_key
        self.vectorstore = self._build_knowledge_base()
        self.retriever = self.get_retriever()

    def _build_knowledge_base(self):
        """
        构建知识库。

        :return: 一个向量存储实例（Chroma）。
        """
        # 读取文件内容
        loader = TextLoader("state_of_the_union.txt")
        documents = loader.load()

        # 分割文本
        text_splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        texts = text_splitter.split_documents(documents)

        # 初始化嵌入模型
        embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

        # 创建向量存储
        vectorstore = FAISS.from_documents(texts, embeddings)

        return vectorstore

    def get_retriever(self):
        """
        获取检索器。

        :return: 检索器实例。
        """
        pass
        return self.vectorstore.as_retriever()

    def get_tools(self):
        """
        获取与知识库相关的工具列表。

        :return: 工具列表。
        """

        tools = [
            Tool(
                name="ProductSearch",
                func=self.retriever.get_relevant_documents,
                description="查询产品库，输入应该是'**的旅游产品'",
            )
        ]

        print('tools构造正常')
        return tools
