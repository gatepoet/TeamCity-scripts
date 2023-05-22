from Plugin import Plugin
from teamcity_api import TeamCityApi


class BuildConfigAnalysisPlugin(Plugin):
    def __init__(self, root_project_id: str):
        self.root_project_id = root_project_id

    def collect_data(self, rest_api):
        """Collect data about the build configuration."""
        build_config = rest_api.call_api(f"/app/rest/buildTypes/id:{self.build_type_id}")
        triggers = rest_api.call_api(f"/app/rest/buildTypes/id:{self.build_type_id}/triggers")
        dependencies = rest_api.call_api(f"/app/rest/buildTypes/id:{self.build_type_id}/snapshot-dependencies")
        return {
            "build_config": build_config,
            "triggers": triggers["trigger"] if "trigger" in triggers else [],
            "dependencies": dependencies["dependency"] if "dependency" in dependencies else []
        }

    def analyze_data(self, data):
        """Analyze the build configuration data to identify potential bottlenecks."""
        bottlenecks = []

        # If the build configuration has a large number of triggers, this could be a bottleneck.
        if len(data["triggers"]) > self.avg_triggers:
            bottlenecks.append("High number of triggers")

        # If the build configuration has a large number of dependencies, this could be a bottleneck.
        if len(data["dependencies"]) > self.avg_dependencies:
            bottlenecks.append("High number of dependencies")

        return bottlenecks

    def document_findings(self, findings):
        """Document the findings in a markdown format."""
        markdown = f"# Build Configuration Analysis for {self.build_type_id}\n"
        markdown += "## Bottlenecks\n"
        markdown += "\n".join(findings)
        return markdown
