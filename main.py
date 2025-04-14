# 导入 Streamlit 库，用于创建交互式Web应用程序
import streamlit as st
from agents import WelcomeAgent, RouteAgent, ChatAgent, SalesAgent
from my_tools import KnowledgeBase, WebSearch

# 设置OpenAI API密钥
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
# 设置OpenAI API的基础URL
OPENAI_BASE_URL = "https://api.openai.com/v1"
# 设置产品信息文件路径
YOUR_FILEPATH = "product_information/product.txt"
# 设置 Tavily API 密钥
TAVILY_API_KEY = "YOUR_TAVILY_API_KEY"

# 设置Web应用程序的标题
st.title('🤖AI小DOG写的旅游聊天机器人')


# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []


# 创建welcome_agent，并调用其生成初始化欢迎词
if "welcome_message" not in st.session_state:
    # 初始化 WelcomeAgent 类的实例
    welcome_agent = WelcomeAgent(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )

    # 调用 generate_welcome_message 方法生成欢迎词,存入 session_state 中
    st.session_state.welcome_message = welcome_agent.generate_welcome_message("简短的欢迎词")

    # 将欢迎词添加到聊天记录中
    st.session_state.messages.append({'role': 'AI', 'content': st.session_state.welcome_message})


# 建立知识库并获取工具列表
if "kb" not in st.session_state:
    st.session_state.kb = KnowledgeBase(filepath=YOUR_FILEPATH, api_key=OPENAI_API_KEY)
    st.session_state.kb_tools = st.session_state.kb.get_tools()


# 创建 route_agent
if "route_agent" not in st.session_state:
    st.session_state.route_agent = RouteAgent(
            tools=st.session_state.kb_tools,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
    )

# 创建 web_search 工具并获取工具列表
if "ws" not in st.session_state:
    st.session_state.ws = WebSearch(api_key=TAVILY_API_KEY)
    st.session_state.ws_tools = st.session_state.ws.get_tools()

# 创建 chat_agent
if "chat_agent" not in st.session_state:
    st.session_state.chat_agent = ChatAgent(
        tools=st.session_state.ws_tools,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )


# 创建 sales_agent
if "sales_agent" not in st.session_state:
    st.session_state.sales_agent = SalesAgent(
            tools=st.session_state.tools,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
            temperature=0.3
    )


# 展示聊天记录
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar='☺️'):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"], avatar='🤖'):
            st.markdown(message["content"])


# 用户输入
if user_input := st.chat_input('我们来聊一点旅游相关的事儿吧'):

    # 将用户输入展示出来
    with st.chat_message('user', avatar='☺️'):
        st.markdown(user_input)

    # 截取最近几条对话
    chat_history = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages[-4:]
    ]

    # 将用户输入添加到聊天记录中
    st.session_state.messages.append({'role': 'user', 'content': user_input})

    # 调用 route_agent 的 generate_route_result 方法生成路由结果
    result = st.session_state.route_agent.generate_route_result(chat_history, user_input)

    # 根据 RouteAgent 的结果生成调用不同的 AI 回复
    if result == "1":
        # 调用 chat_agent 进行普通聊天
        ai_response = st.session_state.chat_agent.generate_ai_response(chat_history, user_input)
        pass
    elif result == "2":
        # 调用 sales_agent 进行销售聊天
        ai_response = st.session_state.sales_agent.generate_ai_response(chat_history, user_input)
        pass
    else:
        ai_response = st.session_state.chat_agent.generate_ai_response(chat_history, user_input)

    # 将 AI 回复添加到聊天记录中
    st.session_state.messages.append({'role': 'AI', 'content': ai_response})

    # 展示 AI 回复
    with st.chat_message('AI', avatar='🤖'):
        st.markdown(ai_response)
