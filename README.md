# 🤖AI旅游聊天机器人

本项目是一个基于LangChain构建的多Agent系统，结合Streamlit实现的Web界面，能够根据用户输入进行网络搜索并提供旅游相关的聊天服务。此外，该系统还具备基于本地知识库的推销功能，为用户提供个性化的旅游产品推荐。

## 项目介绍

本项目旨在开发一个旅游聊天机器人，能够与用户进行自然语言交互，提供旅游相关的信息和建议，并具备基于本地知识库的推销功能。通过LangChain搭建的多Agent系统，机器人可以根据用户的输入智能地选择不同的Agent进行响应，从而实现更加丰富和灵活的对话体验。同时，使用Streamlit编写的Web界面使得用户可以方便地与机器人进行交互。

## 功能特点

- **多Agent系统**：包含WelcomeAgent、RouteAgent、ChatAgent和SalesAgent等多个Agent，能够根据用户的输入智能地选择合适的Agent进行响应。
- **旅游信息推荐**：能够为用户提供旅游景点、路线规划等相关信息。
- **基于本地知识库的推销功能**：通过本地知识库实现旅游产品的推销功能，向用户推荐相关的旅游产品和服务。知识库中存储了旅游产品的详细信息，SalesAgent可以根据用户的兴趣和需求，从知识库中提取相关信息并生成个性化的推销文案。
- **网络搜索功能**：新增加了基于[Tavily搜索引擎](https://tavily.com/)的WebSearch工具，允许Agent进行互联网搜索，为用户提供最新、最准确的信息。
- **友好的Web界面**：使用Streamlit编写的Web界面，用户可以方便地与机器人进行交互，查看聊天记录等。

## 安装指南

### 环境依赖

- Python 3.8+
- Streamlit
- LangChain
- OpenAI API
- Tavily Search API

### 安装步骤

1. 克隆项目：
   ```bash
   git clone [项目地址]
   ```
2. 进入项目目录：
   ```bash
   cd chatbot
   ```

3. 安装依赖：
   ```bash
   poetry install
   ```
   
4. 设置 OpenAI API 密钥、Tacily API 密钥和基础URL：
- 将main.py中的 OPENAI_API_KEY 替换为你的 OpenAI API 密钥。
- 将main.py中的 TAVILY_API_KEY 替换为你的 Tavily API 密钥。
- 如果需要，也可以修改OPENAI_BASE_URL为你使用的OpenAI API的基础URL。

5. 设置产品信息文件路径：
- 将旅游产品的信息存储在本地文件中，例如product_information/product.txt。
- 确保YOUR_FILEPATH指向正确的知识库文件路径。

## 使用方法
- 在项目根目录下，在 cmd 中运行以下命令：
   ```bash
   streamlit run main.py
   ```

## 项目结构
```commandline
chatbot/
├── agents/
│   ├── init.py
│   ├── chat_agent.py
│   ├── route_agent.py
│   ├── sales_agent.py
│   └── welcome_agent.py
├── my_tools/
│   ├── init.py
│   ├── knowledge_base.py
│   └── web_search.py
├── product_information/
│   └── protect.txt
├── main.py
└── pythonproject.toml
```
- **agents**：包含各个Agent的实现代码，如WelcomeAgent、RouteAgent、ChatAgent和SalesAgent。
- **my_tools**：包含自定义工具的代码，如KnowledgeBase，用于管理本地知识库。
- **main.py**：项目的主入口文件，负责启动Web应用程序和初始化各个Agent。
- **product_information**: 包含旅游产品信息文件。
- **pythonproject.toml**：项目的配置文件。

## 技术栈
- **Python**：主要编程语言。
- **Streamlit**：用于创建交互式Web界面。
- **LangChain**：用于搭建多Agent系统。
- **OpenAI API**：提供自然语言处理和生成的能力。
- **Tavily Search API**：提供网络搜索功能。
- **本地知识库**：存储旅游产品信息，用于推销功能。

## 参考
在开发本项目的过程中，我参考了以下项目和资源，它们为我提供了宝贵的思路和代码示例：
- **[LangChain官方文档](https://www.langchain.com.cn/docs/how_to/)**：提供了LangChain框架的详细使用方法和示例代码。
- **[Streamlit官方文档](https://docs.streamlit.io/get-started)**：帮助我快速上手Streamlit，创建交互式Web界面。
- **[OpenAI API文档](https://www.openaidoc.com.cn/docs/introduction)**：提供了OpenAI API的详细信息和使用示例。
- **[langchain_chatbot](https://github.com/jerry1900/langchain_chatbot)**：这个项目在某些功能实现上给了我很大的启发。

## 联系方式
- 邮箱：yang189256@163.com

## 学习感悟
这是学习完 langchain 后写的一个练手项目，搭建了一个基于LangChain的多Agent系统，并利用Streamlit创建Web界面。
这个项目存在的一些问题：
- 由于没有采用流式调用技术，用户往往需要等待较长时间才能得到回应。
- LangChain提供了处理多Agent协作的有效工具——LangGraph框架，但我并没有使用。
- 没有做错误处理代码。<br>

LangChain框架有很多优点，如丰富的工具和组件、易于集成等。但是，LangChain的接口设计相对混乱，每次版本更新都会让一些接口被删除或合并到其他包中。这种变化不利于开发。另外，LangChain的高度抽象和过度封装也增加学习成本。

我认为的LangChain学习路线：先看[B站上的视频教程](https://www.bilibili.com/video/BV1E94y187YX/?share_source=copy_web&vd_source=c14e27255774df8dc181dbb7ab0e9a78)理解LangChain的基本思想和组件用法（不用太过纠结视频中的代码，因为由于LangChain版本的不同，视频中的代码在实际运行中可能也会发生错误）具体开发时参考官方文档即可。

LangChain对OpenAI API适配性最好，其他模型（如通义）等适配不太好，使用起来会有各种奇奇怪怪的Bug，建议开发时直接使用OpenAI API。
