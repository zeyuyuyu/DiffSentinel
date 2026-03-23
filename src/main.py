import os
from typing import List, Dict
from pathlib import Path
import git
import yaml
from transformers import Pipeline
from .analyzers import SecurityAnalyzer, ArchitectureAnalyzer, PerformanceAnalyzer

class DiffSentinel:
    def __init__(self, config_path: str = 'diffsentinel.yml'):
        self.config = self._load_config(config_path)
        self.repo = git.Repo(os.getcwd())
        self.analyzers = self._initialize_analyzers()

    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _initialize_analyzers(self) -> List:
        analyzers = []
        if self.config['analyze'].get('security'):
            analyzers.append(SecurityAnalyzer())
        if self.config['analyze'].get('architecture'):
            analyzers.append(ArchitectureAnalyzer())
        if self.config['analyze'].get('performance'):
            analyzers.append(PerformanceAnalyzer())
        return analyzers

    def analyze_diff(self, commit_range: str) -> Dict:
        diff = self.repo.git.diff(commit_range)
        results = {}
        for analyzer in self.analyzers:
            results[analyzer.name] = analyzer.analyze(diff)
        return results

def main():
    sentinel = DiffSentinel()
    results = sentinel.analyze_diff('HEAD~1')
    print(results)

if __name__ == '__main__':
    main()