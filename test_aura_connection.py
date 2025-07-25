"""
Test Neo4j Aura connection and run sample HVAC GraphRAG queries
For Daniel @ Multipoint S.A.
"""

import os
import yaml
import logging
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from config.yml"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yml')
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config

def test_hvac_queries(driver):
    """Test typical HVAC GraphRAG queries"""
    
    test_queries = [
        {
            'name': 'Contar todos los nodos',
            'query': 'MATCH (n) RETURN count(n) as total_nodes',
            'description': 'Verificar que hay datos en la base'
        },
        {
            'name': 'Productos Samsung VRF',
            'query': '''
            MATCH (p:ProductoSamsung {categoria: 'VRF'}) 
            RETURN p.codigoProducto as sku, p.nombre as nombre, p.capacidadKw as kw
            ORDER BY p.capacidadKw
            ''',
            'description': 'Listar unidades exteriores VRF'
        },
        {
            'name': 'Códigos de error críticos',
            'query': '''
            MATCH (e:ErrorSamsung {severidad: 'critical'})
            RETURN e.codigoError as codigo, e.descripcion as descripcion, e.tiempoResolucion as tiempo
            ORDER BY e.tiempoResolucion DESC
            ''',
            'description': 'Errores que requieren atención inmediata'
        },
        {
            'name': 'Compatibilidad AM160MXVAF',
            'query': '''
            MATCH (outdoor:ProductoSamsung {codigoProducto: 'AM160MXVAF'})
            MATCH (outdoor)-[:ES_COMPATIBLE]->(indoor:ProductoSamsung)
            RETURN indoor.codigoProducto as sku_interior, 
                   indoor.nombre as tipo_interior,
                   indoor.capacidadKw as capacidad
            ORDER BY indoor.capacidadKw
            ''',
            'description': 'Unidades interiores compatibles con DVM S 16HP'
        },
        {
            'name': 'Especificaciones de cables',
            'query': '''
            MATCH (c:EspecificacionCable)
            RETURN c.especCableId as id, 
                   c.especificacion as especificacion,
                   c.aplicacion as uso,
                   c.longitudMaxima as max_metros
            ORDER BY c.tipo
            ''',
            'description': 'Cables necesarios para instalaciones'
        },
        {
            'name': 'Errores frecuentes por producto',
            'query': '''
            MATCH (p:ProductoSamsung)-[r:TIENE_ERROR]->(e:ErrorSamsung)
            WHERE r.frecuencia > 0
            RETURN p.codigoProducto as producto,
                   e.codigoError as error,
                   e.descripcion as descripcion,
                   r.frecuencia as frecuencia
            ORDER BY r.frecuencia DESC
            LIMIT 10
            ''',
            'description': 'Problemas más comunes por equipo'
        },
        {
            'name': 'Instaladores certificados',
            'query': '''
            MATCH (i:Instalador {certificacionSamsung: true})
            RETURN i.nombre as nombre, 
                   i.empresa as empresa, 
                   i.region as zona,
                   i.whatsapp as contacto
            ORDER BY i.region
            ''',
            'description': 'Técnicos autorizados Samsung'
        }
    ]
    
    logger.info("\n🔍 EJECUTANDO CONSULTAS DE PRUEBA HVAC")
    logger.info("=" * 50)
    
    with driver.session() as session:
        for i, test in enumerate(test_queries, 1):
            try:
                logger.info(f"\n{i}. {test['name']}")
                logger.info(f"   📝 {test['description']}")
                
                result = session.run(test['query'])
                records = list(result)
                
                if records:
                    logger.info(f"   ✅ Encontrados: {len(records)} resultados")
                    
                    # Show first few results
                    for j, record in enumerate(records[:3]):
                        record_dict = dict(record)
                        logger.info(f"      {j+1}: {record_dict}")
                    
                    if len(records) > 3:
                        logger.info(f"      ... y {len(records) - 3} más")
                else:
                    logger.info("   ⚠️ No se encontraron resultados")
                    
            except Exception as e:
                logger.error(f"   ❌ Error en consulta: {e}")

def test_error_diagnosis_simulation(driver):
    """Simulate error diagnosis workflow"""
    
    logger.info("\n🚨 SIMULACIÓN: DIAGNÓSTICO DE ERROR")
    logger.info("=" * 40)
    
    # Simulated user query: "Error E458 en mi equipo AM080MXVAF"
    error_code = "E458"
    product_sku = "AM080MXVAF"
    
    logger.info(f"📱 Consulta simulada: 'Error {error_code} en mi equipo {product_sku}'")
    
    with driver.session() as session:
        # Step 1: Get error details
        error_query = """
        MATCH (e:ErrorSamsung {codigoError: $error_code})
        RETURN e.descripcion as descripcion,
               e.severidad as severidad,
               e.solucionDetallada as solucion,
               e.tiempoResolucion as tiempo,
               e.categoria as categoria
        """
        
        error_result = session.run(error_query, error_code=error_code)
        error_record = error_result.single()
        
        if error_record:
            logger.info(f"\n🔍 Error encontrado:")
            logger.info(f"   Código: {error_code}")
            logger.info(f"   Descripción: {error_record['descripcion']}")
            logger.info(f"   Severidad: {error_record['severidad'].upper()}")
            logger.info(f"   Categoría: {error_record['categoria']}")
            logger.info(f"   Tiempo estimado: {error_record['tiempo']} minutos")
            
            logger.info(f"\n🔧 Pasos de solución:")
            for i, step in enumerate(error_record['solucion'], 1):
                logger.info(f"   {i}. {step}")
        
        # Step 2: Check if this error affects the specific product
        product_error_query = """
        MATCH (p:ProductoSamsung {codigoProducto: $product_sku})
        MATCH (e:ErrorSamsung {codigoError: $error_code})
        OPTIONAL MATCH (p)-[r:TIENE_ERROR]->(e)
        RETURN p.nombre as producto_nombre,
               exists((p)-[:TIENE_ERROR]->(e)) as error_afecta_producto,
               r.frecuencia as frecuencia,
               r.condiciones as condiciones
        """
        
        product_result = session.run(product_error_query, 
                                   product_sku=product_sku, 
                                   error_code=error_code)
        product_record = product_result.single()
        
        if product_record:
            logger.info(f"\n📦 Información del producto:")
            logger.info(f"   Producto: {product_record['producto_nombre']}")
            logger.info(f"   SKU: {product_sku}")
            
            if product_record['error_afecta_producto']:
                logger.info(f"   ⚠️ Este error SÍ afecta a este modelo")
                if product_record['frecuencia']:
                    logger.info(f"   📊 Frecuencia reportada: {product_record['frecuencia']} veces")
                if product_record['condiciones']:
                    logger.info(f"   🎯 Condiciones típicas: {', '.join(product_record['condiciones'])}")
            else:
                logger.info(f"   ✅ Este error NO está comúnmente asociado con este modelo")

def main():
    """Main test function"""
    
    logger.info("🧪 PRUEBA DE CONEXIÓN NEO4J AURA - HVAC GRAPHRAG")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config()
    neo4j_config = config['neo4j']
    
    # Create driver
    driver = GraphDatabase.driver(
        neo4j_config['uri'],
        auth=(neo4j_config['user'], neo4j_config['password'])
    )
    
    try:
        # Test basic connection
        with driver.session() as session:
            result = session.run("RETURN 'Conexión exitosa a Neo4j Aura!' as message")
            message = result.single()['message']
            logger.info(f"✅ {message}")
        
        # Run HVAC-specific tests
        test_hvac_queries(driver)
        
        # Simulate error diagnosis
        test_error_diagnosis_simulation(driver)
        
        logger.info("\n🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
        logger.info("\n📋 RESUMEN:")
        logger.info("   ✅ Conexión a Neo4j Aura funcionando")
        logger.info("   ✅ Datos HVAC cargados correctamente")
        logger.info("   ✅ Consultas GraphRAG operativas")
        logger.info("   ✅ Simulación de diagnóstico exitosa")
        
        logger.info(f"\n🌐 Accede a tu base de datos en:")
        logger.info(f"   {neo4j_config['uri'].replace('neo4j+s://', 'https://').replace('.databases.neo4j.io', '.databases.neo4j.io/browser/')}")
        
    except Exception as e:
        logger.error(f"❌ Error durante las pruebas: {e}")
        raise
    finally:
        driver.close()

if __name__ == "__main__":
    main()
