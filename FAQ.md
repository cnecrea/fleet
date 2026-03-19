# Manager de flotă — Întrebări frecvente (FAQ)

---

## Licențiere

### Licența este per vehicul sau per instalare Home Assistant?

Per instalare Home Assistant. O singură cheie de licență acoperă **toate vehiculele** adăugate pe acea instalare, indiferent de numărul lor. Poți adăuga 1 vehicul sau 100 — aceeași licență le acoperă pe toate.

### Ce tipuri de licență există?

| Tip | Durată | Descriere |
|---|---|---|
| **perpetual** | nelimitată | Fără expirare, plată unică |
| **annual** | 365 zile | De la activare, necesită reînnoire |
| **semi_annual** | 180 zile | ~6 luni de la activare |
| **monthly** | 30 zile | De la activare, necesită reînnoire |

### Cum activez o licență?

1. Primești cheia (format: `FLEET-XXXX-XXXX-XXXX-XXXX`)
2. **Setări → Dispozitive și servicii → Manager de flotă**
3. Alegi orice vehicul → **Configurare** → **Licență**
4. Introduci cheia → se activează automat
5. Licența se aplică imediat pe toate vehiculele

### Cum dezactivez o licență?

Din același meniu **Licență** din opțiunile integrării. Cheia revine la status „unused" pe server și poate fi reactivată pe altă instalare.

### De ce aș dezactiva licența?

Dacă muți Home Assistant pe alt hardware (alt server, alt Raspberry Pi, alt NAS). Fingerprint-ul se schimbă odată cu hardware-ul sau reinstalarea OS-ului. Dezactivezi pe serverul vechi, reactivezi pe cel nou cu aceeași cheie.

### Pot folosi aceeași licență pe două instalări HA simultan?

Nu. O cheie poate fi activă pe un singur fingerprint la un moment dat. Dacă încerci să activezi pe alt fingerprint fără dezactivare, serverul refuză cu eroarea `already_used`.

### Ce se întâmplă când expiră licența?

Senzorii afișează „Licență necesară" în loc de date. Se aplică la toate tipurile cu durată limitată (annual, semi_annual, monthly). Configurarea și datele salvate rămân intacte. La activarea unei chei noi, totul revine la normal — nu pierzi nimic.

### Licența poate fi suspendată?

Da, de către administrator pe server. Statusul devine `revoked` — senzorii afișează „Licență necesară". Un trial poate fi de asemenea revocat manual.

### Există plată recurentă obligatorie?

Nu obligatoriu. Depinde de tipul licenței alese: perpetual (plată unică) sau annual/semi_annual/monthly (plată la expirare).

### Ce se întâmplă dacă serverul de licențiere e indisponibil?

Integrarea folosește un cache local al ultimului răspuns valid (implicit 24 de ore). Dacă serverul e indisponibil câteva ore, integrarea continuă normal. La expirarea cache-ului, senzorii afișează „Licență necesară" până la reconectare.

### Cât de des comunică integrarea cu serverul?

Implicit la fiecare **24 de ore**. Intervalul e controlat de server. Dacă cache-ul e valid, nu se face niciun request.

---

## Trial (perioadă de evaluare)

### Cum funcționează trial-ul?

La prima instalare și prima comunicare cu serverul, se creează automat **30 de zile** de evaluare. Nu trebuie să faci nimic — se activează singur.

### Ce funcționalități am în trial?

Toate. Zero restricții. Toate categoriile, toți senzorii, toate serviciile.

### Pot prelungi trial-ul?

Nu. 30 de zile per fingerprint, controlat server-side. Nu se poate reseta sau prelungi local.

### Ce se întâmplă la finalul trial-ului?

Senzorii afișează „Licență necesară". Configurarea rămâne salvată. La activarea unei licențe, totul revine la normal.

### Dacă reinstalezi Home Assistant, primești alt trial?

Fingerprint-ul se schimbă la reinstalare completă (UUID nou + machine-id nou). Un fingerprint nou primește un trial nou.

---

## Vehicule și configurare

### Câte vehicule pot adăuga?

Nelimitat, cu licență validă sau în trial.

### Pot avea mai mulți șoferi per vehicul?

Momentan, fiecare vehicul are un singur set de date pentru șofer. La schimbarea șoferului, actualizezi datele din meniu.

### Ce se întâmplă dacă nu completez toate datele?

Nimic. Senzorii sunt condiționați — apar doar când au date completate. Poți completa treptat.

### Cum funcționează countdown-ul pentru documente?

Fiecare document cu dată de expirare afișează zilele rămase și starea: valid / expiră curând / expirat. Poți folosi senzorii în automatizări HA pentru notificări (ex: notificare la 30 zile înainte de expirarea RCA).

### Ce documente au countdown automat?

RCA, Casco, ITP, Rovinieta, permis de conducere, CPC, card tahograf, fișe medicale și psihologice, atestat ADR șofer, licență transport, copie conformă, licență comunitară, certificat ADR vehicul, trusă prim ajutor, extinctor, ITP/RCA/rovinieta remorcă.

### Cum se calculează sarcina utilă?

Automat: **MMA − masa proprie**. Apare ca atribut, atât pentru vehicul cât și pentru remorcă.

### Pot avea remorcă fără vehicul?

Nu. Remorca e o sub-categorie a vehiculului — se configurează în cadrul unui vehicul existent.

### Ce format au datele calendaristice?

Se introduc în format românesc **ZZ.LL.AAAA** (ex: 18.04.2026). Intern se stochează în format ISO (2026-04-18).

---

## Mentenanță

### Cum funcționează tracking-ul de km?

Pentru revizie ulei, distribuție, plăcuțe și discuri frână: senzorul calculează automat km rămași din diferența între km următoarea operațiune și km curent. Exemplu: revizie la 100.000 km, km curent 95.000 → afișează „5.000 km rămași".

### Ce se întâmplă când reînnoi un document sau fac o operațiune?

Datele vechi se **arhivează automat**. Nu pierzi nimic. Istoricul e disponibil ca atribute ale senzorului și e folosit pentru calculul costului total pe ani.

### Câte intrări de istoric se păstrează?

Nelimitat. Fiecare reînnoire adaugă o intrare nouă.

### Ce categorii au arhivare automată?

RCA, Casco, ITP, Rovinieta, revizie ulei, distribuție, anvelope, baterie, frâne, DPF, turbo, alimentare, copie conformă.

### Cum se calculează costul total?

Senzorul de cost total adună automat pe anul curent: asigurări (RCA + Casco), taxe (rovinieta, impozit, taxe drum), mentenanță (revizie, distribuție, anvelope, baterie, frâne, DPF, turbo), combustibil (alimentări). Include și istoric pe ani anteriori din datele arhivate.

---

## Servicii și automatizări

### Cum actualizez km-ul automat dintr-un GPS tracker?

```yaml
service: fleet.actualizeaza_date
data:
  nr_inmatriculare: "B123ABC"
  km_curent: "{{ states('sensor.gps_tracker_km') | int }}"
```

### Cum fac backup la datele unui vehicul?

Apelează `fleet.exporta_date` cu nr. de înmatriculare. Fișierul se salvează în `config/`. Restaurează cu `fleet.importa_date`.

### Pot muta date între instalări HA?

Da. Exportă pe instalarea veche, copiază JSON-ul pe noua instalare, importă. Include toate datele și istoricul.

### Ce format are backup-ul?

JSON structurat pe categorii, versiune 2. Conține tot inclusiv arhiva. Compatibil cu importul din versiuni anterioare.

---

## Documentație conexă

- **[README.md](README.md)** — Prezentare, instalare, configurare completă
- **[PRIVACY.md](PRIVACY.md)** — Ce date se transmit, securitate, confidențialitate
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Debug, logging, erori și soluții

---

**Copyright (c) 2026 Ciprian Nicolae. All rights reserved.**
