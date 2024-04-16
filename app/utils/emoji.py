from dataclasses import dataclass

@dataclass
class Emoji:

    emoji_numbers = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟"
    }
    CANCEL = "❌"
    EDIT = "✏️"
    SKIP = "⏩"
    SAVE = "💾"
    BACK = "🔙"

    @staticmethod
    def from_number(n: int) -> str:
        return Emoji.emoji_numbers.get(n, str(n))
