# Urban Scenario Library

## Scenario Format
Each scenario covers: Setting · Adversary subtype · Attack method · Access level · Evasion mechanism · AI subsystem targeted · Governance gap flagged

---

## U-01 — Mumbai Local Train, Peak Hours
**Context:** U1 (urban public), T1 (transit)  
**Setting:** Crowded women's compartment; adversary enters at station stop  
**Adversary:** Opportunistic (L0)  
**Attack method:** Suppress + Corrupt  
**Evasion:** Crowd density prevents CV proximity detection; train noise exceeds audio distress threshold; accelerometer cannot distinguish groping from transit movement  
**Subsystems targeted:** Vision, Audio, Sensor Fusion  
**Governance gap:** No conformity assessment standard addresses sensor fusion in high-vibration, high-noise transit environments  
**[CITATION NEEDED: NCRB Crime in India 2022, transport harassment statistics]**

---

## U-02 — App-Based Cab, Night Route
**Context:** U1 → R2 transition (urban to isolated)  
**Setting:** Solo woman passenger; route deviates from expected path  
**Adversary:** Adaptive (L1–L3)  
**Attack method:** Intercept + Spoof  
**Evasion:** Driver moves to low-signal area (corrupt GPS); phone placed face-down or in holder (suppress CV); speaking calmly defeats audio stress detection  
**Subsystems targeted:** GPS/Sensor Fusion, Vision, Audio  
**Governance gap:** No framework requires location-spoofing resistance in personal safety apps; DPDP Act covers data storage, not real-time attack surfaces  
**[CITATION NEEDED: incident data on cab-based harassment, India 2022–2024]**

---

## U-03 — Office / Workplace, Authority Figure
**Context:** U2 (semi-private)  
**Setting:** Late-evening office; adversary is senior colleague or manager  
**Adversary:** Informed (L4–L5)  
**Attack method:** Suppress via social leverage (L5) — no technical attack needed  
**Evasion:** Victim does not trigger alert because adversary holds employer authority; fear of professional consequences outweighs triggering cost  
**Subsystems targeted:** None — alert never initiated  
**Governance gap:** No framework governs sociotechnical suppression; EU AI Act Annex III does not classify workplace safety AI as high-risk  
**[CITATION NEEDED: iCall/iHuman — workplace harassment case patterns]**

---

## U-04 — Street Market, Shoulder Bag Obstruction
**Context:** U1 (urban public)  
**Setting:** Crowded market; adversary follows victim through stalls  
**Adversary:** Opportunistic (L0)  
**Attack method:** Suppress (Vision)  
**Evasion:** Victim's bag or crowd bodies block phone camera angle; CV proximity detection fails; audio baseline elevated by market noise  
**Subsystems targeted:** Vision, Audio  
**Governance gap:** No standard requires CV robustness testing under real-world occlusion conditions  
**[CITATION NEEDED: Safetipin safety audit data — market contexts]**

---

## U-05 — Bus Stop, Late Night — Exhaustion Attack
**Context:** U1 (urban public)  
**Setting:** Isolated bus stop; adversary has used the area before  
**Adversary:** Adaptive (L0)  
**Attack method:** Exhaust  
**Evasion:** Over previous weeks, adversary has triggered false proximity alerts from this location; victim's emergency contacts have begun ignoring notifications  
**Subsystems targeted:** Response layer (L4) — AI system works, human response is defeated  
**Governance gap:** No framework requires testing for alert exhaustion or contact response degradation over time  
**[CITATION NEEDED: no direct citation — novel attack vector, flag as such]**

---

## U-06 — College Campus, Known Acquaintance
**Context:** U2 (semi-private)  
**Setting:** Campus building, after hours; adversary is classmate or junior faculty  
**Adversary:** Adaptive (L1)  
**Attack method:** Corrupt + Social leverage  
**Evasion:** Adversary has observed prior app behavior; stays at edge of detection confidence; victim hesitates to trigger alert against known person in institutional setting  
**Subsystems targeted:** Vision, NLP  
**Governance gap:** NLP check-in systems not tested for neutral-language threat framing; social hesitation not addressed by any framework  
**[CITATION NEEDED: iCall — campus-context harassment patterns]**

---

## U-07 — Social Venue / Party, Noise + Alcohol Context
**Context:** U2 (semi-private)  
**Setting:** Party or social event; ambient noise high; victim may be impaired  
**Adversary:** Opportunistic to Adaptive (L0–L1)  
**Attack method:** Suppress + Corrupt  
**Evasion:** Venue noise corrupts audio classification; crowded, dimly lit space defeats vision proximity detection; victim's impairment raises threshold for triggering alert  
**Subsystems targeted:** Audio, Vision  
**Governance gap:** No certification requires robustness testing in high-ambient-noise social environments; impaired victim state not modeled in any standard  
**[CITATION NEEDED: no direct citation — extrapolate from NCRB assault context data]**

---

## U-08 — Public Toilet / Changing Area, Device Grab
**Context:** U1/U2  
**Setting:** Semi-enclosed public space; momentary isolation  
**Adversary:** Opportunistic (L2)  
**Attack method:** Intercept  
**Evasion:** Adversary grabs device before alert can be sent; or blocks the space (door) while device is out of reach  
**Subsystems targeted:** Communication layer (L3), Response layer (L4)  
**Governance gap:** No framework addresses physical device interception as a failure mode; evidence preservation not certified  
**[CITATION NEEDED: no direct citation — device-grab as suppression vector]**
