
# Set up the project

import os
import logging
from AgentUtilizationAnalysisPlugin import AgentUtilizationAnalysisPlugin
from BuildConfigAnalysisPlugin import BuildConfigAnalysisPlugin
from BuildPerformanceAnalysisPlugin import BuildPerformanceAnalysisPlugin
from ProjectSummaryPlugin import ProjectSummaryPlugin
from teamcity_api import *

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

# Set up the project
api = TeamCityApi(
    os.getenv("TEAMCITY_URL"),
    os.getenv("TEAMCITY_USERNAME"),
    os.getenv("TEAMCITY_PASSWORD")
)

PROJECT_ID = os.getenv('PROJECT_ID')

plugins = [
    ProjectSummaryPlugin(PROJECT_ID),
    # BuildConfigAnalysisPlugin(PROJECT_ID),
    # BuildPerformanceAnalysisPlugin(PROJECT_ID),
    AgentUtilizationAnalysisPlugin()
]

for plugin in plugins:
    data = plugin.collect_data(api)
    findings = plugin.analyze_data(data)
    summary = plugin.document_findings(findings)
    with open("analysis.md", "wt", newline=os.linesep) as file:
        file.write(summary)
