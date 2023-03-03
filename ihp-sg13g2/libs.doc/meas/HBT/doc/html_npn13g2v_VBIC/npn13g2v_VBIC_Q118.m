* Model:                                VBIC (Rev.1.15)
* Date:                                 25.05.18
* Lot:                                  EDJ802
* WAFER:                                02
* CHIP Nr:                              3.3
* Device:                               npn13g2v_VBIC_Q118
* Emitter size (mask):                  Nx *(0.12 x El) um^2 with Nx = 1 - 4, El = 1.0 - 5.0 
* Maximum collector-to-emitter voltage: 2.5
* Measurement data:                     T356_EDJ802_W02_3.3
* Meas. Range forward gummel:           vbe = (0.3 - 1.0)V
* Meas. Range forward output:           vce = (0.4 - 2.0)V
* Nom. Temperature  (TNOM):             27 grd C
* Meas. Temperature (TEMP):             27 grd C
* Valid range for model
* ic: <(0.003*Nx) A  vbe :(0.65 - 0.96) V  vce :(0.4 - 2.0) V
* Temp: -40C - +125C
* Valid numbers: Nx = 1 - 4, El = 1 - 5
* model card checked with SPECTRE 10.x and ADS2009U1
* ________________________________________________________________________

simulator lang=spectre

inline subckt npn13G2v c b e bn
parameters Nx=1 El=5.0 trise=0
npn13G2v (c b e s1) npn13G2v_NX trise=trise m=1

model npn13G2v_NX vbic
+ type = npn
+ bvbe = 1.6
+ bvbc = 7.0
+ bvce = 2.2
+ bvsub = 20
+ vbefwd=0.2
+ vbcfwd=0.2
+ vsubfwd=0.2
+ alarm = sat
+ tnom = 27
+ cbeo = 2.28E-15*(El/2.5)**0.94*(Nx*0.25)**0.95
+ cje = 2.594E-14*(El/2.5)**0.94*(Nx*0.25)**0.95*vbic_cje*(1+(vbic_cje_mm-1)/sqrt(m*Nx))
+ pe = 0.88
+ me = 0.13
+ aje = -0.50
+ wbe = 1.00
+ cbco = 4.37E-15*(El/2.5)**0.85*(Nx*0.25)**0.975
+ cjc = 2.52E-15*(El/2.5)**0.85*(Nx*0.25)**0.975*vbic_cjc*(1+(vbic_cjc_mm-1)/sqrt(m*Nx))
+ pc = 0.397
+ mc = 0.09
+ ajc = -0.50
+ cjep = 6.48E-15*(El/2.5)**0.85*(Nx*0.25)**0.975*vbic_cjc*(1+(vbic_cjc_mm-1)/sqrt(m*Nx))
+ cjcp = 7.60E-15*(El/2.5)**0.65*(Nx*0.25)**0.5*vbic_cjcp*(1+(vbic_cjcp_mm-1)/sqrt(m*Nx))
+ ps = 0.31
+ ms = 0.16
+ ajs = -0.50
+ fc = 0.80
+ vef = 189
+ ver = 5.3
+ is = 1.22E-16*(El/2.5)**0.8*(Nx*0.25)*vbic_is*(1+(vbic_is_mm-1)/sqrt(m*Nx))
+ nf = 1.016
+ ibei = 3.02E-19*(El/2.5)**0.925*(Nx*0.25)*vbic_ibei*(1+(vbic_ibei_mm-1)/sqrt(m*Nx))
+ nei = 1.043
+ iben = 1.44E-15*(El/2.5)**0.925*(Nx*0.25)
+ nen = 2.00
+ ikf = 0.022*(El/2.5)*(Nx*0.25)
+ nr = 1.01
+ ibci = 7.50E-19*(El/2.5)*(Nx*0.25)
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
+ re = 3.30E+00*(2.5/El)*(4/Nx)**0.88*vbic_re*(1+(vbic_re_mm-1)/sqrt(m*Nx))
+ rcx = 1.30E+01*(2.5/El)*(4/Nx)**0.9*vbic_rcx*(1+(vbic_rcx_mm-1)/sqrt(m*Nx))
+ rci = 1.53E+02*(2.5/El)**0.9*(4/Nx)
+ qco = 1.00E-18
+ vo = 2.40
+ gamm = 3.30E-12
+ hrcf = 1000
+ rbx = 1.54E+00*(2.5/El)**0.75*(4/Nx)*vbic_rbx*(1+(vbic_rbx_mm-1)/sqrt(m*Nx))
+ rbi = 6.60E+00*(2.5/El)**0.75*(4/Nx)*vbic_rbx*(1+(vbic_rbx_mm-1)/sqrt(m*Nx))
+ rbp = 6.5*(2.5/El)**0.75*(4/Nx)
+ rs = 1*(2.5/El)*(4/Nx)
+ avc1 = 2.40
+ avc2 = 17.14
+ tf = 4.10E-13*(El/2.5)**0*vbic_tf*(1+(vbic_tf_mm-1)/sqrt(m*Nx))*((temp+273)/300)**0.7
+ qtf = 1.00E-18
+ xtf = 60.0
+ vtf = 20.0
+ itf = 0.390*(El/2.5)*(Nx*0.25)
+ tr = 1.50E-12
+ td = 5.60E-13*(El/2.5)
+ selft = 1
+ cth = 4.40E-12*(El/2.5)**1*(Nx*0.25)**0.8
+ rth = 1.55E+03*(2.5/El)**1*(4/Nx)**0.88
+ ea = 1.030
+ eaie = 1.056
+ eaic = 1.12
+ eais = 1.12
+ eane = 1.12
+ eanc = 1.12
+ eans = 1.12
+ xre = -0.35
+ xrb = 0.90
+ xrc = 0.175
+ xrs = 1.50
+ xvo = 1.50
+ xis = 2.70
+ xii = 3.00
+ xin = 3.00
+ tnf = 0.00015
+ tavc = -0.00075
+ kfn = 6E-7*(2.5/El)*(4/Nx)
+ afn = 2.2
+ bfn = 1.00
Rsub (s1 bn) resistor r = (300+(400*Nx))*(El/2.5)**0.85
Csub (s1 bn) capacitor c = (1.70E-14-(2.00E-15*Nx))*(El/2.5)**0
ends npn13G2v