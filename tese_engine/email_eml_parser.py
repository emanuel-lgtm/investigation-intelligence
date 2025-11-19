"""
TESE V8 - EML Email Parser
Entry 4: .eml email file parser

Parses individual email files in EML format.
"""

import email
from email import policy
from datetime import datetime
from typing import List, Dict


class EmailEMLParser:
    """
    Basic parser for .eml email files.
    """

    def parse(self, content: str) -> List[Dict]:
        """
        Parse EML email file.
        
        Args:
            content: EML file content
            
        Returns:
            List with single message dictionary
        """
        msg = email.message_from_string(content, policy=policy.default)

        ts = None
        if msg.get("Date"):
            try:
                ts = datetime.strptime(msg.get("Date"), "%a, %d %b %Y %H:%M:%S %z")
            except:
                ts = None

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body += part.get_content()
                    except:
                        pass
        else:
            if msg.get_content_type() == "text/plain":
                body = msg.get_content()

        return [{
            "timestamp": ts,
            "sender": msg.get("From", "unknown"),
            "subject": msg.get("Subject", ""),
            "content": body.strip(),
            "platform": "email"
        }]
