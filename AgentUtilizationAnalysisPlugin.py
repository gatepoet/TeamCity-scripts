

from Plugin import Plugin
from teamcity_api import TeamCityApi

class AgentUtilizationAnalysisPlugin(Plugin):
    def _calculate_averages(self, agents = []):
        """Calculate the average number of enabled and authorized agents."""
        total_agents = len(agents)
        enabled_agents = sum(1 for agent in agents if agent["enabled"])
        authorized_agents = sum(1 for agent in agents if agent["authorized"])
        return enabled_agents / total_agents if total_agents else 0, authorized_agents / total_agents if total_agents else 0

    def collect_data(self, rest_api: TeamCityApi):
        """Collect data about the agents."""
        agents = rest_api.call_api("/app/rest/agents")
        agents = agents["agent"] if "agent" in agents else []
        average_enabled_agents, average_authorized_agents = self.calculate_averages(agents)
        return {
            "agents": agents,
            "average_enabled_agents": average_enabled_agents,
            "average_authorized_agents": average_authorized_agents
        }

    def analyze_data(self, data):
        """Analyze the agent data to identify potential bottlenecks."""
        bottlenecks = []

        # Calculate the number of enabled and authorized agents
        enabled_agents = sum(1 for agent in data["agents"] if agent["enabled"])
        authorized_agents = sum(1 for agent in data["agents"] if agent["authorized"])

        # If the number of enabled or authorized agents is low, this could be a bottleneck.
        if enabled_agents < data["average_enabled_agents"]:
            bottlenecks.append("Low number of enabled agents")
        if authorized_agents < data["avg_authorized_agents"]:
            bottlenecks.append("Low number of authorized agents")

        return bottlenecks

    def document_findings(self, findings):
        """Document the findings in a markdown format."""
        markdown = "# Agent Utilization Analysis\n"
        markdown += "## Bottlenecks\n"
        markdown += "\n".join(findings)
        return markdown
