from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


class WelcomeAgent:
    """
    一个用于生成旅游问答机器人欢迎词的agent
    """

    def __init__(self, api_key=None, base_url=None, temperature=0.6):
        """
        初始化 WelcomeAgent。

        :param api_key: OpenAI API 密钥。
        :param base_url: OpenAI API 的基础 URL。
        :param temperature: 控制生成文本的随机性，默认为 0.6。
        """
        # 初始化 OpenAI 配置
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature

        # 初始化 OpenAI 模型
        self.llm = ChatOpenAI(
            temperature=self.temperature,
            api_key=self.api_key,
            base_url=self.base_url
        )

        # 定义欢迎词模板
        # 定义欢迎词模板
        self.chat_prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])

        # 字符串输出解析器，格式化数据，
        output_parser = StrOutputParser()

        # 创建 LLMChain
        self.chain = self.chat_prompt_template | self.llm | output_parser

    SYSTEM_TEMPLATE = """
    你是一个旅游问答机器人的欢迎词生成机器人，你负责生成一句{input}，并提出一个引发话题的问题。
    你的回答可以使用不同的语言风格，可以幽默、可以干练、可以充满想象。
    你不必介绍你是由谁创造的，你的回答请参考以下案例：

    1. 你的回答：你好呀，我们聊点旅游相关的话题吧，你对哪儿感兴趣？
    2. 你的回答：嘻嘻，欢迎来到旅游爱好者天堂，你喜欢旅游么？
    3. 你的回答：终于等到你了，你去哪儿了呀？快告诉我你想去哪儿旅游？

    你的回答：
    """

    def generate_welcome_message(self, input_text="简短的欢迎词") -> str:
        """
        生成欢迎词。

        :param input_text: 输入提示，默认为 "简短的欢迎词"。
        :return: 生成的欢迎词字符串。
        """
        # 调用 LLMChain 生成欢迎词
        response = self.chain.invoke({"input": input_text})
        return response
