from app.enums.discipline_types import DisciplineTypes

discipline_types = {
    DisciplineTypes.PRACTICE: "🟠",
    DisciplineTypes.LECTURE: "🔵",
    DisciplineTypes.LABORATORY: "🟢",
    DisciplineTypes.EXAM: "🟣",
    DisciplineTypes.CONSULTATION: "🟣",
    DisciplineTypes.WORKOUT: "🟣",
    DisciplineTypes.OTHER: "🟣"
}


def get_discipline_type_name(discipline_type: DisciplineTypes) -> str:
    return discipline_types.get(discipline_type, "🟣")
