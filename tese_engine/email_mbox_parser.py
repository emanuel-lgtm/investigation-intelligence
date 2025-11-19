"""
TESE V8 - MBOX Email Parser
Entry 6: .mbox email archive parser

Parses MBOX email archives.
"""

import mailbox
from datetime import datetime
from typing import List, Dict


class EmailMBOXParser:
    """
    Basic parser for .mbox email archives.
    """

    def parse(self, file_path: str) -> List[Dict]:
        """
        Parse MBOX email archive.
        
        Args:
            file_path: Path to MBOX file
            
        Returns:
            List of message dictionaries
        """
        mbox = mailbox.mbox(file_path)
        messages = []
        
        for msg in mbox:
            ts = None
            date_header = msg.get("Date")
            if date_header:
                try:
                    ts = datetime.strptime(date_header, "%a, %d %b %Y %H:%M:%S %z")
                except:
                    ts = None

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body += part.get_payload(decode=True).decode(errors="ignore")
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                except:
                    body = ""

            messages.append({
                "timestamp": ts,
                "sender": msg.get("From", "unknown"),
                "subject": msg.get("Subject", ""),
                "content": body.strip(),
                "platform": "email"
            })
            
        return messages
