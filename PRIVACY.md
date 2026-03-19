# Manager de flotă — Confidențialitate și securitate

---

## Principiu

Toate datele despre vehiculele, șoferii, documentele și costurile tale sunt stocate **exclusiv local** pe instalarea ta Home Assistant. Serverul de licențiere nu primește și nu stochează nicio informație despre flota ta.

---

## Ce date se transmit la serverul de licențiere

Integrarea comunică periodic cu serverul de licențiere (heartbeat) pentru verificarea licenței. Se transmit **exclusiv** următoarele câmpuri:

### La verificare status (`/check` — periodic, implicit la 24h)

| Câmp | Descriere | Conține date personale? |
|---|---|---|
| `fingerprint` | Hash SHA-256 ireversibil din UUID HA + machine-id + salt | Nu |
| `timestamp` | Momentul curent (unix timestamp) | Nu |
| `hmac` | Semnătură de integritate HMAC-SHA256 | Nu |

### La validare licență (`/validate` — periodic, doar dacă ai licență activă)

| Câmp | Descriere | Conține date personale? |
|---|---|---|
| `license_key` | Cheia de licență (ex: FLEET-XXXX-XXXX-XXXX-XXXX) | Nu |
| `fingerprint` | Hash SHA-256 ireversibil | Nu |
| `timestamp` | Momentul curent | Nu |
| `hmac` | Semnătură de integritate | Nu |

### La activare (`/activate` — o singură dată)

Aceleași câmpuri ca la validare: `license_key`, `fingerprint`, `timestamp`, `hmac`.

### La dezactivare (`/deactivate` — o singură dată, la cerere)

Aceleași câmpuri: `license_key`, `fingerprint`, `timestamp`, `hmac`.

---

## Ce date NU se transmit niciodată

- Numere de înmatriculare
- VIN-uri sau serii CIV
- Date despre vehicule (marcă, model, an, motorizare)
- Date despre șoferi (nume, CNP, nr. permis, categorii)
- Date despre documente (RCA, Casco, ITP, rovinieta, licențe transport)
- Kilometraj, ore motor
- Costuri (asigurări, mentenanță, taxe, amenzi, combustibil)
- Date de alimentare
- Date despre remorcă
- Date de mentenanță (revizie, distribuție, anvelope, frâne, DPF, turbo)
- Date despre echipament (trusă, extinctor)
- Adresa IP nu este stocată (e vizibilă la nivel HTTP, dar codul serverului nu o salvează în baza de date)

---

## Fingerprint — ce este și cum funcționează

Fingerprint-ul identifică **unic** instalarea ta Home Assistant. Se generează local din:

1. **UUID-ul instalării HA** — un identificator unic generat de Home Assistant la instalare
2. **Machine-ID-ul OS** — identificator unic al sistemului de operare
3. **Salt intern** — specific integrării Fleet

Aceste trei componente sunt concatenate și trecute prin **SHA-256**, producând un hash ireversibil de 64 caractere hexazecimale. Nimeni (inclusiv serverul) nu poate extrage datele originale din acest hash.

Fingerprint-ul se schimbă la:
- Reinstalarea completă a Home Assistant (UUID nou)
- Reinstalarea sistemului de operare (machine-id nou)
- Mutarea pe alt hardware

---

## Securitate criptografică

### Ed25519 (semnătură asimetrică)

Fiecare token de la server este semnat cu **Ed25519**:
- **Cheia privată** — există exclusiv pe server. Nu este distribuită.
- **Cheia publică** — încorporată în integrare. Permite doar verificarea semnăturilor, nu crearea lor.

Un token falsificat sau modificat este respins automat de integrare.

### HMAC-SHA256 (integritate request)

Fiecare request de la integrare la server este semnat cu **HMAC-SHA256**:
- Cheia HMAC = fingerprint-ul instalării
- Mesajul = JSON-ul payload-ului

Acest mecanism previne alterarea request-urilor în tranzit și asigură că fiecare request provine de la instalarea legitimă.

### Zero constante locale modificabile

Toate deciziile de autorizare (trial, expirare, intervale de cache) sunt controlate **exclusiv de server**. Integrarea nu are constante locale pentru durata trial-ului, perioadă de grație, sau intervale de verificare — aceste valori vin de la server în token-ul semnat.

---

## Stocare locală

Datele de licență (token, cheie mascată, timestamp-uri) se stochează local în Home Assistant prin mecanismul standard **HA Storage** (fișier `.storage/fleet_license`). Acest fișier conține:
- Token-ul de status (cache de la server)
- Token-ul de activare (semnat Ed25519)
- Cheia de licență
- Timestamp-uri (ultima verificare, activare)

Datele despre vehicule se stochează în entry-urile standard HA (`config_entries`), exclusiv local.

---

## Documentație conexă

- **[README.md](README.md)** — Prezentare, instalare, configurare
- **[FAQ.md](FAQ.md)** — Întrebări frecvente
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Debug, erori, soluții

---

**Copyright (c) 2026 Ciprian Nicolae. All rights reserved.**
