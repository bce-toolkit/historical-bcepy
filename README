- BCE Core Library -

The main function of this library is to balance chemical equations and help you to deal with complex equations. It also contains some features(listed following) which can be re-used to build your own application.

Main features:
  *  Balance chemical equations (includes ionic equations, equations with multi-solutions, equations with SRU, equations with hydrates, electronic transferring equations, equations with abbreviations and indefinite equations).
  *  Substitute unknown symbols in chemical equations which contain one or more unknown symbols.
  *  Auto-correction.
  *  Predefined abbreviations and user custom abbreviations.
  *  Humanity error output.
  *  High precision calculation, hardware is the only limitation.
  *  Cross platform (fully written by Python).
  *  Multi languages support.
  *  Simple API to help you integrate this library to your own application.
  *  PyCharm development support.

Re-usable functions:
  *  Chemical equation parser (BCE syntax).
  *  Molecule equation parser (BCE syntax).
  *  Electronic expression parser (BCE syntax).
  *  Math expression parser.
  *  Solve linear equations.
  *  Dictionary-based locale system.
  *  A stack implementation.

For more features like rendering to MathML and reading MOL file, please have a look at the BCE Portal project.

Third party dependencies:
  *  SymPy (http://www.sympy.org/)

Examples (run run_balancer_manual_shell.py to test by your own):

  1) Normal equations:
     >> H2+O2=H2O
     2H2+O2=2H2O
     >> KMnO4=K2MnO4+MnO2+O2
     2KMnO4=K2MnO4+MnO2+O2
     >> P4+P2I4+H2O=PH4I+H3PO4
     13P4+10P2I4+128H2O=40PH4I+32H3PO4
     >> H2+Ca(CN)2+NaAlF4+FeSO4+MgSiO3+KI+H3PO4+PbCrO4+BrCl+CF2Cl2+SO2=PbBr2+CrCl3+MgCO3+KAl(OH)4+Fe(SCN)3+PI3+Na2SiO3+CaF2+H2O
     88H2+15Ca(CN)2+6NaAlF4+10FeSO4+3MgSiO3+6KI+2H3PO4+6PbCrO4+12BrCl+3CF2Cl2+20SO2=6PbBr2+6CrCl3+3MgCO3+6KAl(OH)4+10Fe(SCN)3+2PI3+3Na2SiO3+15CaF2+79H2O
     >> (NH4)2S+Al2(SO4)3+H2O=Al(OH)3+(NH4)2SO4+H2S
     3(NH4)2S+Al2(SO4)3+6H2O=2Al(OH)3+3(NH4)2SO4+3H2S

  2) Hydrate equations:
     >> CuSO4+H2O=CuSO4.5H2O
     CuSO4+5H2O=CuSO4.5H2O
     >> NH4H2PO4+(NH4)2MoO4+HNO3=NH4NO3+(NH4)3(PO4.12MoO3).2H2O+H2O
     NH4H2PO4+12(NH4)2MoO4+22HNO3=22NH4NO3+(NH4)3(PO4.12MoO3).2H2O+10H2O
     >> ((NH4)3(PO4.12MoO3).2H2O)+NaOH=(NH4)2MoO4+Na2MoO4+(NH4)2HPO4+H2O
     2((NH4)3(PO4.12MoO3).2H2O)+46NaOH=(NH4)2MoO4+23Na2MoO4+2(NH4)2HPO4+26H2O
     >> (NH4)2HPO4+(NH4)2MoO4+HNO3=(NH4)3(PO4.12MoO3).H2O+NH4NO3+H2O
     (NH4)2HPO4+12(NH4)2MoO4+23HNO3=(NH4)3(PO4.12MoO3).H2O+23NH4NO3+11H2O
     >> CoSO4+NH4OH+I2=Co2(NH3)10.(SO4)2I2.2H2O+H2O
     2CoSO4+10NH4OH+I2=Co2(NH3)10.(SO4)2I2.2H2O+8H2O
     >> CoSO4+NH3=CoSO4.6NH3
     CoSO4+6NH3=CoSO4.6NH3
     >> CoSO4+(NH4)2CO3+NH3+H2O+O2=(NH4)2SO4+(Co(NH3)4CO3)2SO4.3H2O
     4CoSO4+4(NH4)2CO3+12NH3+4H2O+O2=2(NH4)2SO4+2((Co(NH3)4CO3)2SO4.3H2O)
     >> Co(NO3)2+(NH4)2CO3+H2O=(NH4)2CO3.CoCO3.4H2O+NH4NO3
     Co(NO3)2+2(NH4)2CO3+4H2O=(NH4)2CO3.CoCO3.4H2O+2NH4NO3

  3) Ionic equations:
     >> Li+H<e+>=Li<e+>+H2
     2Li+2H<e+>=2Li<e+>+H2
     >> Li2O+H<e+>=Li<e+>+H2O
     Li2O+2H<e+>=2Li<e+>+H2O
     >> N2H4+H2O=N2H5<e+>+OH<e->
     N2H4+H2O=N2H5<e+>+OH<e->
     >> N2H4+H<e+>=N2H5<e+>
     N2H4+H<e+>=N2H5<e+>
     >> NH2OH=N2+H<e+>+<e->+H2O
     2NH2OH=N2+2H<e+>+2<e->+2H2O
     >> NH2OH+OH<e->=N2+H2O+<e->
     2NH2OH+2OH<e->=N2+4H2O+2<e->
     >> NH4<e+>+I<e->+ClO<e->=NHI2+NH3+Cl<e->+H2O
     2NH4<e+>+2I<e->+2ClO<e->=NHI2+NH3+2Cl<e->+2H2O
     >> NO+MnO4<e->+H<e+>=Mn<2e+>+NO3<e->+H2O
     5NO+3MnO4<e->+4H<e+>=3Mn<2e+>+5NO3<e->+2H2O
     >> NO2<e->+Al+OH<e->+H2O=Al(OH)4<e->+NH3
     NO2<e->+2Al+OH<e->+5H2O=2Al(OH)4<e->+NH3
     >> MnO4<e->+NO2<e->+H<e+>=Mn<2e+>+NO3<e->+H2O
     2MnO4<e->+5NO2<e->+6H<e+>=2Mn<2e+>+5NO3<e->+3H2O
     >> PO4<3e->+MoO4<2e->+NH4<e+>+H<e+>=(NH4)3(P(Mo12O40)).6H2O+H2O
     PO4<3e->+12MoO4<2e->+3NH4<e+>+24H<e+>=(NH4)3(P(Mo12O40)).6H2O+6H2O
     >> KMnO4+Fe<2e+>+H<e+>=Mn<2e+>+K<e+>+Fe<3e+>+H2O
     KMnO4+5Fe<2e+>+8H<e+>=Mn<2e+>+K<e+>+5Fe<3e+>+4H2O

  4) Electronic transferring equation (e.g. Galvanic interaction):
     >> Fe-<e->=Fe<3e+>
     Fe-3<e->=Fe<3e+>
     >> CH3OH+OH<e->=CO3<2e->+H2O+<e->
     CH3OH+8OH<e->=CO3<2e->+6H2O+6<e->
     >> O2+H2O+<e->=OH<e->
     O2+2H2O+4<e->=4OH<e->

  5) Equations with multi-solutions:
     >> C+O2=CO+CO2
     {2*Xa+2*Xb}C+{Xa+2*Xb}O2={2*Xa}CO+{2*Xb}CO2
     >> XeF4+C2H4=Xe+(CH2F)2+CH3CHF2
     {Xa+Xb}XeF4+{2*Xa+2*Xb}C2H4={Xa+Xb}Xe+{2*Xa}(CH2F)2+{2*Xb}CH3CHF2
     >> Cu+HNO3=Cu(NO3)2+NO+NO2+H2O
     {-Xa+3*Xb}Cu+{8*Xb}HNO3={-Xa+3*Xb}Cu(NO3)2+{-2*Xa+2*Xb}NO+{4*Xa}NO2+{4*Xb}H2O
     >> CuS+CN<e->+OH<e->=Cu(CN)4<3e->+NCO<e->+S+S<2e->+H2O
     {2*Xa-2*Xb}CuS+{8*Xa-7*Xb}CN<e->+{2*Xb}OH<e->={2*Xa-2*Xb}Cu(CN)4<3e->+{Xb}NCO<e->+{Xa-2*Xb}S+{Xa}S<2e->+{Xb}H2O
     >> NH4ClO4+HNO3+HCl=HClO4+N2O+Cl2+H2O
     {-4*Xa-4*Xb+4*Xc}NH4ClO4+{12*Xa+4*Xb-4*Xc}HNO3+{8*Xa+11*Xb-4*Xc}HCl={4*Xa-Xb}HClO4+{4*Xa}N2O+{4*Xb}Cl2+{4*Xc}H2O

       6) Equations with SRU (S-Group Repeat Unit):
     >> C{n}H{2n+2}+O2=CO2+H2O
     {(n+1)^(-1)}C{n}H{2n+2}+{(1/2)*(3*n+1)/(n+1)}O2={n/(n+1)}CO2+H2O
     >> X-<e->=X<{n}e+>
     X-{n}<e->=X<{n}e+>
     >> CaSO4+H2O={x}CaSO4.{y}H2O
     {x}CaSO4+{y}H2O={x}CaSO4.{y}H2O
     >> (CH2){n}+HCl=CH3Cl
     {n^(-1)}(CH2){n}+HCl=CH3Cl

  7) Auto-correction (Remove useless molecule / Wrong side correction):
     >> #  Wrong side correction:
     >> CO(NH2)2+NaNO2+N2+H2SO4=Na2SO4+CO2+H2O
     CO(NH2)2+2NaNO2+H2SO4=2N2+Na2SO4+CO2+3H2O
     >> N2O3+C6H4SO2OHNH2+H2O=C6H4SO2OHN2(CH3COO)+CH3COOH
     3H2O+2C6H4SO2OHN2(CH3COO)=N2O3+2C6H4SO2OHNH2+2CH3COOH
     >> #  Remove useless molecule:
     >> A2+B3=A3
     3A2=2A3
     >> (NH4)3PO4+Fe(NO3)2+NaCN+H2O=Fe(NH4)PO4.2H2O+NH4NO3
     (NH4)3PO4+Fe(NO3)2+2H2O=Fe(NH4)PO4.2H2O+2NH4NO3

  8) Equations with abbreviations (see docs/abbreviations/abbr_ref_book.pdf for more abbreviation labels):
     >> [Ph]OH+Na=C6H5ONa+H2
     2[Ph]OH+2Na=2C6H5ONa+H2
     >> [Et]OH+[AcOH]=CH3COOC2H5+H2O
     [Et]OH+[AcOH]=CH3COOC2H5+H2O

  9) Indefinite equations:
     >> K2MnO4;MnO2;O2;KMnO4
     2KMnO4=K2MnO4+MnO2+O2
     >> KMnO4;Cl2;MnCl2;HCl;KCl;H2O
     5Cl2+2MnCl2+2KCl+8H2O=2KMnO4+16HCl
     >> NH4NO3;(NH4)2Cr2O7;KNO3;K2Cr2O7
     2NH4NO3+K2Cr2O7=(NH4)2Cr2O7+2KNO3

Documents and unit tests are coming soon.