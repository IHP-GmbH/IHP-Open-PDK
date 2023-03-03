* SPICE-Parameter HBT-Transistor (nom.)
*
* Model:                                VBIC (Rev.1.15)
* Date:                                 25.05.18
* Lot:                                  EDJ802
* WAFER:                                02
* CHIP Nr:                              3.3
* Device:                               npn13g2l_VBIC_Q118
* Emitter size (mask):                  Nx *(0.07 x El) um^2 with Nx = 1 - 4, El = 1 - 2.5 
* Maximum collector-to-emitter voltage: 1.6
* Measurement data:                     T356_EDJ802_W02_3.3
* Meas. Range forward gummel:           vbe = (0.3 - 1.04)V
* Meas. Range forward output:           vce = (0.4 - 2.0)V
* Nom. Temperature  (TNOM):             27 grd C
* Meas. Temperature (TEMP):             27 grd C
* Valid range for model
* ic: <(...Nx*El) A  vbe :(0.65 - 0.96) V  vce :(0.4 - 2.0) V
* Temp: -40C - +125C
* Valid numbers: Nx = 1 - 4, El = 1 - 2.5
* model card checked with SPECTRE 10.x and ADS2009U1
* ________________________________________________________________________

simulator lang=spectre

inline subckt npn13G2l c b e bn
parameters Nx=1 El=2.5 trise=0
npn13G2l (c b e s1) npn13G2l_NX trise=trise m=1

model npn13G2l_NX vbic
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
+ cbeo = 1.92E-15*(El/2.5)**0.85*(Nx*0.25)**0.95
+ cje = 2.166E-14*(El/2.5)**0.85*(Nx*0.25)**0.95*vbic_cje*(1+(vbic_cje_mm-1)/sqrt(m*Nx))
+ pe = 0.92
+ me = 0.12
+ aje = -0.50
+ wbe = 1.00
+ cbco = 6.33E-15*(El/2.5)**0.85*(Nx*0.25)**0.975
+ cjc = 3.83E-15*(El/2.5)**0.85*(Nx*0.25)**0.975*vbic_cjc*(1+(vbic_cjc_mm-1)/sqrt(m*Nx))
+ pc = 0.558
+ mc = 0.12
+ ajc = -0.50
+ cjep = 7.77E-15*(El/2.5)**0.85*(Nx*0.25)**0.975*vbic_cjc*(1+(vbic_cjc_mm-1)/sqrt(m*Nx))
+ cjcp = 8.36E-15*(El/2.5)**0.55*(Nx*0.25)**0.8*vbic_cjcp*(1+(vbic_cjcp_mm-1)/sqrt(m*Nx))
+ ps = 0.46
+ ms = 0.23
+ ajs = -0.50
+ fc = 0.80
+ vef = 189
+ ver = 5.3
+ is = 7.50E-17*(El/2.5)**0.85*(Nx*0.25)*vbic_is*(1+(vbic_is_mm-1)/sqrt(m*Nx))
+ nf = 1.004
+ ibei = 2.01E-19*(El/2.5)**0.85*(Nx*0.25)*vbic_ibei*(1+(vbic_ibei_mm-1)/sqrt(m*Nx))
+ nei = 1.035
+ iben = 1.20E-15*(El/2.5)**0.85*(Nx*0.25)
+ nen = 2.00
+ ikf = 0.032*(El/2.5)*(Nx*0.25)
+ nr = 1.01
+ ibci = 3.00E-19*(El/2.5)*(Nx*0.25)
+ nci = 1.050
+ ibcn = 1.00E-15*(El/2.5)*(Nx*0.25)
+ ncn = 1.70
+ ikr = 0.01*(El/2.5)*(Nx*0.25)
+ wsp = 1
+ isp = 4.00E-20*(El/2.5)*(Nx*0.25)
+ nfp = 1.04
+ ibcip = 2.00E-15*(El/2.5)*(Nx*0.25)**0.7
+ ncip = 1.00
+ ibcnp = 5.00E-15*(El/2.5)*(Nx*0.25)
+ ncnp = 1.50
+ ikp = 1.00E-04*(El/2.5)*(Nx*0.25)
+ ibeip = 4.00E-19*(El/2.5)*(Nx*0.25)
+ ibenp = 2.00E-14*(El/2.5)*(Nx*0.25)
+ re = 3.19E+00*(2.5/El)*(4/Nx)**0.88*vbic_re*(1+(vbic_re_mm-1)/sqrt(m*Nx))
+ rcx = 3.90E+00*(2.5/El)*(4/Nx)**0.9*vbic_rcx*(1+(vbic_rcx_mm-1)/sqrt(m*Nx))
+ rci = 7.50E+00*(2.5/El)**0.85*(4/Nx)**1
+ qco = 1.00E-18
+ vo = 0.80
+ gamm = 3.00E-14
+ hrcf = 1000
+ rbx = 2.54E+00*(2.5/El)**0.7*(4/Nx)*vbic_rbx*(1+(vbic_rbx_mm-1)/sqrt(m*Nx))
+ rbi = 7.26E+00*(2.5/El)**0.7*(4/Nx)*vbic_rbx*(1+(vbic_rbx_mm-1)/sqrt(m*Nx))
+ rbp = 15.0*(2.5/El)**0.7*(4/Nx)
+ rs = 1*(2.5/El)*(4/Nx)
+ avc1 = 2.40
+ avc2 = 10.81
+ tf = 2.31E-13*(El/2.5)**0.15*vbic_tf*(1+(vbic_tf_mm-1)/sqrt(m*Nx))*((temp+273)/300)**0.7
+ qtf = 1.00E-18
+ xtf = 10.0
+ vtf = 20.0
+ itf = 1.658*(El/2.5)*(Nx*0.25)
+ tr = 5.00E-13
+ td = 2.8e-13*(El/2.5)
+ selft = 1
+ cth = 4.18E-12*(El/2.5)**0.8*(Nx*0.25)**0.8
+ rth = 1.63E+03*(2.5/El)**0.85*(4/Nx)**0.8
+ ea = 1.045
+ eaie = 1.078
+ eaic = 1.12
+ eais = 1.12
+ eane = 1.12
+ eanc = 1.12
+ eans = 1.12
+ xre = -0.42
+ xrb = 0.90
+ xrc = 0.420
+ xrs = 1.50
+ xvo = 1.50
+ xis = 2.30
+ xii = 3.30
+ xin = 3.30
+ tnf = 0.00015
+ tavc = -0.00188
+ kfn = 3E-9*(2.5/El)*(4/Nx)
+ afn = 1.80
+ bfn = 1.00
Rsub (s1 bn) resistor r = (300+(400*Nx))*(El/2.5)**0.5
Csub (s1 bn) capacitor c = (1.70E-14-(2.00E-15*Nx))*(El/2.5)**0
ends npn13G2l
