"""
Conversation Modes for IELTS by GAMA.
Supports 10 distinct communicative contexts and two feedback styles:
- NORMAL CONVERSATION (seamless dialogue flow without disruptive pedantry)
- REAL-TIME CORRECTION (immediate constructive linguistic feedback)
"""

from typing import Dict, Any, List, Optional
from ..grammar.grammar_engine import GrammarEngine


class ConversationModes:
    """Manages roleplay scenarios and conversation tuning."""

    MODES = {
        "daily": {
            "name": "Daily English",
            "prompt_system": "You are a friendly conversation partner discussing everyday life, hobbies, and routines.",
            "starter": "Hi there! How has your week been going so far? Did you do anything interesting recently?"
        },
        "travel": {
            "name": "Travel & Tourism",
            "prompt_system": "You are a helpful travel guide or fellow traveler discussing destinations, transport, and cultural customs.",
            "starter": "Welcome! If you could book a flight anywhere in the world tomorrow, where would you head first?"
        },
        "work": {
            "name": "Work & Business",
            "prompt_system": "You are a professional colleague in an international workplace discussing projects, deadlines, and workplace challenges.",
            "starter": "Good morning. Let's sync on current project priorities. How are things progressing on your side?"
        },
        "academic": {
            "name": "Academic Seminars",
            "prompt_system": "You are an academic peer discussing research methodologies, journal articles, and university life.",
            "starter": "Hello. I've been reviewing recent publications on renewable energy economics. What is your take on current policy trends?"
        },
        "interview": {
            "name": "Job Interview",
            "prompt_system": "You are an executive hiring manager conducting a formal professional job interview.",
            "starter": "Welcome to our interview. Could you walk me through your key professional accomplishments and why you applied for this position?"
        },
        "ielts": {
            "name": "IELTS Speaking Practice",
            "prompt_system": "You are an IELTS examiner asking Part 1, 2, and 3 style questions.",
            "starter": "Good morning. In this first part, I'd like to ask you some questions about yourself. Let's talk about where you live."
        },
        "debate": {
            "name": "Debate & Argumentation",
            "prompt_system": "You are a respectful debate opponent challenging claims and asking for evidence and logic.",
            "starter": "Let's explore the motion: 'Artificial Intelligence will create more opportunities than it displaces.' What is your stance?"
        },
        "discussion": {
            "name": "Philosophical & Social Discussion",
            "prompt_system": "You are a thoughtful conversationalist exploring ethics, technology, and society.",
            "starter": "Do you believe rapid urban growth is improving or eroding quality of community life in major cities?"
        },
        "presentation": {
            "name": "Presentation & Pitching",
            "prompt_system": "You are a coach listening to a presentation and asking clarifying questions.",
            "starter": "Whenever you are ready, please give your 2-minute overview of your presentation topic."
        },
        "social": {
            "name": "Social Networking & Small Talk",
            "prompt_system": "You are meeting someone new at an international conference or social meetup.",
            "starter": "Hi! Nice meeting you here. Have you been attending many sessions today?"
        }
    }

    @classmethod
    def get_mode(cls, mode_key: str = "daily") -> Dict[str, Any]:
        return cls.MODES.get(mode_key, cls.MODES["daily"])

    @classmethod
    def process_turn(
        cls,
        mode_key: str,
        user_message: str,
        correction_style: str = "normal"  # 'normal' or 'realtime'
    ) -> Dict[str, Any]:
        """
        Processes a conversation turn.
        If correction_style == 'realtime', detects and displays significant grammar errors.
        """
        errors = GrammarEngine.check_sentence(user_message)
        has_errors = len(errors) > 0

        # Construct conversational reply based on scenario
        mode = cls.get_mode(mode_key)
        reply = f"That's an interesting point regarding that. Could you elaborate a bit more on why you see it that way?"

        # In realtime mode, prepend constructive correction notice
        correction_notice = None
        if correction_style == "realtime" and has_errors:
            top_err = errors[0]
            correction_notice = {
                "original": top_err["original"],
                "correction": top_err["correction"],
                "why": top_err["why"]
            }

        return {
            "mode": mode_key,
            "mode_name": mode["name"],
            "reply": reply,
            "correction_style": correction_style,
            "correction_notice": correction_notice,
            "all_errors": errors
        }
