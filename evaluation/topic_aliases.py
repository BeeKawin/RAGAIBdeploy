from __future__ import annotations

import re
from collections.abc import Iterable


_NON_WORD_RE = re.compile(r"[^\w\u0E00-\u0E7F]+", re.UNICODE)


TOPIC_ALIAS_GROUPS: dict[str, set[str]] = {
    "measurement": {
        "Measurement",
        "Measurement and Units",
        "SI Units",
        "หน่วยและการวัด",
    },
    "kinematics_1d": {
        "Kinematics 1D",
        "Linear Motion",
        "Motion in One Dimension",
        "การเคลื่อนที่แนวตรง",
        "การเคลื่อนที่ในแนวดิ่ง",
        "การเคลื่อนที่ใน 1 และ 2 มิติ",
    },
    "projectile_motion": {
        "Projectile Motion",
        "Kinematics 2D",
        "Motion in Two Dimensions",
        "time of flight",
        "การเคลื่อนที่แบบโพรเจกไทล์",
    },
    "newtons_laws": {
        "Force and Laws of Motion",
        "Newton's Laws of Motion",
        "Laws of Motion",
        "Newton's Second Law",
        "แรงและกฎการเคลื่อนที่",
        "กฎการเคลื่อนที่ของนิวตัน",
    },
    "work_energy": {
        "Work and Energy",
        "Work Energy and Power",
        "work-energy theorem",
        "งานและพลังงาน",
    },
    "momentum_collisions": {
        "Momentum and Collisions",
        "Impulse and Momentum",
        "โมเมนตัมและการชน",
        "โมเมนตัม แรงดล และการชน",
    },
    "equilibrium": {
        "Equilibrium",
        "Mechanical Equilibrium",
        "สมดุลกล",
        "สภาพสมดุล",
        "สมดุลต่อการเลื่อนที่",
    },
    "simple_harmonic_motion": {
        "Simple Harmonic Motion",
        "Oscillation",
        "คาบและความถี่ของมวลติดสปริง",
        "การเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย",
    },
    "waves_sound": {
        "Waves",
        "Waves and Sound",
        "Sound",
        "wave speed",
        "คลื่นกล",
        "เสียง",
    },
    "ray_optics": {
        "Light and Optics",
        "Geometric Optics",
        "Ray Optics",
        "กระจกและเลนส์",
        "แสงเชิงรังสี",
    },
    "wave_optics": {
        "Wave Optics",
        "การแทรกสอดของแสง",
        "แสงเชิงคลื่น",
    },
    "fluids": {
        "Fluids",
        "Fluid",
        "ของแข็งและของไหล",
        "ความรู้เกี่ยวกับ ของไหล (Fluid)",
    },
    "thermal_physics": {
        "Thermal Physics",
        "Thermodynamics",
        "Heat Transfer",
        "Temperature and Heat",
        "Temperature vs heat",
        "Specific Heat",
        "Specific heat",
        "Latent Heat",
    },
    "electrostatics": {
        "Electrostatics",
        "Coulomb's Law",
        "ไฟฟ้าสถิต",
        "กฎของคูลอมบ์",
    },
    "electric_current": {
        "Electrodynamics",
        "Electric Current and Circuits",
        "Ohm's Law",
        "Kirchhoff's Law",
        "ไฟฟ้ากระแส",
    },
    "magnetism_electricity": {
        "Magnetism",
        "Magnets and Electricity",
        "Electromagnetics",
        "แม่เหล็กและไฟฟ้า",
        "แม่เหล็กไฟฟ้า",
        "แม่เหล็กไฟฟ้า (Electromagnetics)",
    },
    "electromagnetic_wave": {
        "Electromagnetic Wave",
        "Electromagnetic Waves",
        "คลื่นแม่เหล็กไฟฟ้า",
    },
    "atomic_physics": {
        "Atomic Physics",
        "Quantum Physics",
        "ฟิสิกส์อะตอม",
    },
    "nuclear_physics": {
        "Nuclear Physics",
        "ฟิสิกส์นิวเคลียร์",
    },
    "gas_laws": {
        "Gas Laws",
        "Boyle's law",
        "กฎของแก๊ส",
    },
    "density_pressure": {
        "Density",
        "Pressure",
        "Density and Pressure",
        "ความหนาแน่น",
        "ความดัน",
    },
}


def normalize_term(term: str) -> str:
    normalized = str(term or "").strip().lower()
    normalized = _NON_WORD_RE.sub(" ", normalized)
    return " ".join(normalized.split())


ALIAS_TO_CANONICAL = {
    normalize_term(alias): canonical
    for canonical, aliases in TOPIC_ALIAS_GROUPS.items()
    for alias in aliases | {canonical}
}


def canonicalize(term: str) -> str:
    normalized = normalize_term(term)
    if normalized in ALIAS_TO_CANONICAL:
        return ALIAS_TO_CANONICAL[normalized]
    for alias, canonical in sorted(ALIAS_TO_CANONICAL.items(), key=lambda item: len(item[0]), reverse=True):
        if alias and len(alias) >= 5 and alias in normalized:
            return canonical
    return normalized


def canonicalize_terms(terms: Iterable[str]) -> set[str]:
    return {canonicalize(term) for term in terms if normalize_term(term)}


def terms_match(expected_terms: Iterable[str], retrieved_terms: Iterable[str]) -> bool:
    expected_raw = {normalize_term(term) for term in expected_terms if normalize_term(term)}
    retrieved_raw = {normalize_term(term) for term in retrieved_terms if normalize_term(term)}
    expected = canonicalize_terms(expected_raw)
    retrieved = canonicalize_terms(retrieved_raw)
    if expected & retrieved:
        return True

    haystack = " ".join(retrieved_raw)
    for term in expected_raw:
        if term and term in haystack:
            return True
        words = [word for word in term.split() if len(word) >= 4]
        if words and all(word in haystack for word in words):
            return True
    return False
