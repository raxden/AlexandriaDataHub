#!/usr/bin/env python3
"""
Scraper para obtener el Euribor diario desde helpmycash.com
NOTA: Esta web carga el contenido dinámicamente con JavaScript
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Tuple, Union
import re


def fetch() -> Tuple[str, Union[float, str], str, bool]:
    """
    Intenta obtener el Euribor del día desde helpmycash.com
    
    Returns:
        Tupla (fecha, valor_o_error, fuente, éxito)
        - Si éxito=True: valor_o_error es float
        - Si éxito=False: valor_o_error es string con el error
    """
    source_name = "helpmycash.com"
    try:
        print(f"Intentando obtener datos de {source_name}...")
        url = "https://www.helpmycash.com/hipotecas/euribor-actual/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar el texto completo de la página
        text = soup.get_text()
        
        # Intentar varios patrones para encontrar el valor del Euribor
        patterns = [
            r'El euríbor hoy tiene un valor diario del\s+(\d+[.,]\d+)%',
            r'euríbor hoy.*?(\d+[.,]\d{3})%',
            r'valor diario.*?(\d+[.,]\d{3})%',
            r'euribor.*?hoy.*?(\d+[.,]\d{3})%'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                value_str = match.group(1).replace(',', '.')
                value = float(value_str)
                
                # Validar que el valor esté en un rango razonable para el Euribor
                if 0 <= value <= 10:
                    date_str = datetime.now().strftime('%Y-%m-%d')
                    print(f"✓ Datos encontrados: {date_str} = {value}%")
                    return (date_str, value, source_name, True)
        
        error_msg = "El contenido se carga dinámicamente con JavaScript"
        print(f"  ✗ {error_msg}")
        return (datetime.now().strftime('%Y-%m-%d'), error_msg, source_name, False)
            
    except Exception as e:
        error_msg = str(e)
        print(f"  ✗ Error: {error_msg}")
        return (datetime.now().strftime('%Y-%m-%d'), error_msg, source_name, False)
