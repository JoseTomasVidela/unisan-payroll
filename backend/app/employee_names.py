from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class PersonnelName:
    raw_name: str
    paternal_surname: str
    maternal_surname: str
    given_names: tuple[str, ...]

    @property
    def display_name(self) -> str:
        if self.given_names and self.paternal_surname:
            return f"{self.given_names[0]} {self.paternal_surname}"
        return self.raw_name

    @property
    def full_name(self) -> str:
        if not self.given_names:
            return self.raw_name
        surnames = [part for part in (self.paternal_surname, self.maternal_surname) if part]
        return " ".join([*self.given_names, *surnames]).strip() or self.raw_name

    @property
    def aliases(self) -> set[str]:
        values = {
            normalize_employee_name(self.raw_name),
            normalize_employee_name(self.display_name),
            normalize_employee_name(self.full_name),
        }
        if len(self.given_names) >= 2 and self.paternal_surname:
            values.add(normalize_employee_name(f"{self.given_names[0]} {self.given_names[1]} {self.paternal_surname}"))
        if self.paternal_surname and self.maternal_surname and self.given_names:
            values.add(normalize_employee_name(f"{self.given_names[0]} {self.paternal_surname} {self.maternal_surname}"))
        return {value for value in values if value}

    @property
    def token_set(self) -> set[str]:
        return set(name_tokens(self.raw_name))


def strip_accents(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(character)
    )


def normalize_employee_name(value: str | None) -> str:
    if value is None:
        return ""
    text = strip_accents(str(value)).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def name_tokens(value: str | None) -> list[str]:
    normalized = normalize_employee_name(value)
    return [token for token in normalized.split(" ") if token]


def employee_name_key(value: str | None) -> str:
    tokens = sorted(name_tokens(value))
    return " ".join(tokens)


def parse_personnel_name(value: str | None) -> PersonnelName:
    raw_name = " ".join(str(value or "").strip().split())
    tokens = [part.title() for part in raw_name.split() if part]
    if len(tokens) >= 3:
        paternal_surname = tokens[0]
        maternal_surname = tokens[1]
        given_names = tuple(tokens[2:])
    elif len(tokens) == 2:
        paternal_surname = tokens[1]
        maternal_surname = ""
        given_names = (tokens[0],)
    elif len(tokens) == 1:
        paternal_surname = ""
        maternal_surname = ""
        given_names = (tokens[0],)
    else:
        paternal_surname = ""
        maternal_surname = ""
        given_names = ()
    return PersonnelName(
        raw_name=raw_name.title(),
        paternal_surname=paternal_surname,
        maternal_surname=maternal_surname,
        given_names=given_names,
    )


def names_refer_to_same_person(left: str | None, right: str | None) -> bool:
    left_normalized = normalize_employee_name(left)
    right_normalized = normalize_employee_name(right)
    if not left_normalized or not right_normalized:
        return False
    if left_normalized == right_normalized:
        return True
    left_tokens = set(name_tokens(left))
    right_tokens = set(name_tokens(right))
    if len(left_tokens) >= 2 and left_tokens.issubset(right_tokens):
        return True
    if len(right_tokens) >= 2 and right_tokens.issubset(left_tokens):
        return True
    return employee_name_key(left) == employee_name_key(right)
