from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod
    def collect_data(self):
        """Collects data for analysis."""
        raise NotImplementedError

    @abstractmethod
    def analyze_data(self):
        """Analyzes the collected data."""
        raise NotImplementedError

    @abstractmethod
    def document_findings(self):
        """Documents the findings of the analysis."""
        raise NotImplementedError
