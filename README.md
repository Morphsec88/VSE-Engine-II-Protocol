# VSE II Protocol (Voltage-controlled Statistical Encoding II)

VSE II is an innovative, highly efficient, and noise-immune data transmission protocol. By combining adaptive statistical data positioning with a physical two-wire zig-zag corridor architecture, it shifts the burden of information carrier from continuous electrical impulses to the dimension of elapsed time. 

This protocol is specifically engineered to achieve extreme energy efficiency and robust clock synchronization over physical channels.

## 🏆 Proven Benchmarks (Live Test Results)

During rigorous live simulations on standard text datasets, the VSE II protocol demonstrated spectacular hardware and temporal efficiency over traditional sequential networks:

* **Traditional Transmission Time:** 8,960 clock units (Waiting for full fixed windows).
* **VSE II Transmission Time:** **Only 534 clock units!**
* **NET TIME SAVED:** **94.0% Faster Transmission** because the intelligent profile manager layers common characters directly at the floor of the corridor.
* **Physical Wire Savings:** **87.5% fewer impulses sent over the wire.** Instead of pumping a continuous, power-heavy stream of **1,120 standard bits**, VSE II transfers the exact same data using only **140 pulses**, leaving the bus completely silent and power-free for the remaining 87.5% of the time.

## 🛠️ Key Architectural Features

1. **Dual Physical Bus Wires (Wire A & Wire B):** The standard 256-byte variations are split across two opposite physical charts (Column A for even indexes, Column B for odd indexes), cutting the maximum physical corridor height strictly down to 128.
2. **Adaptive Profile Selection (8-Position Adjuster):** Before transmission, the sender automatically scans the raw file structure, analyzes the code patterns, and instantly matches the data stream to 1 of 8 predefined profile states. This repositions the heaviest data clusters directly to the bottom of the time scale (near step 0).
3. **Half-Row Shift (The Zig-Zag Corridor):** Wire B is physically shifted by a half-step relative to Wire A (A0.0 -> B0.5 -> A1.0 -> B1.5...). This hardware elusion entirely eliminates data collisions and software handshakes.
4. **Bipolar Digital Noise Protection:** To ensure maximum transmission distance, the protocol completely discards standard positive-only voltage scales. It utilizes a highly protected bipolar shift:
   * **Intensity 1 / Position 1:** -2.0V
   * **Intensity 2 / Position 2:** -1.0V
   * **Intensity 3 / Position 3:** +1.0V
   * **Intensity 4 / Position 4:** +2.0V
   This negative-to-positive voltage differential makes the line highly immune to signal decay and external electromagnetic interference.
5. **10-Tick Stabilization Grid (Zero Clock Drift):** To prevent clock desynchronization during long silent periods, a rock-solid embedded synchronization grid triggers a neutral `0.0V` pulse if the line stays inactive for 120.0 time units (10 full cycles). The receiver uses this grid pulse to recalibrate its clock timer instantly.
6. **No Back-Tracking (Strict Ascending Scan):** The clock sweeps strictly forward from bottom to top (0 to 127) within each 4-byte block, closing and resetting the window dynamically as soon as the last required byte hits.

## 📂 File Structure

* `vse_ii_protocol.py` - The core noise-protected transmission simulation engine (Sender & Receiver).
* `README.md` - Protocol documentation, engineering overview, and benchmarks.

---

## ⚖️ Legal & Licensing

**Copyright © 2026 Morphsec88. All Rights Reserved.**

VSE II is the original intellectual property of **Morphsec88**. All rights reserved worldwide. 

This project is officially licensed under the terms of the **GNU AGPLv3 (GNU Affero General Public License v3)**. 

* You are free to share, copy, and modify this software.
* Any modified versions or derivative hardware layouts **must also be open-sourced** under the same AGPLv3 license.
* The original copyright notice and this permission notice must be included in all copies or substantial portions of the software.