# Home Laboratory ODMR Setup: NV Centers in Diamond with a CMOS Camera at Room Temperature

> ⚠️ **Project Status: Work in Progress (WIP)**  
> This repository is actively being updated. Hardware and basic structures are documented, while detailed software scripts and final measurement plots are being added progressively. Feel free to watch the repository for updates!

An open-source physics home experiment inspired by the paper *"Modular low-cost 3D printed setup for experiments with NV centers in diamond"* (FH Münster). 

This project implements Optically Detected Magnetic Resonance (ODMR) to observe and manipulate quantum spin states at room temperature, utilizing a **ZWO ASI 585MC CMOS camera** for advanced imaging and flexible Region-of-Interest (ROI) data acquisition.

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
      <em>Figure 1: Full ODMR setup overview.</em>
    </td>
    <td style="width:50.0%; text-align:center; border: none;">
      <img src="images/20261011_163507.jpg" width="400"><br>
      <em>Figure 2: Close-up of the ZWO ASI 585.</em>
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

For the final experiment presented in this project, the **Micro Stripline** layout was selected. The corresponding Gerber files will be made available for download in this repository.


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
      <em>Python-generated Matplotlib plot showing the continuous frequency sweep. The characteristic ODMR dip is clearly resolved with a contrast depth of approximately 2%.</em>
    </td>
  </tr>
</table>

## Acknowledgements & Support

This project was made possible through the support of inspiring academic research and generous material sponsorship from the quantum hardware industry:

*   **Neocrystech (Shanghai, China):** A special thanks to the team at Neocrystech for generously providing the high-quality Ensemble NV Diamond (ENV-20) substrate for this independent research. Their commitment to supporting the quantum community enabled the successful execution of this room-temperature experiment.
*   **FH Münster (University of Applied Sciences):** This setup is conceptually inspired by the pioneering open-source paper *"Modular low-cost 3D printed setup for experiments with NV centers in diamond"* by F. Hoffmann, M. Gregor, et al. Their work provided vital guidance and inspiration for designing budget-friendly quantum hardware.

### Component Sourcing & Fabrication Providers
To make this quantum experiment accessible for community replication, the setup follows a budget-friendly hybrid philosophy. Industry-standard precision optics and stable optomechanical foundations are combined with cost-effective hardware mounts where mechanical tolerances allow.

*   **Thorlabs:** Sourced for high-quality metric post holders and mounting bases, ensuring the necessary mechanical stability and alignment precision in critical optical paths.
*   **JLCPCB:** Sourced for rapid, high-quality fabrication of the custom 0.8 mm FR4 microwave stripline PCBs.
*   **Busse Yachtshop:** Sourced for the specialty 0.8 mm SMA edge connectors utilized in the RF delivery loop.
*   **Conrad Electronic & Amazon:** Sourced for the TRU COMPONENTS excitation laser, microscope objectives, frequency synthesizers, generic optical rails, and general electronic components.

## Bill of Materials (BOM)

*Note on Pricing & Availability: All prices listed above are approximate guidelines based on my local purchases in 2026. Prices and component availability are subject to change depending on the distributor, your region, and market fluctuations.*

The total hardware cost for this hybrid setup is optimized for hobbyists and educational purposes. Below is the complete list of components, including approximate pricing and sourcing links.

### 1. Quantum & Optical Components

| Component | Description | Source / Link | Price (approx.) |
| :--- | :--- | :--- | :--- |
| **NV Diamond** | Ensemble NV Diamond 100, NV density ~7 ppm, (0.5 × 0.5 × 0.3 mm) | [Neocrystech](https://www.neocrystech.com/product/Ensemble-NV-Diamond-100.html) | - |
| **Excitation Laser** | 1 mW 532 nm green laser module (TRU COMPONENTS LM01GND) | [Conrad](https://www.conrad.de/) | 35 EUR |
| **Microscope Objective** | 4x magnification, 0.10 NA, 160/0.17 | [Amazon](https://www.amazon.de/) | 13 EUR |
| **Dichroic Mirror** | Reflects green (532 nm), transmits red (fluorescence) | Custom | - |
| **Optical Filter** | Heat-resistant red lighting filter sheets | [Amazon](https://www.amazon.de/) | 8 EUR |
| **Optical Breadboard** | Solid aluminum base plate (300 × 300 × 12.7 mm) | [Gebert & Weschka](https://gebertweschka.de/) | 145 EUR |

### 2. Signal Detection & Imaging

| Component | Description | Source / Link | Price (approx.) |
| :--- | :--- | :--- | :--- |
| **CMOS Camera** | ZWO ASI 585MC Color USB 3.0 Planetary Camera | [Astroshop](https://astroshop.de) | 586 EUR |
| **Kinematic Mount** | Kinematic Optical Mirror / Camera Mount (Generic RMH-X) per piece| - | 35 EUR |
| **Post Holder** | PH50/M-P5 50 mm Metric Post Holder | [Thorlabs](https://thorlabs.com) | 42 EUR (5 pcs) |
| **Mounting Base** | BA1S/M-P5 25 mm × 10 mm Base | [Thorlabs](https://thorlabs.com) | 25 EUR (5 pcs) |


### 3. RF & Microwave Electronics

| Component | Description | Source / Link | Price (approx.) |
| :--- | :--- | :--- | :--- |
| **Custom PCB** | 2 layouts (Stripline & Loop), 0.8 mm FR4 substrate | [JLCPCB](https://jlcpcb.com/) | 17 USD (5 pcs) |
| **Frequency Synthesizer**| ADF4351 PLL Development Board (35 MHz - 4.4 GHz) | [Amazon](https://www.amazon.de/) | 30 EUR |
| **RF Power Amplifier** | 36 dB 1W Broadband Driver (SBB5089 + SZA3044, 1.5-3.9 GHz) | [AliExpress](https://www.aliexpress.com/) | 15 EUR |
| **SMA Edge Connectors** | 0.8 mm PCB edge launch connectors | [Busse Yachtshop](https://busse-yachtshop.de/) | 30 EUR (8 pcs) |
| **SMA Cable** | RG316 coaxial cable | [Amazon](https://www.amazon.de/) | 8.50 EUR |
| **SMA Terminator** | 50 Ohm, 2W dummy load | [Amazon](https://www.amazon.de/) | 8 EUR (5 pcs) |
| **SMA Attenuator** | 3 dB fixed attenuator, DC - 6 GHz, 50 Ohm | [Amazon](https://www.amazon.de/) | 12 EUR |

### 4. Control Computing

| Component | Description | Source / Link | Price (approx.) |
| :--- | :--- | :--- | :--- |
| **Host Computer** | Raspberry Pi 3 (Model B) for instrument orchestration | - | 45 EUR |


### Sources

- https://www.hb.fh-muenster.de/opus4/frontdoor/deliver/index/docId/20263/file/Modular_low_cost_3D_printed.pdf

## Safety Disclaimer & Laser Safety Notice

### Warning: Laser Safety First!
Even though the laser module used in this setup may be classified as a **Class 1** laser under normal operating conditions, any modification, collimation, or focusing through optical components (such as the microscope objective used in this experiment) can drastically increase the power density and pose a severe risk to your eyes. 

*   **Eye Protection:** Always wear appropriate, certified **laser safety goggles** (laser safety glasses) that are specifically rated for the exact wavelength (nm) and power of your laser module. Never look directly into the beam or its specular reflections.
*   **Microwave Radiation:** This setup utilizes an ADF4351 RF generator. Ensure proper shielding and do not operate high-power RF components uncovered near your body.

### Liability Disclaimer
This project is provided for educational and hobbyist purposes only "as is", without any warranties or guarantees of any kind. The author assumes no responsibility or liability for any damage to hardware, personal injury, or vision loss resulting from the replication or use of the scripts, hardware configurations, or instructions documented in this repository. Replicate this experiment entirely at your own risk.


## Disclaimer

This is a DIY hobbyist project. Code and English wording were assisted by AI tools and optimized for this hardware stack.
