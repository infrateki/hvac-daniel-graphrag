# HVAC GraphRAG - Neo4j Aura Setup Guide
## For Daniel @ Multipoint S.A.

### 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   cd C:\Users\sergi\Desktop\HVAC_DANIEL
   pip install -r requirements.txt
   ```

2. **Populate Neo4j Aura database:**
   ```bash
   python connect_to_aura.py
   ```

3. **Test the connection:**
   ```bash
   python test_aura_connection.py
   ```

### 📊 Your Neo4j Aura Details

- **Instance ID**: 4cf147ca
- **URI**: neo4j+s://4cf147ca.databases.neo4j.io
- **Browser**: https://4cf147ca.databases.neo4j.io/browser/
- **Username**: neo4j
- **Password**: VGnEYje3ygdicoxAxsdPRJA4eyyc7L5Xso0mYwrSzxk

### 🎯 What Gets Created

#### Nodes:
- **7 ProductoSamsung**: 3 outdoor VRF + 4 indoor units
- **5 ErrorSamsung**: Common error codes (E101, E201, E458, E320, CH01)
- **4 EspecificacionCable**: Power and communication cables
- **2 Instalador**: Sample certified installers
- **1 Proyecto**: Sample project "Torre Corporativa Asunción"

#### Relationships:
- **12 ES_COMPATIBLE**: Outdoor ↔ Indoor compatibility
- **~6 TIENE_ERROR**: Product ↔ Error associations
- **3 REQUIERE_CABLE**: Product ↔ Cable requirements

### 🔍 Sample Queries

```cypher
// View all products
MATCH (n) RETURN n LIMIT 25

// Find compatible indoor units for AM160MXVAF
MATCH (outdoor:ProductoSamsung {codigoProducto: 'AM160MXVAF'})
MATCH (outdoor)-[:ES_COMPATIBLE]->(indoor:ProductoSamsung)
RETURN indoor.codigoProducto, indoor.nombre, indoor.capacidadKw

// Get error E458 details
MATCH (e:ErrorSamsung {codigoError: 'E458'})
RETURN e.descripcion, e.solucionDetallada, e.tiempoResolucion

// Find all critical errors
MATCH (e:ErrorSamsung {severidad: 'critical'})
RETURN e.codigoError, e.descripcion
ORDER BY e.tiempoResolucion DESC
```

### 🛠️ Troubleshooting

**Connection issues:**
- Verify your internet connection
- Check that the URI and credentials are correct
- Ensure Neo4j Aura instance is running

**No data visible:**
- Run `connect_to_aura.py` to populate the database
- Refresh the Neo4j Browser page
- Try the sample queries above

**Dependencies:**
- Make sure Python 3.8+ is installed
- Install requirements: `pip install -r requirements.txt`

### 📱 Next Steps

1. **Test queries** - Try the sample queries in Neo4j Browser
2. **Verify data** - Run `test_aura_connection.py`
3. **Explore the graph** - Use the visualization in Neo4j Browser
4. **Add more data** - Import Samsung manuals and additional products

### 🎉 Success Indicators

✅ Connection script runs without errors
✅ Test script shows 19 total nodes
✅ Neo4j Browser displays the graph
✅ Sample queries return results
✅ Error diagnosis simulation works

Your HVAC GraphRAG system is ready for Daniel's technical support queries!