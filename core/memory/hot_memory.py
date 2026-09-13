"""
Hot Memory for IELTS by GAMA.
Maintains volatile in-RAM context for the active conversation or task.
Automatically purges when conversation ends or exceeds turn bounds.
Never persists low-value raw conversation dumps directly to disk.
"""

from typing import List, Dict, Any, Optional
import time


class HotMemory:
    """Manages active turn context in RAM with strict size bounds."""

    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.turns: List[Dict[str, Any]] = []
        self.active_task: Optional[Dict[str, Any]] = None
        self.session_metadata: Dict[str, Any] = {
            "started_at": time.time(),
            "skill_in_focus": None
        }

    def add_turn(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        turn = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        self.turns.append(turn)
        if len(self.turns) > self.max_turns * 2:
            # Keep only the latest turns to prevent RAM bloat
            self.turns = self.turns[-(self.max_turns * 2):]

    def set_active_task(self, task_type: str, context: Dict[str, Any]):
        self.active_task = {
            "type": task_type,
            "context": context,
            "updated_at": time.time()
        }

    def clear_task(self):
        self.active_task = None

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        return list(self.turns)

    def summarize_for_retention(self) -> Optional[Dict[str, Any]]:
        """Extracts high-level topic or lesson takeaways before hot memory reset."""
        if not self.turns:
            return None
        return {
            "skill": self.session_metadata.get("skill_in_focus"),
            "turns_count": len(self.turns),
            "timestamp": time.time()
        }

    def clear(self):
        """Discards all hot data from RAM."""
        self.turns.clear()
        self.active_task = None
        self.session_metadata = {"started_at": time.time(), "skill_in_focus": None}
