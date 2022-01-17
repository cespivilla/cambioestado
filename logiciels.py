
import math

# PROGRAMA "cambiospan" CALCULO MECANICO DEL CONDUCTOR       CEV 2021/09
# DE UN VANO AISLADO (VANO ENTRE PORTICOS SUBESTACIONES O
# VANOS FLOJOS EN LINEAS) CUYA LONGITUD DE VANO VARIA
# TOMA EN CUENTA EL PEQUEÑO GIRO DE LAS CADENAS DE ANCLAJE LO QUE EQUALIZA EL TENSE
# PROGRAMA SOLO VALIDO PARA ACSR 412 mm2, 1.62 kg/m, VANO 450 m **************

def cambiospan(C1,DELTASPAN):

    unilist = []
    
    def equi(C, DSPAN, SPANC, PG1C, PG2C, DIFSPAN, ACPIG, ACPDG, COT1C, DESNC):
        
        while abs(DIFSPAN) > 0.005:

            SPAN0 = SPANC

            PG0C = PG1C + SPANC * 0.5

            WC1 = C * math.sinh((PG0C - PG1C) / C) * 1.62
            WC2 = C * math.sinh((PG2C - PG0C) / C) * 1.62

            ACPI = math.atan((WC1 + 35.0) / (C * 1.62))
            ACPD = math.atan((WC2 + 35.0) / (C * 1.62))

            PG1C = 2.1 * math.cos(ACPI)
            PG2C = 450.0 + DSPAN - 2.1 * math.cos(ACPD)

            COT1C = 100.0 - 2.1 * math.sin(ACPI)
            COT2C = 100.0 - 2.1 * math.sin(ACPD)

            SPANC = PG2C - PG1C
            DESNC = COT2C - COT1C

            DIFSPAN = SPANC - SPAN0

        ACPIG = ACPI * 180 / 3.1415926
        ACPDG = ACPD * 180 / 3.1415926

        return SPANC, PG1C, PG2C, DIFSPAN, ACPIG, ACPDG, DESNC, COT1C
    
    unilist.append(' RESULTADOS')
    unilist.append(' ')
    unilist.append(' MODULO ELAST.(kg/mm2)=  8300')
    unilist.append(' SECCION(mm2)= 412  MASA(Kg/m)=  1.62')
    unilist.append(' ')
    unilist.append(' ------------------------------------------------------------------------------')
    unilist.append(' ESTADO 1   PARAMETRO DE TENSADO (m)= '+ str(C1))
    unilist.append(' PROGRESIVA PORTICO IZQUIERDO(m):  0     COTA PORTICO IZQUIERDO(m):  100')
    unilist.append(' PROGRESIVA PORTICO DERECHO(m):    450   COTA PORTICO DERECHO(m):    100')
    unilist.append(' LONGITUD DE CADENA(m):            2.1   PESO DE CADENA(kgf):        70.0')
    unilist.append(' NUMERO DE SUB-CONDUCTORES:        1')
    unilist.append(' ')

    SPANC = 450.0
    PG1C = 0.0
    PG2C = 450.0
    DIFSPAN = 1.0
    ACPIG = 0
    ACPDG = 0
    COT1C = 0
    DESNC = 0
    SPANC, PG1C, PG2C, DIFSPAN, ACPIG, ACPDG, DESNC, COT1C = equi(C1, 0, SPANC, PG1C, PG2C, DIFSPAN, ACPIG, ACPDG, COT1C, DESNC)
    # Progresiva punto mas bajo
    PG0C = PG1C + SPANC * 0.5

    # Cota punto mas bajo del conductor
    CPMB = COT1C - C1 * (math.cosh((PG0C - PG1C) / C1) - 1)

    unilist.append(' PARAMETROS EN EQUILIBRIO ESTADO INICIAL')
    unilist.append(' ')
    unilist.append(' ANGULO CADENA PUNTO IZQUIERDO(grados):   '+str(ACPIG)+' ANGULO CADENA PUNTO DERECHO(grados): '+str(ACPDG))
    unilist.append(' PROGRESIVA CONDUCTOR PUNTO IZQUIERDO(m): '+str(PG1C))
    unilist.append(' PROGRESIVA CONDUCTOR PUNTO DERECHO(m):   '+str(PG2C))
    unilist.append(' VANO SOLO CONDUCTOR(m):                  '+str(SPANC))
    unilist.append(' TENSE HORIZONTAL CONDUCTOR(kgf):         '+str(1.62 * C1))
    unilist.append(' PROGRESIVA PUNTO MAS BAJO CONDUCTOR(m):  '+str(PG0C))
    unilist.append(' COTA PUNTO MAS BAJO DEL CONDUCTOR(m):    '+str(CPMB))

    L1 = 2 * C1 * math.sqrt((math.sinh(SPANC / 2 / C1)) ** 2 + (DESNC / 2 / C1) ** 2)

    unilist.append(' LONGITUD INICIAL CATENARIA(m):           '+str(L1))

    C2 = C1
    DIFSPAN = 1.0


    SPANC, PG1C, PG2C, DIFSPAN, ACPIG, ACPDG, DESNC, COT1C = equi(C2, DELTASPAN, SPANC, PG1C, PG2C, DIFSPAN, ACPIG, ACPDG, COT1C, DESNC)

    L2 = 2 * C2 * math.sinh(SPANC / 2 / C2)

    MISMATCH0 = L2 - L1 - L1 * (C2 - C1) / 2110864.198

    C0 = C2
    if DELTASPAN < 0:
        C2 = C1 * 0.95
    else:
        C2 = C1 * 1.05
   

    MISMATCH2 = 1.0

    while abs(MISMATCH2) > 0.0001:

        DIFSPAN = 1.0

        SPANC, PG1C, PG2C, DIFSPAN, ACPIG, ACPDG, DESNC, COT1C = equi(C2, DELTASPAN, SPANC, PG1C, PG2C, DIFSPAN, ACPIG, ACPDG, COT1C, DESNC)

        L2 = 2 * C2 * math.sinh(SPANC / 2 / C2)

        MISMATCH2 = L2 - L1 - L1 * (C2 - C1) / 2110864.198

        CTEMP = C2

        C2 = C0 - MISMATCH0 / ((MISMATCH2 - MISMATCH0) / (C2 - C0))
        if C2 < 0:
            if DELTASPAN < 0:
                C2 = CTEMP * 0.95
            else:
                C2 = CTEMP * 1.05
            
        
        C0 = CTEMP
        MISMATCH0 = MISMATCH2
    

    # Progresiva punto mas bajo
    PG0C = PG1C + SPANC * 0.5 - C2 * DESNC / SPANC

    # Cota punto mas bajo del conductor
    CPMB = COT1C - C2 * (math.cosh((PG0C - PG1C) / C2) - 1)


    unilist.append(' ')
    unilist.append(' ')
    unilist.append(' ------------------------------------------------------------------------------')
    unilist.append(' ESTADO 2    ')
    unilist.append(' NUEVA PROGRESIVA PORTICO DERECHO(m):   '+ str(450 + DELTASPAN))
    unilist.append(' ')
    unilist.append(' PARAMETROS EN EQUILIBRIO CON CAMBIO DE ESTADO')
    unilist.append(' ')
    unilist.append(' ANGULO CADENA PUNTO IZQUIERDO(°):        '+ str(ACPIG)+ ' ANGULO CADENA PUNTO DERECHO(°): '+ str(ACPDG))
    unilist.append(' PROGRESIVA CONDUCTOR PUNTO IZQUIERDO(m): '+ str(PG1C))
    unilist.append(' PROGRESIVA CONDUCTOR PUNTO DERECHO(m):   '+ str(PG2C))
    unilist.append(' VANO SOLO CONDUCTOR(m):                  '+ str(SPANC)+ ' DESNIVEL SOLO CONDUCTOR(m): '+ str(DESNC))
    unilist.append(' PARAMETRO CATENARIA(m):                  '+ str(C2))
    unilist.append(' TENSE HORIZONTAL CONDUCTOR(kgf):         '+ str(1.62 * C2))
    unilist.append(' PROGRESIVA PUNTO MAS BAJO CONDUCTOR(m):  '+ str(PG0C))
    unilist.append(' COTA PUNTO MAS BAJO DEL CONDUCTOR(m):    '+ str(CPMB))
    unilist.append(' ')
    unilist.append(' ')
    unilist.append(' EL TENSE HORIZONTAL CONDUCTOR ES POR UN CONDUCTOR')

    return unilist





# PROGRAMA 'SOLOSPAN' CALCULO MECANICO DEL CONDUCTOR       CEV 2021/06
# DE UN VANO AISLADO (VANO ENTRE PORTICOS SUBESTACIONES O
# VANOS FLOJOS EN LINEAS) TOMA EN CUENTA EL PEQUEÑO GIRO DE LAS CADENAS DE ANCLAJE LO QUE EQUALIZA EL TENSE

def solospan(sesion):

    S = float(sesion[0])
    DIA = float(sesion[1])
    W = float(sesion[2])
    E = float(sesion[3])
    ALFA = float(sesion[4])
    TEMP1 = float(sesion[5])
    C1 = float(sesion[6])
    TEMP2 = float(sesion[7])
    PV2 = float(sesion[8])
    EH = float(sesion[9])
    DEICE = float(sesion[10])
    PG1 = float(sesion[11])
    COT1 = float(sesion[12])
    PG2 = float(sesion[13])
    COT2 = float(sesion[14])
    LCAD = float(sesion[15])
    PCAD = float(sesion[16])
    NSUB = int(sesion[17])

    unilist = []
    
    
    def equi(PGI, COTI, PGD, COTD, W, C, NSUBC, PSTR, LSTR, SPANC, DESNC, PG1C, PG2C, DIFSPAN):
        
        while abs(DIFSPAN) > 0.005:
            
            SPAN0 = SPANC
            PG0C = PG1C + SPANC * 0.5 - C * DESNC / SPANC
            
            WC1 = C * math.sinh((PG0C - PG1C)/C) * W * NSUBC
            WC2 = C * math.sinh((PG2C - PG0C) / C) * W * NSUBC
            
            ACPI = math.atan((WC1 + PSTR * 0.5)/(C * W * NSUBC))
            ACPD = math.atan((WC2 + PSTR * 0.5)/(C * W * NSUBC))
            
            PG1C = PGI + LSTR * math.cos(ACPI)
            PG2C = PGD - LSTR * math.cos(ACPD)
            
            COT1C = COTI - LSTR * math.sin(ACPI)
            COT2C = COTD - LSTR * math.sin(ACPD)

            SPANC = PG2C - PG1C
            DESNC = COT2C - COT1C

            DIFSPAN = SPANC - SPAN0

        ACPIG = ACPI * 180 / 3.1415926
        ACPDG = ACPD * 180 / 3.1415926
        
        return PG0C, PG1C, PG2C, COT1C, SPANC, DESNC, ACPIG, ACPDG


    unilist.append('RESULTADOS')
    unilist.append(' ')

    unilist.append(' COEF. DILAT. LINEAL( 1/oC )= '+ str(ALFA) + '  MODULO ELAST.(kg/mm2)='+ str(E))
    unilist.append(' SECCION(mm2)= '+ str(S) + '  DIAMETRO(mm)= '+ str(DIA)+ '  MASA(Kg/m)= '+ str(W))

    unilist.append(' ')
    unilist.append(' ------------------------------------------------------------------------------')
    unilist.append(' ESTADO 1   PARAMETRO DE TENSADO (m)= '+ str(C1) + 'TEMP(oC)= '+ str(TEMP1))
    unilist.append(' PROGRESIVA PORTICO IZQUIERDO(m): ' + str(PG1) + ' COTA PORTICO IZQUIERDO(m): '+ str(COT1))
    unilist.append(' PROGRESIVA PORTICO DERECHO(m):   ' + str(PG2) + ' COTA PORTICO DERECHO(m):   '+ str(COT2))
    unilist.append(' LONGITUD DE CADENA(m):           ' + str(LCAD) + ' PESO DE CADENA(kgf): '+ str(PCAD))
    unilist.append(' NUMERO DE SUB-CONDUCTORES:       ' + str(NSUB))
    unilist.append(' ')

    W1 = W

    PH = DEICE * 3.1415926 / 1000 * (EH ** 2 + EH * DIA)

    W2 = math.sqrt((W + PH) ** 2 + (PV2 * (DIA + 2 * EH) / 1000) ** 2)

    SPANC = PG2 - PG1
    DESNC = COT2 - COT1
    PG1C = PG1
    PG2C = PG2
    DIFSPAN = 1.0


    PG0C, PG1C, PG2C, COT1C, SPANC, DESNC, ACPIG, ACPDG = equi(PG1, COT1, PG2, COT2, W1, C1, NSUB, PCAD, LCAD, SPANC, DESNC, PG1C, PG2C, DIFSPAN)

    # Progresiva punto mas bajo
    PG0C = PG1C + SPANC * 0.5 - C1 * DESNC / SPANC

    # Cota punto mas bajo del conductor
    CPMB = COT1C-C1*(math.cosh((PG0C-PG1C)/C1)-1)

    unilist.append(' PARAMETROS EN EQUILIBRIO ESTADO INICIAL')
    unilist.append(' ')
    unilist.append(' ANGULO CADENA PUNTO IZQUIERDO(grados):   '+ str(ACPIG) + ' ANGULO CADENA PUNTO DERECHO(grados): '+ str(ACPDG))
    unilist.append(' PROGRESIVA CONDUCTOR PUNTO IZQUIERDO(m): '+ str(PG1C))
    unilist.append(' PROGRESIVA CONDUCTOR PUNTO DERECHO(m):   '+ str(PG2C))
    unilist.append(' VANO SOLO CONDUCTOR(m):                  '+ str(SPANC) + ' DESNIVEL SOLO CONDUCTOR(m): '+ str(DESNC))
    unilist.append(' TENSE HORIZONTAL CONDUCTOR(kgf):         '+ str(W1 * C1))
    unilist.append(' PROGRESIVA PUNTO MAS BAJO CONDUCTOR(m):  '+ str(PG0C))
    unilist.append(' COTA PUNTO MAS BAJO DEL CONDUCTOR(m):    '+ str(CPMB))

    L1 = 2 * C1 * math.sqrt((math.sinh(SPANC/2/C1)) ** 2+(DESNC/2/C1) ** 2)

    C2 = C1
    DIFSPAN = 1.0


    PG0C, PG1C, PG2C, COT1C, SPANC, DESNC, ACPIG, ACPDG = equi(PG1, COT1, PG2, COT2, W2, C2, NSUB, PCAD, LCAD, SPANC, DESNC, PG1C, PG2C, DIFSPAN)

    L2 = 2 * C2 * math.sqrt((math.sinh(SPANC/2/C2)) ** 2+(DESNC/2/C2) ** 2)

    MISMATCH0 = L2 - L1 - L1 * (ALFA*(TEMP2-TEMP1)+(C2 * W2 - C1 * W1)/E/S)

    C0 = C2
    C2 = C1 * 1.05

    MISMATCH2 = 1.0

    while abs(MISMATCH2) > 0.0001:
        

        DIFSPAN = 1.0

        PG0C, PG1C, PG2C, COT1C, SPANC, DESNC, ACPIG, ACPDG = equi(PG1, COT1, PG2, COT2, W2, C2, NSUB, PCAD, LCAD, SPANC, DESNC, PG1C, PG2C, DIFSPAN)

        L2 = 2 * C2 * math.sqrt((math.sinh(SPANC/2/C2)) ** 2+(DESNC/2/C2) ** 2)

        MISMATCH2 = L2 - L1 - L1 * (ALFA*(TEMP2-TEMP1)+(C2 * W2 - C1 * W1)/S/E)

        CTEMP = C2

        C2 = C0 - MISMATCH0 / ((MISMATCH2 - MISMATCH0) / (C2 - C0))

        C0 = CTEMP
        MISMATCH0 = MISMATCH2


    # Progresiva punto mas bajo
    PG0C = PG1C + SPANC * 0.5 - C2 * DESNC / SPANC

    # Cota punto mas bajo del conductor
    CPMB = COT1C-C2*(math.cosh((PG0C-PG1C)/C2)-1)


    unilist.append(' ')
    unilist.append(' ')
    unilist.append(' ------------------------------------------------------------------------------')
    unilist.append(' ESTADO 2   TEMP(oC)= '+ str(TEMP2) + '  PRESION DEL VIENTO(kg/m2) '+ str(PV2))
    unilist.append('            ESP.HIELO(mm) '+ str(EH) + '  DENSIDAD HIELO(gr/cm3)= '+ str(DEICE ))
    unilist.append(' ')
    unilist.append(' PARAMETROS EN EQUILIBRIO CON CAMBIO DE ESTADO')
    unilist.append(' ')
    unilist.append(' ANGULO CADENA PUNTO IZQUIERDO(°):        '+ str(ACPIG) + ' ANGULO CADENA PUNTO DERECHO(°): '+ str(ACPDG))
    unilist.append(' PROGRESIVA CONDUCTOR PUNTO IZQUIERDO(m): '+ str(PG1C))
    unilist.append(' PROGRESIVA CONDUCTOR PUNTO DERECHO(m):   '+ str(PG2C))
    unilist.append(' VANO SOLO CONDUCTOR(m):                  '+ str(SPANC) + ' DESNIVEL SOLO CONDUCTOR(m): '+ str(DESNC))
    unilist.append(' PARAMETRO CATENARIA(m):                  '+ str(C2))
    unilist.append(' TENSE HORIZONTAL CONDUCTOR(kgf):         '+ str(W2 * C2))
    unilist.append(' PROGRESIVA PUNTO MAS BAJO CONDUCTOR(m):  '+ str(PG0C))
    unilist.append(' COTA PUNTO MAS BAJO DEL CONDUCTOR(m):    '+ str(CPMB))
    unilist.append(' ')
    unilist.append(' ')
    unilist.append(' EL TENSE HORIZONTAL CONDUCTOR ES POR UN CONDUCTOR')
    unilist.append(' PARA EL TENSE TOTAL CONSIDERAR EL NUMERO DE SUB-CONDUCTORES')

    return unilist



        



