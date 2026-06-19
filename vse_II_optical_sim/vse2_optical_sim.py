# ==============================================================================
# VSE II Protocol - Optical Photon Variant (Light-Controlled Statistical Encoding)
# Core Simulation Engine - Production Hardware-Testable & ARQ Error-Corrected
# Version: 5.3 - Infinite Loop Patch
#
# Copyright (C) 2026 Morphsec88. All Rights Reserved.
# ==============================================================================

import random
from collections import Counter

def hardware_output_trigger(color, voltage, wire):
    """ Interface for physical testing (FPGA, LabVIEW, GPIO outputs) """
    pass  

# 1. RAW DATA AND SAMPLE ANALYSIS
poem_data = """Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever come back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference."""

raw_data = poem_data.encode('utf-8')

frequency = Counter(raw_data)
for i in range(256):
    if i not in frequency: frequency[i] = 0

optimal_order = [byte for byte, _ in frequency.most_common()]
column_A = [optimal_order[x] for x in range(0, 256, 2)]  
column_B = [optimal_order[x] for x in range(1, 256, 2)]  

# ELEVATED INDUSTRIAL SIGNAL LEVELS (High SNR against noise)
AMPLITUDES = {0: 0.5, 1: 1.0, 2: 1.5, 3: 2.0}
PARITY_VOLTAGE = 2.5

retransmit_count = 0
watchdog_trips = 0
total_blocks_sent = 0

# 2. SENDER SIDE
def optical_vse_ii_sender_block(block_bytes):
    photon_stream = []
    block_signals = []
    
    # Checksum calculation Modulo 256
    checksum_byte = sum(block_bytes) % 256
        
    for pos, byte in enumerate(block_bytes):
        wire = "A" if byte in column_A else "B"
        idx = column_A.index(byte) if wire == "A" else column_B.index(byte)
        block_signals.append({"idx": idx, "wire": wire, "pos": pos})
        
    block_signals.sort(key=lambda x: x["idx"])
    
    last_index = -1
    current_color = "x" 
    emitted_in_block = 0
    
    i = 0
    while i < len(block_signals):
        if i + 1 < len(block_signals) and block_signals[i]["idx"] == block_signals[i+1]["idx"]:
            sig1, sig2 = block_signals[i], block_signals[i+1]
            first, second = (sig1, sig2) if sig1["pos"] <= sig2["pos"] else (sig2, sig1)
            
            photon_stream.append({
                "idx": first["idx"], "color": "z", "voltage": AMPLITUDES[first["pos"]], "wire": first["wire"], "counts": True
            })
            photon_stream.append({
                "idx": second["idx"], "color": "y-z", "voltage": AMPLITUDES[second["pos"]], "wire": second["wire"], "counts": True
            })
            emitted_in_block += 2
            last_index = first["idx"]
            i += 2
            continue
        
        sig = block_signals[i]
        if sig["idx"] <= last_index:
            current_color = "y" if current_color == "x" else "x"
        else:
            current_color = "x"
            
            if current_color == "y":
                photon_stream.append({
                    "idx": sig["idx"], "color": "y", "voltage": AMPLITUDES[sig["pos"]], "wire": sig["wire"], "counts": False
                })
                photon_stream.append({
                    "idx": sig["idx"], "color": "x", "voltage": AMPLITUDES[sig["pos"]], "wire": sig["wire"], "counts": True
                })
                emitted_in_block += 1
                last_index = sig["idx"]
                i += 1
                continue
            
        photon_stream.append({
            "idx": sig["idx"], "color": current_color, "voltage": AMPLITUDES[sig["pos"]], "wire": sig["wire"], "counts": True
        })
        emitted_in_block += 1
        last_index = sig["idx"]
        i += 1
        
    while emitted_in_block < 5:
        photon_stream.append({
            "idx": 0, "color": "x", "voltage": 0.0, "wire": "A", "counts": True, "is_dummy": True
        })
        emitted_in_block += 1
        
    parity_wire = "A" if checksum_byte in column_A else "B"
    parity_idx = column_A.index(checksum_byte) if parity_wire == "A" else column_B.index(checksum_byte)
    photon_stream.append({
        "idx": parity_idx, "color": "x", "voltage": PARITY_VOLTAGE, "wire": parity_wire, "counts": False, "is_parity": True
    })
    
    return photon_stream

# 3. PHYSICAL CHANNEL NOISE AND SIGNAL DROP GENERATOR
def inject_channel_faults(photon_stream, force_drop):
    faulty_stream = []
    
    # Select an active data signal to drop if force drop is active
    drop_index = random.randint(0, 2) if force_drop else -1
    active_counter = 0
    
    for signal in photon_stream:
        noisy_signal = signal.copy()
        
        if signal["voltage"] > 0.0 and not signal.get("is_parity", False) and not signal.get("is_dummy", False):
            if active_counter == drop_index:
                noisy_signal["voltage"] = 0.0  # Total drop
            else:
                # Background noise
                noise = random.uniform(-0.16, 0.16)
                noisy_signal["voltage"] = round(signal["voltage"] + noise, 4)
            active_counter += 1
        elif signal.get("is_parity", False):
            # The parity signal also gets noise, but does not drop completely
            noise = random.uniform(-0.16, 0.16)
            noisy_signal["voltage"] = round(signal["voltage"] + noise, 4)
            
        faulty_stream.append(noisy_signal)
    return faulty_stream

# 4. RECEIVER SIDE + INDUSTRIAL SCHMITT-TRIGGER
def schmitt_trigger_filter(voltage):
    if voltage < 0.15: return -1 # Watchdog threshold (near 0V state)
    if 0.25 <= voltage < 0.75: return 0  
    if 0.75 <= voltage < 1.25: return 1  
    if 1.25 <= voltage < 1.75: return 2  
    if 1.75 <= voltage < 2.25: return 3  
    if 2.25 <= voltage <= 2.85: return 4 
    return -1

def optical_vse_ii_receiver_block(photon_stream):
    reconstructed_block = [0] * 4
    anomaly_buffer = []
    hardware_counter = 0
    
    for signal in photon_stream:
        hardware_output_trigger(signal["color"], signal["voltage"], signal["wire"])
        
        # --- WATCHDOG TIMER INTERRUPT ---
        if signal["voltage"] < 0.15 and not signal.get("is_dummy", False) and signal["counts"]:
            return None, True, True  
            
        if signal.get("is_parity", False):
            if hardware_counter != 5:
                return None, True, False  
                
            pos = schmitt_trigger_filter(signal["voltage"])
            if pos != 4: # If parity voltage is distorted by noise
                return None, True, False
                
            p_idx = signal["idx"]
            p_wire = signal["wire"]
            actual_parity_byte = column_A[p_idx] if p_wire == "A" else column_B[p_idx]
            
            calculated_parity = sum(reconstructed_block) % 256
            if calculated_parity == actual_parity_byte:
                return reconstructed_block, False, False 
            else:
                return None, True, False 
                
        if not signal["counts"]: continue
        hardware_counter += 1
        
        if signal.get("is_dummy", False):
            continue
            
        idx = signal["idx"]
        color = signal["color"]
        wire = signal["wire"]
        
        pos = schmitt_trigger_filter(signal["voltage"])
        if pos == -1 or pos == 4: 
            return None, True, False 
            
        if color in ["z", "y-z"]:
            anomaly_buffer.append({"idx": idx, "wire": wire, "pos": pos})
            if len(anomaly_buffer) == 2:
                for s in anomaly_buffer:
                    s_byte = column_A[s["idx"]] if s["wire"] == "A" else column_B[s["idx"]]
                    reconstructed_block[s["pos"]] = s_byte
                anomaly_buffer = []
        else:
            actual_byte = column_A[idx] if wire == "A" else column_B[idx]
            reconstructed_block[pos] = actual_byte
            
    return None, True, False

# 5. AUTOMATIC REPEAT REQUEST LOOP (ARQ)
decoded_bytes = bytearray()
padding_len = (4 - (len(raw_data) % 4)) % 4
padded_data = raw_data + b'\x00' * padding_len

for block_idx in range(0, len(padded_data), 4):
    target_block = padded_data[block_idx:block_idx+4]
    total_blocks_sent += 1
    
    # Forced physical signal drop (0V) on the first attempt every 3 blocks
    force_hardware_drop = (total_blocks_sent % 3 == 0)
    
    while True:
        pure_packet = optical_vse_ii_sender_block(target_block)
        noisy_packet = inject_channel_faults(pure_packet, force_hardware_drop)
        
        result_block, error_detected, watchdog_triggered = optical_vse_ii_receiver_block(noisy_packet)
        
        if watchdog_triggered:
            watchdog_trips += 1
            
        if not error_detected and result_block is not None:
            decoded_bytes.extend(result_block)
            break
        else:
            retransmit_count += 1
            force_hardware_drop = False # DISABLE FOR RETRANSMISSION (Break the loop)

if padding_len > 0:
    decoded_bytes = decoded_bytes[:-padding_len]
final_data = bytes(decoded_bytes)

# 6. STATISTICS
standard_pulses = len(raw_data) * 10
vse_counted_pulses = total_blocks_sent * 5 

saving_percentage = (1 - (vse_counted_pulses / standard_pulses)) * 100
has_error = raw_data != final_data

print(f"Savings: {saving_percentage:.2f}%")
print(f"System Error: {has_error}")
print(f"Retransmissions due to noise: {retransmit_count}")
