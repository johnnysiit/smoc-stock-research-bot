#Author: Tim Tang
def OMBDA_Grading(OMBDA): 
    if OMBDA <= 0.162:
        return 0
    elif 0.162 < OMBDA <= 0.167:
        return 1 
    elif 0.167 < OMBDA <= 0.172:
        return 1.5
    elif 0.172 < OMBDA <= 0.176:
        return 2
    elif 0.176 < OMBDA <= 0.18:
        return 2.5
    elif 0.18 < OMBDA <= 0.189:
        return 3
    elif 0.189 < OMBDA <= 0.198:
        return 3.5
    elif 0.198 < OMBDA <= 0.21:
        return 4
    elif 0.21 < OMBDA <= 0.2219:
        return 4.5
    elif 0.265 < OMBDA:
        return 5
    elif 0.2435 < OMBDA <= 0.265:
        return 5.5 
    elif 0.2219 < OMBDA <= 0.2435:
        return 6

def ROE_Grading(ROE):
    if ROE <= 0.087:
        return 0
    elif 0.087 < ROE <= 0.1055:
        return 1
    elif 0.1055 < ROE <= 0.124:
        return 1.5
    elif 0.124 < ROE <= 0.138:
        return 2
    elif 0.138 < ROE <= 0.152:
        return 2.5
    elif 0.152 < ROE <= 0.185:
        return 3
    elif 0.185 < ROE <= 0.218:
        return 3.5
    elif 0.218 < ROE <= 0.244:
        return 4
    elif 0.244 < ROE <= 0.2699:
        return 4.5
    elif 0.284 < ROE: 
        return 5
    elif 0.277 < ROE <= 0.284:
        return 5.5 
    elif 0.2699 < ROE <= 0.277:
        return 6

def EI_Grading(EI):
    if EI <= 1.4:
        return 0
    elif 1.4 < EI <= 2.4:
        return 1 
    elif 2.4 < EI <= 3.4:
        return 1.5
    elif 3.4 < EI <= 4.6:
        return 2
    elif 4.6 < EI <= 5.8:
        return 2.5
    elif 5.8 < EI <= 8.5:
        return 3
    elif 8.5 < EI <= 11.2:
        return 3.5
    elif 11.2 < EI <= 13.8:
        return 4
    elif 13.8 < EI <= 16.4:
        return 4.5
    elif 16.4 < EI <= 21.3:
        return 5
    elif 21.3 < EI <= 26.2:
        return 5.5 
    elif 26.2 < EI:
        return 6

def EIC_Grading(EIC):
    if EIC <= 2.3:
        return 0
    elif 2.3 < EIC <= 3.55:
        return 1 
    elif 3.55 < EIC <= 4.8:
        return 1.5
    elif 4.8 < EIC <= 6.3:
        return 2
    elif 6.3 < EIC <= 7.8:
        return 2.5
    elif 7.8 < EIC <= 10.65:
        return 3
    elif 10.65 < EIC <= 13.5:
        return 3.5
    elif 13.5 < EIC <= 16.5:
        return 4
    elif 16.5 < EIC <= 19.5:
        return 4.5
    elif 19.5 < EIC <= 25.75:
        return 5
    elif 25.75 < EIC <= 32:
        return 5.5
    elif 32 < EIC:
       return 6

def FCFTD_Grading(FCFTD):
    if FCFTD <= 0.115:
        return 0
    elif 0.115 < FCFTD <= 0.186:
        return 1 
    elif 0.186 < FCFTD <= 0.257:
        return 1.5
    elif 0.257 < FCFTD <= 0.306:
        return 2 
    elif 0.306 < FCFTD <= 0.355:
        return 2.5
    elif 0.355 < FCFTD <= 0.45:
        return 3
    elif 0.45 < FCFTD <= 0.545:
        return 3.5
    elif 0.545 < FCFTD <= 0.6685:
     return 4
    elif 0.6685 < FCFTD <= 0.792:
        return 4.5
    elif 0.792 < FCFTD <= 1.1735:
        return 5
    elif 1.1735 < FCFTD <= 1.555:
        return 5.5
    elif 1.555 < FCFTD:
        return 6

def DTE_Grading(DTE):
    if DTE >= 5.5:
        return 0
    elif 4.3 <= DTE < 5.5:
        return 1 
    elif 3.1 <= DTE < 4.3:
        return 1.5
    elif 2.65 <= DTE < 3.1:
        return 2
    elif 2.2 <= DTE < 2.65:
        return 2.5
    elif 1.85 <= DTE < 2.2:
        return 3
    elif 1.5 <= DTE < 1.85:
        return 3.5
    elif 1.2 <= DTE < 1.5:
        return 4
    elif 0.9 <= DTE < 1.2:
        return 4.5
    elif 0.65 <= DTE < 0.9:
        return 5
    elif 0.4 <= DTE <= 0.65:
        return 5.5
    elif DTE < 0.4:
        return 6
    
def DTDE_Grading(DTDE):
    if DTDE >= 0.732:
        return 0 
    elif 0.6285 <= DTDE < 0.732:
        return 1
    elif 0.525 <= DTDE < 0.6285:
        return 1.5
    elif 0.485 <= DTDE < 0.525:
        return 2
    elif 0.445 <= DTDE < 0.485:
        return 2.5
    elif 0.4065 <= DTDE < 0.445:
        return 3
    elif 0.368 <= DTDE < 0.4065:
        return 3.5
    elif 0.36 <= DTDE < 0.368:
        return 4
    elif 0.352<= DTDE < 0.36:
        return 4.5
    elif 0.2375<= DTDE < 0.352:
     return 5
    elif 0.123 <= DTDE < 0.2375:
        return 5.5
    elif DTDE < 0.123:
        return 6