"""Constante pentru integrarea Fleet (gestiune flotă transport)."""

from typing import Final

# ─────────────────────────────────────────────
# Domeniu și platforme
# ─────────────────────────────────────────────
DOMAIN: Final = "fleet"
PLATFORMS: Final = ["sensor"]

# ─────────────────────────────────────────────
# 1. Date de identificare vehicul (extinse pentru camioane)
# ─────────────────────────────────────────────
CONF_NR_INMATRICULARE: Final = "nr_inmatriculare"
CONF_SERIE_CIV: Final = "serie_civ"
CONF_VIN: Final = "vin"
CONF_MARCA: Final = "marca"
CONF_MODEL: Final = "model"
CONF_AN_FABRICATIE: Final = "an_fabricatie"
CONF_AN_PRIMA_INMATRICULARE: Final = "an_prima_inmatriculare"
CONF_MOTORIZARE: Final = "motorizare"
CONF_COMBUSTIBIL: Final = "combustibil"
CONF_CAPACITATE_CILINDRICA: Final = "capacitate_cilindrica"
CONF_PUTERE_KW: Final = "putere_kw"
CONF_PUTERE_CP: Final = "putere_cp"
# Câmpuri noi transport
CONF_TIP_VEHICUL: Final = "tip_vehicul"
CONF_MMA: Final = "mma"
CONF_MASA_PROPRIE: Final = "masa_proprie"
CONF_NR_AXE: Final = "nr_axe"
CONF_CATEGORIE_EURO: Final = "categorie_euro"
CONF_TIP_SUSPENSIE: Final = "tip_suspensie"

# ─────────────────────────────────────────────
# 2. Șofer
# ─────────────────────────────────────────────
CONF_SOFER_NUME: Final = "sofer_nume"
CONF_SOFER_CNP: Final = "sofer_cnp"
CONF_SOFER_NR_PERMIS: Final = "sofer_nr_permis"
CONF_SOFER_CATEGORII_PERMIS: Final = "sofer_categorii_permis"
CONF_SOFER_DATA_EXPIRARE_PERMIS: Final = "sofer_data_expirare_permis"
CONF_SOFER_CPC_NUMAR: Final = "sofer_cpc_numar"
CONF_SOFER_CPC_DATA_EXPIRARE: Final = "sofer_cpc_data_expirare"
CONF_SOFER_CPC_TIP: Final = "sofer_cpc_tip"
CONF_SOFER_CARD_TAHOGRAF_NUMAR: Final = "sofer_card_tahograf_numar"
CONF_SOFER_CARD_TAHOGRAF_DATA_EXPIRARE: Final = "sofer_card_tahograf_data_expirare"
CONF_SOFER_ATESTAT_ADR_NUMAR: Final = "sofer_atestat_adr_numar"
CONF_SOFER_ATESTAT_ADR_DATA_EXPIRARE: Final = "sofer_atestat_adr_data_expirare"
CONF_SOFER_ATESTAT_ADR_CLASE: Final = "sofer_atestat_adr_clase"
CONF_SOFER_FISA_MEDICALA_DATA: Final = "sofer_fisa_medicala_data"
CONF_SOFER_FISA_MEDICALA_DATA_EXPIRARE: Final = "sofer_fisa_medicala_data_expirare"
CONF_SOFER_FISA_MEDICALA_APT: Final = "sofer_fisa_medicala_apt"
CONF_SOFER_FISA_PSIHOLOGICA_DATA: Final = "sofer_fisa_psihologica_data"
CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE: Final = "sofer_fisa_psihologica_data_expirare"

# ─────────────────────────────────────────────
# 3. Kilometraj & Ore motor
# ─────────────────────────────────────────────
CONF_KM_CURENT: Final = "km_curent"
CONF_ORE_MOTOR: Final = "ore_motor"

# ─────────────────────────────────────────────
# 4. RCA (Asigurare obligatorie)
# ─────────────────────────────────────────────
CONF_RCA_NUMAR_POLITA: Final = "rca_numar_polita"
CONF_RCA_COMPANIE: Final = "rca_companie"
CONF_RCA_DATA_EMITERE: Final = "rca_data_emitere"
CONF_RCA_DATA_EXPIRARE: Final = "rca_data_expirare"
CONF_RCA_COST: Final = "rca_cost"

# ─────────────────────────────────────────────
# 5. Casco (Asigurare facultativă)
# ─────────────────────────────────────────────
CONF_CASCO_NUMAR_POLITA: Final = "casco_numar_polita"
CONF_CASCO_COMPANIE: Final = "casco_companie"
CONF_CASCO_DATA_EMITERE: Final = "casco_data_emitere"
CONF_CASCO_DATA_EXPIRARE: Final = "casco_data_expirare"
CONF_CASCO_COST: Final = "casco_cost"

# ─────────────────────────────────────────────
# 6. ITP (Inspecție tehnică periodică)
# ─────────────────────────────────────────────
CONF_ITP_DATA_EXPIRARE: Final = "itp_data_expirare"
CONF_ITP_STATIE: Final = "itp_statie"
CONF_ITP_KILOMETRAJ: Final = "itp_kilometraj"

# ─────────────────────────────────────────────
# 7. Rovinieta
# ─────────────────────────────────────────────
CONF_ROVINIETA_DATA_INCEPUT: Final = "rovinieta_data_inceput"
CONF_ROVINIETA_DATA_SFARSIT: Final = "rovinieta_data_sfarsit"
CONF_ROVINIETA_CATEGORIE: Final = "rovinieta_categorie"
CONF_ROVINIETA_PRET: Final = "rovinieta_pret"

# ─────────────────────────────────────────────
# 8. Date administrative / fiscale
# ─────────────────────────────────────────────
CONF_IMPOZIT_SUMA: Final = "impozit_suma"
CONF_IMPOZIT_SCADENTA: Final = "impozit_scadenta"
CONF_IMPOZIT_LOCALITATE: Final = "impozit_localitate"
CONF_PROPRIETAR: Final = "proprietar"
CONF_TIP_PROPRIETATE: Final = "tip_proprietate"
CONF_LEASING_DATA_EXPIRARE: Final = "leasing_data_expirare"

# ─────────────────────────────────────────────
# 9. Documente firmă / licențe transport
# ─────────────────────────────────────────────
CONF_LICENTA_TRANSPORT_NUMAR: Final = "licenta_transport_numar"
CONF_LICENTA_TRANSPORT_TIP: Final = "licenta_transport_tip"
CONF_LICENTA_TRANSPORT_DATA_EXPIRARE: Final = "licenta_transport_data_expirare"
CONF_COPIE_CONFORMA_NUMAR: Final = "copie_conforma_numar"
CONF_COPIE_CONFORMA_DATA_EXPIRARE: Final = "copie_conforma_data_expirare"
CONF_LICENTA_COMUNITARA_NUMAR: Final = "licenta_comunitara_numar"
CONF_LICENTA_COMUNITARA_DATA_EXPIRARE: Final = "licenta_comunitara_data_expirare"

# ─────────────────────────────────────────────
# 10. ADR – Transport mărfuri periculoase
# ─────────────────────────────────────────────
CONF_ADR_CERTIFICAT_NUMAR: Final = "adr_certificat_numar"
CONF_ADR_CERTIFICAT_DATA_EXPIRARE: Final = "adr_certificat_data_expirare"
CONF_ADR_CLASE: Final = "adr_clase"
CONF_ADR_CONSILIER_NUME: Final = "adr_consilier_nume"
CONF_ADR_CONSILIER_CERTIFICAT: Final = "adr_consilier_certificat"
CONF_ADR_CONSILIER_DATA_EXPIRARE: Final = "adr_consilier_data_expirare"
CONF_ADR_ECHIPAMENT_COMPLET: Final = "adr_echipament_complet"

# ─────────────────────────────────────────────
# 11. Tahograf
# ─────────────────────────────────────────────
CONF_TAHOGRAF_TIP: Final = "tahograf_tip"
CONF_TAHOGRAF_DATA_VERIFICARE: Final = "tahograf_data_verificare"
CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE: Final = "tahograf_data_urmatoare_verificare"
CONF_TAHOGRAF_DATA_CALIBRARE: Final = "tahograf_data_calibrare"

# ─────────────────────────────────────────────
# 12. Combustibil & AdBlue
# ─────────────────────────────────────────────
CONF_COMBUSTIBIL_CAPACITATE: Final = "combustibil_capacitate"
CONF_COMBUSTIBIL_NIVEL: Final = "combustibil_nivel"
CONF_COMBUSTIBIL_CONSUM_MEDIU: Final = "combustibil_consum_mediu"
CONF_ADBLUE_CAPACITATE: Final = "adblue_capacitate"
CONF_ADBLUE_NIVEL: Final = "adblue_nivel"
CONF_ALIMENTARE_DATA: Final = "alimentare_data"
CONF_ALIMENTARE_LITRI: Final = "alimentare_litri"
CONF_ALIMENTARE_PRET_LITRU: Final = "alimentare_pret_litru"
CONF_ALIMENTARE_COST: Final = "alimentare_cost"
CONF_ALIMENTARE_KM: Final = "alimentare_km"

# ─────────────────────────────────────────────
# 13. Mentenanță – Revizie ulei
# ─────────────────────────────────────────────
CONF_REVIZIE_ULEI_KM_ULTIMUL: Final = "revizie_ulei_km_ultimul"
CONF_REVIZIE_ULEI_KM_URMATOR: Final = "revizie_ulei_km_urmator"
CONF_REVIZIE_ULEI_DATA: Final = "revizie_ulei_data"
CONF_REVIZIE_ULEI_COST: Final = "revizie_ulei_cost"

# ─────────────────────────────────────────────
# 14. Mentenanță – Distribuție
# ─────────────────────────────────────────────
CONF_DISTRIBUTIE_KM_ULTIMUL: Final = "distributie_km_ultimul"
CONF_DISTRIBUTIE_KM_URMATOR: Final = "distributie_km_urmator"
CONF_DISTRIBUTIE_DATA: Final = "distributie_data"
CONF_DISTRIBUTIE_COST: Final = "distributie_cost"

# ─────────────────────────────────────────────
# 15. Mentenanță – Anvelope (extinse)
# ─────────────────────────────────────────────
CONF_ANVELOPE_VARA_DATA: Final = "anvelope_vara_data"
CONF_ANVELOPE_IARNA_DATA: Final = "anvelope_iarna_data"
CONF_ANVELOPE_COST: Final = "anvelope_cost"
CONF_ANVELOPE_DOT: Final = "anvelope_dot"
CONF_ANVELOPE_TIP: Final = "anvelope_tip"
CONF_ANVELOPE_NR_RESAPARI: Final = "anvelope_nr_resapari"
CONF_ANVELOPE_KM_MONTARE: Final = "anvelope_km_montare"

# ─────────────────────────────────────────────
# 16. Mentenanță – Baterie
# ─────────────────────────────────────────────
CONF_BATERIE_DATA_SCHIMB: Final = "baterie_data_schimb"
CONF_BATERIE_COST: Final = "baterie_cost"

# ─────────────────────────────────────────────
# 17. Mentenanță – Frâne
# ─────────────────────────────────────────────
CONF_PLACUTE_FRANA_KM_ULTIMUL: Final = "placute_frana_km_ultimul"
CONF_PLACUTE_FRANA_KM_URMATOR: Final = "placute_frana_km_urmator"
CONF_PLACUTE_FRANA_DATA: Final = "placute_frana_data"
CONF_PLACUTE_FRANA_COST: Final = "placute_frana_cost"
CONF_DISCURI_FRANA_KM_ULTIMUL: Final = "discuri_frana_km_ultimul"
CONF_DISCURI_FRANA_KM_URMATOR: Final = "discuri_frana_km_urmator"
CONF_DISCURI_FRANA_DATA: Final = "discuri_frana_data"
CONF_DISCURI_FRANA_COST: Final = "discuri_frana_cost"

# ─────────────────────────────────────────────
# 18. Mentenanță – DPF (Filtru particule)
# ─────────────────────────────────────────────
CONF_DPF_DATA_CURATARE: Final = "dpf_data_curatare"
CONF_DPF_KM_CURATARE: Final = "dpf_km_curatare"
CONF_DPF_COST: Final = "dpf_cost"

# ─────────────────────────────────────────────
# 19. Mentenanță – Turbosuflantă
# ─────────────────────────────────────────────
CONF_TURBO_DATA_REVIZIE: Final = "turbo_data_revizie"
CONF_TURBO_KM_REVIZIE: Final = "turbo_km_revizie"
CONF_TURBO_COST: Final = "turbo_cost"

# ─────────────────────────────────────────────
# 20. Echipament obligatoriu – Trusă de prim ajutor
# ─────────────────────────────────────────────
CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE: Final = "trusa_prim_ajutor_data_expirare"

# ─────────────────────────────────────────────
# 21. Echipament obligatoriu – Extinctor
# ─────────────────────────────────────────────
CONF_EXTINCTOR_DATA_EXPIRARE: Final = "extinctor_data_expirare"
CONF_EXTINCTOR_CAPACITATE: Final = "extinctor_capacitate"

# ─────────────────────────────────────────────
# 22. Remorcă / Semiremorcă
# ─────────────────────────────────────────────
CONF_REMORCA_NR_INMATRICULARE: Final = "remorca_nr_inmatriculare"
CONF_REMORCA_TIP: Final = "remorca_tip"
CONF_REMORCA_MARCA: Final = "remorca_marca"
CONF_REMORCA_MMA: Final = "remorca_mma"
CONF_REMORCA_MASA_PROPRIE: Final = "remorca_masa_proprie"
CONF_REMORCA_NR_AXE: Final = "remorca_nr_axe"
CONF_REMORCA_AN_FABRICATIE: Final = "remorca_an_fabricatie"
CONF_REMORCA_ITP_DATA_EXPIRARE: Final = "remorca_itp_data_expirare"
CONF_REMORCA_RCA_DATA_EXPIRARE: Final = "remorca_rca_data_expirare"
CONF_REMORCA_ROVINIETA_DATA_SFARSIT: Final = "remorca_rovinieta_data_sfarsit"

# ─────────────────────────────────────────────
# 23. Costuri extinse
# ─────────────────────────────────────────────
CONF_TAXA_DRUM_TARA: Final = "taxa_drum_tara"
CONF_TAXA_DRUM_SUMA: Final = "taxa_drum_suma"
CONF_TAXA_DRUM_VALUTA: Final = "taxa_drum_valuta"
CONF_TAXA_DRUM_DATA: Final = "taxa_drum_data"
CONF_AMENDA_SUMA: Final = "amenda_suma"
CONF_AMENDA_MOTIV: Final = "amenda_motiv"
CONF_AMENDA_TARA: Final = "amenda_tara"
CONF_AMENDA_DATA: Final = "amenda_data"
CONF_AMENDA_STATUS: Final = "amenda_status"

# ─────────────────────────────────────────────
# Opțiuni pentru selectoare
# ─────────────────────────────────────────────
COMBUSTIBIL_OPTIONS: Final = [
    "benzina",
    "diesel",
    "hybrid",
    "electric",
    "gpl",
    "cng",
    "lng",
]

TIP_PROPRIETATE_OPTIONS: Final = [
    "proprietate",
    "leasing",
    "leasing_operational",
    "inchiriere",
    "subcontractat",
]

TIP_VEHICUL_OPTIONS: Final = [
    "autotractor",
    "autocamion",
    "autobuz",
    "remorca",
    "semiremorca",
    "utilitara",
]

CATEGORIE_EURO_OPTIONS: Final = [
    "euro_3",
    "euro_4",
    "euro_5",
    "euro_6",
    "euro_6d",
]

TIP_SUSPENSIE_OPTIONS: Final = [
    "pneumatica",
    "mecanica",
]

TAHOGRAF_TIP_OPTIONS: Final = [
    "analog",
    "digital",
    "smart_v1",
    "smart_v2",
]

CPC_TIP_OPTIONS: Final = [
    "marfa",
    "persoane",
]

SOFER_APT_OPTIONS: Final = [
    "apt",
    "inapt",
    "restrictii",
]

REMORCA_TIP_OPTIONS: Final = [
    "semiremorca",
    "remorca",
    "cisterna",
    "frigorifica",
    "platforma",
    "prelata",
    "basculanta",
]

ANVELOPE_TIP_OPTIONS: Final = [
    "steer",
    "drive",
    "trailer",
    "all_position",
]

AMENDA_STATUS_OPTIONS: Final = [
    "platita",
    "neplatita",
    "contestata",
]

VALUTA_OPTIONS: Final = [
    "ron",
    "eur",
    "huf",
    "bgn",
    "czk",
    "pln",
]

TAXA_DRUM_TARA_OPTIONS: Final = [
    "ro",
    "hu",
    "at",
    "de",
    "bg",
    "cz",
    "pl",
    "sk",
    "si",
    "hr",
    "it",
    "fr",
    "es",
    "be",
    "nl",
    "ch",
]

# ─────────────────────────────────────────────
# Stări senzori
# ─────────────────────────────────────────────
STARE_NECONFIGURAT: Final = "neconfigurat"
STARE_EXPIRAT: Final = "expirat"
STARE_VALID: Final = "valid"

# ─────────────────────────────────────────────
# Licențiere
# ─────────────────────────────────────────────
CONF_LICENSE_KEY: Final = "license_key"
LICENSE_DATA_KEY: Final = "fleet_license_manager"

# ─────────────────────────────────────────────
# Servicii
# ─────────────────────────────────────────────
SERVICE_ACTUALIZEAZA_DATE: Final = "actualizeaza_date"
SERVICE_EXPORTA_DATE: Final = "exporta_date"
SERVICE_IMPORTA_DATE: Final = "importa_date"
SERVICE_BACKUP_FLOTA: Final = "backup_flota"
SERVICE_RESTORE_FLOTA: Final = "restore_flota"

# ─────────────────────────────────────────────
# Backup
# ─────────────────────────────────────────────
BACKUP_VERSION: Final = 2

# ─────────────────────────────────────────────
# Istoric costuri
# ─────────────────────────────────────────────
CONF_ISTORIC: Final = "_istoric"
CONF_ARHIVARE_DATE: Final = "_arhivare_date"

# ─────────────────────────────────────────────
# Atribute dispozitiv
# ─────────────────────────────────────────────
ATTR_NR_INMATRICULARE: Final = "nr_inmatriculare"
ATTR_MARCA: Final = "marca"
ATTR_MODEL: Final = "model"


# ─────────────────────────────────────────────
# Categorii arhivabile (pentru istoric costuri)
# ─────────────────────────────────────────────
CATEGORII_ARHIVABILE: Final = {
    "rca": {
        "Număr poliță": CONF_RCA_NUMAR_POLITA,
        "Companie": CONF_RCA_COMPANIE,
        "Data emitere": CONF_RCA_DATA_EMITERE,
        "Data expirare": CONF_RCA_DATA_EXPIRARE,
        "Cost (RON)": CONF_RCA_COST,
    },
    "casco": {
        "Număr poliță": CONF_CASCO_NUMAR_POLITA,
        "Companie": CONF_CASCO_COMPANIE,
        "Data emitere": CONF_CASCO_DATA_EMITERE,
        "Data expirare": CONF_CASCO_DATA_EXPIRARE,
        "Cost (RON)": CONF_CASCO_COST,
    },
    "itp": {
        "Data expirare": CONF_ITP_DATA_EXPIRARE,
        "Stație": CONF_ITP_STATIE,
        "Kilometraj": CONF_ITP_KILOMETRAJ,
    },
    "rovinieta": {
        "Data început": CONF_ROVINIETA_DATA_INCEPUT,
        "Data sfârșit": CONF_ROVINIETA_DATA_SFARSIT,
        "Categorie": CONF_ROVINIETA_CATEGORIE,
        "Preț (RON)": CONF_ROVINIETA_PRET,
    },
    "revizie_ulei": {
        "Km ultima revizie": CONF_REVIZIE_ULEI_KM_ULTIMUL,
        "Km următoarea revizie": CONF_REVIZIE_ULEI_KM_URMATOR,
        "Data": CONF_REVIZIE_ULEI_DATA,
        "Cost (RON)": CONF_REVIZIE_ULEI_COST,
    },
    "distributie": {
        "Km ultima schimbare": CONF_DISTRIBUTIE_KM_ULTIMUL,
        "Km următoarea schimbare": CONF_DISTRIBUTIE_KM_URMATOR,
        "Data": CONF_DISTRIBUTIE_DATA,
        "Cost (RON)": CONF_DISTRIBUTIE_COST,
    },
    "anvelope": {
        "Data montare vară": CONF_ANVELOPE_VARA_DATA,
        "Data montare iarnă": CONF_ANVELOPE_IARNA_DATA,
        "Cost (RON)": CONF_ANVELOPE_COST,
        "DOT": CONF_ANVELOPE_DOT,
        "Tip": CONF_ANVELOPE_TIP,
        "Nr. reșapări": CONF_ANVELOPE_NR_RESAPARI,
    },
    "baterie": {
        "Data schimb": CONF_BATERIE_DATA_SCHIMB,
        "Cost (RON)": CONF_BATERIE_COST,
    },
    "frane": {
        "Plăcuțe – Km ultima schimbare": CONF_PLACUTE_FRANA_KM_ULTIMUL,
        "Plăcuțe – Km următoarea schimbare": CONF_PLACUTE_FRANA_KM_URMATOR,
        "Plăcuțe – Data schimbare": CONF_PLACUTE_FRANA_DATA,
        "Plăcuțe – Cost (RON)": CONF_PLACUTE_FRANA_COST,
        "Discuri – Km ultima schimbare": CONF_DISCURI_FRANA_KM_ULTIMUL,
        "Discuri – Km următoarea schimbare": CONF_DISCURI_FRANA_KM_URMATOR,
        "Discuri – Data schimbare": CONF_DISCURI_FRANA_DATA,
        "Discuri – Cost (RON)": CONF_DISCURI_FRANA_COST,
    },
    "dpf": {
        "Data curățare": CONF_DPF_DATA_CURATARE,
        "Km curățare": CONF_DPF_KM_CURATARE,
        "Cost (RON)": CONF_DPF_COST,
    },
    "turbo": {
        "Data revizie": CONF_TURBO_DATA_REVIZIE,
        "Km revizie": CONF_TURBO_KM_REVIZIE,
        "Cost (RON)": CONF_TURBO_COST,
    },
    "alimentare": {
        "Data": CONF_ALIMENTARE_DATA,
        "Litri": CONF_ALIMENTARE_LITRI,
        "Preț/litru": CONF_ALIMENTARE_PRET_LITRU,
        "Cost total": CONF_ALIMENTARE_COST,
        "Km la alimentare": CONF_ALIMENTARE_KM,
    },
    "copie_conforma": {
        "Număr": CONF_COPIE_CONFORMA_NUMAR,
        "Data expirare": CONF_COPIE_CONFORMA_DATA_EXPIRARE,
    },
}


# ─────────────────────────────────────────────
# Structura categoriilor (export / diagnostics)
# ─────────────────────────────────────────────
STRUCTURA_CATEGORII: Final = [
    ("identificare", [
        ("marca", CONF_MARCA),
        ("model", CONF_MODEL),
        ("vin", CONF_VIN),
        ("serie_civ", CONF_SERIE_CIV),
        ("an_fabricatie", CONF_AN_FABRICATIE),
        ("an_prima_inmatriculare", CONF_AN_PRIMA_INMATRICULARE),
        ("motorizare", CONF_MOTORIZARE),
        ("combustibil", CONF_COMBUSTIBIL),
        ("capacitate_cilindrica", CONF_CAPACITATE_CILINDRICA),
        ("putere_kw", CONF_PUTERE_KW),
        ("putere_cp", CONF_PUTERE_CP),
        ("tip_vehicul", CONF_TIP_VEHICUL),
        ("mma", CONF_MMA),
        ("masa_proprie", CONF_MASA_PROPRIE),
        ("nr_axe", CONF_NR_AXE),
        ("categorie_euro", CONF_CATEGORIE_EURO),
        ("tip_suspensie", CONF_TIP_SUSPENSIE),
    ]),
    ("kilometraj", [
        ("km_curent", CONF_KM_CURENT),
        ("ore_motor", CONF_ORE_MOTOR),
    ]),
    ("sofer", [
        ("nume", CONF_SOFER_NUME),
        ("cnp", CONF_SOFER_CNP),
        ("nr_permis", CONF_SOFER_NR_PERMIS),
        ("categorii_permis", CONF_SOFER_CATEGORII_PERMIS),
        ("data_expirare_permis", CONF_SOFER_DATA_EXPIRARE_PERMIS),
        ("cpc_numar", CONF_SOFER_CPC_NUMAR),
        ("cpc_data_expirare", CONF_SOFER_CPC_DATA_EXPIRARE),
        ("cpc_tip", CONF_SOFER_CPC_TIP),
        ("card_tahograf_numar", CONF_SOFER_CARD_TAHOGRAF_NUMAR),
        ("card_tahograf_data_expirare", CONF_SOFER_CARD_TAHOGRAF_DATA_EXPIRARE),
        ("atestat_adr_numar", CONF_SOFER_ATESTAT_ADR_NUMAR),
        ("atestat_adr_data_expirare", CONF_SOFER_ATESTAT_ADR_DATA_EXPIRARE),
        ("atestat_adr_clase", CONF_SOFER_ATESTAT_ADR_CLASE),
        ("fisa_medicala_data", CONF_SOFER_FISA_MEDICALA_DATA),
        ("fisa_medicala_data_expirare", CONF_SOFER_FISA_MEDICALA_DATA_EXPIRARE),
        ("fisa_medicala_apt", CONF_SOFER_FISA_MEDICALA_APT),
        ("fisa_psihologica_data", CONF_SOFER_FISA_PSIHOLOGICA_DATA),
        ("fisa_psihologica_data_expirare", CONF_SOFER_FISA_PSIHOLOGICA_DATA_EXPIRARE),
    ]),
    ("asigurari", {
        "rca": [
            ("numar_polita", CONF_RCA_NUMAR_POLITA),
            ("companie", CONF_RCA_COMPANIE),
            ("data_emitere", CONF_RCA_DATA_EMITERE),
            ("data_expirare", CONF_RCA_DATA_EXPIRARE),
            ("cost", CONF_RCA_COST),
        ],
        "casco": [
            ("numar_polita", CONF_CASCO_NUMAR_POLITA),
            ("companie", CONF_CASCO_COMPANIE),
            ("data_emitere", CONF_CASCO_DATA_EMITERE),
            ("data_expirare", CONF_CASCO_DATA_EXPIRARE),
            ("cost", CONF_CASCO_COST),
        ],
    }),
    ("documente", {
        "itp": [
            ("data_expirare", CONF_ITP_DATA_EXPIRARE),
            ("statie", CONF_ITP_STATIE),
            ("kilometraj", CONF_ITP_KILOMETRAJ),
        ],
        "rovinieta": [
            ("data_inceput", CONF_ROVINIETA_DATA_INCEPUT),
            ("data_sfarsit", CONF_ROVINIETA_DATA_SFARSIT),
            ("categorie", CONF_ROVINIETA_CATEGORIE),
            ("pret", CONF_ROVINIETA_PRET),
        ],
        "copie_conforma": [
            ("numar", CONF_COPIE_CONFORMA_NUMAR),
            ("data_expirare", CONF_COPIE_CONFORMA_DATA_EXPIRARE),
        ],
    }),
    ("licente", [
        ("licenta_transport_numar", CONF_LICENTA_TRANSPORT_NUMAR),
        ("licenta_transport_tip", CONF_LICENTA_TRANSPORT_TIP),
        ("licenta_transport_data_expirare", CONF_LICENTA_TRANSPORT_DATA_EXPIRARE),
        ("licenta_comunitara_numar", CONF_LICENTA_COMUNITARA_NUMAR),
        ("licenta_comunitara_data_expirare", CONF_LICENTA_COMUNITARA_DATA_EXPIRARE),
    ]),
    ("administrativ", [
        ("proprietar", CONF_PROPRIETAR),
        ("tip_proprietate", CONF_TIP_PROPRIETATE),
        ("impozit_suma", CONF_IMPOZIT_SUMA),
        ("impozit_scadenta", CONF_IMPOZIT_SCADENTA),
        ("impozit_localitate", CONF_IMPOZIT_LOCALITATE),
        ("leasing_data_expirare", CONF_LEASING_DATA_EXPIRARE),
    ]),
    ("adr", [
        ("certificat_numar", CONF_ADR_CERTIFICAT_NUMAR),
        ("certificat_data_expirare", CONF_ADR_CERTIFICAT_DATA_EXPIRARE),
        ("clase", CONF_ADR_CLASE),
        ("consilier_nume", CONF_ADR_CONSILIER_NUME),
        ("consilier_certificat", CONF_ADR_CONSILIER_CERTIFICAT),
        ("consilier_data_expirare", CONF_ADR_CONSILIER_DATA_EXPIRARE),
        ("echipament_complet", CONF_ADR_ECHIPAMENT_COMPLET),
    ]),
    ("tahograf", [
        ("tip", CONF_TAHOGRAF_TIP),
        ("data_verificare", CONF_TAHOGRAF_DATA_VERIFICARE),
        ("data_urmatoare_verificare", CONF_TAHOGRAF_DATA_URMATOARE_VERIFICARE),
        ("data_calibrare", CONF_TAHOGRAF_DATA_CALIBRARE),
    ]),
    ("combustibil_adblue", [
        ("capacitate_rezervor", CONF_COMBUSTIBIL_CAPACITATE),
        ("nivel_combustibil", CONF_COMBUSTIBIL_NIVEL),
        ("consum_mediu", CONF_COMBUSTIBIL_CONSUM_MEDIU),
        ("adblue_capacitate", CONF_ADBLUE_CAPACITATE),
        ("adblue_nivel", CONF_ADBLUE_NIVEL),
        ("alimentare_data", CONF_ALIMENTARE_DATA),
        ("alimentare_litri", CONF_ALIMENTARE_LITRI),
        ("alimentare_pret_litru", CONF_ALIMENTARE_PRET_LITRU),
        ("alimentare_cost", CONF_ALIMENTARE_COST),
        ("alimentare_km", CONF_ALIMENTARE_KM),
    ]),
    ("mentenanta", {
        "revizie_ulei": [
            ("km_ultimul", CONF_REVIZIE_ULEI_KM_ULTIMUL),
            ("km_urmator", CONF_REVIZIE_ULEI_KM_URMATOR),
            ("data", CONF_REVIZIE_ULEI_DATA),
            ("cost", CONF_REVIZIE_ULEI_COST),
        ],
        "distributie": [
            ("km_ultimul", CONF_DISTRIBUTIE_KM_ULTIMUL),
            ("km_urmator", CONF_DISTRIBUTIE_KM_URMATOR),
            ("data", CONF_DISTRIBUTIE_DATA),
            ("cost", CONF_DISTRIBUTIE_COST),
        ],
        "anvelope": [
            ("data_vara", CONF_ANVELOPE_VARA_DATA),
            ("data_iarna", CONF_ANVELOPE_IARNA_DATA),
            ("cost", CONF_ANVELOPE_COST),
            ("dot", CONF_ANVELOPE_DOT),
            ("tip", CONF_ANVELOPE_TIP),
            ("nr_resapari", CONF_ANVELOPE_NR_RESAPARI),
            ("km_montare", CONF_ANVELOPE_KM_MONTARE),
        ],
        "baterie": [
            ("data_schimb", CONF_BATERIE_DATA_SCHIMB),
            ("cost", CONF_BATERIE_COST),
        ],
        "frane": [
            ("placute_km_ultimul", CONF_PLACUTE_FRANA_KM_ULTIMUL),
            ("placute_km_urmator", CONF_PLACUTE_FRANA_KM_URMATOR),
            ("placute_data", CONF_PLACUTE_FRANA_DATA),
            ("placute_cost", CONF_PLACUTE_FRANA_COST),
            ("discuri_km_ultimul", CONF_DISCURI_FRANA_KM_ULTIMUL),
            ("discuri_km_urmator", CONF_DISCURI_FRANA_KM_URMATOR),
            ("discuri_data", CONF_DISCURI_FRANA_DATA),
            ("discuri_cost", CONF_DISCURI_FRANA_COST),
        ],
        "dpf": [
            ("data_curatare", CONF_DPF_DATA_CURATARE),
            ("km_curatare", CONF_DPF_KM_CURATARE),
            ("cost", CONF_DPF_COST),
        ],
        "turbo": [
            ("data_revizie", CONF_TURBO_DATA_REVIZIE),
            ("km_revizie", CONF_TURBO_KM_REVIZIE),
            ("cost", CONF_TURBO_COST),
        ],
    }),
    ("echipament", {
        "trusa_prim_ajutor": [
            ("data_expirare", CONF_TRUSA_PRIM_AJUTOR_DATA_EXPIRARE),
        ],
        "extinctor": [
            ("data_expirare", CONF_EXTINCTOR_DATA_EXPIRARE),
            ("capacitate", CONF_EXTINCTOR_CAPACITATE),
        ],
    }),
    ("remorca", [
        ("nr_inmatriculare", CONF_REMORCA_NR_INMATRICULARE),
        ("tip", CONF_REMORCA_TIP),
        ("marca", CONF_REMORCA_MARCA),
        ("mma", CONF_REMORCA_MMA),
        ("masa_proprie", CONF_REMORCA_MASA_PROPRIE),
        ("nr_axe", CONF_REMORCA_NR_AXE),
        ("an_fabricatie", CONF_REMORCA_AN_FABRICATIE),
        ("itp_data_expirare", CONF_REMORCA_ITP_DATA_EXPIRARE),
        ("rca_data_expirare", CONF_REMORCA_RCA_DATA_EXPIRARE),
        ("rovinieta_data_sfarsit", CONF_REMORCA_ROVINIETA_DATA_SFARSIT),
    ]),
    ("costuri_extinse", {
        "taxe_drum": [
            ("tara", CONF_TAXA_DRUM_TARA),
            ("suma", CONF_TAXA_DRUM_SUMA),
            ("valuta", CONF_TAXA_DRUM_VALUTA),
            ("data", CONF_TAXA_DRUM_DATA),
        ],
        "amenzi": [
            ("suma", CONF_AMENDA_SUMA),
            ("motiv", CONF_AMENDA_MOTIV),
            ("tara", CONF_AMENDA_TARA),
            ("data", CONF_AMENDA_DATA),
            ("status", CONF_AMENDA_STATUS),
        ],
    }),
]


def normalizeaza_numar(numar: str) -> str:
    """Normalizează numărul de înmatriculare pentru utilizare în ID-uri.

    Numărul trebuie introdus fără spații, cratime sau underscore (ex: B123ABC).
    Exemplu: 'B123ABC' -> 'b123abc'
    """
    return numar.strip().lower()
