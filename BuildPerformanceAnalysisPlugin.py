

from Plugin import Plugin
from teamcity_api import TeamCityApi


class BuildPerformanceAnalysisPlugin(Plugin):
    def __init__(self, build_type_id: str):
        builds = builds["build"] if "build" in builds else []

    def collect_data(self, rest_api: TeamCityApi):
        """Collect data about the builds."""
        builds = rest_api.call_api(f"/app/rest/buildTypes/id:{self.build_type_id}/builds")
        builds = builds["build"] if "build" in builds else []
        
        # Calculate average build time and success rate
        total_time = sum(build["duration"] for build in builds)
        total_builds = len(builds)
        avg_build_time = total_time / total_builds if total_builds else 0

        successful_builds = sum(1 for build in builds if build["status"] == "SUCCESS")
        success_rate = successful_builds / total_builds if total_builds else 0

        return {
            "builds": builds,
            "average_build_time": avg_build_time,
            "average_success_rate": success_rate
        }


    def analyze_data(self, data):
        """Analyze the build data to identify potential bottlenecks."""
        bottlenecks = []

        # Calculate average build time and success rate
        total_time = sum(build["duration"] for build in data["builds"])
        total_builds = len(data["builds"])
        avg_build_time = total_time / total_builds if total_builds else 0

        successful_builds = sum(1 for build in data["builds"] if build["status"] == "SUCCESS")
        success_rate = successful_builds / total_builds if total_builds else 0

        # If the average build time is high, this could be a bottleneck.
        if avg_build_time > data["average_build_time"]:
            bottlenecks.append("Slow average build time")

        # If the success rate is low, this could be a bottleneck.
        if success_rate < data["average_success_rate"]:
            bottlenecks.append("Low success rate")

        return bottlenecks

    def document_findings(self, findings):
        """Document the findings in a markdown format."""
        markdown = f"# Build Performance Analysis for {self.build_type_id}\n"
        markdown += "## Bottlenecks\n"
        markdown += "\n".join(findings)
        return markdown
