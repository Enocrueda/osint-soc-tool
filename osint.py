#!/usr/bin/env python3
"""
OSINT SOC TOOLKIT v1.0.0
Autor: Enoc Rueda
Descripción: Herramienta OSINT para analistas SOC Tier 1
"""

# ============================================================================
# MÓDULO DE IMPORTACIONES
# ============================================================================

import sys                      # Salir del programa
import os                       # Manejo de archivos y rutas
import argparse                 # Procesar argumentos de línea de comandos
import json                     # Guardar resultados en formato JSON
from datetime import datetime   # Timestamps para metadatos
import whois                    # Consultas WHOIS
import dns.resolver             # Consultas DNS
import requests                 # Peticiones HTTP (para geolocalización)
import socket                   # Escaneo de puertos
from concurrent.futures import ThreadPoolExecutor  # Escaneo concurrente

# ============================================================================
# MÓDULO DE CONFIGURACIONES
# ============================================================================

VERSION = "1.0.0"
AUTOR = "Enoc Rueda"

# Diccionario de puertos comunes para identificación rápida
PUERTOS_COMUNES = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    111: 'RPC',
    135: 'RPC',
    139: 'NetBIOS',
    143: 'IMAP',
    443: 'HTTPS',
    445: 'SMB',
    993: 'IMAPS',
    995: 'POP3S',
    1723: 'PPTP',
    3306: 'MySQL',
    3389: 'RDP',
    5432: 'PostgreSQL',
    5900: 'VNC',
    6379: 'Redis',
    8080: 'HTTP-Alt',
    8443: 'HTTPS-Alt'
}

# ============================================================================
# FUNCIÓN: GEO IP (geolocalización)
# ============================================================================

def geo_ip(ip, verbose=False):
    """
    Obtiene la información de geolocalización de una IP usando ip-api.com.

    Args:
        ip (str): Dirección IP a analizar.
        verbose (bool): Si es True, muestra información detallada.

    Returns:
        dict: Diccionario con datos de geolocalización o None si hay error.
    """
    print(f"\n📍 Consultando geolocalización para {ip}...")
    
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get('status') == 'success':
            resultado = {
                'Ip': data.get('query'),
                'Pais': data.get('country'),
                'Region': data.get('regionName'),
                'Ciudad': data.get('city'),
                'Latitud': data.get('lat'),
                'Longitud': data.get('lon'),
                'Isp': data.get('isp'),
                'Organizacion': data.get('org')
            }

            print("✅ Geolocalización encontrada con éxito.")
            if verbose:
                print(f"   País: {resultado['Pais']}")
                print(f"   Ciudad: {resultado['Ciudad']}")
                print(f"   ISP: {resultado['Isp']}")
            return resultado
        else:
            print(f"❌ Error: {data.get('message', 'desconocido')}")
            return None
    except Exception as e:
        print(f"❌ Error en geolocalización: {e}")
        return None

# ============================================================================
# FUNCIÓN: ESCANEO DE UN PUERTO INDIVIDUAL
# ============================================================================

def escan_puerto(ip, puerto, timeout=1):
    """
    Escanea un puerto específico en una IP.

    Args:
        ip (str): IP a escanear.
        puerto (int): Puerto a probar.
        timeout (int): Timeout en segundos.

    Returns:
        dict: Información del puerto si está abierto, None si cerrado.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        resultado = sock.connect_ex((ip, puerto))
        sock.close()
        if resultado == 0:
            # Puerto abierto, intentar obtener banner
            try:
                banner_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                banner_sock.settimeout(2)
                banner_sock.connect((ip, puerto))
                banner_sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = banner_sock.recv(1024).decode('utf-8', errors='ignore')[:100]
                banner_sock.close()
            except:
                banner = "No disponible"
            
            return {
                'puerto': puerto,
                'estado': 'abierto',
                'servicio': PUERTOS_COMUNES.get(puerto, 'desconocido'),
                'banner': banner
            }
        return None
    except:
        return None

# ============================================================================
# FUNCIÓN: ESCANEO DE PUERTOS COMUNES (CONCURRENTE)
# ============================================================================

def escanear_puertos_comunes(ip, verbose=False):
    """
    Escanea los puertos más comunes en una IP usando threads.

    Args:
        ip (str): IP a escanear.
        verbose (bool): Si es True, muestra detalles de cada puerto abierto.

    Returns:
        list: Lista de diccionarios con información de puertos abiertos.
    """
    print(f"\n🔍 Escaneando puertos comunes en {ip}...")
    
    puertos_a_escanear = list(PUERTOS_COMUNES.keys())
    puertos_abiertos = []
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(escan_puerto, ip, puerto): puerto 
                   for puerto in puertos_a_escanear}
        
        for future in futures:
            resultado = future.result()
            if resultado:
                puertos_abiertos.append(resultado)
                if verbose:
                    print(f"   ✅ Puerto {resultado['puerto']}: {resultado['servicio']} (abierto)")
    
    print(f"   📊 Puertos abiertos encontrados: {len(puertos_abiertos)}")
    return puertos_abiertos

# ============================================================================
# FUNCIÓN: MOSTRAR BANNER
# ============================================================================

def mostrar_banner():
    """Muestra el banner del programa."""
    print(f"""
    ╔══════════════════════════════════════════╗
    ║     OSINT SOC TOOLKIT v{VERSION}            ║
    ║     Autor: {AUTOR}                        ║
    ║     Uso exclusivo para fines autorizados  ║
    ╚══════════════════════════════════════════╝
    """)

# ============================================================================
# FUNCIÓN: CARGA DE CONFIGURACIÓN (futura)
# ============================================================================

def cargar_configuracion():
    """
    Carga configuración desde config.yaml (por implementar).
    Por ahora retorna configuración por defecto.
    """
    # TODO: Implementar lectura de YAML
    return {
        'timeout': 30,
        'output_dir': 'reports'
    }

# ============================================================================
# FUNCIÓN: CONSULTA WHOIS
# ============================================================================

def consultar_whois(dominio, verbose=False):
    """
    Consulta WHOIS para un dominio.

    Args:
        dominio (str): El dominio a consultar.
        verbose (bool): Si es True, muestra información detallada.

    Returns:
        dict: Información WHOIS o None si hay error.
    """
    print(f"\n🔍 Consultando WHOIS para {dominio}...")
    
    try:
        w = whois.whois(dominio)
        
        resultado = {
            'dominio': dominio,
            'registrar': str(w.registrar) if w.registrar else None,
            'fecha_creacion': str(w.creation_date[0]) if isinstance(w.creation_date, list) else str(w.creation_date),
            'fecha_expiracion': str(w.expiration_date[0]) if isinstance(w.expiration_date, list) else str(w.expiration_date),
            'servidores_dns': [str(ns) for ns in (w.name_servers or [])],
            'pais': str(w.country) if w.country else None,
            'org': str(w.org) if w.org else None
        }
        
        print("   ✅ WHOIS completado.")
        if verbose:
            print(f"   📋 Registrado por: {resultado['registrar']}")
            print(f"   📅 Creado: {resultado['fecha_creacion']}")
            print(f"   ⏰ Expira: {resultado['fecha_expiracion']}")
        
        return resultado
        
    except Exception as e:
        print(f"   ❌ Error en WHOIS: {e}")
        return None

# ============================================================================
# FUNCIÓN: CONSULTA DNS
# ============================================================================

def consultar_dns(dominio, verbose=False):
    """
    Consulta registros DNS de un dominio.

    Args:
        dominio (str): El dominio a consultar.
        verbose (bool): Si es True, muestra detalles.

    Returns:
        dict: Diccionario con los registros encontrados o None si el dominio no existe.
    """
    print(f"\n🔍 Consultando DNS para {dominio}...")
    
    tipos = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME']
    resultados = {}
    
    for tipo in tipos:
        try:
            respuestas = dns.resolver.resolve(dominio, tipo)
            registros = []
            
            for respuesta in respuestas:
                if tipo == 'MX':
                    registros.append({
                        'prioridad': respuesta.preference,
                        'servidor': str(respuesta.exchange).rstrip('.')
                    })
                elif tipo == 'TXT':
                    txt_strings = [str(s) for s in respuesta.strings]
                    registros.append(' '.join(txt_strings))
                else:
                    registros.append(str(respuesta).rstrip('.'))
            
            if registros:
                resultados[tipo] = registros
                
                if verbose:
                    print(f"   • {tipo}: {len(registros)} registros")
                    
        except dns.resolver.NoAnswer:
            # No hay registros de este tipo (normal)
            pass
        except dns.resolver.NXDOMAIN:
            print(f"   ❌ El dominio {dominio} no existe.")
            return None
        except Exception as e:
            if verbose:
                print(f"   ⚠  Error en {tipo}: {e}")
    
    print(f"   ✅ DNS completado ({len(resultados)} tipos encontrados).")
    return resultados

# ============================================================================
# FUNCIÓN: PROCESAR ARGUMENTOS DE LÍNEA DE COMANDOS
# ============================================================================

def procesar_argumentos():
    """
    Configura y procesa los argumentos de línea de comandos.

    Returns:
        argparse.Namespace: Argumentos parseados.
    """
    parser = argparse.ArgumentParser(
        description='OSINT SOC Toolkit - Herramienta de reconocimiento',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EJEMPLOS:
  python3 osint.py -d ejemplo.com
  python3 osint.py -i 8.8.8.8
  python3 osint.py -d ejemplo.com -o reporte.json -v
        """
    )

    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument('-d', '--dominio', help='Dominio a investigar')
    grupo.add_argument('-i', '--ip', help='IP a analizar')
    parser.add_argument('-o', '--output', help='Archivo de salida JSON')
    parser.add_argument('-v', '--verbose', action='store_true', help='Mostrar información detallada')
    return parser.parse_args()

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que coordina todo el análisis."""
    mostrar_banner()
    args = procesar_argumentos()
    config = cargar_configuracion()  # por ahora no se usa

    # Mostrar argumentos recibidos
    print("\n📋 Argumentos Recibidos:")
    if args.dominio:
        print(f"   Análisis a: DOMINIO")
        print(f"   Dominio objetivo: {args.dominio}")
    elif args.ip:
        print(f"   Análisis a: IP")
        print(f"   IP Objetivo: {args.ip}")
    print(f"   Verbose: {'SÍ' if args.verbose else 'NO'}")
    if args.output:
        print(f"   Guardar en: {args.output}")

    # Estructura de resultados
    resultados = {
        'metadata': {
            'fecha': datetime.now().isoformat(),
            'objetivo': args.dominio or args.ip,
            'tipo_de_analisis': 'dominio' if args.dominio else 'IP',
            'herramienta': f'OSINT-SOC-Toolkit v{VERSION}'
        },
        'whois': None,
        'dns': None,
        'geo': None,
        'puertos': None
    }

    # Ejecutar según el objetivo
    if args.dominio:
        print("\n🔎 Iniciando investigación del dominio")
        print("=" * 50)
        resultados['whois'] = consultar_whois(args.dominio, args.verbose)
        resultados['dns'] = consultar_dns(args.dominio, args.verbose)
    elif args.ip:
        print("\n🔎 Iniciando investigación de la IP")
        print("=" * 50)
        resultados['geo'] = geo_ip(args.ip, args.verbose)
        resultados['puertos'] = escanear_puertos_comunes(args.ip, args.verbose)
        
        print("\n📌 Resumen de IP:")
        print("-" * 30)
        if resultados['geo']:
            print(f"   País: {resultados['geo'].get('Pais')}")
            print(f"   Ciudad: {resultados['geo'].get('Ciudad')}")
            print(f"   ISP: {resultados['geo'].get('Isp')}")
            print(f"   Latitud: {resultados['geo'].get('lat')}")
            print(f"   Longitud: {resultados['geo'].get('lon')}")      
        if resultados['puertos']:
            print(f"   Puertos abiertos: {len(resultados['puertos'])}")
            for p in resultados['puertos']:
                print(f"     {p['puerto']}: {p['servicio']}")
        else:
            print("   No se encontraron puertos comunes abiertos.")

    # Guardar resultados si se solicitó
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(resultados, f, indent=2, default=str)
        print(f"\n💾 Resultados guardados en {args.output}")

    # Resumen final
    print("\n" + "=" * 50)
    print("✅ Resumen de la investigación:")
    if args.dominio:
        if resultados['whois']:
            print("   • WHOIS completado")
        if resultados['dns']:
            print(f"   • DNS: {len(resultados['dns'])} tipos de registros")
    print("\n🏁 Investigación concluida.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠  Programa interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        sys.exit(1)
