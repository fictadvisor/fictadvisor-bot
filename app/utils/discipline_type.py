from app.enums.discipline_types import DisciplineTypes

discipline_types = {
    DisciplineTypes.PRACTICE: "🟠",
    DisciplineTypes.LECTURE: "🔵",
    DisciplineTypes.LABORATORY: "🟢",
    DisciplineTypes.EXAM: "🟣",
    DisciplineTypes.CONSULTATION: "🟣",
    DisciplineTypes.WORKOUT: "🟣",
    DisciplineTypes.OTHER: "🟤"
}

discipline_types_ua_names = {
    DisciplineTypes.PRACTICE: "ПРАКТИКА",
    DisciplineTypes.LECTURE: "ЛЕКЦІЯ",
    DisciplineTypes.LABORATORY: "ЛАБОРАТОРНА",
    DisciplineTypes.EXAM: "ЕКЗАМЕН",
    DisciplineTypes.CONSULTATION: "КОНСУЛЬТАЦІЯ",
    DisciplineTypes.WORKOUT: "ВІДПРАЦЮВАННЯ",
    DisciplineTypes.OTHER: "ІНШЕ"
}


def get_discipline_type_color(discipline_type: DisciplineTypes) -> str:
    return discipline_types.get(discipline_type, "🟤")

def get_discipline_type_ua_name(discipline_type: DisciplineTypes) -> str:
    return discipline_types_ua_names.get(discipline_type, "ІНШЕ")
