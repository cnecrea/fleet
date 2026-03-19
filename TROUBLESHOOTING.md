# Manager de flotă — Troubleshooting

---

## Activare debug logging

Adaugă în `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.fleet: debug
```

Repornește Home Assistant pentru a aplica.

---

## Prefixe de log

Fiecare modul folosește un prefix distinct pentru filtrare:

| Prefix | Modul | Ce loghează |
|---|---|---|
| `[Fleet]` | `__init__.py` | Setup, unload, servicii, lifecycle |
| `[Fleet:License]` | `license.py` | Verificare licență, heartbeat, activare, cache, fingerprint |
| `[Fleet:Sensor]` | `sensor.py` | Creare/actualizare senzori, curățare entități orfane |

Pentru a filtra doar licențierea: caută `[Fleet:License]` în loguri.

---

## Erori la activare licență

### `already_used`
Cheia este activă pe altă instalare HA. Dezactiveaz-o de pe instalarea veche mai întâi, sau solicită o cheie nouă.

### `invalid_key`
Cheia nu există pe server sau a fost revocată. Verifică formatul (`FLEET-XXXX-XXXX-XXXX-XXXX`) și contactează suportul.

### `expired_key`
Cheia a expirat (licență anuală). Ai nevoie de o cheie nouă.

### `network_error`
Integrarea nu poate comunica cu serverul de licențiere. Verifică:
- Conexiunea la internet a instalării HA
- Că Home Assistant poate accesa URL-ul serverului
- Că nu există firewall/proxy care blochează conexiunea

### `invalid_signature`
Token-ul de la server nu a trecut verificarea criptografică Ed25519. Cauze posibile:
- Cheia publică din integrare nu corespunde cheii private de pe server
- Token-ul a fost alterat în tranzit

Contactează suportul.

### `fingerprint_mismatch`
Token-ul returnat de server nu corespunde instalării tale HA. Posibil:
- Problemă temporară de comunicare — încearcă din nou
- Server-ul a returnat un token pentru alt fingerprint (bug rar)

Contactează suportul dacă persistă.

### `invalid_hmac`
Semnătura de integritate a request-ului e invalidă. Posibil:
- Ceasul sistemului e desincronizat semnificativ
- Problemă de rețea care a alterat request-ul

Verifică ora sistemului (`date` în terminal) și sincronizează cu NTP.

---

## Erori generale

### „Licență necesară" pe toți senzorii

Cauze posibile (în ordinea probabilității):
1. **Trial-ul de 30 zile a expirat** — activează o cheie de licență
2. **Nu ai activat încă o cheie** — mergi la Configurare → Licență
3. **Licența anuală a expirat** — activează o cheie nouă
4. **Serverul de licențiere indisponibil și cache-ul a expirat** — verifică conexiunea la internet
5. **Licența a fost revocată de administrator** — contactează suportul

### Un singur senzor după adăugarea vehiculului

Comportament normal. La prima configurare ai doar nr. de înmatriculare — apare doar senzorul de informații generale. Senzorii apar automat pe măsură ce completezi date din meniul de opțiuni.

### Senzorii nu se actualizează după configurare

Așteaptă câteva secunde — senzorii se actualizează la următorul ciclu de refresh HA. Dacă nu apar senzori noi, repornește Home Assistant.

### Entități orfane (senzori care nu mai au date)

Integrarea curăță automat entitățile orfane (senzori ale căror condiții nu mai sunt îndeplinite). Acest lucru se întâmplă la fiecare reload al integrării. În loguri, vezi mesaje cu prefix `[Fleet:Sensor]` despre curățare.

---

## Comportament offline

Integrarea necesită conexiune la internet doar pentru verificarea licenței. Datele despre vehicule sunt stocate exclusiv local.

Dacă internetul e indisponibil:
- **Cache valid** (sub 24h de la ultima verificare): integrarea funcționează normal
- **Cache expirat** (peste 24h fără internet): senzorii afișează „Licență necesară"
- **Datele locale**: rămân salvate indiferent de starea conexiunii
- **La reconectare**: se verifică automat la server și totul revine la normal

Intervalul de cache (24h implicit) e controlat de server prin câmpul `valid_until`. Limitele: minimum 5 minute, maximum 24 ore. Fără niciun token, verifică la fiecare 4 ore.

---

## Comportament la dezinstalare

### Ștergere vehicul individual
1. Se descarcă platformele (senzori)
2. Se elimină entry-ul din `hass.data`
3. Se șterg entitățile și dispozitivul din registry

### Ștergere ultimul vehicul (cleanup complet)
1. Se oprește heartbeat-ul periodic
2. Se elimină LicenseManager din memorie
3. Se elimină domeniul din `hass.data`
4. Se dezînregistrează cele 3 servicii (`actualizeaza_date`, `exporta_date`, `importa_date`)

---

## Date tehnice de referință

| Parametru | Valoare |
|---|---|
| Domeniu | `fleet` |
| Platforme | `sensor` |
| Senzori per vehicul | până la 38 (condiționați) |
| Constante CONF_* | 145 |
| Selectoare | 13 |
| Servicii | 3 |
| Categorii config | 17 |
| Limbi | Română, Engleză |
| Backup version | 2 |
| Storage version | 1 |
| IoT Class | calculated |

---

## Suport

- **GitHub Issues:** https://github.com/cnecrea/fleet/issues

---

**Copyright (c) 2026 Ciprian Nicolae. All rights reserved.**
