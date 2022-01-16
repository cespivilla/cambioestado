
import math

def cambiospan(C1,DELTASPAN, unilist):
    
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






