from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI


class ChatAgent:
    """
    一个用于处理用户聊天的agent，专注于旅游和地理相关话题。
    """

    def __init__(self, tools, api_key=None, base_url=None, temperature=0.6):
        """
        初始化 ChatAgent。

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

        # 初始化工具列表
        self.tools = tools

        # 定义对话模板
        self.chat_prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.SYSTEM_TEMPLATE),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            HumanMessagePromptTemplate.from_template("{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True)
        ])

        # 初始化 Agent
        self.agent = create_tool_calling_agent(self.llm, tools, self.chat_prompt_template)

        # 初始化 AgentExecutor
        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools)

    SYSTEM_TEMPLATE = """
    你是林梓阳创造的旅游问答机器人，你要使用工具从web搜索用户的问题，并根据工具返回回答用户信息，你只回答用户关于旅游和地理方面的问题。
    你可以在对话结束时提一个和用户聊天内容相关的话题，引导用户继续和你聊天。
    如果用户的问题中没有出现地名或者没有出现如下词语则可以判定为与旅游无关：
    ‘玩、旅游、好看、有趣、风景、美食、价格、住宿、酒店、贵、便宜、文化、习俗、消费’
    
    你有如下工具可以使用：
    {tools}
    
    要使用工具包，你必须按照如下格式进行思考和输出:
    ```
    Thought: Do I need to use a tool?YES
    Action: the action to take, should be one of {tool_names}
    Action Input: the input to the action,should be a string
    Observation: the result of the action
    ```

    案例：
    1. 用户问题：今天天气如何？ 你的回答：抱歉，我只负责回答和旅游、地理相关的问题。
    2. 用户问题：你是谁？你的回答：我是林梓阳创造的旅游问答机器人，我只负责回答和旅游、地理相关的问题。
    3. 用户问题：今天股市表现如何？你的回答：抱歉我只负责回答和旅游、地理相关的问题
    """

    def generate_ai_response(self, chat_history: list, user_input: str) -> str:
        """
        根据聊天记录和用户问题生成回复。

        :param chat_history: 聊天记录列表，包含过去的对话内容。
                             格式示例：
                             [
                                 {"role": "user", "content": "北京有哪些好玩的地方？"},
                                 {"role": "AI", "content": "北京有很多著名景点，比如故宫、天安门广场、颐和园等。"}
                             ]
        :param user_input: 用户的当前问题。
        :return: 生成的回答字符串。
        """
        # 构造输入
        inputs = {
            "tools": "\n".join([f"{i + 1}. {tool.name}: {tool.description}" for i, tool in enumerate(self.tools)]),
            "tool_names": ", ".join([tool.name for tool in self.tools]),
            "chat_history": chat_history,
            "input": user_input,
            "agent_scratchpad": []
        }

        # 调用 Agent 并获取响应
        response = self.agent_executor.invoke(inputs)

        return str(response['output'])
