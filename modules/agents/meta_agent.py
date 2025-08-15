class MetaAgent:
    def __init__(self, agents: dict):
        self.agents = agents
        self.history = []

    def route(self, query: str) -> str:
        # シンプルなルール例（実運用ではLLMや意図解析も可）
        if "API" in query or "仕様書" in query:
            agent_key = "api"         
        else:
            agent_key = "qa"
        result = self.agents[agent_key].search(query)
        self.history.append({"query": query, "agent": agent_key, "result": result})
        return result
    
    def get_history(self) -> list:
        return self.history
    def reset_history(self):
        self.history = []
