# Prototipos 3D de picos — Gem Mining Simulator

Este directorio contiene **conceptos de arte**, no modelos aprobados para producción.

Modelos: Legendary, Celestial, Supreme y Mythic. Los cuatro archivos GLB se generan automáticamente desde `generar_modelos.py`. Incluyen geometría 3D real con materiales PBR; todavía necesitan validarse dentro de Roblox Studio.

## Uso sin Blender

El ZIP de los cuatro modelos se encuentra en `GemMining_Picos_3D_Solo_Modelos.zip` (cuando termine el proceso de generación), junto a los archivos individuales `pick_legendary_concept_v1.glb`, `pick_celestial_concept_v1.glb`, `pick_supreme_concept_v1.glb` y `pick_mythic_concept_v1.glb`.

Codex puede importar los GLB directamente con Roblox Studio 3D Importer. Blender es opcional.

## Precauciones

- Trabajar en copia local, nunca en el lugar publicado.
- **No** reemplazar automáticamente `ArtTemplatesV2`.
- Cada GLB necesita la integración de `Handle`, `GripPoint` y `StrikeTip` correspondiente a `PickaxeVisuals` y `MiningMotion`.
- Validar escala, agarre y materiales en R15 antes de proponer su uso.
- No tocar economía, daño, IDs de gamepass ni guardados.

Consulta `PROMPT_Codex_Importacion_Prueba.txt` para una comprobación segura.

**Autores:** prototipos procedurales preparados en ChatGPT para dirección artística del juego.
