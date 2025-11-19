"""
TESE V8 - Skype Parser
Entry 3: Skype conversation log parser

Supports JSON-structured exports and TXT fallback.
"""

import json
from datetime import datetime
from typing import List, Dict


class SkypeParser:
    """
    Basic parser for Skype exported conversation files.
    Supports JSON-structured exports and TXT fallback.
    """

    def parse(self, content: str) -> List[Dict]:
        """
        Parse Skype export (JSON or TXT).
        
        Args:
            content: Skype export content
            
        Returns:
            List of message dictionaries
        """
        try:
            data = json.loads(content)
            return self._parse_json(data)
        except:
            return self._parse_txt(content)

    def _parse_json(self, data: Dict) -> List[Dict]:
        """Parse JSON-formatted Skype export."""
        messages = []
        for msg in data.get("messages", []):
            ts = None
            if "originalarrivaltime" in msg:
                try:
                    ts = datetime.fromisoformat(msg["originalarrivaltime"])
                except:
                    ts = None
            messages.append({
                "timestamp": ts,
                "sender": msg.get("from", "unknown"),
                "content": msg.get("content", ""),
                "platform": "skype"
            })
        return messages

    def _parse_txt(self, text: str) -> List[Dict]:
        """Parse TXT-formatted Skype export."""
        messages = []
        for line in text.splitlines():
            if ":" in line:
                try:
                    ts_str, rest = line.split("] ", 1)
                    ts_str = ts_str.replace("[", "")
                    ts = datetime.fromisoformat(ts_str)
                    sender, content = rest.split(": ", 1)
                except:
                    continue
                messages.append({
                    "timestamp": ts,
                    "sender": sender,
                    "content": content,
                    "platform": "skype"
                })
        return messages
