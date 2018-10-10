    if (macro.Ident == 'M4_D_HIDDEN KTZ - FRAME' or macro.Ident == "Drain for Frame - hidden d BJM machining 4034"):  # Przerobić na wyszukiwanie z JSONA
        writeInc(file, str(inc * 10) + ';0;;XYZ;;' + str(
            Delta_X + macro.WX - 35 / 2 + frezWybrany['diameter'] / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';'  # 9.65 <- wyliczyć skąd, obrót, w innym miejscu makro?
                 + str(
            round(wysDisengage, 2)) + ';;\n')  # fi 8-6/2 , 13wys + 2.79zapasu, X - odwodnienie ma 35/2, frez d/2
        writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round((Delta_Z + frezWybrany['length'] - 37.03),
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  
        writeInc(file, str(inc * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(inc * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;Z;200;' + str(round(Delta_Z + frezWybrany['length'] - 49.03,
                                                              2)) + ';;;;\n')  # Praca w osi Z, zejście - póki co na twardo przyjęte - do przeliczenia.
        writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(
            Delta_X + macro.WX + 35 / 2 - frezWybrany['diameter'] / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';;;\n')
        writeInc(file, str(inc * 10) + ';97;9;;;;;;;\n')
        # Druga polowka
        writeInc(file, str(inc * 10) + ';0;;XYZ;;' + str(
            Delta_X + macro.WX - 35 / 2 + frezWybrany['diameter'] / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';'
                 + str(round(Delta_Z + frezWybrany['length'] - 49.03,
                             2)) + ';;\n')  # fi 8-6/2 , 13wys + 2.79zapasu, X - odwodnienie ma 35/2, frez d/2
        writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(Delta_Z + frezWybrany['length'] - 49.03 - 0.01,
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  0.01 zapasu? nie wiem po co
        writeInc(file, str(inc * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(inc * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;Z;200;' + str(round(Delta_Z + frezWybrany['length'] - 49.03 - 12.37,
                                                              2)) + ';;;;\n')  # Praca w osi Z, zejście - póki co na twardo przyjęte - do przeliczenia. 12.37 w glab
        writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(
            Delta_X + macro.WX + 35 / 2 - frezWybrany['diameter'] / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';;;\n')
        writeInc(file, str(inc * 10) + ';97;9;;;;;;;\n')
        # print(macro.Ident + ' - ' + str(macro.WX) + ' - ' + str(wysDisengage))