"""
Platforma de senzori pentru integrarea Fleet (gestiune flotă transport).

Senzorii sunt CONDIȚIONAȚI – apar DOAR când au date completate.
La prima configurare (doar nr. de înmatriculare), apare doar senzorul Informații.
Pe măsură ce utilizatorul completează date, apar senzorii corespunzători.

Senzori posibili per vehicul:
- Informații generale (marcă, model, etc.) – mereu vizibil
- Kilometraj curent – vizibil când km_curent este setat
- Ore motor – vizibil când ore_motor este setat
- RCA, Casco, ITP, Rovinieta, Impozit, Leasing – vizibili după setare date
- Revizie ulei, Distribuție, Anvelope, Baterie, Frâne – vizibili după setare date
- Trusă prim ajutor, Extinctor – vizibili după setare date
- Șofer (date identificare) – vizibil când sofer_nume este setat
- Permis șofer – vizibil când data_expirare_permis este setată
- CPC, Card tahograf, Fișă medicală, Fișă psihologică – vizibili după setare date
- Licență transport, Copie conformă, Licență comunitară – vizibili după setare date
- ADR, Tahograf – vizibili după setare date
- Combustibil, Alimentare – vizibili după setare date
- DPF, Turbo – vizibili după setare date
- Remorcă (identificare), Remorcă ITP/RCA/Rovinieta – vizibili după setare date
- Cost total – vizibil când cel puțin un cost este completat
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_ADR_CERTIFICAT_DATA_EXPIRARE,
    CONF_ADR_CERTIFICAT_NUMAR,
    CONF_ADR_CLASE,
    CONF_ADR_CONSILIER_CERTIFICAT,
    CONF_ADR_CONSILIER_DATA_EXPIRARE,
    CONF_ADR_CONSILIER_NUME,
    CONF_ADR_ECHIPAMENT_COMPLET,
    CONF_AN_FABRICATIE,
    CONF_AN_PRIMA_INMATRICULARE,
    CONF_ANVELOPE_COST,
    CONF_ANVELOPE_DOT,
    CONF_ANVELOPE_IARNA_DATA,
    CONF_ANVELOPE_KM_MONTARE,
    CONF_ANVELOPE_NR_RESAPARI,
    CONF_ANVELOPE_TIP,
    CONF_ANVELOPE_VARA_DATA,
    CONF_BATERIE_COST,
    CONF_BATERIE_DATA_SCHIMB,
    CONF_CAPACITATE_CILINDRICA,
    CONF_CASCO_COMPANIE,
    CONF_CASCO_COST,
    CONF_CASCO_DATA_EMITERE,
    CONF_CASCO_DATA_EXPIRARE,
    CONF_CASCO_NUMAR_POLITA,
    CONF_COMBUSTIBIL,
    CONF_COMBUSTIBIL_CAPACITATE,
    CONF_COMBUSTIBIL_CONSUM_MEDIU,
    CONF_COMBUSTIBIL_NIVEL,
    CONF_COPIE_CONFORMA_DATA_EXPIRARE,
    CONF_COPIE_CONFORMA_NUMAR,
    CONF_DISCURI_FRANA_COST,
    CONF_DISCURI_FRANA_DATA,
    CONF_DISCURI_FRANA_KM_ULTIMUL,
    CONF_DISCURI_FRANA_KM_URMATOR,
    CONF_DISTRIBUTIE_COST,
    CONF_DISTRIBUTIE_DATA,
    CONF_DISTRIBUTIE_KM_ULTIMUL,
    CONF_DISTRIBUTIE_KM_URMATOR,
    CONF_DPF_COST,
    CONF_DPF_DATA_CURATARE,
    CONF_DPF_KM_CURATARE,
    CONF_EXTINCTOR_CAPACITATE,
    CONF_EXTINCTOR_DATA_EXPIRARE,
    CONF_IMPOZIT_LOCALITATE,
    CONF_IMPOZIT_SCADENTA,
    CONF_IMPOZIT_SUMA,
    CONF_ISTORIC,
    CONF_ITP_DATA_EXPIRARE,
    CONF_ITP_KILOMETRAJ,
    CONF_ITP_STATIE,
    CONF_KM_CURENT,
    CONF_LEASING_DATA_EXPIRARE,
    CONF_LICENTA_COMUNITARA_DATA_EXPIRARE,
    CONF_LICENTA_COMUNITARA_NUMAR,
    CONF_LICENTA_TRANSPORT_DATA_EXPIRARE,
    CONF_LICENTA_TRANSPORT_NUMAR,
    CONF_LICENTA_TRANSPORT_TIP,
    CONF_MARCA,
    CONF_MMA,
    CONF_MODEL,
    CONF_MOTORIZARE,
    CONF_MASA_PROPRIE,
    CONF_NR_AXE,
    CONF_NR_INMATRICULARE,
    CONF_ORE_MOTOR,
    CONF_PLACUTE_FRANA_COST,
    CONF_PLACUTE_FRANA_DATA,
    CONF_PLACUTE_FRANA_KM_ULTIMUL,
    CONF_PLACUTE_FRANA_KM_URMATOR,
    CONF_PROPRIETAR,
    CONF_PUTERE_CP,
    CONF_PUTERE_KW,
    CONF_RCA_COMPANIE,
    CONF_RCA_COST,
    CONF_RCA_DATA_EMITERE,
    CONF_RCA_DATA_EXPIRARE,
    CONF_RCA_NUMAR_POLITA,
    CONF_REMORCA_AN_FABRICATIE,
    CONF_REMORCA_ITP_DATA_EXPIRARE,
    CONF_REMORCA_MARCA,
    CONF_REMORCA_MMA,
    CONF_REMORCA_MASA_PROPRIE,
    CONF_REMORCA_NR_AXE,
    CONF_REMORCA_NR_INMATRICULARE,
    CONF_REMORCA_RCA_DATA_EXPIRARE,
    CONF_REMORCA_ROVINIETA_DATA_SFARSIT,
    CONF_REMORCA_TIP,
    CONF_REVIZIE_ULEI_COST,
    CONF_REVIZIE_ULEI_DATA,
    CONF_REVIZIE_ULEI_KM_ULTIMUL,
    CONF_REVIZIE_ULEI_KM_URMATOR,
    CONF_ROVINIETA_CATEGORIE,
    CONF_ROVINIETA_DATA_INCEPUT,
    CONF_ROVINIETA_DATA_SFARSIT,
    CONF_ROVINIETA_PRET,
    CONF_SERIE_CIV,
    CONF_SOFER_CARD_TAHOGRAF_DATA_EXPIRARE,
    CONF_SOFER_CARD_TAHOGRAF_NUMAR,
    CONF_SOFER_CATEGORII_PERMIS,
    CONF_SOFER_CNP,
    CONF_SOFER_CPC_DATA_EXPIRARE,
    CONF_SOFER_CPC_NUMAR,
    CONF_SOFER_CPC_TIP,
    CONF_SOFER_DATA_EXPIRARE_PERMIS,
    CONF_SOFER_FISA_MEDICALA_APT,
    CONF_SOFER_FISA_MEDICALA_DATA,
    CONF_SOFER_FISA_MEDICALA_DATA_EXPIRARE,
    CONF_SOFER_ATESTAT_ADR_CLASE,
    CONF_SOFER_ATESTAT_ADR_DATA_EXPIRARE,
    CONF_SOFER_ATESTAT_ADR_NUMAR,
    CONF_SOFER_FISA_PSIHOLOGICA_DATA,
    CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE,
    CONF_SOFER_NR_PERMIS,
    CONF_SOFER_NUME,
    CONF_TAHOGRAF_DATA_CALIBRARE,
    CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE,
    CONF_TAHOGRAF_DATA_VERIFICARE,
    CONF_TAHOGRAF_TIP,
    CONF_TIP_PROPRIETATE,
    CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE,
    CONF_TAXA_DRUM_DATA,
    CONF_TAXA_DRUM_SUMA,
    CONF_TAXA_DRUM_TARA,
    CONF_TAXA_DRUM_VALUTA,
    CONF_AMENDA_DATA,
    CONF_AMENDA_MOTIV,
    CONF_AMENDA_STATUS,
    CONF_AMENDA_SUMA,
    CONF_AMENDA_TARA,
    CONF_TURBO_COST,
    CONF_TURBO_DATA_REVIZIE,
    CONF_TURBO_KM_REVIZIE,
    CONF_VIN,
    CONF_ALIMENTARE_COST,
    CONF_ALIMENTARE_DATA,
    CONF_ALIMENTARE_KM,
    CONF_ALIMENTARE_LITRI,
    CONF_ALIMENTARE_PRET_LITRU,
    CONF_ADBLUE_CAPACITATE,
    CONF_ADBLUE_NIVEL,
    CONF_CATEGORIE_EURO,
    CONF_TIP_SUSPENSIE,
    CONF_TIP_VEHICUL,
    DOMAIN,
    LICENSE_DATA_KEY,
    normalizeaza_numar,
)
from .helpers import (
    decimal,
    format_data_ro,
    intreg,
    km_ramasi,
    luni_de_la,
    sarcina_utila,
    sezon_anvelope,
    stare_document,
    zile_ramase,
)

_LOGGER = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Funcții utilitare locale (specifice senzorilor)
# ─────────────────────────────────────────────


def _are_valoare(data: dict[str, Any], *chei: str) -> bool:
    """Verifică dacă cel puțin una din chei are o valoare non-goală în date."""
    return any(data.get(k) not in (None, "") for k in chei)


# ─────────────────────────────────────────────
# Descrieri senzori
# ─────────────────────────────────────────────


@dataclass(frozen=True)
class FleetSensorDescription(SensorEntityDescription):
    """Descriere extinsă pentru senzorii flotei."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None
    attributes_fn: Callable[[dict[str, Any]], dict[str, Any]] | None = None
    # Funcție de vizibilitate: returnează True dacă senzorul trebuie creat.
    # Dacă este None, senzorul este mereu vizibil.
    vizibil_fn: Callable[[dict[str, Any]], bool] | None = None


def _informatii_value(data: dict[str, Any]) -> str | None:
    """Starea senzorului de informații: Marcă Model sau nr. înmatriculare."""
    marca = data.get(CONF_MARCA, "")
    model = data.get(CONF_MODEL, "")
    text = f"{marca} {model}".strip()
    if text:
        return text
    # Fallback: returnăm nr. de înmatriculare (mereu disponibil)
    return data.get(CONF_NR_INMATRICULARE)


def _informatii_attr(data: dict[str, Any]) -> dict[str, Any]:
    """Atributele senzorului de informații."""
    atribute: dict[str, Any] = {}

    # Câmpuri text – se adaugă direct
    campuri_text = {
        "Nr. înmatriculare": CONF_NR_INMATRICULARE,
        "Serie CIV": CONF_SERIE_CIV,
        "VIN": CONF_VIN,
        "Marcă": CONF_MARCA,
        "Model": CONF_MODEL,
        "Motorizare": CONF_MOTORIZARE,
        "Combustibil": CONF_COMBUSTIBIL,
        "Tip vehicul": CONF_TIP_VEHICUL,
        "Categorie Euro": CONF_CATEGORIE_EURO,
        "Tip suspensie": CONF_TIP_SUSPENSIE,
    }
    for eticheta, cheie in campuri_text.items():
        val = data.get(cheie)
        if val is not None and val != "":
            atribute[eticheta] = val

    # Câmpuri numerice – convertim float → int
    campuri_numerice = {
        "An fabricație": CONF_AN_FABRICATIE,
        "An prima înmatriculare": CONF_AN_PRIMA_INMATRICULARE,
        "Capacitate cilindrică (cm³)": CONF_CAPACITATE_CILINDRICA,
        "Putere (kW)": CONF_PUTERE_KW,
        "Putere (CP)": CONF_PUTERE_CP,
        "MMA (kg)": CONF_MMA,
        "Masa proprie (kg)": CONF_MASA_PROPRIE,
        "Nr. axe": CONF_NR_AXE,
    }
    for eticheta, cheie in campuri_numerice.items():
        val = intreg(data.get(cheie))
        if val is not None:
            atribute[eticheta] = val

    # Sarcina utilă calculată
    su = sarcina_utila(data.get(CONF_MMA), data.get(CONF_MASA_PROPRIE))
    if su is not None:
        atribute["Sarcina utilă (kg)"] = su

    return atribute


def _filtrare_atribute(perechi: dict[str, Any]) -> dict[str, Any]:
    """Filtrează atributele: elimină valorile None și stringurile goale."""
    return {k: v for k, v in perechi.items() if v is not None and v != ""}


# ─────────────────────────────────────────────
# Funcții pentru istoric (per categorie)
# ─────────────────────────────────────────────


def _cu_istoric(
    atribute: dict[str, Any], data: dict[str, Any], categorie: str
) -> dict[str, Any]:
    """Adaugă atribute de istoric la un dicționar de atribute existent.

    Afișează:
    - Reînnoiri anterioare: N
    - Ultima arhivare: DD.MM.YYYY
    - Detaliile ultimei intrări arhivate (cu prefix „Anterior – ")
    - Cost total anterior (RON) agregat (dacă > 1 intrare și > 0)
    """
    istoric = data.get(CONF_ISTORIC, [])
    if not isinstance(istoric, list):
        return atribute

    intrari = [
        i for i in istoric
        if isinstance(i, dict) and i.get("tip") == categorie
    ]
    if not intrari:
        return atribute

    # Număr total de reînnoiri
    atribute["Reînnoiri anterioare"] = len(intrari)

    # Ultima intrare arhivată — detalii
    ultima = intrari[-1]
    data_arhivare = ultima.get("data_arhivare")
    if data_arhivare:
        atribute["Ultima arhivare"] = format_data_ro(data_arhivare)

    # Câmpurile din ultima intrare, cu prefix „Anterior – "
    date_vechi = ultima.get("date", {})
    for eticheta, val in date_vechi.items():
        if val is None or val == "":
            continue
        # Încercăm conversie: dată RO > întreg > text brut
        val_afisat: Any = val
        val_data = format_data_ro(val)
        if val_data is not None:
            val_afisat = val_data
        else:
            v_int = intreg(val)
            if v_int is not None:
                val_afisat = v_int
        atribute[f"Anterior – {eticheta}"] = val_afisat

    # Cost total agregat din TOATE intrările (util dacă > 1 reînnoire)
    if len(intrari) > 1:
        total_cost = 0
        for intrare_ist in intrari:
            date_intrare = intrare_ist.get("date", {})
            for cheie_et, v in date_intrare.items():
                if "cost" in cheie_et.lower() or "preț" in cheie_et.lower():
                    vi = intreg(v)
                    if vi is not None:
                        total_cost += vi
        if total_cost > 0:
            atribute["Cost total anterior (RON)"] = total_cost

    return atribute


# ─────────────────────────────────────────────
# Funcții pentru senzorul Cost Total
# ─────────────────────────────────────────────

# ── Mapping cost → data de referință (pentru determinarea anului) ──
# Fiecare cheie de cost are o dată asociată din care extragem anul.
_COST_DATA_REFERINTA: dict[str, str] = {
    CONF_RCA_COST: CONF_RCA_DATA_EMITERE,
    CONF_CASCO_COST: CONF_CASCO_DATA_EMITERE,
    CONF_ROVINIETA_PRET: CONF_ROVINIETA_DATA_INCEPUT,
    CONF_IMPOZIT_SUMA: CONF_IMPOZIT_SCADENTA,
    CONF_REVIZIE_ULEI_COST: CONF_REVIZIE_ULEI_DATA,
    CONF_DISTRIBUTIE_COST: CONF_DISTRIBUTIE_DATA,
    CONF_ANVELOPE_COST: CONF_ANVELOPE_VARA_DATA,
    CONF_BATERIE_COST: CONF_BATERIE_DATA_SCHIMB,
    CONF_PLACUTE_FRANA_COST: CONF_PLACUTE_FRANA_DATA,
    CONF_DISCURI_FRANA_COST: CONF_DISCURI_FRANA_DATA,
    CONF_DPF_COST: CONF_DPF_DATA_CURATARE,
    CONF_TURBO_COST: CONF_TURBO_DATA_REVIZIE,
    CONF_ALIMENTARE_COST: CONF_ALIMENTARE_DATA,
    CONF_TAXA_DRUM_SUMA: CONF_TAXA_DRUM_DATA,
    CONF_AMENDA_SUMA: CONF_AMENDA_DATA,
}

# Costurile grupate pe categorii (pentru defalcare în atribute)
_COSTURI_ASIGURARI: dict[str, str] = {
    "RCA": CONF_RCA_COST,
    "Casco": CONF_CASCO_COST,
}
_COSTURI_TAXE: dict[str, str] = {
    "Rovinieta": CONF_ROVINIETA_PRET,
    "Impozit auto": CONF_IMPOZIT_SUMA,
    "Taxe drum": CONF_TAXA_DRUM_SUMA,
    "Amenzi": CONF_AMENDA_SUMA,
}
_COSTURI_MENTENANTA: dict[str, str] = {
    "Revizie ulei": CONF_REVIZIE_ULEI_COST,
    "Distribuție": CONF_DISTRIBUTIE_COST,
    "Anvelope": CONF_ANVELOPE_COST,
    "Baterie": CONF_BATERIE_COST,
    "Plăcuțe frână": CONF_PLACUTE_FRANA_COST,
    "Discuri frână": CONF_DISCURI_FRANA_COST,
    "DPF": CONF_DPF_COST,
    "Turbo": CONF_TURBO_COST,
}
_COSTURI_COMBUSTIBIL: dict[str, str] = {
    "Alimentare": CONF_ALIMENTARE_COST,
}


def _an_din_data(data_iso: Any) -> int | None:
    """Extrage anul dintr-o dată ISO. Returnează None dacă nu e validă."""
    if not data_iso or data_iso == "":
        return None
    try:
        return date.fromisoformat(str(data_iso)).year
    except (ValueError, TypeError):
        return None


def _costuri_pe_ani(data: dict[str, Any]) -> dict[int, int]:
    """Construiește un dicționar {an: total_cost} din costurile curente.

    Folosește _COST_DATA_REFERINTA pentru a determina anul fiecărui cost.
    Costurile fără dată asociată se atribuie anului curent (fallback).
    """
    costuri: dict[int, int] = {}
    an_curent = date.today().year

    for cheie_cost, cheie_data in _COST_DATA_REFERINTA.items():
        val = intreg(data.get(cheie_cost))
        if val is None or val == 0:
            continue
        an = _an_din_data(data.get(cheie_data)) or an_curent
        costuri[an] = costuri.get(an, 0) + val

    return costuri


def _costuri_istorice_pe_ani(data: dict[str, Any]) -> dict[int, int]:
    """Construiește un dicționar {an: total_cost} din intrările arhivate.

    Scanează _istoric și extrage costurile + anul din datele arhivate.
    Folosește data_arhivare ca fallback dacă nu există date calendaristice.
    """
    istoric = data.get(CONF_ISTORIC, [])
    if not isinstance(istoric, list):
        return {}

    costuri: dict[int, int] = {}

    for intrare in istoric:
        if not isinstance(intrare, dict):
            continue
        date_vechi = intrare.get("date", {})
        # Determinăm anul: căutăm prima dată validă în datele arhivate
        an_intrare: int | None = None
        for _eticheta, val in date_vechi.items():
            an_intrare = _an_din_data(val)
            if an_intrare is not None:
                break
        # Fallback: anul din data_arhivare
        if an_intrare is None:
            an_intrare = _an_din_data(intrare.get("data_arhivare"))
        if an_intrare is None:
            continue

        # Extragem costurile
        for eticheta, val in date_vechi.items():
            if "cost" in eticheta.lower() or "preț" in eticheta.lower():
                v = intreg(val)
                if v is not None and v > 0:
                    costuri[an_intrare] = costuri.get(an_intrare, 0) + v

    return costuri


def _suma_categorie_an(
    data: dict[str, Any], campuri: dict[str, str], an: int,
) -> int:
    """Calculează suma costurilor unei categorii pentru un an specific."""
    total = 0
    for _eticheta, cheie_cost in campuri.items():
        val = intreg(data.get(cheie_cost))
        if val is None or val == 0:
            continue
        cheie_data = _COST_DATA_REFERINTA.get(cheie_cost)
        an_cost = (
            _an_din_data(data.get(cheie_data)) if cheie_data else None
        ) or date.today().year
        if an_cost == an:
            total += val
    return total


def _are_costuri(data: dict[str, Any]) -> bool:
    """Verifică dacă există cel puțin un cost completat (curent sau arhivat)."""
    # Costuri curente
    for cheie_cost in _COST_DATA_REFERINTA:
        val = intreg(data.get(cheie_cost))
        if val is not None and val > 0:
            return True
    # Costuri arhivate
    istoric = data.get(CONF_ISTORIC, [])
    if isinstance(istoric, list):
        for intrare in istoric:
            if not isinstance(intrare, dict):
                continue
            for et, v in intrare.get("date", {}).items():
                if "cost" in et.lower() or "preț" in et.lower():
                    vi = intreg(v)
                    if vi is not None and vi > 0:
                        return True
    return False


def _cost_total_value(data: dict[str, Any]) -> int | None:
    """Returnează costul total al anului curent.

    Suma tuturor costurilor curente care au data de referință în anul curent.
    Returnează None dacă nu există niciun cost (senzorul nu se creează).
    Returnează 0 dacă există costuri dar niciunul nu e din anul curent.
    """
    if not _are_costuri(data):
        return None
    costuri_curente = _costuri_pe_ani(data)
    an_curent = date.today().year
    return costuri_curente.get(an_curent, 0)


def _cost_total_attr(data: dict[str, Any]) -> dict[str, Any]:
    """Atributele senzorului Cost Total: defalcare pe an și categorie.

    Afișează:
    - An curent: defalcare pe categorii (Asigurări / Taxe / Mentenanță / Combustibil)
    - Ani anteriori: total per an (din costuri curente + arhivate)
    """
    atribute: dict[str, Any] = {}
    an_curent = date.today().year

    # ── Defalcare an curent pe categorii ──
    s_asig = _suma_categorie_an(data, _COSTURI_ASIGURARI, an_curent)
    if s_asig > 0:
        atribute[f"Asigurări {an_curent} (RON)"] = s_asig

    s_taxe = _suma_categorie_an(data, _COSTURI_TAXE, an_curent)
    if s_taxe > 0:
        atribute[f"Taxe {an_curent} (RON)"] = s_taxe

    s_ment = _suma_categorie_an(data, _COSTURI_MENTENANTA, an_curent)
    if s_ment > 0:
        atribute[f"Mentenanță {an_curent} (RON)"] = s_ment

    s_comb = _suma_categorie_an(data, _COSTURI_COMBUSTIBIL, an_curent)
    if s_comb > 0:
        atribute[f"Combustibil {an_curent} (RON)"] = s_comb

    # ── Costuri din ani anteriori (curente care nu sunt anul curent) ──
    costuri_curente = _costuri_pe_ani(data)

    # ── Costuri din istoric (arhivate) ──
    costuri_arhivate = _costuri_istorice_pe_ani(data)

    # Combinăm toate costurile pe ani
    toti_anii: dict[int, int] = {}
    for an, total in costuri_curente.items():
        toti_anii[an] = toti_anii.get(an, 0) + total
    for an, total in costuri_arhivate.items():
        toti_anii[an] = toti_anii.get(an, 0) + total

    # Afișăm totaluri per an (descrescător, fără anul curent – deja defalcat)
    for an in sorted(toti_anii.keys(), reverse=True):
        if an == an_curent:
            continue
        atribute[f"Total {an} (RON)"] = toti_anii[an]

    # Total general (toți anii)
    total_general = sum(toti_anii.values())
    if total_general > 0 and len(toti_anii) > 1:
        atribute["Total general (RON)"] = total_general

    # ── Detalii ultima taxă de drum ──
    taxa_tara = data.get(CONF_TAXA_DRUM_TARA)
    if taxa_tara:
        taxa_info = f"{taxa_tara.upper()}"
        taxa_suma = data.get(CONF_TAXA_DRUM_SUMA)
        taxa_valuta = data.get(CONF_TAXA_DRUM_VALUTA)
        if taxa_suma:
            taxa_info += f" – {taxa_suma} {taxa_valuta or ''}"
        atribute["Ultima taxă drum"] = taxa_info.strip()

    # ── Detalii ultima amendă ──
    amenda_suma = intreg(data.get(CONF_AMENDA_SUMA))
    if amenda_suma:
        amenda_info = f"{amenda_suma} RON"
        amenda_motiv = data.get(CONF_AMENDA_MOTIV)
        if amenda_motiv:
            amenda_info += f" – {amenda_motiv}"
        atribute["Ultima amendă"] = amenda_info
        amenda_tara = data.get(CONF_AMENDA_TARA)
        if amenda_tara:
            atribute["Amendă țara"] = amenda_tara.upper()
        amenda_status = data.get(CONF_AMENDA_STATUS)
        if amenda_status:
            atribute["Amendă status"] = amenda_status

    return atribute


SENSOR_DESCRIPTIONS: list[FleetSensorDescription] = [
    # ── Informații vehicul (mereu vizibil – nr. înmatriculare există întotdeauna) ──
    FleetSensorDescription(
        key="informatii",
        translation_key="informatii",
        icon="mdi:car-info",
        # vizibil_fn=None → mereu vizibil
        value_fn=_informatii_value,
        attributes_fn=_informatii_attr,
    ),
    # ── Kilometraj ──
    FleetSensorDescription(
        key="kilometraj",
        translation_key="kilometraj",
        icon="mdi:counter",
        native_unit_of_measurement="km",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        vizibil_fn=lambda d: _are_valoare(d, CONF_KM_CURENT),
        value_fn=lambda d: intreg(d.get(CONF_KM_CURENT)),
        attributes_fn=lambda d: {},
    ),
    # ── Ore motor ──
    FleetSensorDescription(
        key="ore_motor",
        translation_key="ore_motor",
        icon="mdi:engine",
        native_unit_of_measurement="ore",
        vizibil_fn=lambda d: _are_valoare(d, CONF_ORE_MOTOR),
        value_fn=lambda d: intreg(d.get(CONF_ORE_MOTOR)),
        attributes_fn=lambda d: {},
    ),
    # ── RCA ──
    FleetSensorDescription(
        key="rca",
        translation_key="rca",
        icon="mdi:shield-car",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_RCA_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_RCA_DATA_EXPIRARE)),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Număr poliță": d.get(CONF_RCA_NUMAR_POLITA),
                    "Companie": d.get(CONF_RCA_COMPANIE),
                    "Data emitere": format_data_ro(d.get(CONF_RCA_DATA_EMITERE)),
                    "Data expirare": format_data_ro(d.get(CONF_RCA_DATA_EXPIRARE)),
                    "Cost (RON)": intreg(d.get(CONF_RCA_COST)),
                    "Stare": stare_document(d.get(CONF_RCA_DATA_EXPIRARE)),
                }
            ),
            d, "rca",
        ),
    ),
    # ── Casco ──
    FleetSensorDescription(
        key="casco",
        translation_key="casco",
        icon="mdi:shield-plus",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_CASCO_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_CASCO_DATA_EXPIRARE)),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Număr poliță": d.get(CONF_CASCO_NUMAR_POLITA),
                    "Companie": d.get(CONF_CASCO_COMPANIE),
                    "Data emitere": format_data_ro(d.get(CONF_CASCO_DATA_EMITERE)),
                    "Data expirare": format_data_ro(d.get(CONF_CASCO_DATA_EXPIRARE)),
                    "Cost (RON)": intreg(d.get(CONF_CASCO_COST)),
                    "Stare": stare_document(d.get(CONF_CASCO_DATA_EXPIRARE)),
                }
            ),
            d, "casco",
        ),
    ),
    # ── ITP ──
    FleetSensorDescription(
        key="itp",
        translation_key="itp",
        icon="mdi:car-wrench",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_ITP_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_ITP_DATA_EXPIRARE)),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Data expirare": format_data_ro(d.get(CONF_ITP_DATA_EXPIRARE)),
                    "Stație": d.get(CONF_ITP_STATIE),
                    "Kilometraj la ITP": intreg(d.get(CONF_ITP_KILOMETRAJ)),
                    "Stare": stare_document(d.get(CONF_ITP_DATA_EXPIRARE)),
                }
            ),
            d, "itp",
        ),
    ),
    # ── Rovinieta ──
    FleetSensorDescription(
        key="rovinieta",
        translation_key="rovinieta",
        icon="mdi:road-variant",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_ROVINIETA_DATA_SFARSIT),
        value_fn=lambda d: zile_ramase(d.get(CONF_ROVINIETA_DATA_SFARSIT)),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Data început": format_data_ro(d.get(CONF_ROVINIETA_DATA_INCEPUT)),
                    "Data sfârșit": format_data_ro(d.get(CONF_ROVINIETA_DATA_SFARSIT)),
                    "Categorie": d.get(CONF_ROVINIETA_CATEGORIE),
                    "Preț (RON)": intreg(d.get(CONF_ROVINIETA_PRET)),
                    "Stare": stare_document(d.get(CONF_ROVINIETA_DATA_SFARSIT)),
                }
            ),
            d, "rovinieta",
        ),
    ),
    # ── Impozit ──
    FleetSensorDescription(
        key="impozit",
        translation_key="impozit",
        icon="mdi:cash",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_IMPOZIT_SCADENTA),
        value_fn=lambda d: zile_ramase(d.get(CONF_IMPOZIT_SCADENTA)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Sumă (RON)": intreg(d.get(CONF_IMPOZIT_SUMA)),
                "Scadență": format_data_ro(d.get(CONF_IMPOZIT_SCADENTA)),
                "Localitate": d.get(CONF_IMPOZIT_LOCALITATE),
                "Proprietar": d.get(CONF_PROPRIETAR),
                "Tip proprietate": d.get(CONF_TIP_PROPRIETATE),
            }
        ),
    ),
    # ── Leasing (apare DOAR dacă tip_proprietate = leasing) ──
    FleetSensorDescription(
        key="leasing",
        translation_key="leasing",
        icon="mdi:file-document-outline",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: d.get(CONF_TIP_PROPRIETATE) in ("leasing", "leasing_operational"),
        value_fn=lambda d: zile_ramase(d.get(CONF_LEASING_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Data expirare": format_data_ro(d.get(CONF_LEASING_DATA_EXPIRARE)),
                "Tip proprietate": d.get(CONF_TIP_PROPRIETATE),
                "Stare": stare_document(d.get(CONF_LEASING_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Revizie ulei ──
    FleetSensorDescription(
        key="revizie_ulei",
        translation_key="revizie_ulei",
        icon="mdi:oil",
        native_unit_of_measurement="km",
        vizibil_fn=lambda d: _are_valoare(d, CONF_REVIZIE_ULEI_KM_URMATOR),
        value_fn=lambda d: km_ramasi(
            d.get(CONF_KM_CURENT), d.get(CONF_REVIZIE_ULEI_KM_URMATOR)
        ),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Km ultima revizie": intreg(d.get(CONF_REVIZIE_ULEI_KM_ULTIMUL)),
                    "Km următoarea revizie": intreg(d.get(CONF_REVIZIE_ULEI_KM_URMATOR)),
                    "Data ultima revizie": format_data_ro(d.get(CONF_REVIZIE_ULEI_DATA)),
                    "Cost (RON)": intreg(d.get(CONF_REVIZIE_ULEI_COST)),
                    "Km curent": intreg(d.get(CONF_KM_CURENT)),
                }
            ),
            d, "revizie_ulei",
        ),
    ),
    # ── Distribuție ──
    FleetSensorDescription(
        key="distributie",
        translation_key="distributie",
        icon="mdi:engine",
        native_unit_of_measurement="km",
        vizibil_fn=lambda d: _are_valoare(d, CONF_DISTRIBUTIE_KM_URMATOR),
        value_fn=lambda d: km_ramasi(
            d.get(CONF_KM_CURENT), d.get(CONF_DISTRIBUTIE_KM_URMATOR)
        ),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Km ultima schimbare": intreg(d.get(CONF_DISTRIBUTIE_KM_ULTIMUL)),
                    "Km următoarea schimbare": intreg(d.get(CONF_DISTRIBUTIE_KM_URMATOR)),
                    "Data ultima schimbare": format_data_ro(d.get(CONF_DISTRIBUTIE_DATA)),
                    "Cost (RON)": intreg(d.get(CONF_DISTRIBUTIE_COST)),
                    "Km curent": intreg(d.get(CONF_KM_CURENT)),
                }
            ),
            d, "distributie",
        ),
    ),
    # ── Anvelope ──
    FleetSensorDescription(
        key="anvelope",
        translation_key="anvelope",
        icon="mdi:tire",
        vizibil_fn=lambda d: _are_valoare(
            d, CONF_ANVELOPE_VARA_DATA, CONF_ANVELOPE_IARNA_DATA
        ),
        value_fn=lambda d: sezon_anvelope(
            d.get(CONF_ANVELOPE_VARA_DATA), d.get(CONF_ANVELOPE_IARNA_DATA)
        ),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Data montare vară": format_data_ro(d.get(CONF_ANVELOPE_VARA_DATA)),
                    "Data montare iarnă": format_data_ro(d.get(CONF_ANVELOPE_IARNA_DATA)),
                    "Cost (RON)": intreg(d.get(CONF_ANVELOPE_COST)),
                    "Cod DOT": d.get(CONF_ANVELOPE_DOT),
                    "Tip anvelopă": d.get(CONF_ANVELOPE_TIP),
                    "Nr. reșapări": intreg(d.get(CONF_ANVELOPE_NR_RESAPARI)),
                    "Km la montare": intreg(d.get(CONF_ANVELOPE_KM_MONTARE)),
                    "Sezon recomandat": (
                        "Iarnă"
                        if date.today().month in (11, 12, 1, 2, 3)
                        else "Vară"
                    ),
                }
            ),
            d, "anvelope",
        ),
    ),
    # ── Baterie ──
    FleetSensorDescription(
        key="baterie",
        translation_key="baterie",
        icon="mdi:car-battery",
        native_unit_of_measurement="luni",
        vizibil_fn=lambda d: _are_valoare(d, CONF_BATERIE_DATA_SCHIMB),
        value_fn=lambda d: luni_de_la(d.get(CONF_BATERIE_DATA_SCHIMB)),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Data schimb": format_data_ro(d.get(CONF_BATERIE_DATA_SCHIMB)),
                    "Cost (RON)": intreg(d.get(CONF_BATERIE_COST)),
                }
            ),
            d, "baterie",
        ),
    ),
    # ── Plăcuțe frână ──
    FleetSensorDescription(
        key="placute_frana",
        translation_key="placute_frana",
        icon="mdi:car-brake-alert",
        native_unit_of_measurement="km",
        vizibil_fn=lambda d: _are_valoare(d, CONF_PLACUTE_FRANA_KM_URMATOR),
        value_fn=lambda d: km_ramasi(
            d.get(CONF_KM_CURENT), d.get(CONF_PLACUTE_FRANA_KM_URMATOR)
        ),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Km ultima schimbare": intreg(d.get(CONF_PLACUTE_FRANA_KM_ULTIMUL)),
                    "Km următoarea schimbare": intreg(d.get(CONF_PLACUTE_FRANA_KM_URMATOR)),
                    "Data schimbare": format_data_ro(d.get(CONF_PLACUTE_FRANA_DATA)),
                    "Cost (RON)": intreg(d.get(CONF_PLACUTE_FRANA_COST)),
                    "Km curent": intreg(d.get(CONF_KM_CURENT)),
                }
            ),
            d, "frane",
        ),
    ),
    # ── Discuri frână ──
    FleetSensorDescription(
        key="discuri_frana",
        translation_key="discuri_frana",
        icon="mdi:disc",
        native_unit_of_measurement="km",
        vizibil_fn=lambda d: _are_valoare(d, CONF_DISCURI_FRANA_KM_URMATOR),
        value_fn=lambda d: km_ramasi(
            d.get(CONF_KM_CURENT), d.get(CONF_DISCURI_FRANA_KM_URMATOR)
        ),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Km ultima schimbare": intreg(d.get(CONF_DISCURI_FRANA_KM_ULTIMUL)),
                    "Km următoarea schimbare": intreg(d.get(CONF_DISCURI_FRANA_KM_URMATOR)),
                    "Data schimbare": format_data_ro(d.get(CONF_DISCURI_FRANA_DATA)),
                    "Cost (RON)": intreg(d.get(CONF_DISCURI_FRANA_COST)),
                    "Km curent": intreg(d.get(CONF_KM_CURENT)),
                }
            ),
            d, "frane",
        ),
    ),
    # ── Trusă de prim ajutor (obligatorie în România) ──
    FleetSensorDescription(
        key="trusa_prim_ajutor",
        translation_key="trusa_prim_ajutor",
        icon="mdi:medical-bag",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Data expirare": format_data_ro(d.get(CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE)),
                "Stare": stare_document(d.get(CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Extinctor (obligatoriu în România) ──
    FleetSensorDescription(
        key="extinctor",
        translation_key="extinctor",
        icon="mdi:fire-extinguisher",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_EXTINCTOR_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_EXTINCTOR_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Data expirare": format_data_ro(d.get(CONF_EXTINCTOR_DATA_EXPIRARE)),
                "Capacitate (kg)": intreg(d.get(CONF_EXTINCTOR_CAPACITATE)),
                "Stare": stare_document(d.get(CONF_EXTINCTOR_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Șofer (date identificare) ──
    FleetSensorDescription(
        key="sofer",
        translation_key="sofer",
        icon="mdi:account-tie",
        vizibil_fn=lambda d: _are_valoare(d, CONF_SOFER_NUME),
        value_fn=lambda d: d.get(CONF_SOFER_NUME),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Nume": d.get(CONF_SOFER_NUME),
                "CNP": d.get(CONF_SOFER_CNP),
                "Nr. permis": d.get(CONF_SOFER_NR_PERMIS),
                "Categorii permis": d.get(CONF_SOFER_CATEGORII_PERMIS),
                "Atestat ADR nr.": d.get(CONF_SOFER_ATESTAT_ADR_NUMAR),
                "Atestat ADR expirare": format_data_ro(d.get(CONF_SOFER_ATESTAT_ADR_DATA_EXPIRARE)),
                "Atestat ADR clase": d.get(CONF_SOFER_ATESTAT_ADR_CLASE),
            }
        ),
    ),
    # ── Permis șofer ──
    FleetSensorDescription(
        key="sofer_permis",
        translation_key="sofer_permis",
        icon="mdi:card-account-details",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_SOFER_DATA_EXPIRARE_PERMIS),
        value_fn=lambda d: zile_ramase(d.get(CONF_SOFER_DATA_EXPIRARE_PERMIS)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Nr. permis": d.get(CONF_SOFER_NR_PERMIS),
                "Categorii": d.get(CONF_SOFER_CATEGORII_PERMIS),
                "Data expirare": format_data_ro(d.get(CONF_SOFER_DATA_EXPIRARE_PERMIS)),
                "Stare": stare_document(d.get(CONF_SOFER_DATA_EXPIRARE_PERMIS)),
            }
        ),
    ),
    # ── CPC (Certificat de Competență Profesională) ──
    FleetSensorDescription(
        key="sofer_cpc",
        translation_key="sofer_cpc",
        icon="mdi:certificate",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_SOFER_CPC_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_SOFER_CPC_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Număr CPC": d.get(CONF_SOFER_CPC_NUMAR),
                "Tip": d.get(CONF_SOFER_CPC_TIP),
                "Data expirare": format_data_ro(d.get(CONF_SOFER_CPC_DATA_EXPIRARE)),
                "Stare": stare_document(d.get(CONF_SOFER_CPC_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Card tahograf ──
    FleetSensorDescription(
        key="sofer_card_tahograf",
        translation_key="sofer_card_tahograf",
        icon="mdi:card-bulleted",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_SOFER_CARD_TAHOGRAF_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_SOFER_CARD_TAHOGRAF_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Număr card": d.get(CONF_SOFER_CARD_TAHOGRAF_NUMAR),
                "Data expirare": format_data_ro(d.get(CONF_SOFER_CARD_TAHOGRAF_DATA_EXPIRARE)),
                "Stare": stare_document(d.get(CONF_SOFER_CARD_TAHOGRAF_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Fișă medicală ──
    FleetSensorDescription(
        key="sofer_fisa_medicala",
        translation_key="sofer_fisa_medicala",
        icon="mdi:hospital-box",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_SOFER_FISA_MEDICALA_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_SOFER_FISA_MEDICALA_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Data examen": format_data_ro(d.get(CONF_SOFER_FISA_MEDICALA_DATA)),
                "Data expirare": format_data_ro(d.get(CONF_SOFER_FISA_MEDICALA_DATA_EXPIRARE)),
                "Apt/Inapt": d.get(CONF_SOFER_FISA_MEDICALA_APT),
                "Stare": stare_document(d.get(CONF_SOFER_FISA_MEDICALA_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Fișă psihologică ──
    FleetSensorDescription(
        key="sofer_fisa_psihologica",
        translation_key="sofer_fisa_psihologica",
        icon="mdi:brain",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Data examen": format_data_ro(d.get(CONF_SOFER_FISA_PSIHOLOGICA_DATA)),
                "Data expirare": format_data_ro(d.get(CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE)),
                "Stare": stare_document(d.get(CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Licență transport ──
    FleetSensorDescription(
        key="licenta_transport",
        translation_key="licenta_transport",
        icon="mdi:license",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_LICENTA_TRANSPORT_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_LICENTA_TRANSPORT_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Număr": d.get(CONF_LICENTA_TRANSPORT_NUMAR),
                "Tip": d.get(CONF_LICENTA_TRANSPORT_TIP),
                "Data expirare": format_data_ro(d.get(CONF_LICENTA_TRANSPORT_DATA_EXPIRARE)),
                "Stare": stare_document(d.get(CONF_LICENTA_TRANSPORT_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Copie conformă ──
    FleetSensorDescription(
        key="copie_conforma",
        translation_key="copie_conforma",
        icon="mdi:file-certificate",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_COPIE_CONFORMA_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_COPIE_CONFORMA_DATA_EXPIRARE)),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Număr": d.get(CONF_COPIE_CONFORMA_NUMAR),
                    "Data expirare": format_data_ro(d.get(CONF_COPIE_CONFORMA_DATA_EXPIRARE)),
                    "Stare": stare_document(d.get(CONF_COPIE_CONFORMA_DATA_EXPIRARE)),
                }
            ),
            d, "copie_conforma",
        ),
    ),
    # ── Licență comunitară ──
    FleetSensorDescription(
        key="licenta_comunitara",
        translation_key="licenta_comunitara",
        icon="mdi:earth",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_LICENTA_COMUNITARA_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_LICENTA_COMUNITARA_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Număr": d.get(CONF_LICENTA_COMUNITARA_NUMAR),
                "Data expirare": format_data_ro(d.get(CONF_LICENTA_COMUNITARA_DATA_EXPIRARE)),
                "Stare": stare_document(d.get(CONF_LICENTA_COMUNITARA_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── ADR (Transport mărfuri periculoase) ──
    FleetSensorDescription(
        key="adr_certificat",
        translation_key="adr_certificat",
        icon="mdi:hazard-lights",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_ADR_CERTIFICAT_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_ADR_CERTIFICAT_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Număr": d.get(CONF_ADR_CERTIFICAT_NUMAR),
                "Clase ADR": d.get(CONF_ADR_CLASE),
                "Data expirare": format_data_ro(d.get(CONF_ADR_CERTIFICAT_DATA_EXPIRARE)),
                "Consilier": d.get(CONF_ADR_CONSILIER_NUME),
                "Certificat consilier": d.get(CONF_ADR_CONSILIER_CERTIFICAT),
                "Expirare certificat consilier": format_data_ro(d.get(CONF_ADR_CONSILIER_DATA_EXPIRARE)),
                "Echipament complet": d.get(CONF_ADR_ECHIPAMENT_COMPLET),
                "Stare": stare_document(d.get(CONF_ADR_CERTIFICAT_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Tahograf ──
    FleetSensorDescription(
        key="tahograf",
        translation_key="tahograf",
        icon="mdi:smart-card-reader-outline",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Tip": d.get(CONF_TAHOGRAF_TIP),
                "Data verificare": format_data_ro(d.get(CONF_TAHOGRAF_DATA_VERIFICARE)),
                "Data următoare verificare": format_data_ro(d.get(CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE)),
                "Data calibrare": format_data_ro(d.get(CONF_TAHOGRAF_DATA_CALIBRARE)),
                "Stare": stare_document(d.get(CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE)),
            }
        ),
    ),
    # ── Combustibil ──
    FleetSensorDescription(
        key="combustibil",
        translation_key="combustibil",
        icon="mdi:gas-station",
        vizibil_fn=lambda d: _are_valoare(
            d, CONF_COMBUSTIBIL_CAPACITATE, CONF_COMBUSTIBIL_NIVEL
        ),
        value_fn=lambda d: (
            f"{intreg(d.get(CONF_COMBUSTIBIL_NIVEL))}%"
            if d.get(CONF_COMBUSTIBIL_NIVEL)
            else "Configurat"
        ),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Capacitate rezervor (L)": intreg(d.get(CONF_COMBUSTIBIL_CAPACITATE)),
                "Nivel (%)": intreg(d.get(CONF_COMBUSTIBIL_NIVEL)),
                "Consum mediu (L/100km)": decimal(d.get(CONF_COMBUSTIBIL_CONSUM_MEDIU)),
                "AdBlue capacitate (L)": intreg(d.get(CONF_ADBLUE_CAPACITATE)),
                "AdBlue nivel (%)": intreg(d.get(CONF_ADBLUE_NIVEL)),
            }
        ),
    ),
    # ── Alimentare (costuri combustibil) ──
    FleetSensorDescription(
        key="alimentare",
        translation_key="alimentare",
        icon="mdi:fuel",
        native_unit_of_measurement="RON",
        vizibil_fn=lambda d: _are_valoare(d, CONF_ALIMENTARE_COST),
        value_fn=lambda d: intreg(d.get(CONF_ALIMENTARE_COST)),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Data": format_data_ro(d.get(CONF_ALIMENTARE_DATA)),
                    "Litri": decimal(d.get(CONF_ALIMENTARE_LITRI)),
                    "Preț/litru": decimal(d.get(CONF_ALIMENTARE_PRET_LITRU)),
                    "Cost total": intreg(d.get(CONF_ALIMENTARE_COST)),
                    "Km la alimentare": intreg(d.get(CONF_ALIMENTARE_KM)),
                }
            ),
            d, "alimentare",
        ),
    ),
    # ── DPF (Filtru particule) ──
    FleetSensorDescription(
        key="dpf",
        translation_key="dpf",
        icon="mdi:air-filter",
        native_unit_of_measurement="km",
        vizibil_fn=lambda d: _are_valoare(d, CONF_DPF_KM_CURATARE),
        value_fn=lambda d: km_ramasi(
            d.get(CONF_KM_CURENT), d.get(CONF_DPF_KM_CURATARE)
        ),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Data curățare": format_data_ro(d.get(CONF_DPF_DATA_CURATARE)),
                    "Km curățare": intreg(d.get(CONF_DPF_KM_CURATARE)),
                    "Cost (RON)": intreg(d.get(CONF_DPF_COST)),
                }
            ),
            d, "dpf",
        ),
    ),
    # ── Turbo ──
    FleetSensorDescription(
        key="turbo",
        translation_key="turbo",
        icon="mdi:turbine",
        native_unit_of_measurement="km",
        vizibil_fn=lambda d: _are_valoare(d, CONF_TURBO_KM_REVIZIE),
        value_fn=lambda d: km_ramasi(
            d.get(CONF_KM_CURENT), d.get(CONF_TURBO_KM_REVIZIE)
        ),
        attributes_fn=lambda d: _cu_istoric(
            _filtrare_atribute(
                {
                    "Data revizie": format_data_ro(d.get(CONF_TURBO_DATA_REVIZIE)),
                    "Km revizie": intreg(d.get(CONF_TURBO_KM_REVIZIE)),
                    "Cost (RON)": intreg(d.get(CONF_TURBO_COST)),
                }
            ),
            d, "turbo",
        ),
    ),
    # ── Remorcă (identificare) ──
    FleetSensorDescription(
        key="remorca",
        translation_key="remorca",
        icon="mdi:truck-trailer",
        vizibil_fn=lambda d: _are_valoare(d, CONF_REMORCA_NR_INMATRICULARE),
        value_fn=lambda d: d.get(CONF_REMORCA_NR_INMATRICULARE),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Tip": d.get(CONF_REMORCA_TIP),
                "Marcă": d.get(CONF_REMORCA_MARCA),
                "MMA (kg)": intreg(d.get(CONF_REMORCA_MMA)),
                "Masa proprie (kg)": intreg(d.get(CONF_REMORCA_MASA_PROPRIE)),
                "Sarcina utilă (kg)": sarcina_utila(
                    d.get(CONF_REMORCA_MMA), d.get(CONF_REMORCA_MASA_PROPRIE)
                ),
                "Nr. axe": intreg(d.get(CONF_REMORCA_NR_AXE)),
                "An fabricație": intreg(d.get(CONF_REMORCA_AN_FABRICATIE)),
            }
        ),
    ),
    # ── Remorcă ITP ──
    FleetSensorDescription(
        key="remorca_itp",
        translation_key="remorca_itp",
        icon="mdi:clipboard-check",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_REMORCA_ITP_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_REMORCA_ITP_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Data expirare": format_data_ro(d.get(CONF_REMORCA_ITP_DATA_EXPIRARE)),
                "Stare": stare_document(d.get(CONF_REMORCA_ITP_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Remorcă RCA ──
    FleetSensorDescription(
        key="remorca_rca",
        translation_key="remorca_rca",
        icon="mdi:shield-car",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_REMORCA_RCA_DATA_EXPIRARE),
        value_fn=lambda d: zile_ramase(d.get(CONF_REMORCA_RCA_DATA_EXPIRARE)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Data expirare": format_data_ro(d.get(CONF_REMORCA_RCA_DATA_EXPIRARE)),
                "Stare": stare_document(d.get(CONF_REMORCA_RCA_DATA_EXPIRARE)),
            }
        ),
    ),
    # ── Remorcă Rovinieta ──
    FleetSensorDescription(
        key="remorca_rovinieta",
        translation_key="remorca_rovinieta",
        icon="mdi:road-variant",
        native_unit_of_measurement="zile",
        vizibil_fn=lambda d: _are_valoare(d, CONF_REMORCA_ROVINIETA_DATA_SFARSIT),
        value_fn=lambda d: zile_ramase(d.get(CONF_REMORCA_ROVINIETA_DATA_SFARSIT)),
        attributes_fn=lambda d: _filtrare_atribute(
            {
                "Data sfârșit": format_data_ro(d.get(CONF_REMORCA_ROVINIETA_DATA_SFARSIT)),
                "Stare": stare_document(d.get(CONF_REMORCA_ROVINIETA_DATA_SFARSIT)),
            }
        ),
    ),
    # ── Cost Total ──
    FleetSensorDescription(
        key="cost_total",
        translation_key="cost_total",
        icon="mdi:cash-multiple",
        native_unit_of_measurement="RON",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        vizibil_fn=lambda d: _are_costuri(d),
        value_fn=_cost_total_value,
        attributes_fn=_cost_total_attr,
    ),
]


# ─────────────────────────────────────────────
# Configurare platformă
# ─────────────────────────────────────────────


def _senzor_vizibil(desc: FleetSensorDescription, date_vehicul: dict[str, Any]) -> bool:
    """Verifică dacă un senzor trebuie creat pe baza datelor disponibile.

    Senzorii fără vizibil_fn sunt mereu vizibili (ex: Informații).
    Ceilalți apar doar când au date completate.
    """
    if desc.vizibil_fn is None:
        return True
    return desc.vizibil_fn(date_vehicul)


def _is_license_valid(hass: HomeAssistant) -> bool:
    """Verifică dacă licența este validă (real-time)."""
    mgr = hass.data.get(DOMAIN, {}).get(LICENSE_DATA_KEY)
    if mgr is None:
        return False
    return mgr.is_valid


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurează senzorii pentru un vehicul din flotă."""
    nr_inmatriculare = entry.data[CONF_NR_INMATRICULARE]
    numar_normalizat = normalizeaza_numar(nr_inmatriculare)

    _LOGGER.debug(
        "[Fleet:Sensor] ── async_setup_entry ── vehicul=%s, entry_id=%s",
        nr_inmatriculare,
        entry.entry_id,
    )

    # Verificare licență
    licenta_valida = _is_license_valid(hass)
    _LOGGER.debug(
        "[Fleet:Sensor] Licență validă=%s",
        licenta_valida,
    )

    # Combinăm data + options într-un singur dicționar
    date_vehicul: dict[str, Any] = {**entry.data, **entry.options}
    _LOGGER.debug(
        "[Fleet:Sensor] Date vehicul: %d chei (data=%d, options=%d)",
        len(date_vehicul),
        len(entry.data),
        len(entry.options),
    )

    # Determinăm care senzori sunt activi și care nu
    chei_active: set[str] = set()
    chei_inactive: set[str] = set()

    if not licenta_valida:
        # ── Fără licență: DOAR senzorul LicentaNecesaraSensor ──
        # Nu se creează alți senzori.
        chei_active = set()
        for desc in SENSOR_DESCRIPTIONS:
            chei_inactive.add(desc.key)
        _LOGGER.debug(
            "[Fleet:Sensor] %s: fără licență — doar senzorul LicentaNecesaraSensor",
            nr_inmatriculare,
        )
    else:
        for desc in SENSOR_DESCRIPTIONS:
            if _senzor_vizibil(desc, date_vehicul):
                chei_active.add(desc.key)
            else:
                chei_inactive.add(desc.key)

    _LOGGER.debug(
        "[Fleet:Sensor] %s: %d senzori activi, %d inactivi (din %d total)",
        nr_inmatriculare,
        len(chei_active),
        len(chei_inactive),
        len(SENSOR_DESCRIPTIONS),
    )

    # Curățăm entitățile orfane din Entity Registry
    if chei_inactive:
        _curata_entitati_orfane(hass, entry, numar_normalizat, chei_inactive)

    entitati: list[SensorEntity] = []

    if not licenta_valida:
        # Creează senzorul de licență necesară
        entitati.append(
            LicentaNecesaraSensor(
                entry=entry,
                nr_inmatriculare=nr_inmatriculare,
                numar_normalizat=numar_normalizat,
                date_vehicul=date_vehicul,
            )
        )
    else:
        # Curăță senzorul de licență orfan (dacă exista anterior)
        registru = er.async_get(hass)
        licenta_uid = f"fleet_licenta_{numar_normalizat}"
        entitate_licenta = registru.async_get_entity_id("sensor", DOMAIN, licenta_uid)
        if entitate_licenta is not None:
            registru.async_remove(entitate_licenta)
            _LOGGER.debug(
                "[Fleet:Sensor] Entitate LicentaNecesaraSensor orfană eliminată: %s",
                entitate_licenta,
            )

        # Creează senzorii obișnuiți din Fleet
        entitati = [
            FleetSensor(
                entry=entry,
                description=desc,
                nr_inmatriculare=nr_inmatriculare,
                numar_normalizat=numar_normalizat,
                date_vehicul=date_vehicul,
            )
            for desc in SENSOR_DESCRIPTIONS
            if desc.key in chei_active
        ]

    _LOGGER.debug(
        "[Fleet:Sensor] %s: adaug %d entități senzor",
        nr_inmatriculare,
        len(entitati),
    )

    async_add_entities(entitati, update_before_add=True)
    _LOGGER.debug("[Fleet:Sensor] %s: senzori adăugați cu succes", nr_inmatriculare)


def _curata_entitati_orfane(
    hass: HomeAssistant,
    entry: ConfigEntry,
    numar_normalizat: str,
    chei_inactive: set[str],
) -> None:
    """Elimină din Entity Registry entitățile care nu mai sunt necesare.

    Aceasta rezolvă problema „entitate nu mai este furnizată de integrare"
    când se schimbă condițiile de vizibilitate ale unui senzor.
    """
    registru = er.async_get(hass)

    for cheie in chei_inactive:
        unique_id = f"fleet_{numar_normalizat}_{cheie}"

        entitate = registru.async_get_entity_id("sensor", DOMAIN, unique_id)
        if entitate is not None:
            _LOGGER.debug(
                "[Fleet:Sensor] Elimin entitatea orfană: %s (unique_id: %s)",
                entitate,
                unique_id,
            )
            registru.async_remove(entitate)


# ─────────────────────────────────────────────
# Entitate senzor
# ─────────────────────────────────────────────


class FleetSensor(SensorEntity):
    """Senzor pentru un aspect al vehiculului din flotă."""

    entity_description: FleetSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        description: FleetSensorDescription,
        nr_inmatriculare: str,
        numar_normalizat: str,
        date_vehicul: dict[str, Any],
    ) -> None:
        """Inițializează senzorul."""
        self.entity_description = description
        self._entry = entry
        self._nr_inmatriculare = nr_inmatriculare
        self._numar_normalizat = numar_normalizat
        self._date_vehicul = date_vehicul

        # ID unic: fleet_{numar_normalizat}_{tip_senzor}
        self._attr_unique_id = f"fleet_{numar_normalizat}_{description.key}"

    @property
    def _license_valid(self) -> bool:
        """Verificare real-time a licenței (nu boolean static)."""
        mgr = self.hass.data.get(DOMAIN, {}).get(LICENSE_DATA_KEY)
        if mgr is None:
            return False
        return mgr.is_valid

    @property
    def device_info(self) -> DeviceInfo:
        """Informații despre dispozitiv (vehiculul din flotă)."""
        marca = self._date_vehicul.get(CONF_MARCA, "")
        model = self._date_vehicul.get(CONF_MODEL, "")
        return DeviceInfo(
            identifiers={(DOMAIN, self._numar_normalizat)},
            name=f"Fleet {self._nr_inmatriculare}",
            manufacturer=marca or None,
            model=model or None,
            entry_type=None,
        )

    @property
    def native_value(self) -> Any:
        """Returnează starea senzorului.

        Fără licență, returnează None. Senzorul de licență (LicentaNecesaraSensor)
        va afișa mesajul corespunzător. Aceasta evită conflicte cu
        native_unit_of_measurement pe senzorii numerici.
        """
        if not self._license_valid:
            return None
        if self.entity_description.value_fn is None:
            return None
        return self.entity_description.value_fn(self._date_vehicul)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Returnează atributele suplimentare ale senzorului."""
        if not self._license_valid:
            return {}
        if self.entity_description.attributes_fn is None:
            return {}
        return self.entity_description.attributes_fn(self._date_vehicul)


# ─────────────────────────────────────────────
# Senzor de licență necesară
# ─────────────────────────────────────────────


class LicentaNecesaraSensor(SensorEntity):
    """Senzor care afișează 'Licență necesară' când nu există licență validă."""

    _attr_icon = "mdi:license"
    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        nr_inmatriculare: str,
        numar_normalizat: str,
        date_vehicul: dict[str, Any],
    ) -> None:
        """Inițializează senzorul."""
        self._entry = entry
        self._nr_inmatriculare = nr_inmatriculare
        self._numar_normalizat = numar_normalizat
        self._date_vehicul = date_vehicul
        self._attr_unique_id = f"fleet_licenta_{numar_normalizat}"
        self._attr_name = "Licență necesară"
        # OBLIGATORIU: entity_id explicit — pattern consistent între integrări
        self.entity_id = f"sensor.fleet_licenta_{numar_normalizat}"

    @property
    def device_info(self) -> DeviceInfo:
        """Informații despre dispozitiv (vehiculul din flotă)."""
        marca = self._date_vehicul.get(CONF_MARCA, "")
        model = self._date_vehicul.get(CONF_MODEL, "")
        return DeviceInfo(
            identifiers={(DOMAIN, self._numar_normalizat)},
            name=f"Fleet {self._nr_inmatriculare}",
            manufacturer=marca or None,
            model=model or None,
            entry_type=None,
        )

    @property
    def native_value(self) -> str:
        """Returnează status-ul licenței — vizibil clar pentru utilizator."""
        mgr = self.hass.data.get(DOMAIN, {}).get(LICENSE_DATA_KEY)
        if mgr is not None:
            status = mgr.status
            if status == "expired":
                return "Licență expirată"
            if status == "trial":
                days = mgr.trial_days_remaining
                return f"Trial — {days} zile rămase" if days > 0 else "Trial expirat"
        return "Licență necesară"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Returnează informații de diagnostic: status, zile rămase, link achiziție."""
        attrs: dict[str, Any] = {
            "nr_inmatriculare": self._nr_inmatriculare,
        }
        mgr = self.hass.data.get(DOMAIN, {}).get(LICENSE_DATA_KEY)
        if mgr is not None:
            attrs["status_licență"] = mgr.status
            if mgr.status == "trial":
                attrs["zile_trial_rămase"] = mgr.trial_days_remaining
            attrs["informații"] = (
                "Achiziționează o licență de pe hubinteligent.org "
                "sau din Buy Me a Coffee."
            )
        return attrs
