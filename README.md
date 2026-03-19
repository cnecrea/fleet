# Manager de flotă — Integrare Home Assistant

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-41BDF5?logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/cnecrea/fleet)](https://github.com/cnecrea/fleet/releases)
[![GitHub Stars](https://img.shields.io/github/stars/cnecrea/fleet?style=flat&logo=github)](https://github.com/cnecrea/fleet/stargazers)
[![Instalări](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cnecrea/fleet/main/statistici/shields/descarcari.json)](https://github.com/cnecrea/fleet)
[![Ultima versiune](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cnecrea/fleet/main/statistici/shields/ultima_release.json)](https://github.com/cnecrea/fleet/releases/latest)

---

## Despre

**Manager de flotă** este o integrare custom pentru Home Assistant care transformă instanța ta într-un sistem complet de management al flotei de vehicule. A fost concepută pentru firmele de transport, dar funcționează la fel de bine pentru oricine dorește să-și țină evidența vehiculelor într-un singur loc.

Integrarea centralizează toate informațiile legate de un vehicul: documente (RCA, ITP, rovinieta, licențe transport), asigurări, mentenanță cu tracking pe kilometri, combustibil și AdBlue, date despre șofer (permis, CPC, card tahograf, fișe medicale), remorcă, costuri extinse (taxe de drum pe 16 țări, amenzi) și echipament obligatoriu. Totul este accesibil prin interfața nativă Home Assistant, fără a depinde de aplicații externe.

Fiecare vehicul adăugat apare ca un **dispozitiv separat** cu senzori dedicați. Senzorii sunt **condiționați** — apar doar când au date completate. La prima configurare (doar nr. de înmatriculare), apare un singur senzor de informații generale. Pe măsură ce completezi date, apar automat senzorii corespunzători.

---

## Cum funcționează

Integrarea se bazează pe arhitectura nativă Home Assistant: **config entries** (câte unul per vehicul), **options flow** (pentru editare), **senzori** (pentru monitorizare) și **servicii** (pentru acțiuni automate).

**Fluxul de lucru:**
1. Adaugi un vehicul prin numărul de înmatriculare
2. Completezi datele din meniul de opțiuni (Setări → Manager de flotă → Configurare)
3. Senzorii apar automat pe baza datelor introduse
4. Home Assistant calculează countdown-uri, km rămași, costuri
5. Creezi automatizări pe baza senzorilor (ex: notificare la 30 de zile înainte de expirarea RCA)

**Datele sunt stocate local** în Home Assistant (`.storage/`). Singura comunicare externă este verificarea periodică a licenței cu serverul de licențe (vezi [PRIVACY.md](PRIVACY.md)).

---

## Cerințe

- **Home Assistant** 2024.1 sau mai nou
- **Conexiune la internet** — necesară pentru verificarea licenței (vezi [PRIVACY.md](PRIVACY.md))

---

## Instalare

### HACS (recomandat)

1. Deschide HACS → Integrări → ⋮ → **Depozite personalizate**
2. Adaugă `https://github.com/cnecrea/fleet` ca **Integrare**
3. Caută **Manager de flotă** și apasă **Descarcă**
4. Repornește Home Assistant

### Manual

1. Copiază folderul `fleet` în directorul `config/custom_components/`
2. Repornește Home Assistant

### După instalare

3. Mergi la **Setări → Dispozitive și servicii → Adaugă integrare**
4. Caută **Manager de flotă**
5. Introdu numărul de înmatriculare al vehiculului (format: B123ABC, fără spații)
6. Vehiculul apare imediat ca dispozitiv — configurarea datelor se face din **meniul de opțiuni** al integrării

Pentru vehicule suplimentare, repetă pașii 3–6. Nu există limită de vehicule cu licență validă.

---

## Configurare

Configurarea se face prin **meniul de opțiuni** al fiecărei intrări (vehicul). Completezi doar ce ai nevoie — senzorii apar automat pe baza datelor introduse.

Toate datele calendaristice se introduc în format românesc: **ZZ.LL.AAAA** (ex: 18.04.2026).

### Categorii disponibile

1. **Identificare vehicul** — nr. înmatriculare, serie CIV, VIN, marcă, model, an fabricație, an prima înmatriculare, motorizare, combustibil (benzină/diesel/hybrid/electric/GPL/CNG/LNG), capacitate cilindrică, putere kW/CP, tip vehicul (autotractor/autocamion/autobuz/remorcă/semiremorcă/utilitară), MMA, masa proprie, sarcina utilă (calculată automat: MMA − masa proprie), nr. axe, categorie Euro (3/4/5/6/6d), tip suspensie (pneumatică/mecanică)

2. **Kilometraj** — km curent (actualizabil și prin serviciu), ore motor

3. **RCA** — nr. poliță, companie, data emitere, data expirare, cost (RON)

4. **Casco** — nr. poliță, companie, data emitere, data expirare, cost (RON)

5. **ITP** — data expirare, stație ITP, kilometraj la ITP

6. **Rovinieta** — data început, data sfârșit, categorie, preț (RON)

7. **Date administrative** — proprietar, tip proprietate (proprietate/leasing/leasing operațional/închiriere/subcontractat), impozit (sumă, scadență, localitate), leasing data expirare

8. **Șofer** — nume, CNP, nr. permis, categorii permis, data expirare permis, CPC (număr, tip marfă/persoane, data expirare), card tahograf (număr, data expirare), atestat ADR (număr, clase, data expirare), fișă medicală (data, data expirare, rezultat apt/inapt/restricții), fișă psihologică (data, data expirare)

9. **Licențe transport** — licență transport (număr, tip, data expirare), copie conformă (număr, data expirare), licență comunitară (număr, data expirare)

10. **ADR** — certificat vehicul (număr, clase, data expirare), consilier siguranță (nume, nr. certificat, data expirare), echipament complet (da/nu)

11. **Tahograf** — tip (analog/digital/smart v1/smart v2), data verificare, data următoare verificare, data calibrare

12. **Combustibil și AdBlue** — capacitate rezervor, nivel combustibil (%), consum mediu (l/100km), AdBlue (capacitate, nivel), alimentare (data, litri, preț/litru, cost total, km)

13. **Mentenanță** — revizie ulei (km ultimul/următor, data, cost), distribuție (km ultimul/următor, data, cost), anvelope (data vară/iarnă, tip steer/drive/trailer/all position, DOT, nr. reșapări, km montare, cost), baterie (data schimb, cost), plăcuțe frână (km ultimul/următor, data, cost), discuri frână (km ultimul/următor, data, cost), DPF (data curățare, km, cost), turbosuflantă (data revizie, km, cost)

14. **Echipament obligatoriu** — trusă prim ajutor (data expirare), extinctor (data expirare, capacitate kg)

15. **Remorcă / Semiremorcă** — nr. înmatriculare, tip (semiremorcă/remorcă/cisternă/frigorifică/platformă/prelată/basculantă), marcă, MMA, masa proprie, sarcina utilă (calculată automat), nr. axe, an fabricație, ITP data expirare, RCA data expirare, rovinieta data expirare

16. **Costuri extinse** — taxe drum (16 țări: RO/HU/AT/DE/BG/CZ/PL/SK/SI/HR/IT/FR/ES/BE/NL/CH, sumă, valută RON/EUR/HUF/BGN/CZK/PLN, data), amenzi (sumă, motiv, țară, data, status plătită/neplătită/contestată)

17. **Licență software** — vizualizare status, perioadă de valabilitate (de la/până la), activare/reînnoire cheie de licență

---

## Senzori

Fiecare document cu dată de expirare generează un senzor cu **countdown automat** — afișează zilele rămase și starea (valid / expiră curând / expirat). Acești senzori pot fi folosiți în automatizări pentru notificări.

Categoriile de mentenanță cu tracking pe km (revizie ulei, distribuție, plăcuțe/discuri frână) afișează **km rămași** calculați automat din diferența între km următoarea operațiune și km curent al vehiculului.

Senzorul **Cost total** calculează automat costul pe anul curent, cu defalcare pe categorii (asigurări, taxe, mentenanță, combustibil) și istoric pe ani anteriori din datele arhivate.

### Exemple de automatizări

```yaml
# Notificare RCA expiră în 30 de zile
automation:
  - alias: "Manager flotă - RCA expiră curând"
    trigger:
      - platform: numeric_state
        entity_id: sensor.fleet_b123abc_rca
        below: 31
    action:
      - service: notify.mobile_app
        data:
          title: "Manager flotă - RCA expiră curând!"
          message: "RCA pentru B123ABC expiră în {{ states('sensor.fleet_b123abc_rca') }} zile."

# Notificare revizie ulei — sub 5000 km rămași
automation:
  - alias: "Manager flotă - Revizie ulei necesară"
    trigger:
      - platform: numeric_state
        entity_id: sensor.fleet_b123abc_revizie_ulei
        below: 5001
    action:
      - service: notify.mobile_app
        data:
          title: "Manager flotă - Revizie ulei"
          message: "B123ABC — mai sunt {{ states('sensor.fleet_b123abc_revizie_ulei') }} km până la schimbul de ulei."
```

---

## Arhivare automată

La reînnoirea unui document sau operațiune de mentenanță, datele vechi se **arhivează automat**. Istoricul e disponibil ca atribute ale senzorului.

Categorii arhivabile: RCA, Casco, ITP, Rovinieta, revizie ulei, distribuție, anvelope, baterie, frâne, DPF, turbo, alimentare, copie conformă.

Funcția de arhivare se activează din checkbox-ul **„Arhivează intrările vechi"** disponibil în fiecare categorie compatibilă.

---

## Servicii

### `fleet.actualizeaza_date`
Actualizează kilometrajul unui vehicul. Parametri: `nr_inmatriculare` (obligatoriu), `km_curent` (obligatoriu, 0–9.999.999).

### `fleet.exporta_date`
Exportă toate datele unui vehicul în fișier JSON (backup individual). Parametru: `nr_inmatriculare` (obligatoriu). Fișierul se salvează în `config/fleet_backup_<nr>.json`.

### `fleet.importa_date`
Importă datele dintr-un backup JSON. Dacă vehiculul nu există, îl creează automat. Parametru: `cale_fisier` (obligatoriu, ex: `/config/fleet_backup_b123abc.json`).

### `fleet.backup_flota`
Creează un **backup complet al întregii flote** într-o singură arhivă ZIP. Toate vehiculele configurate sunt exportate simultan. Nu necesită parametri.

Fișierul se salvează automat în `config/fleet_backups/fleet_backup_YYYYMMDD_HHMMSS.zip` cu următoarea structură:

```
fleet_backup_20260318_120000.zip
├── metadata.json          ← versiune, dată export, nr. vehicule
└── vehicule/
    ├── B123ABC.json       ← toate datele vehiculului B123ABC
    ├── TM55DEF.json       ← toate datele vehiculului TM55DEF
    └── ...                ← câte un JSON per vehicul
```

Backup-ul include toate categoriile: identificare, kilometraj, șofer, asigurări, documente, licențe, ADR, tahograf, combustibil, mentenanță, echipament, remorcă, costuri și istoric arhivat.

### `fleet.restore_flota`
Restaurează **toate vehiculele** dintr-o arhivă ZIP de backup. Parametru: `cale_fisier` (obligatoriu, ex: `/config/fleet_backups/fleet_backup_20260318_120000.zip`).

Comportament la restaurare:
- **Vehicul existent** (nr. înmatriculare deja configurat) → datele sunt actualizate cu cele din backup
- **Vehicul nou** (nr. înmatriculare inexistent) → vehiculul este creat automat ca entry nou

La final, se afișează o **notificare persistentă** cu raportul complet: câte vehicule au fost restaurate cu succes și câte au eșuat (dacă e cazul).

### Exemple de utilizare servicii

```yaml
# Backup zilnic al flotei la ora 2:00
automation:
  - alias: "Manager flotă - Backup zilnic"
    trigger:
      - platform: time
        at: "02:00:00"
    action:
      - service: fleet.backup_flota

# Actualizare km prin automatizare (ex: din OBD2)
automation:
  - alias: "Manager flotă - Actualizare km din OBD2"
    trigger:
      - platform: state
        entity_id: sensor.obd2_km
    action:
      - service: fleet.actualizeaza_date
        data:
          nr_inmatriculare: "B123ABC"
          km_curent: "{{ states('sensor.obd2_km') | int }}"
```

---

## Licențiere

Manager de flotă folosește un sistem de licențiere **server-side**. Licența este **per instalare Home Assistant** (nu per vehicul) — o singură licență acoperă toate vehiculele de pe acea instalare.

La prima instalare se activează automat o perioadă de **trial de 30 de zile** cu funcționalitate completă. După trial, este necesară activarea unei chei de licență.

### Tipuri de licență

| Tip | Durată | Descriere |
|---|---|---|
| **perpetual** | nelimitată | Fără dată de expirare, plată unică |
| **annual** | 365 zile | De la momentul activării |
| **semi_annual** | 180 zile | ~6 luni de la activare |
| **monthly** | 30 zile | De la momentul activării |

### Activare

Activarea se face din **Setări → Manager de flotă → Configurare → Licență**, unde introduci cheia primită (format: `FLEET-XXXX-XXXX-XXXX-XXXX`).

După activare, ecranul de licență afișează statusul complet: tipul licenței, cheia mascată, data activării și data expirării.

### Cum funcționează licențierea

- La fiecare pornire, integrarea trimite un **fingerprint** (hash unic al instalării HA) la serverul de licențe
- Serverul răspunde cu un **token semnat digital** (Ed25519) care confirmă statusul
- Token-ul este **cached local** — integrarea nu contactează serverul la fiecare acțiune, ci doar periodic (intervalul e controlat de server)
- Dacă serverul nu e disponibil temporar, integrarea continuă să funcționeze pe baza cache-ului valid
- Nicio dată personală sau despre vehicule nu este transmisă — doar fingerprint-ul instalării (vezi [PRIVACY.md](PRIVACY.md))

---

## Traduceri

Integrarea este disponibilă complet în **română** și **engleză**. Limba se schimbă automat pe baza limbii setate în Home Assistant.

---

## Structura fișierelor

```
custom_components/fleet/
├── __init__.py           ← Setup, servicii, backup/restore
├── config_flow.py        ← Config flow + options flow complet
├── const.py              ← Constante, opțiuni selectoare, mapping-uri
├── sensor.py             ← Toți senzorii (countdown, km, costuri)
├── license.py            ← Manager licențe (Ed25519, heartbeat)
├── manifest.json         ← Metadata integrare
├── services.yaml         ← Definiții servicii
├── strings.json          ← Traduceri de bază (EN)
└── translations/
    ├── en.json           ← Traduceri engleză
    └── ro.json           ← Traduceri română
```

---

## Debug / Logging

Pentru a activa loguri detaliate, adaugă în `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.fleet: debug
```

Logurile integrării includ prefix `[Fleet]` pentru componentele generale și `[Fleet:License]` pentru licențiere, facilitând filtrarea.

---

## Documentație suplimentară

- **[FAQ.md](FAQ.md)** — Întrebări frecvente despre licențiere, trial, vehicule, mentenanță, servicii
- **[PRIVACY.md](PRIVACY.md)** — Ce date se transmit la server, securitate, confidențialitate
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Debug, logging, erori comune și soluții

---

## Suport

- **GitHub Issues:** https://github.com/cnecrea/fleet/issues

---

**Copyright (c) 2026 Ciprian Nicolae. All rights reserved.**
