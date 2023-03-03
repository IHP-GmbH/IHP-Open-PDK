* SPICE-Parameter HBT-Transistor (nom.)
* 
* Model:                                VBIC (Rev.1.15)
* Date:                                 25.05.18
* Lot:                                  EDJ802
* WAFER:                                02
* CHIP Nr:                              
* Device:                               npn13g2_VBIC_Q118
* Emitter size (mask):                  Nx *(0.07 x 0.90) µm^2 with Nx = 1 - 10
* Maximum collector-to-emitter voltage: 1.6
* Measurement data:                     T274_PQX402_W05_8.2
* Meas. Range forward gummel:           vbe = (0.3 - 1.04)V
* Meas. Range forward output:           vce = (0.4 - 2.0)V
* Nom. Temperature  (TNOM):             27 grd C
* Meas. Temperature (TEMP):             27 grd C
* Valid range for model                 
* ic: <(0.003*Nx) A  vbe :(0.65 - 0.96) V  vce :(0.4 - 2.0) V
* Temp: -40°C - +125°C
* Valid numbers: NX = 1 - 10
* model card checked with SPECTRE 10.x and ADS2009U1
* ________________________________________________________________________
*
* Note: Ny and we must not be changed. Kept for formal reasons
*
inline subckt npn13G2_vbic  c b e bn
parameters Nx=1 trise=0.0

npn13G2_vbic (c b e s1) npn13G2_NX trise=trise

model npn13G2_NX vbic
+ type = npn
+ bvbe = 1.6
+ bvbc = 5.1
+ bvce = 1.6
+ bvsub = 20
+ vbefwd=0.2
+ vbcfwd=0.2
+ vsubfwd=0.2
+ alarm = sat
+ tnom = 27
+ cbeo = 8.00E-16*(Nx*0.25)**0.975
+ cje = 8.418E-15*(Nx*0.25)**0.975*vbic_cje*(1+(vbic_cje_mm-1)/sqrt(m*Nx))
+ pe = 0.92
+ me = 0.12
+ aje = -0.50
+ wbe = 1.00
+ cbco = 2.36E-15*(Nx*0.25)
+ cjc = 1.53E-15*(Nx*0.25)*vbic_cjc*(1+(vbic_cjc_mm-1)/sqrt(m*Nx))
+ pc = 0.558
+ mc = 0.12
+ ajc = -0.50
+ cjep = 3.56E-15*(Nx*0.25)*vbic_cjc*(1+(vbic_cjc_mm-1)/sqrt(m*Nx))
+ cjcp = 4.56E-15*(Nx*0.25)**0.8*vbic_cjcp*(1+(vbic_cjcp_mm-1)/sqrt(m*Nx))
+ ps = 0.46
+ ms = 0.23
+ ajs = -0.50
+ fc = 0.80
+ vef = 189
+ ver = 5.3
+ is = 5.53E-17*(Nx*0.25)*vbic_is*(1+(vbic_is_mm-1)/sqrt(m*Nx))
+ nf = 1.018
+ ibei = 2.12E-19*(Nx*0.25)*vbic_ibei*(1+(vbic_ibei_mm-1)/sqrt(m*Nx))
+ nei = 1.066
+ iben = 4.00E-16*(Nx*0.25)
+ nen = 2.00
+ ikf = 0.009*(Nx*0.25)
+ nr = 1.01
+ ibci = 1.50E-20*(Nx*0.25)
+ nci = 1.103
+ ibcn = 1.00E-15*(Nx*0.25)
+ ncn = 1.96
+ ikr = 0.01*(Nx*0.25)
+ wsp = 1
+ isp = 4.00E-20*(Nx*0.25)
+ nfp = 1.04
+ ibcip = 2.00E-15*(Nx*0.25)**0.7
+ ncip = 1.00
+ ibcnp = 5.00E-15*(Nx*0.25)
+ ncnp = 1.50
+ ikp = 1.00E-04*(Nx*0.25)
+ ibeip = 4.00E-19*(Nx*0.25)
+ ibenp = 2.00E-14*(Nx*0.25)
+ re = 7.13E+00*(4/Nx)**1*vbic_re*(1+(vbic_re_mm-1)/sqrt(m*Nx))
+ rcx = 1.30E+01*(4/Nx)**1*vbic_rcx*(1+(vbic_rcx_mm-1)/sqrt(m*Nx))
+ rci = 1.29E+01*(4/Nx)**1
+ qco = 1.00E-18
+ vo = 0.80
+ gamm = 2.25E-14
+ hrcf = 1000
+ rbx = 6.93E+00*(4/Nx)**0.95*vbic_rbx*(1+(vbic_rbx_mm-1)/sqrt(m*Nx))
+ rbi = 2.20E+01*(4/Nx)**0.95*vbic_rbx*(1+(vbic_rbx_mm-1)/sqrt(m*Nx))
+ rbp = 5.5*(4/Nx)
+ rs = 1
+ avc1 = 2.40
+ avc2 = 10.81
+ tf = 2.02E-13*vbic_tf*(1+(vbic_tf_mm-1)/sqrt(m*Nx))*((temp+273)/300)**0.7
+ qtf = 1.00E-18
+ xtf = 10.0
+ vtf = 20.0
+ itf = 0.585*(Nx*0.25)
+ tr = 3.50E-13
+ td = 2.80E-15*(Nx*0.25)**0
+ selft = 1
+ cth = 1.60E-12*(Nx*0.25)**0.95
+ rth = 3.26E+03*(4/Nx)**0.9
+ ea = 1.040
+ eaie = 1.056
+ eaic = 1.12
+ eais = 1.12
+ eane = 1.12
+ eanc = 1.12
+ eans = 1.12
+ xre = -0.42
+ xrb = 0.90
+ xrc = 0.245
+ xrs = 1.50
+ xvo = 1.50
+ xis = 2.30
+ xii = 3.30
+ xin = 3.30
+ tnf = 0.00015
+ tavc = -0.00188
+ kfn = 6E-9*(4/Nx)
+ afn = 1.80
+ bfn = 1.00

Rsub (s1 bn) resistor r = 300+100*Nx
Csub (s1 bn) capacitor c = 2.30E-14-(1.50E-15*Nx)
ends npn13G2_vbic
