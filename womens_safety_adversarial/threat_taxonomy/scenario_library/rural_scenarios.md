# Rural Scenario Library

## Scenario Format
Each scenario covers: Setting · Adversary subtype · Attack method · Access level · Evasion mechanism · AI subsystem targeted · Governance gap flagged

---

## R-01 — Agricultural Field, Isolated Worker
**Context:** R2 (rural isolated)  
**Setting:** Field or plantation; victim working alone or with small group; no bystanders; weak or no network  
**Adversary:** Opportunistic to Adaptive (L0–L3)  
**Attack method:** Intercept (network dead zone) + Suppress  
**Evasion:** No cellular signal — alert cannot transmit even if triggered; isolation removes bystander deterrence  
**Subsystems targeted:** Communication layer (L3)  
**Governance gap:** No framework requires offline fallback capability; rural deployment not addressed in EU AI Act or NIST AI RMF; India DPDP Act covers data, not connectivity failure  
**[CITATION NEEDED: NCRB — assault in agricultural/rural workplace settings]**

---

## R-02 — Village Pathway, Dusk
**Context:** R1 (rural public)  
**Setting:** Pathway between village and fields; poor lighting; adversary familiar with route timing  
**Adversary:** Adaptive (L0–L3 environmental)  
**Attack method:** Suppress (Vision — lighting)  
**Evasion:** Darkness defeats CV; adversary knows victim's route and timing (environmental familiarity); audio baseline is low but so is bystander likelihood  
**Subsystems targeted:** Vision, Response  
**Governance gap:** No standard certifies CV performance under low-light rural conditions; Safetipin data shows lighting as primary safety gap in rural pathways  
**[CITATION NEEDED: Safetipin rural lighting audit data]**

---

## R-03 — Isolated Road Between Villages, Moving Vehicle
**Context:** R2 + T1 (rural isolated transit)  
**Setting:** Auto-rickshaw or shared vehicle on road with no network coverage; victim is sole passenger or small group  
**Adversary:** Opportunistic to Informed (L0–L2)  
**Attack method:** Intercept (network) + Corrupt (GPS)  
**Evasion:** Route passes through signal dead zone — adversary with local knowledge times action to this window; GPS fix lost; no alert can transmit  
**Subsystems targeted:** Sensor Fusion (GPS), Communication (L3)  
**Governance gap:** Cross-jurisdictional gap — no state-level framework coordinates rural connectivity requirements with safety app certification  
**[CITATION NEEDED: NCRB — transit harassment, rural state data]**

---

## R-04 — Village Common / Weekly Market, Community Authority
**Context:** R1 (rural public)  
**Setting:** Village common or market; adversary is senior community figure (panchayat member, elder, employer)  
**Adversary:** Informed + Environmental Controller (L4–L5)  
**Attack method:** Suppress via social leverage — no technical attack  
**Evasion:** Victim does not trigger alert because adversary holds community authority; bystanders are socially conditioned not to intervene; triggering a public alert against a community authority figure carries reputational cost that exceeds perceived protection benefit  
**Subsystems targeted:** None — alert never initiated  
**Governance gap:** Sociotechnical suppression absent from all frameworks; India IT Act addresses digital harm, not social suppression of safety systems  
**[CITATION NEEDED: iCall/iHuman — rural authority figure case patterns]**

---

## R-05 — Agricultural Employer Context, Seasonal Labour
**Context:** R1–R2  
**Setting:** Seasonal agricultural labour; victim is migrant or dependent worker; adversary is employer or supervisor  
**Adversary:** Informed (L4–L5)  
**Attack method:** Suppress (social leverage) + Corrupt (device access)  
**Evasion:** Employer has authority over victim's livelihood and housing; victim's economic dependency raises threshold for triggering alert; employer may have incidental access to device (charging, storage)  
**Subsystems targeted:** Response (social), Vision/Audio (device access)  
**Governance gap:** Economic coercion as suppression vector not addressed by any framework; labour law and safety app certification exist in completely separate regulatory silos  
**[CITATION NEEDED: no direct citation — flag as novel sociotechnical vector]**
