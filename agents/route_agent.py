from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor


class RouteAgent:
    """
    一个用于路由的agent，调用工具搜索本地知识库，判断调用 ChatAgent 还是 SalesAgent
    """

    def __init__(self, tools, api_key=None, base_url=None, temperature=0.6):
        """
        初始化 RouteAgent。

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
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True)
        ])

        # 初始化 Agent
        self.agent = create_tool_calling_agent(self.llm, tools, self.chat_prompt_template)

        # 初始化 AgentExecutor
        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools)

    SYSTEM_TEMPLATE = """
    你是一个帮助对话聊天机器人确定聊天阶段的推理助理，你的最终回答只能是”1“或者”2“，你的工作如下：
    1. 你通过查询历史聊天记录用户最近的两次对话内容，如果你发现在用户最近的几条聊天内容和用户的问题中，都提到同一个景点、地理位置或旅游项目，则判断其为用户的“兴趣旅游地点”。
    2. 你必须要使用工具包查询和用户"兴趣旅游地点”相关的产品信息，包括产品名称、产品价格和行程安排。如果没有查到相关产品或查到的产品信息不是用户的“兴趣旅游地点”,则输出 1 ，否则输出 2。
    
    过去的聊天记录以"==="为标记开始，以"***"为标记结束。
    用户的聊天内容以"用户:"开头，AI的系统回复以"AI:"开头。
    
    过去的聊天记录：
    ===
    {chat_history}
    user:{input}
    ***
    
    你有如下工具可以使用：
    {tools}
    
    要使用工具包，你必须按照如下格式进行思考和输出:
    ```
    Thought: Do I need to use a tool?YES
    Action: the action to take, should be one of {tool_names}
    Action Input: the input to the action,should be a string
    Observation: the result of the action
    ```

    当你无法将用户兴趣点和ProductSearch工具中的产品匹配时，你必须按照如下格式进行输出：
    AI: 1
    
    当你能够将用户兴趣点和ProductSearch工具中的产品匹配时，你必须按照如下格式进行输出：
    AI: 2
    
    你的回答只能是两种数字的一种，不要有其他文字描述!!!
    你的回答只能是两种数字的一种，不要有其他文字描述!!!
    """

    def generate_route_result(self, chat_history: list, user_input: str) -> str:
        """
        根据历史聊天记录决定调用哪个Agent。

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
