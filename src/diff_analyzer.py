import re
from typing import Dict, List, Tuple

class DiffAnalyzer:
    def __init__(self):
        self.risk_patterns = {
            'high': [
                r'(?i)(password|secret|token|key)',
                r'(?i)(delete|drop|truncate)\\s+table',
                r'while\\s*\\(true\\)',
            ],
            'medium': [
                r'(?i)(TODO|FIXME|HACK)',
                r'catch\\s*\\(Exception\\s+e\\)',
                r'null\\s*=',
            ],
            'low': [
                r'print\\s*\\(',
                r'console\\.log',
                r'\\#\\s*DEBUG',
            ]
        }
        
        self.impact_weights = {
            'high': 10,
            'medium': 5,
            'low': 2
        }

    def analyze_diff(self, diff_content: str) -> Dict:
        '''
        Analyzes a diff content and returns impact metrics
        '''
        lines = diff_content.split('\
')
        added_lines = [line[1:] for line in lines if line.startswith('+') and not line.startswith('+++')]
        removed_lines = [line[1:] for line in lines if line.startswith('-') and not line.startswith('---')]
        
        impact_score = self._calculate_impact_score(added_lines, removed_lines)
        risk_patterns = self._identify_risk_patterns(added_lines)
        
        return {
            'impact_score': impact_score,
            'risk_patterns': risk_patterns,
            'changes': {
                'additions': len(added_lines),
                'deletions': len(removed_lines),
                'total': len(added_lines) + len(removed_lines)
            }
        }

    def _calculate_impact_score(self, added_lines: List[str], removed_lines: List[str]) -> float:
        '''
        Calculates an impact score based on code changes
        '''
        base_score = len(added_lines) + (len(removed_lines) * 1.2)  # Removals weighted slightly higher
        
        # Analyze complexity of changes
        complexity_factor = self._assess_complexity(added_lines)
        risk_factor = self._assess_risk_patterns(added_lines)
        
        return round(base_score * complexity_factor * risk_factor, 2)

    def _assess_complexity(self, lines: List[str]) -> float:
        '''
        Assesses code complexity based on various factors
        '''
        complexity = 1.0
        
        # Increase complexity for control structures
        control_structures = sum(1 for line in lines if re.search(r'(if|for|while|switch|try)', line))
        complexity += (control_structures * 0.1)
        
        # Increase for nested structures
        indentation_levels = [len(line) - len(line.lstrip()) for line in lines]
        if indentation_levels:
            max_depth = max(indentation_levels) // 4  # Assuming 4 spaces per level
            complexity += (max_depth * 0.15)
            
        return complexity

    def _assess_risk_patterns(self, lines: List[str]) -> float:
        '''
        Assesses risk based on identified patterns
        '''
        risk_factor = 1.0
        
        for severity, patterns in self.risk_patterns.items():
            for pattern in patterns:
                matches = sum(1 for line in lines if re.search(pattern, line))
                if matches:
                    risk_factor += (matches * self.impact_weights[severity] * 0.01)
                    
        return risk_factor

    def _identify_risk_patterns(self, lines: List[str]) -> Dict[str, List[Tuple[str, str]]]:
        '''
        Identifies specific risk patterns in the code
        '''
        findings = {
            'high': [],
            'medium': [],
            'low': []
        }
        
        for severity, patterns in self.risk_patterns.items():
            for pattern in patterns:
                for line in lines:
                    if re.search(pattern, line):
                        findings[severity].append((pattern, line.strip()))
                        
        return findings