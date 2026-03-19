"""
Flux de configurare pentru integrarea Fleet (gestiune flotă transport).

ConfigFlow: adaugă un vehicul nou (cere doar nr. de înmatriculare).
OptionsFlow: meniu cu categorii pentru editarea datelor vehiculului.

Câmpurile de dată folosesc TextSelector cu format românesc ZZ.LL.AAAA
(ex: 18.04.2026). Intern, datele se stochează în format ISO (2026-04-18).

Câmpurile de an folosesc TextSelector cu validare server-side
(evită eroarea „Value X is too small" de la NumberSelector în timpul tastării).
"""

from __future__ import annotations

import logging
import re
from datetime import date
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    AMENDA_STATUS_OPTIONS,
    CONF_LICENSE_KEY,
    LICENSE_DATA_KEY,
    ANVELOPE_TIP_OPTIONS,
    CATEGORII_ARHIVABILE,
    CATEGORIE_EURO_OPTIONS,
    COMBUSTIBIL_OPTIONS,
    CONF_ADBLUE_CAPACITATE,
    CONF_ADBLUE_NIVEL,
    CONF_ADR_CERTIFICAT_DATA_EXPIRARE,
    CONF_ADR_CERTIFICAT_NUMAR,
    CONF_ADR_CLASE,
    CONF_ADR_CONSILIER_CERTIFICAT,
    CONF_ADR_CONSILIER_DATA_EXPIRARE,
    CONF_ADR_CONSILIER_NUME,
    CONF_ADR_ECHIPAMENT_COMPLET,
    CONF_ALIMENTARE_COST,
    CONF_ALIMENTARE_DATA,
    CONF_ALIMENTARE_KM,
    CONF_ALIMENTARE_LITRI,
    CONF_ALIMENTARE_PRET_LITRU,
    CONF_AMENDA_DATA,
    CONF_AMENDA_MOTIV,
    CONF_AMENDA_STATUS,
    CONF_AMENDA_SUMA,
    CONF_AMENDA_TARA,
    CONF_AN_FABRICATIE,
    CONF_AN_PRIMA_INMATRICULARE,
    CONF_ANVELOPE_COST,
    CONF_ANVELOPE_DOT,
    CONF_ANVELOPE_IARNA_DATA,
    CONF_ANVELOPE_KM_MONTARE,
    CONF_ANVELOPE_NR_RESAPARI,
    CONF_ANVELOPE_TIP,
    CONF_ANVELOPE_VARA_DATA,
    CONF_ARHIVARE_DATE,
    CONF_BATERIE_COST,
    CONF_BATERIE_DATA_SCHIMB,
    CONF_CAPACITATE_CILINDRICA,
    CONF_CASCO_COMPANIE,
    CONF_CASCO_COST,
    CONF_CASCO_DATA_EMITERE,
    CONF_CASCO_DATA_EXPIRARE,
    CONF_CASCO_NUMAR_POLITA,
    CONF_CATEGORIE_EURO,
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
    CONF_MASA_PROPRIE,
    CONF_MMA,
    CONF_MODEL,
    CONF_MOTORIZARE,
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
    CONF_REMORCA_MASA_PROPRIE,
    CONF_REMORCA_MMA,
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
    CONF_SOFER_ATESTAT_ADR_CLASE,
    CONF_SOFER_ATESTAT_ADR_DATA_EXPIRARE,
    CONF_SOFER_ATESTAT_ADR_NUMAR,
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
    CONF_SOFER_FISA_PSIHOLOGICA_DATA,
    CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE,
    CONF_SOFER_NR_PERMIS,
    CONF_SOFER_NUME,
    CONF_TAHOGRAF_DATA_CALIBRARE,
    CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE,
    CONF_TAHOGRAF_DATA_VERIFICARE,
    CONF_TAHOGRAF_TIP,
    CONF_TAXA_DRUM_DATA,
    CONF_TAXA_DRUM_SUMA,
    CONF_TAXA_DRUM_TARA,
    CONF_TAXA_DRUM_VALUTA,
    CONF_TIP_PROPRIETATE,
    CONF_TIP_SUSPENSIE,
    CONF_TIP_VEHICUL,
    CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE,
    CONF_TURBO_COST,
    CONF_TURBO_DATA_REVIZIE,
    CONF_TURBO_KM_REVIZIE,
    CONF_VIN,
    CPC_TIP_OPTIONS,
    DOMAIN,
    REMORCA_TIP_OPTIONS,
    SOFER_APT_OPTIONS,
    TAHOGRAF_TIP_OPTIONS,
    TAXA_DRUM_TARA_OPTIONS,
    TIP_PROPRIETATE_OPTIONS,
    TIP_SUSPENSIE_OPTIONS,
    TIP_VEHICUL_OPTIONS,
    VALUTA_OPTIONS,
    normalizeaza_numar,
)
from .helpers import (
    FORMAT_DATA_RO,
    converteste_date_la_iso,
    pregateste_valori_sugerate,
    valideaza_campuri_an,
    valideaza_campuri_data,
)

_LOGGER = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Selector UI local
# ─────────────────────────────────────────────


def _selector_data() -> selector.TextSelector:
    """Returnează un TextSelector pentru date în format românesc ZZ.LL.AAAA."""
    return selector.TextSelector(
        selector.TextSelectorConfig(suffix=FORMAT_DATA_RO)
    )


# ─────────────────────────────────────────────
# Config Flow
# ─────────────────────────────────────────────


class FleetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Flux de configurare pentru adăugarea unui vehicul de transport."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Pasul inițial: solicită numărul de înmatriculare."""
        errors: dict[str, str] = {}

        if user_input is not None:
            numar = user_input[CONF_NR_INMATRICULARE].strip().upper()

            if not numar:
                errors["base"] = "numar_gol"
            elif not re.fullmatch(r"[A-Z0-9]+", numar):
                errors["base"] = "format_numar_invalid"
            else:
                numar_normalizat = normalizeaza_numar(numar)
                await self.async_set_unique_id(numar_normalizat)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=numar,
                    data={CONF_NR_INMATRICULARE: numar},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NR_INMATRICULARE): selector.TextSelector(
                        selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_import(
        self, import_data: dict[str, Any]
    ) -> config_entries.ConfigFlowResult:
        """Creează o intrare din import (utilizat de serviciul importa_date)."""
        numar = import_data[CONF_NR_INMATRICULARE].strip().upper()
        numar_normalizat = normalizeaza_numar(numar)

        await self.async_set_unique_id(numar_normalizat)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=numar,
            data={CONF_NR_INMATRICULARE: numar},
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> FleetOptionsFlow:
        """Returnează fluxul de opțiuni pentru editarea datelor."""
        return FleetOptionsFlow()


# ─────────────────────────────────────────────
# Options Flow
# ─────────────────────────────────────────────


class FleetOptionsFlow(config_entries.OptionsFlow):
    """Flux de opțiuni cu meniu pentru editarea datelor vehiculului de transport."""

    # ─────────────────────────────────────────
    # Meniu principal
    # ─────────────────────────────────────────
    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Afișează meniul principal cu categoriile de date."""
        return self.async_show_menu(
            step_id="init",
            menu_options=[
                "identificare",
                "sofer",
                "rca",
                "casco",
                "itp",
                "rovinieta",
                "administrativ",
                "licente",
                "adr",
                "tahograf",
                "combustibil_adblue",
                "mentenanta",
                "remorca",
                "costuri",
                "kilometraj",
                "licenta",
            ],
        )

    # ─────────────────────────────────────────
    # 1. Date de identificare (extinse transport)
    # ─────────────────────────────────────────
    async def async_step_identificare(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru datele de identificare ale vehiculului.

        Include câmpuri noi pentru transport: tip vehicul, MMA, masă proprie,
        nr. axe, categorie Euro, tip suspensi.
        """
        errors: dict[str, str] = {}
        an_curent = date.today().year

        chei = {
            CONF_MARCA, CONF_MODEL, CONF_VIN, CONF_SERIE_CIV,
            CONF_AN_FABRICATIE, CONF_AN_PRIMA_INMATRICULARE,
            CONF_MOTORIZARE, CONF_COMBUSTIBIL,
            CONF_CAPACITATE_CILINDRICA, CONF_PUTERE_KW, CONF_PUTERE_CP,
            CONF_TIP_VEHICUL, CONF_MMA, CONF_MASA_PROPRIE,
            CONF_NR_AXE, CONF_CATEGORIE_EURO, CONF_TIP_SUSPENSIE,
        }

        if user_input is not None:
            errors = valideaza_campuri_an(
                user_input,
                an_max_fabricatie=an_curent + 1,
                an_max_inmatriculare=an_curent,
            )
            if not errors:
                return self._salveaza_si_inchide(user_input, chei)

        schema = vol.Schema(
            {
                vol.Optional(CONF_MARCA): selector.TextSelector(),
                vol.Optional(CONF_MODEL): selector.TextSelector(),
                vol.Optional(CONF_VIN): selector.TextSelector(),
                vol.Optional(CONF_SERIE_CIV): selector.TextSelector(),
                vol.Optional(CONF_AN_FABRICATIE): selector.TextSelector(
                    selector.TextSelectorConfig(
                        suffix=f"(1900–{an_curent + 1})"
                    )
                ),
                vol.Optional(CONF_AN_PRIMA_INMATRICULARE): selector.TextSelector(
                    selector.TextSelectorConfig(
                        suffix=f"(1900–{an_curent})"
                    )
                ),
                vol.Optional(CONF_MOTORIZARE): selector.TextSelector(),
                vol.Optional(CONF_COMBUSTIBIL): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=COMBUSTIBIL_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="combustibil",
                    )
                ),
                vol.Optional(CONF_CAPACITATE_CILINDRICA): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="cm³",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_PUTERE_KW): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9999, step=1,
                        unit_of_measurement="kW",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_PUTERE_CP): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9999, step=1,
                        unit_of_measurement="CP",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_TIP_VEHICUL): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=TIP_VEHICUL_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="tip_vehicul",
                    )
                ),
                vol.Optional(CONF_MMA): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=999_999, step=1,
                        unit_of_measurement="kg",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_MASA_PROPRIE): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=999_999, step=1,
                        unit_of_measurement="kg",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_NR_AXE): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=2, max=10, step=1,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_CATEGORIE_EURO): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=CATEGORIE_EURO_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="categorie_euro",
                    )
                ),
                vol.Optional(CONF_TIP_SUSPENSIE): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=TIP_SUSPENSIE_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="tip_suspensie",
                    )
                ),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="identificare",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 2. Șofer
    # ─────────────────────────────────────────
    async def async_step_sofer(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru datele șoferului alocat vehiculului.

        Include: date personale, permis, CPC, card tahograf,
        atestat ADR, fișă medicală, fișă psihologică.
        """
        errors: dict[str, str] = {}
        chei = {
            CONF_SOFER_NUME, CONF_SOFER_CNP,
            CONF_SOFER_NR_PERMIS, CONF_SOFER_CATEGORII_PERMIS,
            CONF_SOFER_DATA_EXPIRARE_PERMIS,
            CONF_SOFER_CPC_NUMAR, CONF_SOFER_CPC_DATA_EXPIRARE, CONF_SOFER_CPC_TIP,
            CONF_SOFER_CARD_TAHOGRAF_NUMAR, CONF_SOFER_CARD_TAHOGRAF_DATA_EXPIRARE,
            CONF_SOFER_ATESTAT_ADR_NUMAR, CONF_SOFER_ATESTAT_ADR_DATA_EXPIRARE,
            CONF_SOFER_ATESTAT_ADR_CLASE,
            CONF_SOFER_FISA_MEDICALA_DATA, CONF_SOFER_FISA_MEDICALA_DATA_EXPIRARE,
            CONF_SOFER_FISA_MEDICALA_APT,
            CONF_SOFER_FISA_PSIHOLOGICA_DATA, CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_SOFER_NUME): selector.TextSelector(),
                vol.Optional(CONF_SOFER_CNP): selector.TextSelector(),
                vol.Optional(CONF_SOFER_NR_PERMIS): selector.TextSelector(),
                vol.Optional(CONF_SOFER_CATEGORII_PERMIS): selector.TextSelector(
                    selector.TextSelectorConfig(
                        suffix="(ex: C, CE, C1)"
                    )
                ),
                vol.Optional(CONF_SOFER_DATA_EXPIRARE_PERMIS): _selector_data(),
                vol.Optional(CONF_SOFER_CPC_NUMAR): selector.TextSelector(),
                vol.Optional(CONF_SOFER_CPC_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_SOFER_CPC_TIP): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=CPC_TIP_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="cpc_tip",
                    )
                ),
                vol.Optional(CONF_SOFER_CARD_TAHOGRAF_NUMAR): selector.TextSelector(),
                vol.Optional(CONF_SOFER_CARD_TAHOGRAF_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_SOFER_ATESTAT_ADR_NUMAR): selector.TextSelector(),
                vol.Optional(CONF_SOFER_ATESTAT_ADR_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_SOFER_ATESTAT_ADR_CLASE): selector.TextSelector(
                    selector.TextSelectorConfig(
                        suffix="(ex: 1, 2, 3, 4.1)"
                    )
                ),
                vol.Optional(CONF_SOFER_FISA_MEDICALA_DATA): _selector_data(),
                vol.Optional(CONF_SOFER_FISA_MEDICALA_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_SOFER_FISA_MEDICALA_APT): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=SOFER_APT_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="sofer_apt",
                    )
                ),
                vol.Optional(CONF_SOFER_FISA_PSIHOLOGICA_DATA): _selector_data(),
                vol.Optional(CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE): _selector_data(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="sofer",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 3. Asigurare RCA
    # ─────────────────────────────────────────
    async def async_step_rca(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru datele asigurării RCA."""
        errors: dict[str, str] = {}
        chei = {
            CONF_RCA_NUMAR_POLITA, CONF_RCA_COMPANIE,
            CONF_RCA_DATA_EMITERE, CONF_RCA_DATA_EXPIRARE, CONF_RCA_COST,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="rca",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_RCA_NUMAR_POLITA): selector.TextSelector(),
                vol.Optional(CONF_RCA_COMPANIE): selector.TextSelector(),
                vol.Optional(CONF_RCA_DATA_EMITERE): _selector_data(),
                vol.Optional(CONF_RCA_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_RCA_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="rca",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 4. Asigurare Casco
    # ─────────────────────────────────────────
    async def async_step_casco(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru datele asigurării Casco."""
        errors: dict[str, str] = {}
        chei = {
            CONF_CASCO_NUMAR_POLITA, CONF_CASCO_COMPANIE,
            CONF_CASCO_DATA_EMITERE, CONF_CASCO_DATA_EXPIRARE, CONF_CASCO_COST,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="casco",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_CASCO_NUMAR_POLITA): selector.TextSelector(),
                vol.Optional(CONF_CASCO_COMPANIE): selector.TextSelector(),
                vol.Optional(CONF_CASCO_DATA_EMITERE): _selector_data(),
                vol.Optional(CONF_CASCO_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_CASCO_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="casco",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 5. ITP
    # ─────────────────────────────────────────
    async def async_step_itp(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru datele ITP."""
        errors: dict[str, str] = {}
        chei = {CONF_ITP_DATA_EXPIRARE, CONF_ITP_STATIE, CONF_ITP_KILOMETRAJ}

        if not self._verifica_km_curent():
            errors["base"] = "km_necesar"
        elif user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="itp",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_ITP_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_ITP_STATIE): selector.TextSelector(),
                vol.Optional(CONF_ITP_KILOMETRAJ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="itp",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 6. Rovinieta
    # ─────────────────────────────────────────
    async def async_step_rovinieta(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru datele rovinietei."""
        errors: dict[str, str] = {}
        chei = {
            CONF_ROVINIETA_DATA_INCEPUT,
            CONF_ROVINIETA_DATA_SFARSIT,
            CONF_ROVINIETA_CATEGORIE,
            CONF_ROVINIETA_PRET,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="rovinieta",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_ROVINIETA_DATA_INCEPUT): _selector_data(),
                vol.Optional(CONF_ROVINIETA_DATA_SFARSIT): _selector_data(),
                vol.Optional(CONF_ROVINIETA_CATEGORIE): selector.TextSelector(),
                vol.Optional(CONF_ROVINIETA_PRET): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="rovinieta",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 7. Date administrative / fiscale
    # ─────────────────────────────────────────
    async def async_step_administrativ(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru datele administrative și fiscale.

        Câmpul „Data expirare leasing" apare DOAR dacă tip_proprietate
        include leasing (leasing sau leasing_operational).
        """
        errors: dict[str, str] = {}
        chei = {
            CONF_PROPRIETAR, CONF_TIP_PROPRIETATE,
            CONF_IMPOZIT_SUMA, CONF_IMPOZIT_SCADENTA, CONF_IMPOZIT_LOCALITATE,
        }

        tip_salvat = self.config_entry.options.get(CONF_TIP_PROPRIETATE, "")
        este_leasing = tip_salvat in ("leasing", "leasing_operational")

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                date_convertite = converteste_date_la_iso(user_input)
                chei.add(CONF_LEASING_DATA_EXPIRARE)

                tip_selectat = user_input.get(CONF_TIP_PROPRIETATE)
                if tip_selectat in ("leasing", "leasing_operational") and not este_leasing:
                    self._date_admin_temp = date_convertite
                    self._chei_admin_temp = chei
                    return await self.async_step_leasing_data()

                return self._salveaza_si_inchide(date_convertite, chei)

        campuri: dict[vol.Optional, Any] = {
            vol.Optional(CONF_PROPRIETAR): selector.TextSelector(),
            vol.Optional(CONF_TIP_PROPRIETATE): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=TIP_PROPRIETATE_OPTIONS,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                    translation_key="tip_proprietate",
                )
            ),
            vol.Optional(CONF_IMPOZIT_SUMA): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0, max=999_999, step=1,
                    unit_of_measurement="RON",
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Optional(CONF_IMPOZIT_SCADENTA): _selector_data(),
            vol.Optional(CONF_IMPOZIT_LOCALITATE): selector.TextSelector(),
        }

        if este_leasing:
            campuri[vol.Optional(CONF_LEASING_DATA_EXPIRARE)] = _selector_data()

        schema = vol.Schema(campuri)

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="administrativ",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    async def async_step_leasing_data(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Pas suplimentar: data expirare leasing."""
        errors: dict[str, str] = {}

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                date_convertite = converteste_date_la_iso(user_input)
                date_complete = {**self._date_admin_temp, **date_convertite}
                chei_complete = self._chei_admin_temp | {
                    CONF_LEASING_DATA_EXPIRARE
                }
                return self._salveaza_si_inchide(date_complete, chei_complete)

        schema = vol.Schema(
            {
                vol.Optional(CONF_LEASING_DATA_EXPIRARE): _selector_data(),
            }
        )

        valori = pregateste_valori_sugerate(self.config_entry.options)

        return self.async_show_form(
            step_id="leasing_data",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 8. Licențe transport
    # ─────────────────────────────────────────
    async def async_step_licente(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru licențe de transport și copie conformă.

        Licența de transport, copie conformă vehicul, licență comunitară.
        """
        errors: dict[str, str] = {}
        chei = {
            CONF_LICENTA_TRANSPORT_NUMAR, CONF_LICENTA_TRANSPORT_TIP,
            CONF_LICENTA_TRANSPORT_DATA_EXPIRARE,
            CONF_COPIE_CONFORMA_NUMAR, CONF_COPIE_CONFORMA_DATA_EXPIRARE,
            CONF_LICENTA_COMUNITARA_NUMAR, CONF_LICENTA_COMUNITARA_DATA_EXPIRARE,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="copie_conforma",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_LICENTA_TRANSPORT_NUMAR): selector.TextSelector(),
                vol.Optional(CONF_LICENTA_TRANSPORT_TIP): selector.TextSelector(
                    selector.TextSelectorConfig(
                        suffix="(național / internațional)"
                    )
                ),
                vol.Optional(CONF_LICENTA_TRANSPORT_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_COPIE_CONFORMA_NUMAR): selector.TextSelector(),
                vol.Optional(CONF_COPIE_CONFORMA_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_LICENTA_COMUNITARA_NUMAR): selector.TextSelector(),
                vol.Optional(CONF_LICENTA_COMUNITARA_DATA_EXPIRARE): _selector_data(),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="licente",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 9. ADR – Transport mărfuri periculoase
    # ─────────────────────────────────────────
    async def async_step_adr(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru certificat ADR vehicul.

        Certificat vehicul, clase ADR autorizate, consilier siguranță,
        echipament ADR complet.
        """
        errors: dict[str, str] = {}
        chei = {
            CONF_ADR_CERTIFICAT_NUMAR, CONF_ADR_CERTIFICAT_DATA_EXPIRARE,
            CONF_ADR_CLASE,
            CONF_ADR_CONSILIER_NUME, CONF_ADR_CONSILIER_CERTIFICAT,
            CONF_ADR_CONSILIER_DATA_EXPIRARE,
            CONF_ADR_ECHIPAMENT_COMPLET,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_ADR_CERTIFICAT_NUMAR): selector.TextSelector(),
                vol.Optional(CONF_ADR_CERTIFICAT_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_ADR_CLASE): selector.TextSelector(
                    selector.TextSelectorConfig(
                        suffix="(ex: 1, 2, 3, 4.1, 5.1)"
                    )
                ),
                vol.Optional(CONF_ADR_CONSILIER_NUME): selector.TextSelector(),
                vol.Optional(CONF_ADR_CONSILIER_CERTIFICAT): selector.TextSelector(),
                vol.Optional(CONF_ADR_CONSILIER_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_ADR_ECHIPAMENT_COMPLET): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="adr",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 10. Tahograf
    # ─────────────────────────────────────────
    async def async_step_tahograf(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru tahograf (obligatoriu conform Reg. EU 561/2006).

        Tip tahograf, data verificării, data următoarei verificări, data calibrării.
        """
        errors: dict[str, str] = {}
        chei = {
            CONF_TAHOGRAF_TIP, CONF_TAHOGRAF_DATA_VERIFICARE,
            CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE, CONF_TAHOGRAF_DATA_CALIBRARE,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_TAHOGRAF_TIP): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=TAHOGRAF_TIP_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="tahograf_tip",
                    )
                ),
                vol.Optional(CONF_TAHOGRAF_DATA_VERIFICARE): _selector_data(),
                vol.Optional(CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE): _selector_data(),
                vol.Optional(CONF_TAHOGRAF_DATA_CALIBRARE): _selector_data(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="tahograf",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 11. Combustibil & AdBlue
    # ─────────────────────────────────────────
    async def async_step_combustibil_adblue(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru combustibil, AdBlue și ultima alimentare.

        Capacitate rezervor, nivel curent, consum mediu,
        AdBlue, și datele ultimei alimentări (arhivabile).
        """
        errors: dict[str, str] = {}
        chei = {
            CONF_COMBUSTIBIL_CAPACITATE, CONF_COMBUSTIBIL_NIVEL,
            CONF_COMBUSTIBIL_CONSUM_MEDIU,
            CONF_ADBLUE_CAPACITATE, CONF_ADBLUE_NIVEL,
            CONF_ALIMENTARE_DATA, CONF_ALIMENTARE_LITRI,
            CONF_ALIMENTARE_PRET_LITRU, CONF_ALIMENTARE_COST,
            CONF_ALIMENTARE_KM,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="alimentare",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_COMBUSTIBIL_CAPACITATE): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9999, step=1,
                        unit_of_measurement="L",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_COMBUSTIBIL_NIVEL): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=100, step=1,
                        unit_of_measurement="%",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_COMBUSTIBIL_CONSUM_MEDIU): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=200, step=0.1,
                        unit_of_measurement="L/100km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_ADBLUE_CAPACITATE): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=999, step=1,
                        unit_of_measurement="L",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_ADBLUE_NIVEL): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=100, step=1,
                        unit_of_measurement="%",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_ALIMENTARE_DATA): _selector_data(),
                vol.Optional(CONF_ALIMENTARE_LITRI): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9999, step=0.1,
                        unit_of_measurement="L",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_ALIMENTARE_PRET_LITRU): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99, step=0.01,
                        unit_of_measurement="RON/L",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_ALIMENTARE_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=0.01,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_ALIMENTARE_KM): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="combustibil_adblue",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 12. Mentenanță – Sub-meniu
    # ─────────────────────────────────────────
    async def async_step_mentenanta(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Sub-meniu pentru categoriile de mentenanță."""
        return self.async_show_menu(
            step_id="mentenanta",
            menu_options=[
                "revizie_ulei",
                "distributie",
                "anvelope",
                "baterie",
                "frane",
                "dpf",
                "turbo",
                "trusa_prim_ajutor",
                "extinctor",
            ],
        )

    # ── 12a. Revizie ulei ──
    async def async_step_revizie_ulei(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru revizia de ulei."""
        errors: dict[str, str] = {}
        chei = {
            CONF_REVIZIE_ULEI_KM_ULTIMUL, CONF_REVIZIE_ULEI_KM_URMATOR,
            CONF_REVIZIE_ULEI_DATA, CONF_REVIZIE_ULEI_COST,
        }

        if not self._verifica_km_curent():
            errors["base"] = "km_necesar"
        elif user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="revizie_ulei",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_REVIZIE_ULEI_KM_ULTIMUL): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_REVIZIE_ULEI_KM_URMATOR): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_REVIZIE_ULEI_DATA): _selector_data(),
                vol.Optional(CONF_REVIZIE_ULEI_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="revizie_ulei",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ── 12b. Distribuție ──
    async def async_step_distributie(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru distribuție."""
        errors: dict[str, str] = {}
        chei = {
            CONF_DISTRIBUTIE_KM_ULTIMUL, CONF_DISTRIBUTIE_KM_URMATOR,
            CONF_DISTRIBUTIE_DATA, CONF_DISTRIBUTIE_COST,
        }

        if not self._verifica_km_curent():
            errors["base"] = "km_necesar"
        elif user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="distributie",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_DISTRIBUTIE_KM_ULTIMUL): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_DISTRIBUTIE_KM_URMATOR): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_DISTRIBUTIE_DATA): _selector_data(),
                vol.Optional(CONF_DISTRIBUTIE_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="distributie",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ── 12c. Anvelope (extinse) ──
    async def async_step_anvelope(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru anvelope (extins cu DOT, tip, reșapări, km montare)."""
        errors: dict[str, str] = {}
        chei = {
            CONF_ANVELOPE_VARA_DATA, CONF_ANVELOPE_IARNA_DATA, CONF_ANVELOPE_COST,
            CONF_ANVELOPE_DOT, CONF_ANVELOPE_TIP,
            CONF_ANVELOPE_NR_RESAPARI, CONF_ANVELOPE_KM_MONTARE,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="anvelope",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_ANVELOPE_VARA_DATA): _selector_data(),
                vol.Optional(CONF_ANVELOPE_IARNA_DATA): _selector_data(),
                vol.Optional(CONF_ANVELOPE_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_ANVELOPE_DOT): selector.TextSelector(
                    selector.TextSelectorConfig(
                        suffix="(ex: 2524 = săpt. 25, an 2024)"
                    )
                ),
                vol.Optional(CONF_ANVELOPE_TIP): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=ANVELOPE_TIP_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="anvelope_tip",
                    )
                ),
                vol.Optional(CONF_ANVELOPE_NR_RESAPARI): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=10, step=1,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_ANVELOPE_KM_MONTARE): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="anvelope",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ── 12d. Baterie ──
    async def async_step_baterie(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru baterie."""
        errors: dict[str, str] = {}
        chei = {CONF_BATERIE_DATA_SCHIMB, CONF_BATERIE_COST}

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="baterie",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_BATERIE_DATA_SCHIMB): _selector_data(),
                vol.Optional(CONF_BATERIE_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="baterie",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ── 12e. Frâne ──
    async def async_step_frane(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru plăcuțe și discuri de frână."""
        errors: dict[str, str] = {}
        chei = {
            CONF_PLACUTE_FRANA_KM_ULTIMUL, CONF_PLACUTE_FRANA_KM_URMATOR,
            CONF_PLACUTE_FRANA_DATA, CONF_PLACUTE_FRANA_COST,
            CONF_DISCURI_FRANA_KM_ULTIMUL, CONF_DISCURI_FRANA_KM_URMATOR,
            CONF_DISCURI_FRANA_DATA, CONF_DISCURI_FRANA_COST,
        }

        if not self._verifica_km_curent():
            errors["base"] = "km_necesar"
        elif user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input),
                    chei,
                    categorie_arhivare="frane",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_PLACUTE_FRANA_KM_ULTIMUL): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_PLACUTE_FRANA_KM_URMATOR): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_PLACUTE_FRANA_DATA): _selector_data(),
                vol.Optional(CONF_PLACUTE_FRANA_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_DISCURI_FRANA_KM_ULTIMUL): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_DISCURI_FRANA_KM_URMATOR): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_DISCURI_FRANA_DATA): _selector_data(),
                vol.Optional(CONF_DISCURI_FRANA_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="frane",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ── 12f. DPF (Filtru de particule) ──
    async def async_step_dpf(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru curățarea filtrului de particule (DPF)."""
        errors: dict[str, str] = {}
        chei = {CONF_DPF_DATA_CURATARE, CONF_DPF_KM_CURATARE, CONF_DPF_COST}

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="dpf",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_DPF_DATA_CURATARE): _selector_data(),
                vol.Optional(CONF_DPF_KM_CURATARE): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_DPF_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="dpf",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ── 12g. Turbosuflantă ──
    async def async_step_turbo(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru revizia turbosuflantei."""
        errors: dict[str, str] = {}
        chei = {CONF_TURBO_DATA_REVIZIE, CONF_TURBO_KM_REVIZIE, CONF_TURBO_COST}

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei,
                    categorie_arhivare="turbo",
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_TURBO_DATA_REVIZIE): _selector_data(),
                vol.Optional(CONF_TURBO_KM_REVIZIE): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_TURBO_COST): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=1,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ARHIVARE_DATE, default=False
                ): selector.BooleanSelector(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="turbo",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ── 12h. Trusă de prim ajutor ──
    async def async_step_trusa_prim_ajutor(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru trusa de prim ajutor (obligatorie)."""
        errors: dict[str, str] = {}
        chei = {CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE}

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE): _selector_data(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="trusa_prim_ajutor",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ── 12i. Extinctor (extins cu capacitate) ──
    async def async_step_extinctor(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru extinctor (obligatoriu, extins cu capacitate)."""
        errors: dict[str, str] = {}
        chei = {CONF_EXTINCTOR_DATA_EXPIRARE, CONF_EXTINCTOR_CAPACITATE}

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_EXTINCTOR_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_EXTINCTOR_CAPACITATE): selector.TextSelector(
                    selector.TextSelectorConfig(
                        suffix="(ex: 6 kg, 9 kg)"
                    )
                ),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="extinctor",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 13. Remorcă / Semiremorcă
    # ─────────────────────────────────────────
    async def async_step_remorca(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru datele remorcii/semiremorcii atașate."""
        errors: dict[str, str] = {}
        an_curent = date.today().year
        chei = {
            CONF_REMORCA_NR_INMATRICULARE, CONF_REMORCA_TIP, CONF_REMORCA_MARCA,
            CONF_REMORCA_MMA, CONF_REMORCA_MASA_PROPRIE, CONF_REMORCA_NR_AXE,
            CONF_REMORCA_AN_FABRICATIE,
            CONF_REMORCA_ITP_DATA_EXPIRARE, CONF_REMORCA_RCA_DATA_EXPIRARE,
            CONF_REMORCA_ROVINIETA_DATA_SFARSIT,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            # Validare an fabricație remorcă
            an_fab = user_input.get(CONF_REMORCA_AN_FABRICATIE)
            if an_fab is not None and an_fab != "":
                try:
                    an_val = int(an_fab) if isinstance(an_fab, str) else an_fab
                    if not (1900 <= an_val <= an_curent + 1):
                        errors[CONF_REMORCA_AN_FABRICATIE] = "an_invalid"
                except (ValueError, TypeError):
                    errors[CONF_REMORCA_AN_FABRICATIE] = "an_invalid"
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_REMORCA_NR_INMATRICULARE): selector.TextSelector(),
                vol.Optional(CONF_REMORCA_TIP): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=REMORCA_TIP_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="remorca_tip",
                    )
                ),
                vol.Optional(CONF_REMORCA_MARCA): selector.TextSelector(),
                vol.Optional(CONF_REMORCA_MMA): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=999_999, step=1,
                        unit_of_measurement="kg",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_REMORCA_MASA_PROPRIE): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=999_999, step=1,
                        unit_of_measurement="kg",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_REMORCA_NR_AXE): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1, max=6, step=1,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_REMORCA_AN_FABRICATIE): selector.TextSelector(
                    selector.TextSelectorConfig(
                        suffix=f"(1900–{an_curent + 1})"
                    )
                ),
                vol.Optional(CONF_REMORCA_ITP_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_REMORCA_RCA_DATA_EXPIRARE): _selector_data(),
                vol.Optional(CONF_REMORCA_ROVINIETA_DATA_SFARSIT): _selector_data(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="remorca",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 14. Costuri – Sub-meniu
    # ─────────────────────────────────────────
    async def async_step_costuri(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Sub-meniu pentru costuri extinse (taxe drum, amenzi)."""
        return self.async_show_menu(
            step_id="costuri",
            menu_options=[
                "taxe_drum",
                "amenzi",
            ],
        )

    # ── 14a. Taxe drum ──
    async def async_step_taxe_drum(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru taxe de drum (viniete europene, etc.)."""
        errors: dict[str, str] = {}
        chei = {
            CONF_TAXA_DRUM_TARA, CONF_TAXA_DRUM_SUMA,
            CONF_TAXA_DRUM_VALUTA, CONF_TAXA_DRUM_DATA,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_TAXA_DRUM_TARA): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=TAXA_DRUM_TARA_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="taxa_drum_tara",
                    )
                ),
                vol.Optional(CONF_TAXA_DRUM_SUMA): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=0.01,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_TAXA_DRUM_VALUTA): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=VALUTA_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="valuta",
                    )
                ),
                vol.Optional(CONF_TAXA_DRUM_DATA): _selector_data(),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="taxe_drum",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ── 14b. Amenzi ──
    async def async_step_amenzi(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru amenzi (trafic, parcare, etc.)."""
        errors: dict[str, str] = {}
        chei = {
            CONF_AMENDA_SUMA, CONF_AMENDA_MOTIV, CONF_AMENDA_TARA,
            CONF_AMENDA_DATA, CONF_AMENDA_STATUS,
        }

        if user_input is not None:
            errors = valideaza_campuri_data(user_input)
            if not errors:
                return self._salveaza_si_inchide(
                    converteste_date_la_iso(user_input), chei
                )

        schema = vol.Schema(
            {
                vol.Optional(CONF_AMENDA_SUMA): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=99999, step=0.01,
                        unit_of_measurement="RON",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_AMENDA_MOTIV): selector.TextSelector(),
                vol.Optional(CONF_AMENDA_TARA): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=TAXA_DRUM_TARA_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="taxa_drum_tara",
                    )
                ),
                vol.Optional(CONF_AMENDA_DATA): _selector_data(),
                vol.Optional(CONF_AMENDA_STATUS): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=AMENDA_STATUS_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="amenda_status",
                    )
                ),
            }
        )

        valori = pregateste_valori_sugerate(
            {**self.config_entry.options, **(user_input or {})}
            if user_input
            else self.config_entry.options
        )

        return self.async_show_form(
            step_id="amenzi",
            data_schema=self.add_suggested_values_to_schema(schema, valori),
            errors=errors,
        )

    # ─────────────────────────────────────────
    # 15. Kilometraj & Ore motor
    # ─────────────────────────────────────────
    async def async_step_kilometraj(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru kilometraj curent și ore motor."""
        chei = {CONF_KM_CURENT, CONF_ORE_MOTOR}
        if user_input is not None:
            return self._salveaza_si_inchide(user_input, chei)

        schema = vol.Schema(
            {
                vol.Optional(CONF_KM_CURENT): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=9_999_999, step=1,
                        unit_of_measurement="km",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(CONF_ORE_MOTOR): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=999_999, step=1,
                        unit_of_measurement="h",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="kilometraj",
            data_schema=self.add_suggested_values_to_schema(
                schema, self.config_entry.options
            ),
        )

    # ─────────────────────────────────────────
    # Licențiere
    # ─────────────────────────────────────────
    async def async_step_licenta(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Formular pentru activarea / vizualizarea licenței Fleet."""
        from .license import LicenseManager

        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}

        # Obține LicenseManager
        mgr: LicenseManager | None = self.hass.data.get(DOMAIN, {}).get(
            LICENSE_DATA_KEY
        )
        if mgr is None:
            mgr = LicenseManager(self.hass)
            await mgr.async_load()

        # Informații pentru descrierea formularului
        server_status = mgr.status  # 'licensed', 'trial', 'expired', 'unlicensed'

        if server_status == "licensed":
            from datetime import datetime

            tip = mgr.license_type or "necunoscut"
            status_lines = [f"✅ Licență activă ({tip})"]

            if mgr.license_key_masked:
                status_lines[0] += f" — {mgr.license_key_masked}"

            # Data activării
            if mgr.activated_at:
                act_date = datetime.fromtimestamp(
                    mgr.activated_at
                ).strftime("%d.%m.%Y %H:%M")
                status_lines.append(f"Activată la: {act_date}")

            # Data expirării
            if mgr.license_expires_at:
                exp_date = datetime.fromtimestamp(
                    mgr.license_expires_at
                ).strftime("%d.%m.%Y %H:%M")
                status_lines.append(f"📅 Expiră la: {exp_date}")
            elif tip == "perpetual":
                status_lines.append("Valabilitate: nelimitată (perpetuă)")

            description_placeholders["license_status"] = "\n".join(
                status_lines
            )

        elif server_status == "trial":
            description_placeholders["license_status"] = (
                f"⏳ Evaluare — {mgr.trial_days_remaining} zile rămase"
            )
        elif server_status == "expired":
            from datetime import datetime

            status_lines = ["❌ Licență expirată"]

            if mgr.activated_at:
                act_date = datetime.fromtimestamp(
                    mgr.activated_at
                ).strftime("%d.%m.%Y")
                status_lines.append(f"Activată la: {act_date}")
            if mgr.license_expires_at:
                exp_date = datetime.fromtimestamp(
                    mgr.license_expires_at
                ).strftime("%d.%m.%Y")
                status_lines.append(f"Expirată la: {exp_date}")

            description_placeholders["license_status"] = "\n".join(
                status_lines
            )
        else:
            description_placeholders["license_status"] = (
                "❌ Fără licență — funcționalitate blocată"
            )

        if user_input is not None:
            cheie = user_input.get(CONF_LICENSE_KEY, "").strip()

            if not cheie:
                errors["base"] = "license_key_empty"
            elif len(cheie) < 10:
                errors["base"] = "license_key_invalid"
            else:
                # Activare prin API
                result = await mgr.async_activate(cheie)

                if result.get("success"):
                    # Notificare de succes
                    from homeassistant.components import (
                        persistent_notification,
                    )

                    persistent_notification.async_create(
                        self.hass,
                        f"Licența Fleet a fost activată cu succes! "
                        f"Tip: {mgr.license_type or 'necunoscut'}.",
                        title="Licență activată",
                        notification_id="fleet_license_activated",
                    )
                    return self.async_create_entry(
                        data=self.config_entry.options
                    )

                # Mapare erori API
                api_error = result.get("error", "unknown_error")
                error_map = {
                    "invalid_key": "license_key_invalid",
                    "already_used": "license_already_used",
                    "expired_key": "license_key_expired",
                    "fingerprint_mismatch": "license_fingerprint_mismatch",
                    "invalid_signature": "license_server_error",
                    "network_error": "license_network_error",
                    "server_error": "license_server_error",
                }
                errors["base"] = error_map.get(api_error, "license_server_error")

        schema = vol.Schema(
            {
                vol.Optional(CONF_LICENSE_KEY): selector.TextSelector(
                    selector.TextSelectorConfig(
                        type=selector.TextSelectorType.TEXT,
                        suffix="FLEET-XXXX-XXXX-XXXX",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="licenta",
            data_schema=schema,
            errors=errors,
            description_placeholders=description_placeholders,
        )

    # ─────────────────────────────────────────
    # Utilitar: salvează și închide
    # ─────────────────────────────────────────
    def _salveaza_si_inchide(
        self,
        user_input: dict[str, Any],
        chei_formular: set[str] | None = None,
        categorie_arhivare: str | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Îmbină datele noi cu opțiunile existente și închide fluxul.

        Comportament:
        - Câmpuri cu valoare non-goală: se actualizează / adaugă
        - Câmpuri golite explicit (None sau ""): se șterg din opțiuni
        - Câmpuri din formular absente din user_input: se șterg din opțiuni
        - Câmpuri nemodificate: rămân neschimbate

        Dacă categorie_arhivare este specificată ȘI utilizatorul a bifat
        opțiunea de arhivare, datele vechi sunt salvate în lista _istoric.
        """
        doreste_arhivare = user_input.pop(CONF_ARHIVARE_DATE, False)

        optiuni_noi = {**self.config_entry.options}

        # ── Arhivare datelor vechi (doar dacă utilizatorul a bifat) ──
        if (
            doreste_arhivare
            and categorie_arhivare
            and categorie_arhivare in CATEGORII_ARHIVABILE
        ):
            campuri_categorie = CATEGORII_ARHIVABILE[categorie_arhivare]
            date_vechi: dict[str, Any] = {}
            for eticheta, cheie_const in campuri_categorie.items():
                val = optiuni_noi.get(cheie_const)
                if val is not None and val != "":
                    date_vechi[eticheta] = val
            if date_vechi:
                istoric = list(optiuni_noi.get(CONF_ISTORIC, []))
                istoric.append(
                    {
                        "tip": categorie_arhivare,
                        "data_arhivare": date.today().isoformat(),
                        "date": date_vechi,
                    }
                )
                optiuni_noi[CONF_ISTORIC] = istoric

        # ── Îmbinare date noi ──
        for cheie, valoare in user_input.items():
            if valoare is not None and valoare != "":
                optiuni_noi[cheie] = valoare
            else:
                optiuni_noi.pop(cheie, None)

        # Câmpuri care erau în formular dar NU au fost trimise de HA
        if chei_formular:
            for cheie in chei_formular:
                if cheie not in user_input:
                    optiuni_noi.pop(cheie, None)

        return self.async_create_entry(data=optiuni_noi)

    def _verifica_km_curent(self) -> bool:
        """Verifică dacă kilometrajul curent este configurat."""
        return self.config_entry.options.get(CONF_KM_CURENT) is not None
