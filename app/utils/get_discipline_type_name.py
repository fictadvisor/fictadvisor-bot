from app.enums.discipline_types import DisciplineTypes

discipline_types = {
    DisciplineTypes.PRACTICE: "практика",
    DisciplineTypes.LECTURE: "лекція",
    DisciplineTypes.LABORATORY: "лабораторна"
}


def get_discipline_type_name(discipline_type: DisciplineTypes) -> str:
    return discipline_types[discipline_type]
