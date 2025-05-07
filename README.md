# uns-semantic-space-explorer
Semantic metadata modeling and 3D visualization for Unified Namespace (UNS) in industrial systems
# UNS Semantic Space Explorer

This project provides a structured **semantic metadata model** and an interactive **3D visualization tool** to explore the Unified Namespace (UNS) in industrial environments.

## 🌐 What Is This?

- **Semantic Metadata Modeling**: Defines a 6-dimensional abstraction for UNS topics, including layers such as Factory, Process Unit, Entity, Phenomenon, Quantity, and Role.
- **Interactive Visualization**: A Dash-powered 3D interface that lets you visually explore the combinatorial space of semantic dimensions — experience the joy of **"seeing high-dimensional space through 3D"**.

> 💡 Designed for industrial engineers, data architects, and curious minds working with IIoT and unified data models.

## 📊 Dimensions

```python
dim_values = {
    "Factory": ["ShanghaiPlant", "SingaporeSite", "BeijingFactory", "BerlinHub", "TexasUnit"],
    "ProcessUnit": ["BoilerRoom", "HVACZone", "CoolingTower", "PackagingLine", "AssemblyArea"],
    "Entity": ["AHU", "Chiller", "Zone", "Pump", "Room"],  # Equipment, System, Space
    "EntityType": ["Equipment", "System", "Space"],         # For classification
    "Phenomenon": ["steam", "light", "electricity", "gas", "liquid"],
    "Quantity": ["temp", "flow", "power", "pressure", "humidity"],
    "Role": ["entering", "leaving", "setpoint", "feedback", "calculated"],
    "ContextType": ["Technical", "Business", "Hybrid"],
    "ContextLocation": ["Field", "NonField", "Mixed"]
}

### 🎬 Demo Video

> Click the image below to watch a quick demo on YouTube.

[![Click to watch the video](https://github.com/witch-Judy/uns-semantic-space-explorer/raw/main/page1.png)](https://www.youtube.com/watch?v=b1tVNqwFiQc)


