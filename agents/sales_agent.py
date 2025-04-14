from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor


class SalesAgent:
    """
    一个用于推荐旅游产品的agent，调用知识库工具查询相关产品信息。
    """

    def __init__(self, tools, api_key=None, base_url=None, temperature=0.6):
        """
        初始化 SalesAgent。

        :param tools: 工具列表，用于搜索本地知识库。
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

        # 定义 PromptTemplate
        self.chat_prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template("{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True)
        ])

        # 初始化 Agent
        self.agent = create_tool_calling_agent(self.llm, tools, self.chat_prompt_template)

        # 初始化 AgentExecutor
        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools)

    SYSTEM_TEMPLATE = """
    你是一个旅游产品推荐机器人，你的工作如下：
    1. 你通过查询历史聊天记录用户最近的两次对话内容，判断用户的兴趣点，兴趣点被标记为“兴趣点”。用户最近的两次对话内容，是指聊天记录里最靠近以"用户："开头且在文本位置底部、靠近"***"的内容。
    2. 你要使用工具包查询和用户"兴趣点”相关的产品信息，包括产品名称、产品价格和行程安排。
    3. 当你通过工具获取产品信息后，你要向用户推荐产品，你的推荐介绍可以这样开头：“尊敬的用户，根据和您的聊天，我们向您推荐一款产品...”

    工具包:
    -----
    你有如下工具可以使用：
    {tools}

    要使用工具包，你必须按照如下格式进行思考和输出:
    ```
    Thought: Do I need to use a tool?YES
    Action: the action to take, should be one of {tool_names}
    Action Input: the input to the action,should be a string
    Observation: the result of the action
    ```
    当你已经得到了一个答案，你必须按照如下格式进行输出：
    ```
    Thought: Do I get the answer?YES.
    AI: [your response here, if previously used a tool, rephrase latest observation]
    ```
    当你无法将用户兴趣点和ProductSearch工具中的产品匹配时，你必须按照如下格式进行输出：
    ```
    Thought: Do I get the answer?NO.
    AI: 抱歉，我们暂时没有找到与您的兴趣点相关的产品信息。
    ```

    过去的聊天记录以"==="为标记开始，以”***“为标记结束。
    用户的聊天内容以"用户:"开头，AI的系统回复以"AI:"开头。

    过去的聊天记录：
    ===
    {chat_history}
    ***
    
    """

    def generate_ai_response(self, chat_history: list, user_input: str) -> str:
        """
        根据历史聊天记录生成产品推荐。

        :param chat_history: 聊天记录列表，包含过去的对话内容。
                             格式示例：
                             [
                                 {"role": "user", "content": "北京有哪些好玩的地方？"},
                                 {"role": "AI", "content": "北京有很多著名景点，比如故宫、天安门广场、颐和园等。"}
                             ]
        :param user_input: 用户的当前问题。
        :return: 返回1表示知识库中没有找到相关信息，返回2表示知识库中有相关信息。
        """
        # 将聊天记录转换为字符串
        history_str = "\n".join([
            f"用户: {item['content']}" if item["role"] == "user" else f"AI: {item['content']}"
            for item in chat_history
        ])

        # 构造输入
        inputs = {
            "chat_history": history_str,
            "tools": "\n".join([f"{i+1}. {tool.name}: {tool.description}" for i, tool in enumerate(self.tools)]),
            "tool_names": ", ".join([tool.name for tool in self.tools]),
            "input": user_input,
            "agent_scratchpad": []
        }

        # 调用 Agent 并获取响应
        response = self.agent_executor.invoke(inputs)

        return str(response['output'])
