"""
Integrarea Fleet pentru Home Assistant.

Gestionarea flotei de vehicule de transport, documentelor
și notificărilor pentru expirări.
"""

from __future__ import annotations

import json
import logging
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

import voluptuous as vol
from homeassistant.components import persistent_notification
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

from .const import (
    BACKUP_VERSION,
    CONF_KM_CURENT,
    CONF_NR_INMATRICULARE,
    DOMAIN,
    LICENSE_DATA_KEY,
    PLATFORMS,
    SERVICE_ACTUALIZEAZA_DATE,
    SERVICE_BACKUP_FLOTA,
    SERVICE_EXPORTA_DATE,
    SERVICE_IMPORTA_DATE,
    SERVICE_RESTORE_FLOTA,
    normalizeaza_numar,
)
from .helpers import aplatizeaza_optiuni, structureaza_optiuni
from .license import LicenseManager

_LOGGER = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Scheme pentru servicii
# ─────────────────────────────────────────────

SCHEMA_ACTUALIZEAZA_DATE = vol.Schema(
    {
        vol.Required(CONF_NR_INMATRICULARE): cv.string,
        vol.Required(CONF_KM_CURENT): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=9_999_999)
        ),
    }
)

SCHEMA_EXPORTA_DATE = vol.Schema(
    {
        vol.Required(CONF_NR_INMATRICULARE): cv.string,
    }
)

SCHEMA_IMPORTA_DATE = vol.Schema(
    {
        vol.Required("cale_fisier"): cv.string,
    }
)

SCHEMA_RESTORE_FLOTA = vol.Schema(
    {
        vol.Required("cale_fisier"): cv.string,
    }
)

# Caractere permise în numere de înmatriculare (alfanumerice)
import re as _re

_NUMAR_SAFE_RE = _re.compile(r"^[a-z0-9]+$")


def _valideaza_cale_fisier(
    hass: HomeAssistant, cale: str, extensie: str = ""
) -> Path:
    """Validează și rezolvă calea, restricționând-o la /config/.

    Aruncă ValueError dacă:
    - calea rezolvată iese din directorul HA config
    - calea conține componente '..'
    - extensia nu corespunde (dacă e specificată)
    """
    cale_path = Path(cale)
    config_dir = Path(hass.config.path()).resolve()
    cale_rezolvata = cale_path.resolve()

    # Verificare path traversal
    if ".." in cale_path.parts:
        raise ValueError(
            f"Calea conține componente nepermise (..): {cale}"
        )

    if not str(cale_rezolvata).startswith(str(config_dir)):
        raise ValueError(
            f"Calea trebuie să fie în directorul config ({config_dir}): {cale}"
        )

    if extensie and not cale_rezolvata.name.endswith(extensie):
        raise ValueError(
            f"Fișierul trebuie să aibă extensia {extensie}: {cale}"
        )

    return cale_rezolvata


def _sanitize_nr_for_path(nr_norm: str) -> str:
    """Verifică că nr normalizat e sigur pentru utilizare în path-uri.

    Aruncă ValueError dacă conține caractere neașteptate.
    """
    if not _NUMAR_SAFE_RE.match(nr_norm):
        raise ValueError(
            f"Număr de înmatriculare normalizat conține caractere "
            f"nepermise: {nr_norm!r}"
        )
    return nr_norm


def _valideaza_zip_entry_name(name: str) -> bool:
    """Verifică că un entry din ZIP este sigur (fără path traversal)."""
    if ".." in name or name.startswith("/") or name.startswith("\\"):
        return False
    # Verifică că path-ul normalizat nu iese din rădăcina ZIP
    normalized = Path(name).as_posix()
    if normalized.startswith("..") or "/../" in normalized:
        return False
    return True


# ─────────────────────────────────────────────
# Setup / Unload
# ─────────────────────────────────────────────


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurează o intrare pentru un vehicul de transport."""
    nr = entry.data.get(CONF_NR_INMATRICULARE, "?")
    _LOGGER.debug(
        "[Fleet] ── async_setup_entry ── vehicul=%s, entry_id=%s",
        nr,
        entry.entry_id,
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry

    # ── Inițializare License Manager (o singură instanță per domeniu) ──
    if LICENSE_DATA_KEY not in hass.data.get(DOMAIN, {}):
        _LOGGER.debug("[Fleet] Inițializez LicenseManager (prima entry)")
        license_mgr = LicenseManager(hass)
        await license_mgr.async_load()
        hass.data[DOMAIN][LICENSE_DATA_KEY] = license_mgr
        _LOGGER.debug(
            "[Fleet] LicenseManager: status=%s, valid=%s, fingerprint=%s...",
            license_mgr.status,
            license_mgr.is_valid,
            license_mgr.fingerprint[:16],
        )

        # Heartbeat periodic — intervalul vine de la server (via valid_until)
        from datetime import timedelta

        interval_sec = license_mgr.check_interval_seconds
        _LOGGER.debug(
            "[Fleet] Programez heartbeat periodic la fiecare %d secunde (%d ore)",
            interval_sec,
            interval_sec // 3600,
        )

        async def _heartbeat_periodic(_now: Any) -> None:
            """Verifică statusul la server dacă cache-ul a expirat."""
            mgr: LicenseManager | None = hass.data.get(DOMAIN, {}).get(
                LICENSE_DATA_KEY
            )
            if not mgr:
                _LOGGER.debug("[Fleet] Heartbeat: LicenseManager nu există, skip")
                return
            if mgr.needs_heartbeat:
                _LOGGER.debug("[Fleet] Heartbeat: cache expirat, verific la server")
                await mgr.async_heartbeat()
            else:
                _LOGGER.debug("[Fleet] Heartbeat: cache valid, nu e nevoie de verificare")

        # Stocăm cancel-ul heartbeat-ului la nivel de domeniu,
        # NU pe entry (ca să nu dispară când se șterge prima entry)
        cancel_heartbeat = async_track_time_interval(
            hass,
            _heartbeat_periodic,
            timedelta(seconds=interval_sec),
        )
        hass.data[DOMAIN]["_cancel_heartbeat"] = cancel_heartbeat
        _LOGGER.debug("[Fleet] Heartbeat programat și stocat în hass.data")

        # ── Notificare re-enable (dacă a fost dezactivată anterior) ──
        was_disabled = hass.data.pop(f"{DOMAIN}_was_disabled", False)
        if was_disabled:
            await license_mgr.async_notify_event("integration_enabled")

        if not license_mgr.is_valid:
            _LOGGER.warning(
                "[Fleet] Integrarea nu are licență validă. "
                "Senzorii vor afișa 'Licență necesară'."
            )
        elif license_mgr.is_trial_valid:
            _LOGGER.info(
                "[Fleet] Perioadă de evaluare — %d zile rămase",
                license_mgr.trial_days_remaining,
            )
        else:
            _LOGGER.info(
                "[Fleet] Licență activă — tip: %s",
                license_mgr.license_type,
            )
    else:
        _LOGGER.debug(
            "[Fleet] LicenseManager există deja (entry suplimentară: %s)", nr
        )

    entry.async_on_unload(entry.add_update_listener(_async_actualizare_optiuni))

    _LOGGER.debug("[Fleet] Încep forward_entry_setups pentru platforme: %s", PLATFORMS)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("[Fleet] Platforme configurate pentru %s", nr)

    await _async_inregistreaza_servicii(hass)

    _LOGGER.info("[Fleet] Vehiculul %s configurat cu succes", nr)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descarcă o intrare (vehicul șters)."""
    nr = entry.data.get(CONF_NR_INMATRICULARE, "?")
    _LOGGER.debug(
        "[Fleet] ── async_unload_entry ── vehicul=%s, entry_id=%s",
        nr,
        entry.entry_id,
    )

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    _LOGGER.debug("[Fleet] Unload platforme: %s", "OK" if unload_ok else "EȘUAT")

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        _LOGGER.debug("[Fleet] Entry %s eliminat din hass.data", nr)

        # Verifică dacă mai sunt entry-uri active
        entry_ids_ramase = {
            e.entry_id
            for e in hass.config_entries.async_entries(DOMAIN)
            if e.entry_id != entry.entry_id
        }

        _LOGGER.debug(
            "[Fleet] Entry-uri rămase după unload: %d (%s)",
            len(entry_ids_ramase),
            entry_ids_ramase or "niciuna",
        )

        if not entry_ids_ramase:
            _LOGGER.info("[Fleet] Ultimul vehicul descărcat — curăț domeniul complet")

            # ── Notificare lifecycle (înainte de cleanup!) ──
            mgr = hass.data[DOMAIN].get(LICENSE_DATA_KEY)
            if mgr and not hass.is_stopping:
                if entry.disabled_by:
                    await mgr.async_notify_event("integration_disabled")
                    # Flag pentru async_setup_entry: la re-enable, trimitem "enabled"
                    hass.data[f"{DOMAIN}_was_disabled"] = True
                else:
                    # Salvăm fingerprint-ul pentru async_remove_entry
                    # (care se apelează DUPĂ ce LicenseManager e distrus)
                    hass.data.setdefault(f"{DOMAIN}_notify", {}).update({
                        "fingerprint": mgr.fingerprint,
                        "license_key": mgr._data.get("license_key", ""),
                    })
                    _LOGGER.debug(
                        "[Fleet] Fingerprint salvat pentru async_remove_entry"
                    )

            # Oprește heartbeat-ul
            cancel_hb = hass.data[DOMAIN].pop("_cancel_heartbeat", None)
            if cancel_hb:
                cancel_hb()
                _LOGGER.debug("[Fleet] Heartbeat periodic oprit")

            # Elimină LicenseManager
            hass.data[DOMAIN].pop(LICENSE_DATA_KEY, None)
            _LOGGER.debug("[Fleet] LicenseManager eliminat")

            # Elimină domeniul
            hass.data.pop(DOMAIN, None)
            _LOGGER.debug("[Fleet] hass.data[%s] eliminat complet", DOMAIN)

            # Elimină serviciile
            for svc in (
                SERVICE_ACTUALIZEAZA_DATE,
                SERVICE_EXPORTA_DATE,
                SERVICE_IMPORTA_DATE,
                SERVICE_BACKUP_FLOTA,
                SERVICE_RESTORE_FLOTA,
            ):
                hass.services.async_remove(DOMAIN, svc)
                _LOGGER.debug("[Fleet] Serviciu eliminat: %s.%s", DOMAIN, svc)

            _LOGGER.info("[Fleet] Cleanup complet — domeniul %s descărcat", DOMAIN)
    else:
        _LOGGER.error("[Fleet] Unload EȘUAT pentru %s", nr)

    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Curăță complet la ștergerea unui vehicul de transport.

    Elimină dispozitivul și entitățile orfane din registry.
    """
    nr_inmatriculare = entry.data.get(CONF_NR_INMATRICULARE, "")
    numar_normalizat = normalizeaza_numar(nr_inmatriculare)

    _LOGGER.debug(
        "[Fleet] ── async_remove_entry ── vehicul=%s, entry_id=%s",
        nr_inmatriculare,
        entry.entry_id,
    )

    registru_entitati = er.async_get(hass)
    entitati_de_sters = er.async_entries_for_config_entry(
        registru_entitati, entry.entry_id
    )
    _LOGGER.debug(
        "[Fleet] Entități de șters pentru %s: %d",
        nr_inmatriculare,
        len(entitati_de_sters),
    )
    for entitate in entitati_de_sters:
        _LOGGER.debug("[Fleet] Elimin entitatea: %s", entitate.entity_id)
        registru_entitati.async_remove(entitate.entity_id)

    registru_dispozitive = dr.async_get(hass)
    dispozitiv = registru_dispozitive.async_get_device(
        identifiers={(DOMAIN, numar_normalizat)}
    )
    if dispozitiv is not None:
        _LOGGER.debug(
            "[Fleet] Elimin dispozitivul: %s (id: %s)",
            dispozitiv.name,
            dispozitiv.id,
        )
        registru_dispozitive.async_remove_device(dispozitiv.id)
    else:
        _LOGGER.debug(
            "[Fleet] Dispozitivul pentru %s nu a fost găsit (deja eliminat?)",
            nr_inmatriculare,
        )

    _LOGGER.info("[Fleet] Vehiculul %s a fost complet eliminat", nr_inmatriculare)

    # ── Notificare „integration_removed" dacă e ultima intrare ──
    # LicenseManager nu mai există (distrus în async_unload_entry),
    # dar fingerprint-ul a fost salvat în hass.data[f"{DOMAIN}_notify"].
    remaining = hass.config_entries.async_entries(DOMAIN)
    if not remaining:
        notify_data = hass.data.pop(f"{DOMAIN}_notify", None)
        if notify_data and notify_data.get("fingerprint"):
            await _send_lifecycle_event(
                hass,
                notify_data["fingerprint"],
                notify_data.get("license_key", ""),
                "integration_removed",
            )


async def _send_lifecycle_event(
    hass: HomeAssistant, fingerprint: str, license_key: str, action: str
) -> None:
    """Trimite un eveniment lifecycle direct (fără LicenseManager).

    Folosit în async_remove_entry când LicenseManager nu mai există.
    """
    import hashlib
    import hmac as hmac_lib
    import time

    import aiohttp

    from .license import INTEGRATION, LICENSE_API_URL

    timestamp = int(time.time())
    payload = {
        "fingerprint": fingerprint,
        "timestamp": timestamp,
        "action": action,
        "license_key": license_key,
        "integration": INTEGRATION,
    }
    # HMAC cu fingerprint ca cheie (identic cu LicenseManager._compute_request_hmac)
    data = {k: v for k, v in payload.items() if k != "hmac"}
    import json as _json
    msg = _json.dumps(data, sort_keys=True).encode()
    payload["hmac"] = hmac_lib.new(
        fingerprint.encode(), msg, hashlib.sha256
    ).hexdigest()

    try:
        session = async_get_clientsession(hass)
        async with session.post(
            f"{LICENSE_API_URL}/notify",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=10),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Fleet-HA-Integration/3.0",
            },
        ) as resp:
            if resp.status == 200:
                result = await resp.json()
                if not result.get("success"):
                    _LOGGER.warning(
                        "[Fleet] Server a refuzat '%s': %s",
                        action, result.get("error"),
                    )
    except Exception as err:  # noqa: BLE001
        _LOGGER.debug("[Fleet] Nu s-a putut raporta '%s': %s", action, err)


async def _async_actualizare_optiuni(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Reîncarcă intrarea când opțiunile se schimbă."""
    _LOGGER.debug(
        "[Fleet] Opțiuni actualizate pentru %s – reîncarc",
        entry.data.get(CONF_NR_INMATRICULARE),
    )
    await hass.config_entries.async_reload(entry.entry_id)


# ─────────────────────────────────────────────
# Utilitar intern: caută vehicul după nr. înmatriculare
# ─────────────────────────────────────────────


def _gaseste_vehicul(
    hass: HomeAssistant, nr_inmatriculare: str
) -> ConfigEntry | None:
    """Returnează ConfigEntry pentru vehiculul dat sau None."""
    for entry in hass.config_entries.async_entries(DOMAIN):
        if entry.data.get(CONF_NR_INMATRICULARE) == nr_inmatriculare:
            return entry
    return None


# ─────────────────────────────────────────────
# Înregistrare servicii
# ─────────────────────────────────────────────


async def _async_inregistreaza_servicii(hass: HomeAssistant) -> None:
    """Înregistrează serviciile domeniului (o singură dată)."""
    if hass.services.has_service(DOMAIN, SERVICE_ACTUALIZEAZA_DATE):
        return

    # ── Actualizare date (kilometraj) ──

    async def _handle_actualizeaza_date(call: ServiceCall) -> None:
        """Procesează apelul de actualizare date (kilometraj)."""
        nr_inmatriculare = call.data[CONF_NR_INMATRICULARE].strip().upper()
        km_nou = call.data[CONF_KM_CURENT]

        _LOGGER.debug(
            "Actualizez datele pentru %s – km: %d",
            nr_inmatriculare,
            km_nou,
        )

        entry = _gaseste_vehicul(hass, nr_inmatriculare)

        if entry is None:
            _LOGGER.warning(
                "[Fleet] Nu am găsit vehiculul cu nr. %s", nr_inmatriculare
            )
            return

        optiuni_noi: dict[str, Any] = {
            **entry.options,
            CONF_KM_CURENT: km_nou,
        }
        hass.config_entries.async_update_entry(entry, options=optiuni_noi)

    # ── Export date vehicul ──

    async def _handle_exporta_date(call: ServiceCall) -> None:
        """Exportă datele unui vehicul într-un fișier JSON."""
        nr_inmatriculare = call.data[CONF_NR_INMATRICULARE].strip().upper()
        nr_norm = normalizeaza_numar(nr_inmatriculare)

        try:
            _sanitize_nr_for_path(nr_norm)
        except ValueError as err:
            _LOGGER.error("[Fleet] Export: %s", err)
            return

        entry = _gaseste_vehicul(hass, nr_inmatriculare)

        if entry is None:
            _LOGGER.warning("[Fleet] Export: nu am găsit vehiculul %s", nr_inmatriculare)
            persistent_notification.async_create(
                hass,
                f"Nu am găsit vehiculul cu nr. {nr_inmatriculare}.",
                title="Export eșuat",
                notification_id=f"fleet_export_{nr_norm}",
            )
            return

        date_export = {
            "version": BACKUP_VERSION,
            "integration": DOMAIN,
            "nr_inmatriculare": nr_inmatriculare,
            "data_export": datetime.now().isoformat(),
            **structureaza_optiuni(dict(entry.options)),
        }

        cale = Path(hass.config.path(f"fleet_backup_{nr_norm}.json"))

        def _scrie() -> None:
            cale.write_text(
                json.dumps(date_export, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        await hass.async_add_executor_job(_scrie)

        _LOGGER.info("Export reușit: %s → %s", nr_inmatriculare, cale)
        persistent_notification.async_create(
            hass,
            (
                f"Datele vehiculului **{nr_inmatriculare}** au fost exportate "
                f"in:\n`{cale}`"
            ),
            title="Export reușit",
            notification_id=f"fleet_export_{nr_norm}",
        )

    # ── Import date vehicul ──

    async def _handle_importa_date(call: ServiceCall) -> None:
        """Importă datele unui vehicul dintr-un fișier JSON."""
        cale_raw = call.data["cale_fisier"]

        # SEC-01: Validare path — restricționare la directorul config
        try:
            cale_valida = _valideaza_cale_fisier(hass, cale_raw, ".json")
        except ValueError as err:
            _notifica_eroare_import(hass, str(err))
            return

        def _citeste() -> dict:
            return json.loads(cale_valida.read_text(encoding="utf-8"))

        try:
            date_import = await hass.async_add_executor_job(_citeste)
        except FileNotFoundError:
            _notifica_eroare_import(
                hass, f"Fișierul nu a fost găsit: {cale_valida}"
            )
            return
        except (json.JSONDecodeError, OSError) as err:
            _notifica_eroare_import(
                hass, f"Eroare la citirea fișierului: {err}"
            )
            return

        if (
            not isinstance(date_import, dict)
            or CONF_NR_INMATRICULARE not in date_import
        ):
            _notifica_eroare_import(
                hass,
                "Structura JSON este invalida. Fisierul trebuie sa contina "
                "campul 'nr_inmatriculare'.",
            )
            return

        nr = date_import[CONF_NR_INMATRICULARE].strip().upper()
        nr_norm = normalizeaza_numar(nr)

        # SEC-03: Toate versiunile trec prin aplatizeaza_optiuni (whitelist)
        versiune = date_import.get("version", 1)
        if versiune >= 2:
            optiuni = aplatizeaza_optiuni(date_import)
        elif "optiuni" in date_import and isinstance(
            date_import["optiuni"], dict
        ):
            # v1: wrap opțiunile într-o structură temporară și filtrăm
            optiuni_raw = date_import["optiuni"]
            optiuni = {
                k: v for k, v in optiuni_raw.items()
                if isinstance(k, str) and not k.startswith("_")
            }
        else:
            _notifica_eroare_import(
                hass,
                "Structura JSON este invalida. Fisierul v1 trebuie sa "
                "contina campul 'optiuni'.",
            )
            return

        entry = _gaseste_vehicul(hass, nr)

        if entry is None:
            result = await hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": "import"},
                data={CONF_NR_INMATRICULARE: nr},
            )
            if result.get("type") == "create_entry":
                entry = result["result"]
            else:
                motiv = result.get("reason", "necunoscut")
                _notifica_eroare_import(
                    hass,
                    f"Nu am putut crea vehiculul {nr}: {motiv}",
                )
                return

        hass.config_entries.async_update_entry(entry, options=optiuni)

        _LOGGER.info("Import reușit pentru %s din %s", nr, cale)
        persistent_notification.async_create(
            hass,
            f"Datele vehiculului **{nr}** au fost importate cu succes.",
            title="Import reușit",
            notification_id=f"fleet_import_{nr_norm}",
        )

    # ── Backup flotă (toate vehiculele → ZIP) ──

    async def _handle_backup_flota(call: ServiceCall) -> None:
        """Exportă toate vehiculele într-o singură arhivă ZIP.

        Structura ZIP-ului:
        fleet_backup_YYYYMMDD_HHMMSS.zip
        ├── metadata.json          (versiune, data, nr vehicule)
        └── vehicule/
            ├── b123abc.json       (config + opțiuni structurate)
            ├── bh09xyz.json
            └── ...
        """
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            _LOGGER.warning("[Fleet] Backup: niciun vehicul configurat")
            persistent_notification.async_create(
                hass,
                "Nu există vehicule configurate pentru backup.",
                title="Backup eșuat",
                notification_id="fleet_backup_flota",
            )
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(hass.config.path("fleet_backups"))

        metadata = {
            "version": BACKUP_VERSION,
            "integration": DOMAIN,
            "data_backup": datetime.now().isoformat(),
            "nr_vehicule": len(entries),
            "vehicule": [],
        }

        vehicule_data: dict[str, dict[str, Any]] = {}

        for entry in entries:
            nr = entry.data.get(CONF_NR_INMATRICULARE, "")
            nr_norm = normalizeaza_numar(nr)

            # SEC-04: Sanitizare nr pentru utilizare ca filename în ZIP
            try:
                _sanitize_nr_for_path(nr_norm)
            except ValueError:
                _LOGGER.warning(
                    "[Fleet] Backup: nr normalizat nesigur, skip: %r",
                    nr_norm,
                )
                continue

            vehicul_export = {
                "version": BACKUP_VERSION,
                "integration": DOMAIN,
                "nr_inmatriculare": nr,
                "data_export": datetime.now().isoformat(),
                **structureaza_optiuni(dict(entry.options)),
            }

            vehicule_data[nr_norm] = vehicul_export
            metadata["vehicule"].append(
                {
                    "nr_inmatriculare": nr,
                    "nr_optiuni": len(entry.options),
                }
            )

        def _scrie_zip() -> Path:
            backup_dir.mkdir(parents=True, exist_ok=True)
            cale_zip = backup_dir / f"fleet_backup_{timestamp}.zip"

            with zipfile.ZipFile(
                cale_zip, "w", zipfile.ZIP_DEFLATED
            ) as zf:
                # Metadata
                zf.writestr(
                    "metadata.json",
                    json.dumps(metadata, ensure_ascii=False, indent=2),
                )

                # Fiecare vehicul într-un JSON separat
                for nr_norm, date_vehicul in vehicule_data.items():
                    zf.writestr(
                        f"vehicule/{nr_norm}.json",
                        json.dumps(
                            date_vehicul, ensure_ascii=False, indent=2
                        ),
                    )

            return cale_zip

        cale_zip = await hass.async_add_executor_job(_scrie_zip)

        _LOGGER.info(
            "[Fleet] Backup flotă reușit: %d vehicule → %s",
            len(entries),
            cale_zip,
        )
        persistent_notification.async_create(
            hass,
            (
                f"Backup complet: **{len(entries)}** vehicule salvate în:\n"
                f"`{cale_zip}`"
            ),
            title="Backup flotă reușit",
            notification_id="fleet_backup_flota",
        )

    # ── Restore flotă (ZIP → toate vehiculele) ──

    async def _handle_restore_flota(call: ServiceCall) -> None:
        """Importă toate vehiculele dintr-o arhivă ZIP.

        Comportament:
        - Vehicul existent → actualizează opțiunile
        - Vehicul inexistent → creează config entry nouă
        - Notifică rezultatul (câte au reușit / eșuat)
        """
        cale_raw = call.data["cale_fisier"]

        # SEC-01: Validare path — restricționare la directorul config
        try:
            cale_valida = _valideaza_cale_fisier(hass, cale_raw, ".zip")
        except ValueError as err:
            _notifica_eroare_import(hass, str(err))
            return

        def _citeste_zip() -> tuple[dict, dict[str, dict]]:
            if not cale_valida.exists():
                raise FileNotFoundError(
                    f"Fișierul nu a fost găsit: {cale_valida}"
                )

            with zipfile.ZipFile(cale_valida, "r") as zf:
                # Citește metadata
                try:
                    meta = json.loads(zf.read("metadata.json"))
                except KeyError:
                    meta = {}

                # Citește toate vehiculele
                vehicule: dict[str, dict] = {}
                for name in zf.namelist():
                    # SEC-02: Validare entry name (anti zip-slip)
                    if not _valideaza_zip_entry_name(name):
                        _LOGGER.warning(
                            "[Fleet] Restore: entry suspect ignorat: %s",
                            name,
                        )
                        continue
                    if name.startswith("vehicule/") and name.endswith(
                        ".json"
                    ):
                        content = json.loads(zf.read(name))
                        nr = content.get(CONF_NR_INMATRICULARE, "")
                        if nr:
                            vehicule[nr] = content

            return meta, vehicule

        try:
            meta, vehicule = await hass.async_add_executor_job(
                _citeste_zip
            )
        except FileNotFoundError as err:
            _notifica_eroare_import(hass, str(err))
            return
        except (zipfile.BadZipFile, json.JSONDecodeError, OSError) as err:
            _notifica_eroare_import(
                hass, f"Eroare la citirea arhivei: {err}"
            )
            return

        if not vehicule:
            _notifica_eroare_import(
                hass, "Arhiva nu conține vehicule valide."
            )
            return

        _LOGGER.info(
            "[Fleet] Restore flotă: %d vehicule găsite în arhivă",
            len(vehicule),
        )

        reusit = 0
        esuat = 0
        detalii: list[str] = []

        for nr, date_vehicul in vehicule.items():
            nr_curat = nr.strip().upper()

            try:
                versiune = date_vehicul.get("version", 1)
                if versiune >= 2:
                    optiuni = aplatizeaza_optiuni(date_vehicul)
                elif "optiuni" in date_vehicul and isinstance(
                    date_vehicul["optiuni"], dict
                ):
                    # SEC-03: v1 — filtrăm chei cu underscore prefix
                    optiuni_raw = date_vehicul["optiuni"]
                    optiuni = {
                        k: v for k, v in optiuni_raw.items()
                        if isinstance(k, str) and not k.startswith("_")
                    }
                else:
                    optiuni = aplatizeaza_optiuni(date_vehicul)

                entry = _gaseste_vehicul(hass, nr_curat)

                if entry is None:
                    # Vehicul nou — creează config entry
                    result = await hass.config_entries.flow.async_init(
                        DOMAIN,
                        context={"source": "import"},
                        data={CONF_NR_INMATRICULARE: nr_curat},
                    )
                    if result.get("type") == "create_entry":
                        entry = result["result"]
                        _LOGGER.debug(
                            "[Fleet] Restore: vehicul nou creat — %s",
                            nr_curat,
                        )
                    else:
                        motiv = result.get("reason", "necunoscut")
                        _LOGGER.warning(
                            "[Fleet] Restore: nu am putut crea %s — %s",
                            nr_curat,
                            motiv,
                        )
                        esuat += 1
                        detalii.append(f"✗ {nr_curat} — {motiv}")
                        continue

                # Actualizează opțiunile
                hass.config_entries.async_update_entry(
                    entry, options=optiuni
                )
                reusit += 1
                detalii.append(f"✓ {nr_curat}")
                _LOGGER.debug(
                    "[Fleet] Restore: %s restaurat cu succes (%d opțiuni)",
                    nr_curat,
                    len(optiuni),
                )

            except Exception as err:  # noqa: BLE001
                _LOGGER.error(
                    "[Fleet] Restore: eroare la %s — %s", nr_curat, err
                )
                esuat += 1
                detalii.append(f"✗ {nr_curat} — {err}")

        _LOGGER.info(
            "[Fleet] Restore flotă finalizat: %d reușit, %d eșuat (din %d)",
            reusit,
            esuat,
            len(vehicule),
        )

        detalii_text = "\n".join(detalii)
        persistent_notification.async_create(
            hass,
            (
                f"Restore finalizat: **{reusit}** reușit, **{esuat}** eșuat "
                f"(din {len(vehicule)} vehicule)\n\n{detalii_text}"
            ),
            title="Restaurare completă",
            notification_id="fleet_restore_flota",
        )

    # ── Înregistrare efectivă ──

    hass.services.async_register(
        DOMAIN,
        SERVICE_ACTUALIZEAZA_DATE,
        _handle_actualizeaza_date,
        schema=SCHEMA_ACTUALIZEAZA_DATE,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_EXPORTA_DATE,
        _handle_exporta_date,
        schema=SCHEMA_EXPORTA_DATE,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_IMPORTA_DATE,
        _handle_importa_date,
        schema=SCHEMA_IMPORTA_DATE,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_BACKUP_FLOTA,
        _handle_backup_flota,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_RESTORE_FLOTA,
        _handle_restore_flota,
        schema=SCHEMA_RESTORE_FLOTA,
    )
    _LOGGER.debug("[Fleet] Serviciile %s au fost înregistrate", DOMAIN)


def _notifica_eroare_import(hass: HomeAssistant, mesaj: str) -> None:
    """Creează o notificare persistentă pentru erori de import."""
    _LOGGER.error("[Fleet] Import: %s", mesaj)
    persistent_notification.async_create(
        hass,
        mesaj,
        title="Import eșuat",
        notification_id="fleet_import_eroare",
    )
