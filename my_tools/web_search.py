from langchain_core.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults


class WebSearch:
    """
    一个用于封装 Tavily 搜索引擎的工具类。
    """

    def __init__(self, api_key: str, max_results: int = 2):
        """
        初始化 WebSearch。

        :param max_results: 搜索结果的最大数量，默认为 2。
        """
        self.max_results = max_results
        self.api_key = api_key
        self.search = TavilySearchResults(tavily_api_key=self.api_key, max_results=self.max_results)

    def search_web(self, query: str):
        """
        使用 Tavily 搜索引擎进行互联网搜索。

        :param query: 用户的搜索查询。
        :return: 搜索结果。
        """
        try:
            results = self.search.invoke(query)
            return results
        except Exception as e:
            return f"Error during web search: {str(e)}"

    def get_tools(self):
        """
        获取与 WebSearch 相关的工具列表。

        :return: 工具列表。
        """
        tools = [
            Tool(
                name="WebSearch",
                func=self.search_web,
                description="使用 Tavily 搜索引擎查询互联网上的相关信息。",
            )
        ]

        print('WebSearch 工具构造正常')
        return tools
