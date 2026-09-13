"""
Smart Task Router for IELTS by GAMA.
Directs tasks to Local or Cloud providers based on connectivity,
user privacy preferences, and task complexity.
"""

from enum import Enum
from ..sync.connectivity import ConnectivityState


class TaskType(str, Enum):
    GRAMMAR = "grammar"
    VOCABULARY = "vocabulary"
    READING_EVAL = "reading_eval"
    LISTENING_EVAL = "listening_eval"
    WRITING_EVAL = "writing_eval"
    SPEAKING_EVAL = "speaking_eval"
    CONVERSATION = "conversation"
    GENERAL_CHAT = "general_chat"
    DEEP_RESEARCH = "deep_research"


class TaskRouter:
    """Decides optimal AI execution target (local vs cloud)."""

    @classmethod
    def decide_target(
        cls,
        task_type: TaskType,
        connectivity_state: ConnectivityState,
        cloud_ai_enabled: bool = False,
        local_confidence: float = 1.0
    ) -> str:
        """
        Returns 'local' or 'cloud'.
        Strict local-first policy:
        1. If offline -> always 'local'.
        2. If user disabled cloud AI -> always 'local'.
        3. Simple grammar, vocabulary, reading, listening -> always 'local'.
        4. If local confidence is high (>= 0.70) -> 'local'.
        5. Complex writing evaluation or deep research with low local confidence -> 'cloud' if online.
        """
        if connectivity_state not in [ConnectivityState.ONLINE, ConnectivityState.SYNCING]:
            return "local"

        if not cloud_ai_enabled:
            return "local"

        if task_type in [TaskType.GRAMMAR, TaskType.VOCABULARY, TaskType.READING_EVAL, TaskType.LISTENING_EVAL]:
            return "local"

        if local_confidence >= 0.70:
            return "local"

        if task_type in [TaskType.WRITING_EVAL, TaskType.DEEP_RESEARCH]:
            return "cloud"

        return "local"
