import re
from typing import List, Dict, Optional, Pattern

class DiffAnalyzer:
    def __init__(self):
        self._patterns: Dict[str, Pattern] = {}
        self._default_patterns = {
            'secret': r'(?i)(api[_-]?key|secret|password|token|credentials).*[\'"=]\\s*[a-zA-Z0-9+/=]{8,}',
            'pii': r'(?i)(ssn|social security|credit card|passport)\\s*[:\\s][^\
]{4,}',
            'ip_addr': r'\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b',
            'aws_key': r'(?i)aws[_-]?(secret|key|token)[_-]?(access)?[\'"=]\\s*[A-Za-z0-9/+=]{20,}',
        }
        self.load_default_patterns()

    def load_default_patterns(self) -> None:
        """Load the default security patterns for analysis"""
        for name, pattern in self._default_patterns.items():
            self.add_pattern(name, pattern)

    def add_pattern(self, name: str, pattern: str) -> None:
        """Add a new pattern for detection
        
        Args:
            name: Identifier for the pattern
            pattern: Regular expression pattern string
        """
        try:
            self._patterns[name] = re.compile(pattern)
        except re.error as e:
            raise ValueError(f'Invalid regex pattern for {name}: {e}')

    def analyze_diff(self, diff_content: str) -> List[Dict]:
        """Analyze a diff content for sensitive patterns
        
        Args:
            diff_content: The git diff content to analyze
            
        Returns:
            List of findings with pattern matches and locations
        """
        findings = []
        lines = diff_content.split('\
')
        
        for line_num, line in enumerate(lines, 1):
            # Only check added lines
            if not line.startswith('+'):
                continue
                
            content = line[1:]  # Remove the '+' prefix
            
            for pattern_name, pattern in self._patterns.items():
                matches = pattern.finditer(content)
                
                for match in matches:
                    findings.append({
                        'pattern': pattern_name,
                        'line': line_num,
                        'match': match.group(),
                        'start': match.start(),
                        'end': match.end()
                    })
        
        return findings

    def get_pattern_names(self) -> List[str]:
        """Get list of currently loaded pattern names"""
        return list(self._patterns.keys())

    def remove_pattern(self, name: str) -> bool:
        """Remove a pattern from the analyzer
        
        Args:
            name: Pattern identifier to remove
            
        Returns:
            True if pattern was removed, False if not found
        """
        return bool(self._patterns.pop(name, None))
