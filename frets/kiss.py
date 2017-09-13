#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Jul 15, 2016

@author: sgemme
@modif: jLevesque
'''

#Déclaration des caractères spéciaux de Kiss
FEND=0xC0
FESC=0XDB
TFEND=0xDC
TFESC=0xDD


def toKiss(bytes):
    '''
    Prend en argument un objet de type string ou bytearray
    et rajoute les caractères de délimitations Kiss pour 
    un flux de données asynchrones 
    '''
    
    #Si on reçoit une string on la transforme en byte array
    bytes = bytearray(bytes)
    
    #On crée la nouvelle matrice de bytes 'res' transposée en Kiss
    res = bytearray()
    
    for b in bytes:
        
        #Si on a le caractère spécial dans les datas on fait un escape et on rajoute un transpose
        if b == FEND:
            res.extend([FESC,TFEND])
            
        elif b == FESC:
            
             res.extend([FESC,TFESC])
                          
        else:
            res.append(b)
    
    #on insert le délimiteur FEND au début de la trame/matrice de bytes (as per KISS protocol)
    res.insert(0, FEND)
    
    #on insert le délimiteur FEND à la fin de la trame/matrice de bytes (as per KISS protocol)
    res.append(FEND)
     
    return res

def fromKiss(bytes):
    
    #variable permettant de voir des bytes subséquents dans l'array
    index = 0
    
    #On crée la nouvelle matrice de bytes 'res' transposée en byte Array de Kiss     
    res = bytearray()
    
    try:
        #On enlève les FEND de début et de fin de trame
        bytes.pop() == FEND    
        bytes.pop(0)== FEND
        
    except:
            print("Error on Array")   
    
    for b in bytes:
        
        if b == FESC:
            
            #Si le prochain byte est un caractère transposé TFEND
            if bytes[index +1] == TFEND:
                res.append(FEND)
                index += 1
                
            #Si le prochain byte est un caractère transposé TFESC    
            elif bytes[index +1] == TFESC:
                res.append(FESC)
                index += 1
        
        #Si le caractère n'est pas spécial on append normalement                
        elif b!= TFEND and b!= TFESC:
            res.append(b)
            index +=1
        
        
        else:
            index +=1
                               
    return res


#Petite démo
'''if __name__ == '__main__':

    arr = bytearray([FEND, 0x01, FESC])
    
    arr = toKiss(arr)
    
    print(repr(arr))
    
    arr = fromKiss(arr)
    
    print(repr(arr))
    
    pass'''