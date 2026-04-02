# Manager de flotă — Întrebări frecvente (FAQ)

- [Licență — Ce e și de ce am nevoie de ea?](#ce-e-licența-și-de-ce-am-nevoie-de-ea)
- [Licență — Am introdus licența dar senzorii tot arată „Licență necesară". De ce?](#am-introdus-licența-dar-senzorii-tot-arată-licență-necesară-de-ce)
- [Licența este per vehicul sau per instalare Home Assistant?](#licența-este-per-vehicul-sau-per-instalare-home-assistant)
- [Ce tipuri de licență există?](#ce-tipuri-de-licență-există)
- [Cum activez o licență?](#cum-activez-o-licență)
- [Cum dezactivez o licență?](#cum-dezactivez-o-licență)
- [De ce aș dezactiva licența?](#de-ce-aș-dezactiva-licența)
- [Pot folosi aceeași licență pe două instalări HA simultan?](#pot-folosi-aceeași-licență-pe-două-instalări-ha-simultan)
- [Ce se întâmplă când expiră licența?](#ce-se-întâmplă-când-expiră-licența)
- [Licența poate fi suspendată?](#licența-poate-fi-suspendată)
- [Există plată recurentă obligatorie?](#există-plată-recurentă-obligatorie)
- [Ce se întâmplă dacă serverul de licențiere e indisponibil?](#ce-se-întâmplă-dacă-serverul-de-licențiere-e-indisponibil)
- [Cât de des comunică integrarea cu serverul?](#cât-de-des-comunică-integrarea-cu-serverul)
- [Cum funcționează trial-ul?](#cum-funcționează-trial-ul)
- [Ce funcționalități am în trial?](#ce-funcționalități-am-în-trial)
- [Pot prelungi trial-ul?](#pot-prelungi-trial-ul)
- [Ce se întâmplă la finalul trial-ului?](#ce-se-întâmplă-la-finalul-trial-ului)
- [Dacă reinstalezi Home Assistant, primești alt trial?](#dacă-reinstalezi-home-assistant-primești-alt-trial)
- [Câte vehicule pot adăuga?](#câte-vehicule-pot-adăuga)
- [Pot avea mai mulți șoferi per vehicul?](#pot-avea-mai-mulți-șoferi-per-vehicul)
- [Ce se întâmplă dacă nu completez toate datele?](#ce-se-întâmplă-dacă-nu-completez-toate-datele)
- [Cum funcționează countdown-ul pentru documente?](#cum-funcționează-countdown-ul-pentru-documente)
- [Ce documente au countdown automat?](#ce-documente-au-countdown-automat)
- [Cum se calculează sarcina utilă?](#cum-se-calculează-sarcina-utilă)
- [Pot avea remorcă fără vehicul?](#pot-avea-remorcă-fără-vehicul)
- [Ce format au datele calendaristice?](#ce-format-au-datele-calendaristice)
- [Cum funcționează tracking-ul de km?](#cum-funcționează-tracking-ul-de-km)
- [Ce se întâmplă când reînnoi un document sau fac o operațiune?](#ce-se-întâmplă-când-reînnoi-un-document-sau-fac-o-operațiune)
- [Câte intrări de istoric se păstrează?](#câte-intrări-de-istoric-se-păstrează)
- [Ce categorii au arhivare automată?](#ce-categorii-au-arhivare-automată)
- [Cum se calculează costul total?](#cum-se-calculează-costul-total)
- [Cum actualizez km-ul automat dintr-un GPS tracker?](#cum-actualizez-km-ul-automat-dintr-un-gps-tracker)
- [Cum fac backup la datele unui vehicul?](#cum-fac-backup-la-datele-unui-vehicul)
- [Pot muta date între instalări HA?](#pot-muta-date-între-instalări-ha)
- [Ce format are backup-ul?](#ce-format-are-backup-ul)

---

## Ce e licența și de ce am nevoie de ea?

<a name="ce-e-licența-și-de-ce-am-nevoie-de-ea"></a>

Integrarea folosește un sistem de licențiere **server-side (v3.3)** cu semnături **Ed25519** și **HMAC-SHA256**. Fără o licență validă, integrarea afișează doar senzorul „Licență necesară" și nu creează senzori sau servicii funcționale.

Licența se achiziționează de la: [hubinteligent.org/licenta/fleet](https://hubinteligent.org/licenta/fleet)

După achiziție, introdu cheia de licență din OptionsFlow:
1. **Setări** → **Dispozitive și Servicii** → **Manager de flotă** → **Configurare**
2. Selectează **Licență**
3. Completează câmpul „Cheie licență"
4. Salvează

---

## Am introdus licența dar senzorii tot arată „Licență necesară". De ce?

<a name="am-introdus-licența-dar-senzorii-tot-arată-licență-necesară-de-ce"></a>

Câteva cauze posibile:

1. **Licența nu a fost validată** — verifică logurile pentru mesaje cu `LICENSE`
2. **Serverul de licențe nu este accesibil** — dacă HA nu are acces la internet, validarea eșuează
3. **Cheie greșită** — verifică că ai copiat cheia corect, fără spații suplimentare
4. **Restartare necesară** — în rare cazuri, un restart al HA poate rezolva problema

Activează debug logging ([TROUBLESHOOTING.md](TROUBLESHOOTING.md)) și caută mesaje legate de licență.

---

## Licențiere

<a name="licența-este-per-vehicul-sau-per-instalare-home-assistant"></a>

### Licența este per vehicul sau per instalare Home Assistant?

<a name="licența-este-per-vehicul-sau-per-instalare-home-assistant"></a>

Per instalare Home Assistant. O singură cheie de licență acoperă **toate vehiculele** adăugate pe acea instalare, indiferent de numărul lor. Poți adăuga 1 vehicul sau 100 — aceeași licență le acoperă pe toate.

### Ce tipuri de licență există?

<a name="ce-tipuri-de-licență-există"></a>

| Tip | Durată | Descriere |
|---|---|---|
| **perpetual** | nelimitată | Fără expirare, plată unică |
| **annual** | 365 zile | De la activare, necesită reînnoire |
| **semi_annual** | 180 zile | ~6 luni de la activare |
| **monthly** | 30 zile | De la activare, necesită reînnoire |

### Cum activez o licență?

<a name="cum-activez-o-licență"></a>

1. Primești cheia (format: `FLEET-XXXX-XXXX-XXXX-XXXX`)
2. **Setări → Dispozitive și servicii → Manager de flotă**
3. Alegi orice vehicul → **Configurare** → **Licență**
4. Introduci cheia → se activează automat
5. Licența se aplică imediat pe toate vehiculele

### Cum dezactivez o licență?

<a name="cum-dezactivez-o-licență"></a>

Din același meniu **Licență** din opțiunile integrării. Cheia revine la status „unused" pe server și poate fi reactivată pe altă instalare.

### De ce aș dezactiva licența?

<a name="de-ce-aș-dezactiva-licența"></a>

Dacă muți Home Assistant pe alt hardware (alt server, alt Raspberry Pi, alt NAS). Fingerprint-ul se schimbă odată cu hardware-ul sau reinstalarea OS-ului. Dezactivezi pe serverul vechi, reactivezi pe cel nou cu aceeași cheie.

### Pot folosi aceeași licență pe două instalări HA simultan?

<a name="pot-folosi-aceeași-licență-pe-două-instalări-ha-simultan"></a>

Nu. O cheie poate fi activă pe un singur fingerprint la un moment dat. Dacă încerci să activezi pe alt fingerprint fără dezactivare, serverul refuză cu eroarea `already_used`.

### Ce se întâmplă când expiră licența?

<a name="ce-se-întâmplă-când-expiră-licența"></a>

Senzorii afișează „Licență necesară" în loc de date. Se aplică la toate tipurile cu durată limitată (annual, semi_annual, monthly). Configurarea și datele salvate rămân intacte. La activarea unei chei noi, totul revine la normal — nu pierzi nimic.

### Licența poate fi suspendată?

<a name="licența-poate-fi-suspendată"></a>

Da, de către administrator pe server. Statusul devine `revoked` — senzorii afișează „Licență necesară". Un trial poate fi de asemenea revocat manual.

### Există plată recurentă obligatorie?

<a name="există-plată-recurentă-obligatorie"></a>

Nu obligatoriu. Depinde de tipul licenței alese: perpetual (plată unică) sau annual/semi_annual/monthly (plată la expirare).

### Ce se întâmplă dacă serverul de licențiere e indisponibil?

<a name="ce-se-întâmplă-dacă-serverul-de-licențiere-e-indisponibil"></a>

Integrarea folosește un cache local al ultimului răspuns valid (implicit 24 de ore). Dacă serverul e indisponibil câteva ore, integrarea continuă normal. La expirarea cache-ului, senzorii afișează „Licență necesară" până la reconectare.

### Cât de des comunică integrarea cu serverul?

<a name="cât-de-des-comunică-integrarea-cu-serverul"></a>

Implicit la fiecare **24 de ore**. Intervalul e controlat de server. Dacă cache-ul e valid, nu se face niciun request.

---

## Trial (perioadă de evaluare)

### Cum funcționează trial-ul?

<a name="cum-funcționează-trial-ul"></a>

La prima instalare și prima comunicare cu serverul, se creează automat **30 de zile** de evaluare. Nu trebuie să faci nimic — se activează singur.

### Ce funcționalități am în trial?

<a name="ce-funcționalități-am-în-trial"></a>

Toate. Zero restricții. Toate categoriile, toți senzorii, toate serviciile.

### Pot prelungi trial-ul?

<a name="pot-prelungi-trial-ul"></a>

Nu. 30 de zile per fingerprint, controlat server-side. Nu se poate reseta sau prelungi local.

### Ce se întâmplă la finalul trial-ului?

<a name="ce-se-întâmplă-la-finalul-trial-ului"></a>

Senzorii afișează „Licență necesară". Configurarea rămâne salvată. La activarea unei licențe, totul revine la normal.

### Dacă reinstalezi Home Assistant, primești alt trial?

<a name="dacă-reinstalezi-home-assistant-primești-alt-trial"></a>

Fingerprint-ul se schimbă la reinstalare completă (UUID nou + machine-id nou). Un fingerprint nou primește un trial nou.

---

## Vehicule și configurare

### Câte vehicule pot adăuga?

<a name="câte-vehicule-pot-adăuga"></a>

Nelimitat, cu licență validă sau în trial.

### Pot avea mai mulți șoferi per vehicul?

<a name="pot-avea-mai-mulți-șoferi-per-vehicul"></a>

Momentan, fiecare vehicul are un singur set de date pentru șofer. La schimbarea șoferului, actualizezi datele din meniu.

### Ce se întâmplă dacă nu completez toate datele?

<a name="ce-se-întâmplă-dacă-nu-completez-toate-datele"></a>

Nimic. Senzorii sunt condiționați — apar doar când au date completate. Poți completa treptat.

### Cum funcționează countdown-ul pentru documente?

<a name="cum-funcționează-countdown-ul-pentru-documente"></a>

Fiecare document cu dată de expirare afișează zilele rămase și starea: valid / expiră curând / expirat. Poți folosi senzorii în automatizări HA pentru notificări (ex: notificare la 30 zile înainte de expirarea RCA).

### Ce documente au countdown automat?

<a name="ce-documente-au-countdown-automat"></a>

RCA, Casco, ITP, Rovinieta, permis de conducere, CPC, card tahograf, fișe medicale și psihologice, atestat ADR șofer, licență transport, copie conformă, licență comunitară, certificat ADR vehicul, trusă prim ajutor, extinctor, ITP/RCA/rovinieta remorcă.

### Cum se calculează sarcina utilă?

<a name="cum-se-calculează-sarcina-utilă"></a>

Automat: **MMA − masa proprie**. Apare ca atribut, atât pentru vehicul cât și pentru remorcă.

### Pot avea remorcă fără vehicul?

<a name="pot-avea-remorcă-fără-vehicul"></a>

Nu. Remorca e o sub-categorie a vehiculului — se configurează în cadrul unui vehicul existent.

### Ce format au datele calendaristice?

<a name="ce-format-au-datele-calendaristice"></a>

Se introduc în format românesc **ZZ.LL.AAAA** (ex: 18.04.2026). Intern se stochează în format ISO (2026-04-18).

---

## Mentenanță

### Cum funcționează tracking-ul de km?

<a name="cum-funcționează-tracking-ul-de-km"></a>

Pentru revizie ulei, distribuție, plăcuțe și discuri frână: senzorul calculează automat km rămași din diferența între km următoarea operațiune și km curent. Exemplu: revizie la 100.000 km, km curent 95.000 → afișează „5.000 km rămași".

### Ce se întâmplă când reînnoi un document sau fac o operațiune?

<a name="ce-se-întâmplă-când-reînnoi-un-document-sau-fac-o-operațiune"></a>

Datele vechi se **arhivează automat**. Nu pierzi nimic. Istoricul e disponibil ca atribute ale senzorului și e folosit pentru calculul costului total pe ani.

### Câte intrări de istoric se păstrează?

<a name="câte-intrări-de-istoric-se-păstrează"></a>

Nelimitat. Fiecare reînnoire adaugă o intrare nouă.

### Ce categorii au arhivare automată?

<a name="ce-categorii-au-arhivare-automată"></a>

RCA, Casco, ITP, Rovinieta, revizie ulei, distribuție, anvelope, baterie, frâne, DPF, turbo, alimentare, copie conformă.

### Cum se calculează costul total?

<a name="cum-se-calculează-costul-total"></a>

Senzorul de cost total adună automat pe anul curent: asigurări (RCA + Casco), taxe (rovinieta, impozit, taxe drum), mentenanță (revizie, distribuție, anvelope, baterie, frâne, DPF, turbo), combustibil (alimentări). Include și istoric pe ani anteriori din datele arhivate.

---

## Servicii și automatizări

### Cum actualizez km-ul automat dintr-un GPS tracker?

<a name="cum-actualizez-km-ul-automat-dintr-un-gps-tracker"></a>

```yaml
service: fleet.actualizeaza_date
data:
  nr_inmatriculare: "B123ABC"
  km_curent: "{{ states('sensor.gps_tracker_km') | int }}"
```

### Cum fac backup la datele unui vehicul?

<a name="cum-fac-backup-la-datele-unui-vehicul"></a>

Apelează `fleet.exporta_date` cu nr. de înmatriculare. Fișierul se salvează în `config/`. Restaurează cu `fleet.importa_date`.

### Pot muta date între instalări HA?

<a name="pot-muta-date-între-instalări-ha"></a>

Da. Exportă pe instalarea veche, copiază JSON-ul pe noua instalare, importă. Include toate datele și istoricul.

### Ce format are backup-ul?

<a name="ce-format-are-backup-ul"></a>

JSON structurat pe categorii, versiune 2. Conține tot inclusiv arhiva. Compatibil cu importul din versiuni anterioare.

---

## Documentație conexă

- **[README.md](README.md)** — Prezentare, instalare, configurare completă
- **[PRIVACY.md](PRIVACY.md)** — Ce date se transmit, securitate, confidențialitate
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Debug, logging, erori și soluții

---

**Copyright (c) 2026 Ciprian Nicolae. All rights reserved.**
