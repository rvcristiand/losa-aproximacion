from docxtpl import DocxTemplate

if __name__ == "__main__":
    doc = DocxTemplate("DISEÑO DE LA LOSA DE APROXIMACION DEL PUENTE.docx")

    context = {'nombre': "Puente El Portillo"}

    context ['departamento'] = "Cesar"
    context ['municipio'] = "San Martín"
    context ['coordenadas'] = "7°59'57.2\"N 73°30'57.6\"W"
    
    # Resistencia del Concreto
    fc = 28
    context['fc'] = fc 
   
    # Resistecia del Acero
    fy = 420
    context['fy'] = fy
   
    #Dimensiones del Puente
    L = 5 
    context['L'] = L
    
    ancho_de_carril = 3.6
    context['ancho_de_carril'] = ancho_de_carril

    ancho_de_berma = 1.4
    context['ancho_de_berma'] = ancho_de_berma

    ancho_de_anden = 0
    context['ancho_de_anden'] = ancho_de_anden

    espesor_de_carpeta_asfaltica = 0.08
    context['espesor_carpeta_asfaltica'] = espesor_de_carpeta_asfaltica

    ancho_inferior_de_barrera = 0.0
    context['ancho_inferior_de_barrera'] = ancho_inferior_de_barrera

    ancho_superior_de_barrera = 0.0
    context['ancho_superior_de_barrera'] = ancho_superior_de_barrera
    
    altura_de_barrera = 0.0
    context['altura_de_barrera'] = altura_de_barrera
    
    num_carriles = 2
    
    ancho_total = round((((ancho_de_carril *num_carriles / 2 )+ ancho_de_berma + ancho_de_anden + ancho_inferior_de_barrera) * 2),2)
    context['ancho_total'] = ancho_total

    

    #Altura de la losa
    h = round(((1.2 * ( L + 3)) / 30),2)
    context['h'] = h

    #ancho de franja equivalente
    if ancho_total < 9 :
        
        anchofreq_uncarril = ancho_total
        
    else : anchofreq_uncarril = 9 
    
    if L < 18 :
        
        luzfreq_uncarril = L
        
    else : luzfreq_uncarril = 18 

    E_un_carril = round((0.25 + 0.42 * ( anchofreq_uncarril * luzfreq_uncarril ) ** 0.5),2)

    if E_un_carril > (ancho_total/num_carriles) :
        E_un_carril = (ancho_total/num_carriles)
    
    if ancho_total < 18 :
        
        anchofreq_doscarriles = ancho_total
        
    else : anchofreq_doscarriles = 18

    E_dos_carriles = round((2.1 + 0.12 * ( anchofreq_doscarriles * luzfreq_uncarril ) ** 0.5),2)
    
    if E_dos_carriles > (ancho_total/num_carriles) :
        E_dos_carriles = (ancho_total/num_carriles)
    
    if E_un_carril < E_dos_carriles :
        
        E_tomado = E_un_carril
        
    else : E_tomado = E_dos_carriles

    context['E_un_carril'] = E_un_carril
    context['E_dos_carriles'] = E_dos_carriles
    context['E_tomado'] = E_tomado
    
    espesor_relleno = context['espesor_relleno'] = context.get('espesor_relleno', 0.6)

    #Solicitaciones
    #Por carga muerta
    # pesos especificos en kN/m3
    pespecifico_concreto = 2.4 * 9.81
    pespecifico_carpeta_asfaltica = 2.2 * 9.81
    pespecifico_relleno = 1.8 * 9.81

    # Cargas distrbuidas muertas
    DC = pespecifico_concreto * h
    DW = round ((pespecifico_carpeta_asfaltica * espesor_de_carpeta_asfaltica),2)
    DEV = round(pespecifico_relleno * espesor_relleno, 2)
    
    context['pespecifico_carpeta_asfaltica'] = round(pespecifico_carpeta_asfaltica)
    context['pespecifico_concreto'] = round(pespecifico_concreto)
    context['DC'] = DC
    context['DW'] = DW
    context['DEV'] = DW
    
    #Momentos máximos
    # Cargas Permanentes
    # Unidades en kN/m
    MDC = round(((DC * L ** 2 / 8) ))
    MDW = round(((DW * L ** 2 / 8) ))
    MDEV = round(((DEV * L ** 2 / 8) ))
    context['MDC'] = MDC
    context['MDW'] = MDW
    context['MDEV'] = MDEV
    
    #Momento máximo debido al camión de diseño (360 kN) # Ecuación válida para luces mayores de 10.04 m 

    MAcamion = 360 / L * (L / 2 + 0.717) ** 2 - 688
    context['MACamion'] = MAcamion

    # Momento máximo debido al tandem de diseño (250 kN) # Ecuación válida para luces mayores de 1.8 m 
    Mtandem = round(250 / L * ( L / 2 + 0.3) ** 2 - 150)
    context['Mtandem'] = Mtandem

    if Mtandem > MAcamion:
        Mcviva = Mtandem
    else : Mcviva = MAcamion
    
    #Momento máximo debido al carril de diseño (10.33 kN/m)
    Mcarril = round(10.3 * L **2 / 8)
    context['Mcarril'] = Mcarril
    #Momento maximo debido a la carga vehicular de diseño con amplificación dinámica

    MLLIM = round(1.33 * Mcviva + Mcarril)
    context['MLLIM'] = MLLIM
    
    #Momento por carga viva por metro de ancho de franja equivalente

    MLLIMafequiv = round(MLLIM / E_tomado)
    context['MLLIMafequiv'] = MLLIMafequiv
    
    #Diseño a Flexión
    #Factores de modificación de carga 1.3.2
    #Factor relacionado con la ductilidad
    factor_ductilidad = 1

    #Factor relacionado con la redundancia
    factor_redundancia = 1

    #Factor relacionado con la importancia operativa
    factor_imp_operativa = 1

    factor_mod_carga = factor_ductilidad *  factor_imp_operativa * factor_redundancia
    context['factor_mod_carga'] = factor_mod_carga

    # Momento ultimo
    Mu = factor_mod_carga * ( 1.25 * MDC + 1.5 * MDW +1.35 * MDEV + 1.75 * MLLIMafequiv )
    Mu_tonm = Mu / 9.81
    context['Mu'] = Mu

    # Recubrimiento de armadura principal no protegida TAbla 5.12.3.1
    recub = 0.09
    # factor phi para diseño a flexión
    phi = 0.9
    d = h - recub
    context['d'] = d 

    K = round (Mu_tonm / (1 * d ** 2),1)
    context['K'] = K

    #cuantía de acero
    cuantia = round(0.0567 * (1 - ( 1- (35.3 * K / 37800)) ** 0.5 ), 5)
    context['cuantia'] = cuantia 

    cuantia_kN = round(( 1 - ( 1 - ( 2 * Mu / ( phi * 1 * d ** 2 * 0.85 * fc * 1000 ) ) ) ** 0.5 ) * 0.85 * fc /  fy, 5)  
    context['cuantia_kN'] = cuantia_kN

    #Area de refuerzo de la losa en cm2
    As_flexion = round(cuantia_kN * d * 100 * 100, 2)
    context['As_flexion'] = As_flexion

    #Para barras #8 As = 5.1 cm2
    As_8 = 5.1 # definir al inicio
    No_barras_8_flexion = round(As_flexion / As_8)
    context['No_barras_8_flexion'] = No_barras_8_flexion
    context['As_8'] = As_8

    #Espaciamiento Armadura a flexión
    espac_arm_prin_flexion = round (100 / No_barras_8_flexion)
    context['espac_arm_prin_flexion'] = espac_arm_prin_flexion

    # Revisión del factor phi = 0.9 para el diseño a flexión

    a_f = round(cuantia * d * fy /( 0.85 * fc), 4)
    context['a_f'] = a_f
    #profundidad eje neutro

    betha_1 = 0.85
    c_f = round(a_f / betha_1 , 4) 
    context['c_f'] = c_f
    #Relacion de  deformaciones en la sección de concreto reforzado

    defor_total = round((d - c_f) * (0.003 / c_f), 4)  
    context['defor_total'] = defor_total
    #Armadura dedistribución para losas con armadura principal paralela a la dirección del trafico (9.7.3.2)

    Armadura_de_distribucion = 55 / (L) ** 0.5 / 100
    context['Armadura_de_distribucion'] = Armadura_de_distribucion

    As_4 = 1.29
    As_Armadura_de_distribucion = round ( Armadura_de_distribucion * As_flexion , 2)
    context['As_Armadura_de_distribucion'] = As_Armadura_de_distribucion

    No_barras_4_dist =  round( As_Armadura_de_distribucion / As_4 )
    context['No_barras_4_dist'] = No_barras_4_dist

    espac_arm_dist = round( 100 / No_barras_4_dist )
    context['espac_arm_dist'] = espac_arm_dist

    #Armadura minima
    #Modulo de rotura del concreto
    fr = round(0.62 * fc ** 0.5, 2)
    context['fr'] = fr 
    # factor de variacion de l afisuracion por flexion 5.7.3.3.2 
    gamma_1 = 1.6

    #relacion entre la reistencia especificada a fluencia y la resistencia ultima atracción del refuerzo
    #refuerzo a706, Grado 60
    gamma_3 = 0.75

    #Modulo elastico de la seccion

    Sc = round(1 * h ** 2 / 6, 4 )
    context['Sc'] = Sc

    Mcr = round (gamma_1 ** 2 * gamma_3 * fr * Sc * 1000)
    context['Mcr'] = Mcr

    if Mcr > Mu :
        print ('No cumple Armadura mínima')
    
    # Control de fisuración
    # Factor de exposición clase 1. 5.7.3.4 
    gamma_e = 1.0

    #De acuerdo con 5.12.3-1, el espesor de recubrimiento de concreto medido desde la fibra extrema a tracción hasta el centro del refuerzo de flexión mas cercano, para losas vaciadas in situ 25 mm

    d_c = 0.025 + 0.0254 / 2

    if d_c < 0.050 : 
        d_c = 0.050

    #De acuerdo con el Art 5.7.3.4, el coeficiente beta s 
    beta_s = round (1 + d_c / (0.7 * (h - d_c)), 3)
    context['beta_s'] = beta_s

    #Calculo de fss: Esfuerzo actuante a tracción en el acero para estado limite de servicio I
    
    #Combinación para el estado limite de servicio tabla 3.4.1
    Msi = 1 * (MDC + MDW +MDEV +MLLIMafequiv)
    context['Msi'] = Msi

    # Modulo de elasticidad del concreto - densidad normal MPa

    E_concreto = round(0.043 * 2320 ** 1.5 * (fc) ** 0.5, 2)
    context['E_concreto'] = E_concreto

    # Modulo de elasticidad del acero MPa
    
    E_acero = 200000

    #Relación modular

    rel_mod = round(E_acero / E_concreto)
    context['rel_mod'] = rel_mod

    #Momento de primer orden de la sección  fisurada, de 1m de ancho, con respecto al eje neutro

    #Tomando momentos con respecto al eje neutro de la sección:

    X_cf = round (( -(2 * rel_mod * As_flexion * 10 ** -4) + ((2 * rel_mod * As_flexion * 10 ** -4 ) ** 2 - (4 * 1 * -2 * rel_mod * As_flexion * 10 ** -4 * d )) ** 0.5 ) / (2 * 1), 2)
    context['X_cf'] = X_cf
    
    # Momento de inercia de la seccion fisurada

    I_c = round(X_cf ** 3 / 3 + rel_mod * As_flexion * 10 ** -4 * (d - X_cf) ** 2, 8)
    context['I_c'] = I_c

    fss = round (rel_mod * Msi * (d - X_cf) / I_c / 1000, 2)
    context['fss'] = fss

    # Reemplazando en la ecuación 5.7.3.4.1
    
    espac_control_fisuracion = round((123000 * gamma_e / (beta_s * fss) ) - (2 * d_c * 1000))
    context['espac_control_fisuracion'] = espac_control_fisuracion /10

    if espac_control_fisuracion / 100 > espac_arm_prin_flexion :
        print ('No cumple control de fisuración')

    # Separacion centro a centro de barras 
    diametro_barra_8 = 2.54
    espac_libre = espac_arm_prin_flexion - diametro_barra_8 
    context['espac_libre'] = espac_libre

    # Espaciamiento minimo de la armadura vaciada in situ 5.10.3 
    
    #tamaño agregado 3/4in en cm
    tamaño_agregado = 1.905

    if espac_libre < 1.5 * diametro_barra_8 :
        print ('No cumple espaciamineto minimo 5.10.3')
    if espac_libre < 1.5 * tamaño_agregado :
        print ('No cumple espaciamineto minimo 5.10.3')
    if espac_libre < 3.8 :
        print ('No cumple espaciamineto minimo 5.10.3')

    #Armadura por retraccion de fraguado y temperatura
    As_retytemp = round(750 * ancho_total * h / (2 * (ancho_total + h) * fy) * 1000)

    if 234 > As_retytemp :
        print ('No cumple Retraccion y Temperatura')
    if  As_retytemp > 1278:
        print ('No cumple Retraccion y Temperatura') 
    context['As_retytemp'] = As_retytemp
    As_3 = context['As_3'] = 0.71
    No_barras_3_retytemp = round (As_retytemp /100 / As_3, 2) 
    context ['No_barras_3_retytemp'] = No_barras_3_retytemp

    espa_arm_retytemp = round(100 / No_barras_3_retytemp)
    context['espa_arm_retytemp'] = espa_arm_retytemp
    h3 = 3 * h
    context['h3'] = h3 
    

    ##Verificación por fatiga
    # De acuerdo con 3.6.1.4.1 la carga de fatiga debe ser el camion de diseño 360 kN con un espaciamiento constante de 9 m entre ejes

    # Factor de carga especificado en 3.4.1-1 para la combinacion de carga de fatiga
    gamma_fatiga = context['gamma_fatiga'] = 1.5

    #MLL+IM Fatiga, camion de diseño kN

    if L > 14.48 :
        MLLIM_fatiga = round(1.15 * (360/L * (L/2 + 1.76) ** 2) - 1440, 2)
    else :
        print('ingrese valor de MLLIM_fatiga')
        MLLIM_fatiga = 230

    anchofreq_uncarril_fatiga = context['anchofreq_uncarril_fatiga'] = E_un_carril / 1.2
    MLLIM_fatiga_fraequiv = context['MLLIM_fatiga_fraequiv'] = round(MLLIM_fatiga / anchofreq_uncarril_fatiga)

    #Momento seccion no fisurada
    Mseccion_fisurada = context['Mseccion_fisurada'] = round(MDC + MDW+ MDEV + 1.5 * MLLIM_fatiga_fraequiv)

    # esfuerzo actuante seccion no fisurada

    Y_inf = h / 2
    I_seccion = 1 * h ** 3 / 12
    f_c_nofisurado = context['f_c_nofisurado'] = round(Mseccion_fisurada * Y_inf / (I_seccion) /1000)
    jd = d - X_cf/3

    condicion_esf_seccion_fisurada = round(0.25 * (fc) ** 0.5,1)
    if f_c_nofisurado > condicion_esf_seccion_fisurada :
        deltaf = MLLIM_fatiga_fraequiv / ( As_flexion * 10 ** -4 * jd)
    context['condicion_esf_seccion_fisurada'] = condicion_esf_seccion_fisurada
    
    #verificacion de esfuerzos sobre la seccion fisurada

    f_seccion_fisurada = context['f_seccion_fisurada'] = round(gamma_fatiga * deltaf /1000)

    #Esfuerzo minimo debido a la carga viva que resulta de la combinacion de carga de fatiga I,combinado con el esfuerzo mas severo de cargas permanentes
    #El minmo esfuerzo sobre el acero de refuerzo se produce cuando no actua carga viva
    f_min = context['f_min'] = round((MDC + MDW + MDEV) / (As_flexion * 10 ** -4 *jd) /1000)

    deltaF_TH = context['deltaF_TH'] = round(166 - 0.33 * f_min)

    if f_seccion_fisurada > deltaF_TH :
        print ('No cumple verificación por fatiga')
    
    print (f_seccion_fisurada,f_min, deltaF_TH, jd, X_cf, As_flexion)

    
    

    doc.render(context)

    doc.save("{}.docx".format('Losa de aproximacion - ' + context['nombre']))
