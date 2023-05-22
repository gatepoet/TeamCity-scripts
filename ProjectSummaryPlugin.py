from Plugin import Plugin
from teamcity_api import TeamCityApi

class ProjectSummaryPlugin(Plugin):
    def __init__(self, root_project_id: str):
        self.root_project_id = root_project_id

    def collect_data(self, rest_api: TeamCityApi):
        self.data = rest_api.get_project(self.root_project_id)
        return self.data

    def analyze_data(self, data=None):
        return self._create_project_model(self.data)

    def _create_project_model(self, project_json):
        return {
            "name": project_json.get("name"),
            "description": project_json.get("description"),
            "buildConfigurations": [self._create_build_configuration_model(bc) for bc in project_json.get("buildTypes", {}).get("buildType", [])],
            "subProjects": [self._create_project_model(sp) for sp in project_json.get("projects", {}).get("project", [])]
        }

    def _create_build_configuration_model(self, build_config_json):
        return {
            "name": build_config_json.get("name"),
            "description": build_config_json.get("description"),
            "triggersSummary": self._create_summary(build_config_json.get("triggers", {}).get("trigger", [])),
            "dependenciesSummary": self._create_summary(build_config_json.get("snapshot-dependencies", {}).get("snapshot-dependency", []))
        }

    def _create_summary(self, items):
        summary = {}
        for item in items:
            type = item.get("type")
            summary[type] = summary.get(type, 0) + 1
        return summary

    def document_findings(self, findings):
        return self._render_project(findings)

    def _render_project(self, findings):
        if findings is None:
            return ""  # Or any appropriate error handling

        return f"h1. {findings['name']}\n" \
            f"{findings['description']}\n" \
            f"h2. Build Configurations\n" \
            f"{self._render_build_configurations(findings['buildConfigurations'])}\n" \
            f"h2. Sub-Projects\n" \
            f"{self._render_sub_projects(findings['subProjects'])}\n"

    def _render_build_configurations(self, build_configurations):
        return "\n".join([self._render_build_configuration(bc) for bc in build_configurations])

    def _render_build_configuration(self, build_configuration):
        return f"h3. {build_configuration['name']}\n" \
            f"{build_configuration['description']}\n" \
            f"*Triggers Summary:*\n" \
            f"{self._render_summary(build_configuration['triggersSummary'])}\n" \
            f"*Dependencies Summary:*\n" \
            f"{self._render_summary(build_configuration['dependenciesSummary'])}\n"

    def _render_sub_projects(self, sub_projects):
        return "\n".join([self._render_project(sp) for sp in sub_projects])

    def _render_summary(self, summary):
        return "\n".join([f"* {type}: {count}" for type, count in summary.items()])
