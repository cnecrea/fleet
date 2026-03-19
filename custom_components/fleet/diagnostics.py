"""
Diagnosticare pentru integrarea Fleet.

Exportă informații de diagnostic structurate pe categorii,
mascând datele sensibile (VIN, serie CIV, nr. poliță, CNP, etc.).

Structura de categorii este aceeași ca în exportul JSON (STRUCTURA_CATEGORII)
pentru consistență între export și diagnostics.
"""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_ADR_CERTIFICAT_NUMAR,
    CONF_ADR_CONSILIER_CERTIFICAT,
    CONF_CASCO_NUMAR_POLITA,
    CONF_COPIE_CONFORMA_NUMAR,
    CONF_ISTORIC,
    CONF_LICENTA_COMUNITARA_NUMAR,
    CONF_LICENTA_TRANSPORT_NUMAR,
    CONF_NR_INMATRICULARE,
    CONF_PROPRIETAR,
    CONF_RCA_NUMAR_POLITA,
    CONF_REMORCA_NR_INMATRICULARE,
    CONF_SERIE_CIV,
    CONF_SOFER_CARD_TAHOGRAF_NUMAR,
    CONF_SOFER_CNP,
    CONF_SOFER_CPC_NUMAR,
    CONF_SOFER_NR_PERMIS,
    CONF_SOFER_NUME,
    CONF_VIN,
    DOMAIN,
    LICENSE_DATA_KEY,
    STRUCTURA_CATEGORII,
    normalizeaza_numar,
)

# ─────────────────────────────────────────────
# Câmpuri sensibile (se maschează în diagnostic)
# ─────────────────────────────────────────────
CAMPURI_SENSIBILE: frozenset[str] = frozenset(
    {
        CONF_VIN,
        CONF_SERIE_CIV,
        CONF_NR_INMATRICULARE,
        CONF_RCA_NUMAR_POLITA,
        CONF_CASCO_NUMAR_POLITA,
        CONF_PROPRIETAR,
        CONF_SOFER_NUME,
        CONF_SOFER_CNP,
        CONF_SOFER_NR_PERMIS,
        CONF_SOFER_CPC_NUMAR,
        CONF_SOFER_CARD_TAHOGRAF_NUMAR,
        CONF_LICENTA_TRANSPORT_NUMAR,
        CONF_COPIE_CONFORMA_NUMAR,
        CONF_LICENTA_COMUNITARA_NUMAR,
        CONF_ADR_CERTIFICAT_NUMAR,
        CONF_ADR_CONSILIER_CERTIFICAT,
        CONF_REMORCA_NR_INMATRICULARE,
    }
)


# ─────────────────────────────────────────────
# Funcții de mascare
# ─────────────────────────────────────────────


def _mascheaza(cheie_conf: str, valoare: Any) -> Any:
    """Maschează valorile sensibile, păstrând primul și ultimele 2 caractere."""
    if cheie_conf not in CAMPURI_SENSIBILE:
        return valoare
    if valoare is None or valoare == "":
        return valoare
    text = str(valoare)
    if len(text) <= 4:
        return "****"
    return f"{text[:1]}{'*' * (len(text) - 3)}{text[-2:]}"


# ─────────────────────────────────────────────
# Construcție diagnostic structurat
# ─────────────────────────────────────────────


def _extrage_campuri_diagnostic(
    sursa: dict[str, Any], campuri: list[tuple[str, str]]
) -> dict[str, Any]:
    """Extrage și maschează câmpurile dintr-un dicționar sursă."""
    rezultat: dict[str, Any] = {}
    for cheie_json, cheie_conf in campuri:
        val = sursa.get(cheie_conf)
        if val is not None and val != "":
            rezultat[cheie_json] = _mascheaza(cheie_conf, val)
    return rezultat


def _structureaza_diagnostic(sursa: dict[str, Any]) -> dict[str, Any]:
    """Structurează datele vehiculului pe categorii cu mascare."""
    rezultat: dict[str, Any] = {}

    for categorie, continut in STRUCTURA_CATEGORII:
        if isinstance(continut, list):
            sectiune = _extrage_campuri_diagnostic(sursa, continut)
            if sectiune:
                rezultat[categorie] = sectiune
        elif isinstance(continut, dict):
            sectiune_dict: dict[str, Any] = {}
            for sub_categorie, campuri in continut.items():
                sub_sectiune = _extrage_campuri_diagnostic(sursa, campuri)
                if sub_sectiune:
                    sectiune_dict[sub_categorie] = sub_sectiune
            if sectiune_dict:
                rezultat[categorie] = sectiune_dict

    return rezultat


def _structureaza_istoric(
    istoric: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Structurează lista de intrări istorice pentru export."""
    if not isinstance(istoric, list):
        return []
    rezultat: list[dict[str, Any]] = []
    for intrare in istoric:
        if not isinstance(intrare, dict):
            continue
        rezultat.append(
            {
                "tip": intrare.get("tip", "necunoscut"),
                "data_arhivare": intrare.get("data_arhivare"),
                "date": intrare.get("date", {}),
            }
        )
    return rezultat


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Returnează datele de diagnostic structurate pe categorii."""
    toate_datele: dict[str, Any] = {**entry.data, **entry.options}
    numar_normalizat = normalizeaza_numar(
        entry.data.get(CONF_NR_INMATRICULARE, "")
    )

    categorii = _structureaza_diagnostic(toate_datele)

    istoric_raw = toate_datele.get(CONF_ISTORIC, [])
    istoric = _structureaza_istoric(istoric_raw)

    senzori_activi = [
        entitate.entity_id
        for entitate in hass.states.async_all("sensor")
        if entitate.entity_id.startswith(
            f"sensor.fleet_{numar_normalizat}"
        )
    ]

    # Informații licență (inclusiv fingerprint complet pentru diagnostic)
    licenta_info: dict[str, Any] = {}
    domain_data = hass.data.get(DOMAIN, {})
    license_mgr = domain_data.get(LICENSE_DATA_KEY)
    if license_mgr is not None:
        licenta_info = {
            "status": license_mgr.status,
            "is_valid": license_mgr.is_valid,
            "is_trial_valid": license_mgr.is_trial_valid,
            "trial_days_remaining": license_mgr.trial_days_remaining,
            "license_type": license_mgr.license_type,
            "license_key": license_mgr.license_key_masked,
            "fingerprint_full": license_mgr.fingerprint,
            "check_interval_seconds": license_mgr.check_interval_seconds,
        }

    return {
        "intrare": {
            "titlu": _mascheaza(
                CONF_NR_INMATRICULARE,
                entry.title,
            ),
            "versiune": entry.version,
            "domeniu": DOMAIN,
        },
        "licenta": licenta_info,
        **categorii,
        "istoric": istoric,
        "stare": {
            "senzori_activi": len(senzori_activi),
            "lista_senzori": sorted(senzori_activi),
        },
    }
