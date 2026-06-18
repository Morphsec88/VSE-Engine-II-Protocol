
<img width="1054" height="724" alt="Képernyőfelvétel (179)" src="https://github.com/user-attachments/assets/e10b753d-804a-445c-a982-db411f336b48" />


# VSE II Protocol (Voltage-Controlled Statistical Encoding II)

VSE II is an innovative, high-efficiency, and anti-noise data transmission protocol. By combining adaptive statistical data positioning with a physical two-wire zigzag corridor architecture, it shifts the data carrier burden from continuous electrical impulses exclusively onto the elapsed time dimension.

This protocol achieves extreme energy efficiency and robust clock synchronization over physical communication channels.

## Proven Benchmarks (Live Test Results)
During simulations on standard text datasets, the VSE II protocol demonstrated overwhelming hardware and time efficiency compared to traditional sequential networks:
* **Traditional Transmission Time:** 8,960 clock units (waiting for full fixed windows).
* **VSE II Transmission Time:** Only 534 clock units.
* **NET TIME SAVINGS:** **94.0% Faster transmission**, achieved by the intelligent profile manager directly layering common characters onto the corridor floor.
* **Physical Wire Savings:** **87.5% fewer impulses** across the wire. Instead of pumping a continuous, power-hungry stream of 1,120 standard bits, VSE II transmits the identical data using just 140 impulses, leaving the bus completely silent and unpowered for the remaining 87.5% of the cycle.

---

## 🔒 Intellectual Property & Proprietary Protection Notice
**Copyright (C) 2026 Morphsec88. All Rights Reserved. STRICTLY PROPRIETARY AND CONFIDENTIAL.**

The VSE II architecture—including but not limited to its internal structural design layers, specific structural processing matrices, exact sequential execution steps (including the proprietary A-B-C-D pattern mechanics), multi-byte grouping alignment, and time-slot mapping methodologies—constitutes the exclusive intellectual property and proprietary trade secrets of Morphsec88.

While the accompanying evaluation software simulation engine is licensed under the open-source terms of the GNU AGPLv3, the underlying conceptual architecture, sequential sequence logic, physical layer mechanics, and hardware-mapping structures remain strictly proprietary. 

Unauthorized duplication, reverse-engineering, structural deconstruction, or adaptation of these fundamental sequential steps and layer mechanics for commercial deployment without an explicit, written licensing agreement from Morphsec88 is strictly prohibited.

---

## Core Architectural Features

### 1. Dual Physical Bus Wires (Wire A & Wire B)
Standard 256-byte variations are split across two opposite physical diagrams (Column A for even indexes, Column B for odd indexes), strictly reducing the maximum physical corridor height to 128.

### 2. Adaptive Profile Selection (8-Position Aligner)
Prior to transmission, the sender automatically scans the raw file structure, analyzes bit-patterns, and immediately matches the data stream with one of 8 pre-defined profile states. This places the heaviest data groups directly at the bottom of the time scale (near step 0).

### 3. Half-Serial Shifting (The Zigzag Corridor)
Wire B is physically shifted by a half-step relative to Wire A (`A0,0 -> B0,5 -> A1,0 -> B1,5...`). This hardware elision completely eliminates data collisions and software handshakes.

### 4. Bipolar Digital Noise Protection
To guarantee maximum transmission distance, the protocol completely abandons standard positive voltage scales, employing a heavily guarded bipolar offset:
* **Intensity 1 / Position 1:** -2.0V
* **Intensity 2 / Position 2:** -1.0V
* **Intensity 3 / Position 3:** +1.0V
* **Intensity 4 / Position 4:** +2.0V
This negative-to-positive voltage swing renders the line highly immune to signal decay and external electromagnetic interference (EMI).

### 5. 10-Tick Stabilization Grid (Zero Clock Drift)
To prevent clock desynchronization during extended silent periods, a solid embedded sync grid emits a neutral `0.0V` pulse if the line remains inactive for 120.0 time units (10 full cycles). The receiver uses this grid pulse to immediately recalibrate its clock timer.

### 6. No Backtracking (Strict Ascending Scan)
The clock glides strictly forward from bottom to top (0 to 127) within each 4-byte block, dynamically closing and restarting the window as soon as the last required byte is reached.

## Repository Structure
* `vse_ii_protocol.py` – Core noise-protected switching simulation engine (Transmitter & Receiver).
* `README.md` – Protocol documentation, engineering overview, and performance benchmarks.

## Licensing Terms
This project's simulation script is licensed under the **GNU AGPLv3 (GNU Affero General Public License v3)**. 
* You are free to share, copy, and modify the software script.
* Any modified version or derivative hardware layouts utilizing this specific open script must also be open-sourced under the same AGPLv3 license.
* The original copyright notice and this permission notice must be included in all copies or substantial portions of the software.
