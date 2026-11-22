# Compact ODMR Setup: NV Centers in Diamond with a CMOS Camera at Room Temperature

> ⚠️ **Project Status: Work in Progress (WIP)**  
> This repository is actively being updated. Hardware and basic structures are documented, while detailed software scripts and final measurement plots are being added progressively. Feel free to watch the repository for updates!

An independent, open-source physics setup inspired by the paper *"Modular low-cost 3D printed setup for experiments with NV centers in diamond"* (FH Münster). 

This project implements Optically Detected Magnetic Resonance (ODMR) to observe and manipulate quantum spin states at room temperature, utilizing a **ZWO ASI 585MC CMOS camera** for advanced imaging and flexible Region-of-Interest (ROI) data acquisition.

## Key Takeaways

* **Dichroic Mirror Limitation (~0.2% Contrast):** Initial measurements only reached a maximum ODMR contrast of ~0.2% because the dichroic mirror used transmitted 532 nm green light and reflected red fluorescence, delivering insufficient green excitation power to the NV diamond.
* **50:50 Beam Splitter & Differential Masking (~1.0–1.55% Contrast):** Replacing the dichroic mirror with a 50:50 beam splitter significantly increased the green excitation intensity on the diamond, boosting the ODMR contrast above 1% (up to ~1.55% when combined with the CPWG micro-loop, HMC284 differential switching, and a >90% ROI pixel mask).
* **RF Amplifier Input Protection:** Always place a sufficiently large attenuator (e.g., 3 dB) in front of the RF power amplifier to prevent permanent damage, as this broadband amplifier module is rated for a maximum input power of **+2 dBm**.


## Optical Path & Table Setup

The optical setup is designed to efficiently couple the excitation light into the diamond and capture the resulting spin-dependent fluorescence:

*   **Excitation Source:** A 532 nm green laser module (1 mW output power, driven at 3 V) is coupled into the optical path via a 45-degree dichroic mirror, which reflects the green excitation light at a right angle (90 degrees).
*   **Focusing & Sample Interaction:** The reflected laser light is channeled through a 4x microscope objective, focusing it directly onto the NV ensemble. The diamond is mounted on the custom stripline PCB at the focal point.
*   **Fluorescence Collection:** The red fluorescence emitted by the NV centers is collected by the same 4x microscope objective (confocal configuration) and sent back through the objective alongside the reflected green excitation light.
*   **Optical Filtering:** Upon reaching the 45-degree dichroic mirror from the reverse direction, most of the reflected green laser light passes back toward the laser source. Any remaining green background noise is effectively blocked by an additional red longpass filter.
*   **Detection:** The purified red NV fluorescence passes through the red filter and hits the **ZWO ASI 585MC CMOS camera**. The camera is securely mounted on a kinematic mount for precise alignment, using a custom tube assembly fixed to the objective nosepiece.

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="images/20260909_072345.jpg" width="300"><br>
      <em>Full ODMR setup overview.</em>
    </td>
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="images/20261011_163507.jpg" width="400"><br>
      <em>Close-up of the ZWO ASI 585.</em>
    </td>
  </tr>
</table>

### Ensemble NV Diamond 100

The Ensemble diamond was supplied by Neocrystech (Shanghai, China). It is a Ensemble NV diamond (ENV-20) with a high density of NV centers (7ppm) and size of 0.5x0.5x0.3mm.

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20260904_225643.jpg" width="200"><br>
      <em>NV in box green laser light</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20260904_225633.jpg" width="200"><br>
      <em>NV in box green laser light red filter</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20260906_200406.jpg" width="300"><br>
      <em>NV under 4x microscope objective no filter</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20260906_200445.jpg" width="300"><br>
      <em>NV under 4x microscope objective red filter</em>
    </td>
  </tr>
</table>

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="images/nv1.png" width="600"><br>
      <em>NV ensemble different exposure time</em>
    </td>
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="images/nv2.png" width="600"><br>
      <em>NV ensemble different exposure time</em>
    </td>
  </tr>
</table>

## Custom PCB Design

This setup utilizes custom-made stripline designs fabricated on a 0.8 mm FR4, designed using **KiCAD 10.0**. Two distinct layouts were evaluated to optimize microwave delivery to the NV centers:

*   **Design 1: "Micro Stripline"** – The trace width was calculated to achieve a 50-Ohm characteristic impedance, tapering down to a width of c 0.55 mm at the sample area. To protect the traces and prevent unwanted reflections, the entire stripline is covered with a green solder mask, excluding a small exposed window around the 0.55 mm section.
*   **Design 2: "Stripline with Loop"** – This alternative design tapers down into a micro-loop with a trace width of 0.2 mm, featuring an integrated via fence for improved RF shielding. Similar to the first design, a selective solder mask window leaves only the placement area for the NV diamond exposed.

For the final experiment presented in this project, the **Micro Stripline** layout was selected. The corresponding Gerber files are available for download in this repository.


<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20260923_223229.jpg" width="300"><br>
      <em>Front</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20260922_232023.jpg" width="300"><br>
      <em>Front zoom stripline design</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20260922_232012.jpg" width="300"><br>
      <em>Front zoom loop design</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20260923_223239.jpg" width="300"><br>
      <em>Back</em>
    </td>
  </tr>
</table>

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20261008_163400.jpg" width="200"><br>
      <em>Front</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20261008_163408.jpg" width="200"><br>
      <em>Back</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/Capture_00001.png" width="300"><br>
      <em>Stripline under 4x microscope objective</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/Capture_00005.png" width="300"><br>
      <em>Loop under 4x microscope objective</em>
    </td>
  </tr>
</table>

## NV Diamond Assembly on PCB Stripline

To ensure efficient microwave coupling, the NV diamond ensemble must be precisely positioned and secured directly onto the PCB stripline. 

### Mounting Process & Lessons Learned
During development, different fixation methods were evaluated, yielding important practical insights:

*   **Nail Polish Method (Capillary Action):** Initially, the diamond was secured using standard nail polish. The key lesson learned is that the diamond should be placed onto the stripline while the surface is completely dry. Then, using a fine needle, a tiny drop of nail polish can be applied adjacent to the crystal. **Capillary forces** will automatically draw the liquid underneath the diamond without the need to touch or disturb it. However, a remaining difficulty is that the fluid motion can still cause the diamond to shift slightly out of alignment.
*   **Alternative Methods:** Using **Kapton tape** alone was considered as an alternative dry-fixation method to prevent any sample movement.

### Final Configuration
For the final setup presented in this project, a hybrid approach was chosen to ensure maximum security: the diamond was carefully glued with a minimal amount of nail polish, covered with a standard **microscope coverslip** for protection, and finally secured to the PCB using **Kapton tape** to eliminate any risk of losing the diamond during optical alignment. Note that while Kapton tape is famous for its high-temperature resistance, this property is not strictly required here; the 1 mW laser power does not generate significant heat, meaning standard clear tape could theoretically suffice, though Kapton remains ideal for its stability and residue-free application.

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20261011_120717.jpg" width="300"><br>
      <em>NV on PCB</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20261010_225847.jpg" width="300"><br>
      <em>NV on PCB</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/20261011_120720.jpg" width="300"><br>
      <em>Zoom</em>
    </td>
    <td style="width:25.0%; text-align:center; border: none;">
      <img src="images/Capture_00002.png" width="300"><br>
      <em>NV on PCB under 4x microscope objective</em>
    </td>
  </tr>
</table>

## Hardware

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="images/20261011_163457.jpg" width="400"><br>
      <em>Raspberry Pi 3 and ADF4351 frequency synthesizer</em>
    </td>
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="images/20261011_163445.jpg" width="400"><br>
      <em>RF Amplifier with 15V voltage supply</em>
    </td>
  </tr>
</table>

## Experimental Results & Data Acquisition Modes

The spin-dependent fluorescence of the NV ensemble was succesfully mapped using the **ZWO ASI 585MC** camera. To balance acquisition speed and signal-to-noise ratio (SNR), two distinct measurement configurations were established in the Python data acquisition loop:

### Mode 1: Fast Sweep / Coarse Scan
Optimized for rapid resonance localization and initial alignment checking.
*   **Region of Interest (ROI):** 320 × 240 pixels
*   **Exposure Time:** 60 ms
*   **Sensor Gain:** 252
*   **Frame Averaging:** 8 frames per frequency step
*   **ADF4351 Lock Time:** 10 ms delay after frequency switch
*   **Frequency Step Width:** 10 MHz

### Mode 2: High-Resolution Sweep / Precision Scan
Optimized for high-fidelity ODMR curve fitting, hyperfine structure evaluation, and noise reduction.
*   **Region of Interest (ROI):** 320 × 240 pixels
*   **Exposure Time:** 60 ms
*   **Sensor Gain:** 252
*   **Frame Averaging:** 30 frames per frequency step (enhanced SNR)
*   **ADF4351 Lock Time:** 15 ms delay after frequency switch (ensuring synthesizer stabilization)
*   **Frequency Step Width:** 1 MHz

*The resulting Matplotlib plots generated from these data points clearly illustrate the characteristic ODMR dip at the NV resonance frequencies.*

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="results/Figure_1 (10Mhz).png" width="500"><br>
      <em>First succesfull sweep with 5MHz step width</em>
    </td>
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="results/ODMR 1MHz sweep.png" width="500"><br>
      <em>Sweep with 1MHz step width</em>
    </td>
  </tr>
</table>

### Mode 3: High-Resolution Precision Sweep (Python-Controlled)
While the automated frequency sweep and data logging are executed entirely via the custom Python automation script, the camera's field of view and Region of Interest (ROI) were initially verified using SharpCap. 

The configuration parameters for this sweep mode are:
*   **Region of Interest (ROI):** 320 × 240 pixels
*   **Exposure Time:** 60 ms
*   **Sensor Gain:** 252
*   **Frame Averaging:** 30 frames per frequency step (Python loop)
*   **ADF4351 Lock Time:** 15 ms delay after frequency switch
*   **Frequency Step Width:** 1 MHz

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="results/shrapcap 2.png" width="600"><br>
      <em>ROI visualization in SharpCap. The diamond is slightly out of focus as the optical plane is intentionally set near the PCB stripline surface where the microwave magnetic field is strongest.</em>
    </td>
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="results/shrapcap 3.png" width="600"><br>
      <em>Structural alignment view in SharpCap. Increased exposure time is used here purely for visualization to resolve the underlying copper stripline beneath the diamond crystal.</em>
    </td>
  </tr>
</table>


### ODMR Resonance Contrast & ROI Mapping

The correlation between the selected camera pixel area and the measured quantum spin resonance is detailed below. The automatic Python routine sweeps the microwave frequency while recording the intensity within the highlighted Region of Interest:

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="results/shrapcap 1.png" width="600"><br>
      <em>320×240 pixel Region of Interest (ROI) visualization in SharpCap, centering the brightest fluorescence area of the NV ensemble.</em>
    </td>
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="results/Figure_1.png" width="500"><br>
      <em>Python-generated Matplotlib plot showing the continuous frequency sweep. The characteristic ODMR dip is clearly resolved with a contrast depth of approximately 0.2%.</em>
    </td>
  </tr>
</table>

## Enhanced setup using a 50:50 Beam Splitter and 642-842nm bandpass filter

The enhanced setup uses a 50:50 beam splitter to let more light through to the NV and a 642-842nm bandpass filter to block the green light from entering the ZWO ASI camera and only letting the relevant fluorescence of the NV diamond through.

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="images/20261122_173402.jpg" width="300"><br>
      <em>Optical bench without magnet</em>
    </td>
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="images/20261122_173343.jpg" width="400"><br>
      <em>Optical bench with magnet for Zeeman splitting</em>
    </td>
  </tr>
</table>

## Grounded Coplanar Waveguide (CPWG) Loop with NV ensemble (100)

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:33.3%; text-align:center; border: none;">
      <img src="images/20260922_232012.jpg" width="300"><br>
      <em>Loop design with taper and 0.2 mm trace width</em>
    </td>
    <td style="width:33.3%; text-align:center; border: none;">
      <img src="images/Capture_00005.png" width="300"><br>
      <em>Zoom of the CPWG loop using a 4x objective</em>
    </td>
    <td style="width:33.3%; text-align:center; border: none;">
      <img src="images/Capture_00006.png" width="300"><br>
      <em>Loop design with 0.5 × 0.5 × 0.3 mm NV diamond</em>
    </td>
  </tr>
</table>

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:35.0%; text-align:center; vertical-align:middle; border: none;">
      <img src="images/20261115_171859.jpg" width="250"><br>
      <em>CPWG loop prior to diamond positioning</em>
    </td>
    <td style="width:65.0%; text-align:center; vertical-align:middle; border: none;">
      <img src="images/20261115_172347.jpg" width="650"><br>
      <em>CPWG loop with the NV diamond positioned in place—secured without glue using four layers of Kapton tape as spacers beneath a microscope coverslip.</em>
    </td>
  </tr>
</table>

### RF Power Verification via Thermal Imaging

To reliably verify that the amplified microwave signal passes through the CPWG micro-loop and reaches the 50 Ω dummy load terminator, a thermal camera was used to monitor the resistor's temperature rise under RF load:

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:50.0%; text-align:center; vertical-align:middle; border: none;">
      <img src="images/P1_261112_213500_151.jpg" width="400"><br>
      <em>Thermal camera image of the 50 Ω dummy load at the end of the CPWG loop reading <strong>20.2 °C</strong> with the microwave switched <strong>OFF</strong>.</em>
    </td>
    <td style="width:50.0%; text-align:center; vertical-align:middle; border: none;">
      <img src="images/P1_261112_213433_466.jpg" width="400"><br>
      <em>Thermal camera image of the 50 Ω dummy load at the end of the CPWG loop warming up to <strong>21.9 °C</strong> with the microwave switched <strong>ON</strong>.</em>
    </td>
  </tr>
</table>

## Electronics

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:45%; text-align:center; vertical-align:middle; border: none;">
      <img src="images/20261122_173505.jpg" width="350"><br>
      <em>ADF4351 Frequency Synthesizer</em>
    </td>
    <td style="width:55%; text-align:left; vertical-align:middle; border: none;">
      <ul>
        <li><strong>Frequency Synthesizer:</strong> ADF4351 PLL board (35 MHz – 4.4 GHz) generating the microwave excitation signal around 2.87 GHz.</li>
        <li><strong>RF Output Configuration:</strong> 50 Ω terminator on the <code>OUT-</code> port, while <code>OUT+</code> is routed via an SMA cable to the HMC284 RF switch.</li>
        <li><strong>Power Supply:</strong> Powered externally via a dedicated 5 V cable.</li>
      </ul>
    </td>
  </tr>
</table>

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:45%; text-align:center; vertical-align:middle; border: none;">
      <img src="images/20261122_173417.jpg" width="100"><br>
      <em>HMC284 RF Switch</em>
    </td>
    <td style="width:55%; text-align:left; vertical-align:middle; border: none;">
      <ul>
        <li><strong>HMC284 RF Switch:</strong> Used for fast microwave modulation (switching the RF signal on and off).</li>
        <li><strong>RF Port Configuration:</strong> 50 Ω terminator on the <code>OUT1</code> port, while <code>OUT2</code> is routed via an SMA cable to the RF amplifier.</li>
        <li><strong>Input Protection:</strong> A 3 dB attenuator is placed inline between the HMC284 switch and the RF amplifier to protect the amplifier's input stage (rated for a maximum input power of +2 dBm).</li>
        <li><strong>Control & Level Shifting:</strong> The <code>GND</code>, <code>A</code>, and <code>B</code> control pins on the left are driven by a Raspberry Pi Pico via an <strong>SN74AHCT125</strong> buffer gate to step up the 3.3 V logic signals to ~4–5 V.</li>
      </ul>
    </td>
  </tr>
</table>


<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:45%; text-align:center; vertical-align:middle; border: none;">
      <img src="images/20261011_163445.jpg" width="400"><br>
      <em>RF Power Amplifier</em>
    </td>
    <td style="width:55%; text-align:left; vertical-align:middle; border: none;">
      <ul>
        <li><strong>RF Power Amplifier:</strong> 36 dB, 1 W broadband driver (SBB5089 + SZA3044, 1.5–3.9 GHz).</li>
        <li><strong>RF Port Configuration:</strong> Input receives the attenuated signal from the HMC284 RF switch, while the amplified output is routed via an SMA cable directly to the CPWG micro-loop PCB, which is terminated with a 50 Ω dummy load after the loop.</li>
        <li><strong>Power Supply:</strong> Powered by an external 15 V DC voltage supply.</li>
      </ul>
    </td>
  </tr>
</table>


<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:45%; text-align:center; vertical-align:middle; border: none;">
      <img src="images/20261122_173520.jpg" width="400"><br>
      <em>Raspberry Pi Pico connected via <strong>SN74AHCT125</strong></em>
    </td>
    <td style="width:55%; text-align:left; vertical-align:middle; border: none;">
      <ul>
        <li><strong>Raspberry Pi Pico:</strong> Receives trigger commands from the host Raspberry Pi to toggle the <code>A</code> and <code>B</code> control lines, switching the HMC284 RF gate on and off.</li>
        <li><strong>Control & Level Shifting:</strong> The <code>GND</code>, <code>A</code>, and <code>B</code> control pins are routed through an <strong>SN74AHCT125</strong> buffer gate to step up the Pico's 3.3 V logic signals to ~4–5 V for reliable RF switching.</li>
      </ul>
    </td>
  </tr>
</table>


## Automated ODMR Acquisition Pipeline (`scripts/sweep_v2`)

The following three scripts located in `scripts/sweep_v2` orchestrate the synchronized frequency sweep, fast microwave modulation, and CMOS image acquisition used to generate the experimental results:

* **`sweep_desktop.py` (Host PC Controller & Data Analysis):**
  * Controls the **ZWO ASI 585MC** camera (`RAW16` mode, `64 × 64` ROI, 3 ms exposure, Gain 252) and applies a static **90th-percentile pixel mask** with dark-frame offset subtraction (`741 ADU`) to isolate the brightest NV fluorescence region.
  * Communicates with the Raspberry Pi via TCP/IP sockets (`port 5005`) to step through frequencies (`2.765–2.960 GHz` in `5 MHz` steps) after a 3-second thermal pre-heating phase at `2.750 GHz`.
  * Performs **pairwise differential normalization** ($I_{\text{ON}} / I_{\text{OFF}}$) across 15 averages per frequency step to suppress laser and thermal drift, exports the raw data to CSV, and fits a **double Lorentzian model** to extract the zero-field splitting ($D$), strain/Zeeman splitting ($E$), contrast depth, and FWHM linewidths.

* **`sweep_raspberry.py` (Raspberry Pi 3 RF Server):**
  * Runs a TCP socket server that receives frequency (`GHz`), output power (`POWER:0–3`), and gate (`OFF`) commands from the desktop host.
  * Programs the **ADF4351** PLL synthesizer via SPI (`CE` on GPIO 17) and verifies phase-lock stability via the hardware `LOCK` pin (GPIO 24) before asserting the trigger line (GPIO 22).

* **`main.py` (Raspberry Pi Pico Hardware Gate Driver):**
  * Runs a low-latency hardware polling loop at 125 MHz monitoring the trigger signal from the Raspberry Pi (`GP22`).
  * Toggles the complementary control lines `A` (`GP14`) and `B` (`GP15`) via the **SN74AHCT125** level shifter to route the microwave signal through the **HMC284** RF switch either to the amplifier/CPWG loop (`A=1, B=0`) or safely into the 50 Ω dummy load (`A=0, B=1`).


<div align="center">
  <img src="images/odmr_roi1302_1000_exp3ms_avg15_mask90_pwr1_20261122_123820_sensor.png" width="600"><br>
  <em>NV diamond under the 4x microscope objective with the 64 × 64 ROI set to the brightest fluorescence spot above the CPWG loop.</em>
</div>


<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:55%; text-align:center; vertical-align:middle; border: none;">
      <img src="results/odmr_roi1302_1000_exp3ms_avg15_mask90_pwr1_20261122_123820.png" width="650"><br>
      <em>CW-ODMR spectrum showing raw PL drift compensation (top) and double Lorentzian fit (bottom).</em>
    </td>
    <td style="width:45%; text-align:left; vertical-align:middle; border: none;">
      <ul>
        <li><strong>CW-ODMR Protocol:</strong> Differential Snap-Sync sweep from <strong>2.765–2.960 GHz</strong> in <strong>5.0 MHz</strong> steps (15× pairwise averaging per step).</li>
        <li><strong>Microwave Drive:</strong> ADF4351 output set to <strong>Level 1 (-1.0 dBm)</strong>, modulated via the HMC284 switch.</li>
        <li><strong>Camera & ROI:</strong> <strong>64 × 64 px</strong> ROI at <code>(1302, 1000)</code>, <strong>3.0 ms</strong> exposure, Gain <strong>252</strong>, with a <strong>&gt;90%</strong> intensity mask (410 active pixels) and 741 ADU dark offset subtraction.</li>
        <li><strong>Resonance Contrast:</strong> <strong>1.55%</strong> fitted contrast (<strong>1.58%</strong> raw peak dip) — a ~7.5× improvement over the earlier unmasked stripline setup.</li>
        <li><strong>Double Lorentzian Fit:</strong> Center zero-field splitting <strong><em>D</em> = 2.8709 GHz</strong>, strain/residual field splitting <strong><em>E</em> = 9.5 MHz</strong>, with sub-dips at <strong>2.8615 GHz</strong> (FWHM 33.3 MHz) and <strong>2.8804 GHz</strong> (FWHM 36.2 MHz).</li>
      </ul>
    </td>
  </tr>
</table>

## Outlook: 3D Magnetic Field Alignment, Rabi Oscillations & Next Hardware Steps

Building on the current CW-ODMR setup, the existing hardware already opens the door to magnetic field vector sensing and first experiments toward coherent spin control:

### 1. Selecting a Single NV Axis with a Permanent Magnet (8-Dip Zeeman Splitting)

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:55%; text-align:center; vertical-align:middle; border: none;">
      <img src="results/zeeman_8_dips.png" width="650"><br>
      <em>Preliminary 8-line Zeeman splitting spectrum (2.0 MHz step width, center D = 2.8724 GHz) recorded with an external permanent magnet.</em>
    </td>
    <td style="width:45%; text-align:left; vertical-align:middle; border: none;">
      <ul>
        <li><strong>Separating the 4 Diamond Axes:</strong> Because NV centers sit along four possible crystal orientations inside the diamond, applying an external bar magnet splits the single resonance into <strong>4 pairs (8 dips)</strong>.</li>
        <li><strong>Addressing One Specific Axis:</strong> By adjusting the position and orientation of the permanent magnet, a single NV axis can be isolated and tuned to a distinct resonance frequency so that only this sub-ensemble is addressed by the microwave field.</li>
        <li><strong>Measurement Status:</strong> This spectrum (2.78–2.94 GHz) was an initial test run before shifting focus to pulsed microwave experiments; reproducing and calibrating it provides the foundation for 3D magnetic field measurements.</li>
      </ul>
    </td>
  </tr>
</table>

### 2. First Rabi Oscillation Tests & Why a TTL Laser Is the Next Step

With the **HMC284 RF switch** and **Raspberry Pi Pico** already built into the microwave path, the setup can already generate short microwave pulses at the selected resonance frequency.

* **Goal – Superposition & $R_y(\theta)$ Gate:** Starting from the optically initialized ground state $|0\rangle$, applying a resonant microwave pulse of duration $\tau$ rotates the spin state on the Bloch sphere, realizing a single-qubit rotation gate $R_y(\theta)$ with rotation angle $\theta = \Omega_R \tau$ (where $\Omega_R$ is the Rabi frequency):
  $$|\psi\rangle = R_y(\theta)|0\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + \sin\left(\frac{\theta}{2}\right)|1\rangle$$
  For a $\pi/2$ pulse ($\theta = \pi/2$), the NV spin is placed into an equal **superposition state**:
  $$|\psi\rangle = \frac{1}{\sqrt{2}}\big(|0\rangle + |1\rangle\big)$$
* **Current Observation (Damped Oscillations):** Initial pulsed-microwave tests already show hints of Rabi oscillations, but the signal quickly flattens out. Because the current **532 nm TRU COMPONENTS laser** runs in continuous-wave (CW) mode, the green light constantly re-polarizes the spins back into $|0\rangle$ while the microwave pulse is trying to rotate them.
* **Planned Hardware Upgrade (TTL-Modulated Laser):** Since the current laser module cannot be switched fast enough via TTL, the logical next upgrade outside the scope of this initial paper is replacing it with a **TTL-modulated 530 nm laser**. Pulsing both the laser and the microwaves will allow clean state initialization, undisturbed $R_y(\theta)$ spin rotation in the dark, and synchronized fluorescence readout.


### 3. Preliminary Pulsed-Microwave Test (Damped Rabi Oscillation Attempt)

<table style="width:100%; border: none;">
  <tr style="border: none;">
    <td style="width:55%; text-align:center; vertical-align:middle; border: none;">
      <img src="images/20261119_224556.jpg" width="650"><br>
      <em>Preliminary pulsed-microwave measurement showing initial oscillatory behavior followed by rapid damping under continuous-wave (CW) green laser illumination.</em>
    </td>
    <td style="width:45%; text-align:left; vertical-align:middle; border: none;">
      <ul>
        <li><strong>Experimental Test:</strong> Pulsed microwave excitation applied via the HMC284 RF switch and Raspberry Pi Pico while sweeping the pulse duration.</li>
        <li><strong>Observed Behavior:</strong> Initial hints of Rabi oscillations appear at short pulse durations before the curve rapidly flattens out (damping).</li>
        <li><strong>Physical Cause:</strong> Because the current 532 nm laser runs continuously (CW), the green excitation light constantly re-polarizes the NV spins back into the |0&rang; ground state during the microwave pulse.</li>
        <li><strong>Next Step:</strong> Investigation into upgrading to a TTL-modulated 530 nm diode laser to allow switching the laser off during the microwave pulse to observe undamped Rabi oscillations.</li>
      </ul>
    </td>
  </tr>
</table>

## Acknowledgements & Support

This project was made possible through the support of inspiring academic research and material supply from the quantum hardware industry:

* **Neocrystech (Shanghai, China):** Thank you to the team at Neocrystech for supplying the Ensemble NV Diamond (ENV-20) sample used in this independent research project. Their commitment to supporting the quantum community enabled the successful execution of this room-temperature experiment.

*   **FH Münster (University of Applied Sciences):** This setup is conceptually inspired by the pioneering open-source paper *"Modular low-cost 3D printed setup for experiments with NV centers in diamond"* by F. Hoffmann, M. Gregor, et al. Their work provided vital guidance and inspiration for designing budget-friendly quantum hardware.

### Component Sourcing & Fabrication Providers
To make this quantum experiment accessible for community replication, the setup follows a budget-friendly hybrid philosophy. Industry-standard precision optics and stable optomechanical foundations are combined with cost-effective hardware mounts where mechanical tolerances allow.

*   **Thorlabs:** Sourced for high-quality metric post holders and mounting bases, ensuring the necessary mechanical stability and alignment precision in critical optical paths.
*   **JLCPCB:** Sourced for rapid, high-quality fabrication of the custom 0.8 mm FR4 microwave stripline PCBs.
*   **Busse Yachtshop:** Sourced for the specialty 0.8 mm SMA edge connectors utilized in the RF delivery loop.
*   **Conrad Electronic & Amazon:** Sourced for the TRU COMPONENTS excitation laser, microscope objectives, frequency synthesizers, generic optical rails, and general electronic components.

## Bill of Materials (BOM)

*Note on Pricing & Availability: All prices listed below are approximate guidelines based on my local purchases in 2026. Prices and component availability are subject to change depending on the distributor, your region, and market fluctuations.*

The total hardware cost for this hybrid setup is optimized for educational and independent research purposes. Below is the complete list of components, including approximate pricing and sourcing links.

### 1. Quantum & Optical Components

| Component | Description | Source / Link | Price (approx.) |
| :--- | :--- | :--- | :--- |
| **NV Diamond** | Ensemble NV Diamond 100, NV density ~7 ppm (0.5 × 0.5 × 0.3 mm) | Neocrystech | On request |
| **Excitation Laser** | 1 mW 532 nm green laser module (TRU COMPONENTS LM01GND) | Conrad | 35 EUR |
| **Microscope Objective** | 4x magnification, 0.10 NA, 160/0.17 | Amazon | 13 EUR |
| **Dichroic Mirror** | Transmits green (532 nm), reflects red (fluorescence) | Custom | On request |
| **50:50 Beam Splitter** | Transmits 50% of green (532 nm) and red (fluorescence) | Custom | On request |
| **Optical Filter (Initial)** | Heat-resistant red lighting filter sheets | Amazon | 8 EUR |
| **Optical Filter (Enhanced)** | Astronomik ProPlanet 642 BP 1.25" bandpass filter | [Astroshop](https://astroshop.de) | 79 EUR |
| **Optical Breadboard** | Solid aluminum base plate (300 × 300 × 12.7 mm) | Gebert & Weschka | 145 EUR |

### 2. Signal Detection & Imaging

| Component | Description | Source / Link | Price (approx.) |
| :--- | :--- | :--- | :--- |
| **CMOS Camera** | ZWO ASI 585MC Color USB 3.0 Planetary Camera | [Astroshop](https://astroshop.de) | 586 EUR |
| **Kinematic Mount** | Kinematic Optical Mirror / Camera Mount (Generic RMH-X) per piece | - | 35 EUR |
| **Post Holder** | PH50/M-P5 50 mm Metric Post Holder | [Thorlabs](https://thorlabs.com) | 42 EUR (5 pcs) |
| **Mounting Base** | BA1S/M-P5 25 mm × 10 mm Base | [Thorlabs](https://thorlabs.com) | 25 EUR (5 pcs) |

### 3. RF & Microwave Electronics

| Component | Description | Source / Link | Price (approx.) |
| :--- | :--- | :--- | :--- |
| **Custom PCB** | 2 layouts (Stripline & Loop), 0.8 mm FR4 substrate | [JLCPCB](https://jlcpcb.com/) | 17 USD (5 pcs) |
| **Frequency Synthesizer** | ADF4351 PLL Development Board (35 MHz – 4.4 GHz) | [Amazon](https://www.amazon.de/) | 30 EUR |
| **RF Switch** | HMC284 SPDT RF Switch Module (DC – 3.5 GHz) for fast microwave gating | [AliExpress](https://www.aliexpress.com/) | 17 EUR |
| **RF Power Amplifier** | 36 dB, 1 W Broadband Driver (SBB5089 + SZA3044, 1.5–3.9 GHz) | [AliExpress](https://www.aliexpress.com/) | 19 EUR |
| **SMA Edge Connectors** | 0.8 mm PCB edge launch connectors | [Busse Yachtshop](https://busse-yachtshop.de/) | 30 EUR (8 pcs) |
| **SMA Cable** | RG316 coaxial cable | [Amazon](https://www.amazon.de/) | 8.50 EUR |
| **SMA Terminator** | 50 Ohm, 2 W dummy load | [Amazon](https://www.amazon.de/) | 8 EUR (5 pcs) |
| **SMA Attenuator** | 3 dB fixed attenuator, DC – 6 GHz, 50 Ohm | [Amazon](https://www.amazon.de/) | 12 EUR |

### 4. Control Computing & Logic Interfacing

| Component | Description | Source / Link | Price (approx.) |
| :--- | :--- | :--- | :--- |
| **Host Computer** | Raspberry Pi 3 (Model B) for instrument orchestration | - | 45 EUR |
| **Hardware Trigger MCU** | Raspberry Pi Pico (RP2040) for low-latency RF gate switching | [Amazon](https://www.amazon.de/) | 15 EUR |
| **Logic Level Shifter** | SN74AHCT125 Quad Bus Buffer Gate (3.3 V to 5 V TTL level shifting) | [Amazon](https://www.amazon.de/) | 10 EUR (10 pcs)|


### Sources

- https://www.hb.fh-muenster.de/opus4/frontdoor/deliver/index/docId/20263/file/Modular_low_cost_3D_printed.pdf

## Safety Disclaimer & Laser Safety Notice

### Warning: Laser Safety First!
Even though the laser module used in this setup may be classified as a **Class 1** laser under normal operating conditions, any modification, collimation, or focusing through optical components (such as the microscope objective used in this experiment) can drastically increase the power density and pose a severe risk to your eyes. 

*   **Eye Protection:** Always wear appropriate, certified **laser safety goggles** (laser safety glasses) that are specifically rated for the exact wavelength (nm) and power of your laser module. Never look directly into the beam or its specular reflections.
*   **Microwave Radiation:** This setup utilizes an ADF4351 RF generator. Ensure proper shielding and do not operate high-power RF components uncovered near your body.

### Liability Disclaimer
This project is provided for educational and research purposes only "as is", without any warranties or guarantees of any kind. The author assumes no responsibility or liability for any damage to hardware, personal injury, or vision loss resulting from the replication or use of the scripts, hardware configurations, or instructions documented in this repository. Replicate this experiment entirely at your own risk.


## Disclaimer

This is an independent open-source project. Code and English wording were assisted by AI tools and optimized for this hardware stack.
