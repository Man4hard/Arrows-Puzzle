#!/usr/bin/env python3
"""
Extreme Level Prefab Generator for Arrows Puzzle (Unity)
Generates YAML level prefab files with complex line shapes for Levels 26-75.
"""

import os
import hashlib
import uuid
import math
import random

OUTPUT_DIR = "/Users/abcadvt/.gemini/antigravity/scratch/Arrows-Puzzle/Assets/_Game/Resources/Levels"

# ─── Line Prefab Constants ────────────────────────────────────────
LINE_PREFAB_GUID = "5134ca6e224a9b84b8bd86f152cf67fc"
LINE_PREFAB_FILEID = "100100000"

PF = {
    "root_go":         "4852218959071952598",
    "root_transform":  "6705024964587633368",
    "line_renderer":   "5703179247697745139",
    "line_script":     "2004340178550153643",
    "line_animation":  "2889735952934244776",
    "line_destroyer":  "579988495362921800",
    "line_click":      "4698239093576954667",
    "collider_spawner":"3898713965489042308",
    "material_handler":"8190878419885716933",
    "snap_fixer":      "1088355798733759430",
    "head_transform":  "9200941245333506865",
    "head_sprite_tr":  "8852158018286561598",
    "head_script":     "1227772318919715864",
    "head_collision":  "5917618282005337659",
    "line_collider_ref":"2728101366424247942",
}

LEVEL_SCRIPT_GUID    = "9b1abbcdfbba6c844807deabc3f8a362"
LEVEL_CONFIG_GUID    = "a82a1eba272d8eb499dec65a1bd4440a"
LINE_MANAGER_GUID    = "048ea9fa111669c4eaddae4f0f33d2d2"
V3_POOL_GUID         = "c6692c0c09548c4419b5429d125c4c12"
BG_MATERIAL_GUID     = "a3ae4006d9b5b5b4b8c0a4cfd4c6b6c9"

S = {
    "root_go":            "803803965156243063",
    "root_transform":     "8655635823615927415",
    "level_script":       "4408890181075704862",
    "campoint_go":        "2837266096709259451",
    "campoint_transform": "4774320401754682918",
    "levelconfig_go":     "4720622960744099466",
    "levelconfig_transform":"4070432621108208573",
    "levelconfig_script": "531334829852373596",
    "pool_go":            "5394252221369916936",
    "pool_transform":     "1299602328605539289",
    "pool_script":        "5000651016614165200",
    "bg_go":              "5540697370112924935",
    "bg_transform":       "6245650384963763403",
    "bg_meshfilter":      "4868594600767944750",
    "bg_meshrenderer":    "2897135612290006292",
    "linemanager_go":     "7159275398082964930",
    "linemanager_transform":"5930082216675289285",
    "linemanager_script": "8253618541472653865",
}

def gen_id(seed: str) -> str:
    """Generate a deterministic 17-digit fileID from a seed string."""
    h = hashlib.sha256(seed.encode()).hexdigest()
    # 9 * 10**17 is safely below long.MaxValue (9,223,372,036,854,775,807)
    num = int(h[:15], 16) % (9 * 10**17) + 10**17
    return str(num)

def gen_guid() -> str:
    return uuid.uuid4().hex

# ═══════════════════════════════════════════════════════════════════
# GENERATOR ALGORITHMS
# ═══════════════════════════════════════════════════════════════════

def generate_chaotic_points(points_count, scale):
    """Generates a random wiggly line."""
    pts = [(0, 0)]
    cx, cy = 0, 0
    directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]
    for _ in range(points_count - 1):
        dx, dy = random.choice(directions)
        cx += dx * scale
        cy += dy * scale
        # Add some jitter
        cx += random.uniform(-0.5, 0.5)
        cy += random.uniform(-0.5, 0.5)
        pts.append((round(cx, 2), round(cy, 2)))
    return pts

def generate_spiral_points(points_count, scale):
    pts = []
    for i in range(points_count):
        angle = i * 0.5
        radius = i * scale * 0.5
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        pts.append((round(x, 2), round(y, 2)))
    return pts

def generate_levels():
    levels = {}
    random.seed(42)  # For deterministic generation
    
    for level_num in range(26, 76):
        num_lines = 10 + int((level_num - 25) * 0.4) # scales up to ~30 lines
        lines = []
        
        for i in range(num_lines):
            # Pick a starting position in a grid
            pos_x = random.randint(-8, 8)
            pos_y = random.randint(-8, 8)
            
            # Decide line complexity based on level
            points_count = random.randint(3, 5 + int(level_num/5))
            
            shape_type = random.choice(["chaotic", "chaotic", "chaotic", "spiral", "zigzag"])
            
            if shape_type == "chaotic":
                pts = generate_chaotic_points(points_count, scale=2)
            elif shape_type == "spiral":
                pts = generate_spiral_points(points_count, scale=1)
            else: # zigzag
                pts = [(0,0)]
                cx, cy = 0, 0
                for j in range(points_count-1):
                    cx += random.choice([2, -2])
                    cy += random.choice([2, -2])
                    pts.append((cx, cy))

            # Ensure minimal length
            if len(pts) < 2:
                pts.append((2, 0))

            lines.append({
                "position": (pos_x, pos_y),
                "points": pts,
                "destroy_delay": random.randint(3, 6)
            })
            
        levels[level_num] = lines
    return levels

# ═══════════════════════════════════════════════════════════════════
# YAML GENERATION
# ═══════════════════════════════════════════════════════════════════

def generate_level_yaml(level_num, lines):
    lines_go_id = gen_id(f"L{level_num}_lines_go")
    lines_tr_id = gen_id(f"L{level_num}_lines_tr")

    lids = []
    for i in range(len(lines)):
        lids.append({
            "pi":  gen_id(f"L{level_num}_li{i}_pi"),
            "str": gen_id(f"L{level_num}_li{i}_str"),
            "slr": gen_id(f"L{level_num}_li{i}_slr"),
        })

    parts = []
    parts.append("%YAML 1.1\n%TAG !u! tag:unity3d.com,2011:")

    # ── Root Level GO ──
    parts.append(f"""--- !u!1 &{S['root_go']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {S['root_transform']}}}
  - component: {{fileID: {S['level_script']}}}
  m_Layer: 0
  m_Name: Level {level_num}
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1""")

    # ── Root Transform ──
    parts.append(f"""--- !u!4 &{S['root_transform']}
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['root_go']}}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0.29, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children:
  - {{fileID: {S['bg_transform']}}}
  - {{fileID: {S['campoint_transform']}}}
  - {{fileID: {S['levelconfig_transform']}}}
  - {{fileID: {S['linemanager_transform']}}}
  - {{fileID: {lines_tr_id}}}
  - {{fileID: {S['pool_transform']}}}
  m_Father: {{fileID: 0}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}""")

    # ── Level Script ──
    parts.append(f"""--- !u!114 &{S['level_script']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['root_go']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {LEVEL_SCRIPT_GUID}, type: 3}}
  m_Name: 
  m_EditorClassIdentifier: 
  _tileSizeArray:
    gridSize: {{x: 3, y: 3}}
    cellSize: {{x: 32, y: 16}}
    cells:
    - row: 000000000000000000000000
    - row: 000000000000000000000000
    - row: 000000000000000000000000
  _levelTime: 120
  _isLevelWon: 0
  _money: 10
  _lineManager: {{fileID: {S['linemanager_script']}}}
  _linesParent: {{fileID: {lines_tr_id}}}""")

    # ── CamPoint ──
    parts.append(f"""--- !u!1 &{S['campoint_go']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {S['campoint_transform']}}}
  m_Layer: 0
  m_Name: CamPoint
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &{S['campoint_transform']}
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['campoint_go']}}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 15, z: 10}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {{fileID: {S['root_transform']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}""")

    # ── LINES Parent ──
    children = "\n".join([f"  - {{fileID: {l['str']}}}" for l in lids])
    parts.append(f"""--- !u!1 &{lines_go_id}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {lines_tr_id}}}
  m_Layer: 0
  m_Name: LINES
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &{lines_tr_id}
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {lines_go_id}}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children:
{children}
  m_Father: {{fileID: {S['root_transform']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}""")

    # ── LevelConfig ──
    parts.append(f"""--- !u!1 &{S['levelconfig_go']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {S['levelconfig_transform']}}}
  - component: {{fileID: {S['levelconfig_script']}}}
  m_Layer: 0
  m_Name: LevelConfig
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &{S['levelconfig_transform']}
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['levelconfig_go']}}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {{fileID: {S['root_transform']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
--- !u!114 &{S['levelconfig_script']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['levelconfig_go']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {LEVEL_CONFIG_GUID}, type: 3}}
  m_Name: 
  m_EditorClassIdentifier: 
  _timeThresholdsSec:
  - 30
  - 45
  - 60
  _livesThresholds: 050000000300000001000000
  _winCoins: 10
  _failCoins: 0""")

    # ── Vector3ArrayPool ──
    parts.append(f"""--- !u!1 &{S['pool_go']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {S['pool_transform']}}}
  - component: {{fileID: {S['pool_script']}}}
  m_Layer: 0
  m_Name: Vector3ArrayPool
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &{S['pool_transform']}
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['pool_go']}}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {{fileID: {S['root_transform']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
--- !u!114 &{S['pool_script']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['pool_go']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {V3_POOL_GUID}, type: 3}}
  m_Name: 
  m_EditorClassIdentifier: 
  _initialSize: 8
  _maxSize: 64
  _root: {{fileID: {S['pool_transform']}}}
  _maxArrayLength: 100""")

    # ── Background ──
    parts.append(f"""--- !u!1 &{S['bg_go']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {S['bg_transform']}}}
  - component: {{fileID: {S['bg_meshfilter']}}}
  - component: {{fileID: {S['bg_meshrenderer']}}}
  m_Layer: 0
  m_Name: Background
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &{S['bg_transform']}
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['bg_go']}}}
  serializedVersion: 2
  m_LocalRotation: {{x: -0.5, y: 0.5, z: -0.5, w: 0.5}}
  m_LocalPosition: {{x: 0, y: 2.5, z: 0}}
  m_LocalScale: {{x: 3, y: 3, z: 3}}
  m_ConstrainProportionsScale: 1
  m_Children: []
  m_Father: {{fileID: {S['root_transform']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 90, z: -90}}
--- !u!33 &{S['bg_meshfilter']}
MeshFilter:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['bg_go']}}}
  m_Mesh: {{fileID: 10209, guid: 0000000000000000e000000000000000, type: 0}}
--- !u!23 &{S['bg_meshrenderer']}
MeshRenderer:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['bg_go']}}}
  m_Enabled: 1
  m_CastShadows: 1
  m_ReceiveShadows: 1
  m_DynamicOccludee: 1
  m_StaticShadowCaster: 0
  m_MotionVectors: 1
  m_LightProbeUsage: 1
  m_ReflectionProbeUsage: 1
  m_RayTracingMode: 2
  m_RayTraceProcedural: 0
  m_RayTracingAccelStructBuildFlagsOverride: 0
  m_RayTracingAccelStructBuildFlags: 1
  m_SmallMeshCulling: 1
  m_RenderingLayerMask: 1
  m_RendererPriority: 0
  m_Materials:
  - {{fileID: 2100000, guid: {BG_MATERIAL_GUID}, type: 2}}
  m_StaticBatchInfo:
    firstSubMesh: 0
    subMeshCount: 0
  m_StaticBatchRoot: {{fileID: 0}}
  m_ProbeAnchor: {{fileID: 0}}
  m_LightProbeVolumeOverride: {{fileID: 0}}
  m_ScaleInLightmap: 1
  m_ReceiveGI: 1
  m_PreserveUVs: 0
  m_IgnoreNormalsForChartDetection: 0
  m_ImportantGI: 0
  m_StitchLightmapSeams: 1
  m_SelectedEditorRenderState: 3
  m_MinimumChartSize: 4
  m_AutoUVMaxDistance: 0.5
  m_AutoUVMaxAngle: 89
  m_LightmapParameters: {{fileID: 0}}
  m_SortingLayerID: 0
  m_SortingLayer: 0
  m_SortingOrder: 0
  m_AdditionalVertexStreams: {{fileID: 0}}""")

    # ── LineManager ──
    parts.append(f"""--- !u!1 &{S['linemanager_go']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {S['linemanager_transform']}}}
  - component: {{fileID: {S['linemanager_script']}}}
  m_Layer: 0
  m_Name: LineManager
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &{S['linemanager_transform']}
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['linemanager_go']}}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {{fileID: {S['root_transform']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
--- !u!114 &{S['linemanager_script']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {S['linemanager_go']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {LINE_MANAGER_GUID}, type: 3}}
  m_Name: 
  m_EditorClassIdentifier: 
  _activeLines: []
  _vector3ArrayPool: {{fileID: {S['pool_script']}}}""")

    # ── Line PrefabInstances ──
    for i, line_data in enumerate(lines):
        parts.append(gen_line_yaml(i, line_data, lids[i], lines_tr_id))

    return "\n".join(parts) + "\n"

def gen_line_yaml(idx, ld, ids, lines_tr_id):
    G = LINE_PREFAB_GUID
    name = ld.get("name", f"Line ({idx + 1})")
    pos = ld["position"]
    pts = ld["points"]
    dd = ld.get("destroy_delay", 3)
    w = ld.get("width", 0.2)
    lp = pts[-1]

    m = []
    m.append(f"    - target: {{fileID: {PF['line_destroyer']}, guid: {G}, type: 3}}\n      propertyPath: destroyDelay\n      value: {dd}\n      objectReference: {{fileID: 0}}")
    m.append(f"    - target: {{fileID: {PF['snap_fixer']}, guid: {G}, type: 3}}\n      propertyPath: m_Enabled\n      value: 0\n      objectReference: {{fileID: 0}}")
    m.append(f"    - target: {{fileID: {PF['head_script']}, guid: {G}, type: 3}}\n      propertyPath: _lineRenderer\n      value: \n      objectReference: {{fileID: {ids['slr']}}}")
    m.append(f"    - target: {{fileID: {PF['head_script']}, guid: {G}, type: 3}}\n      propertyPath: _rotationOffset\n      value: -90\n      objectReference: {{fileID: 0}}")
    m.append(f"    - target: {{fileID: {PF['line_collider_ref']}, guid: {G}, type: 3}}\n      propertyPath: lr\n      value: \n      objectReference: {{fileID: {ids['slr']}}}")
    m.append(f"    - target: {{fileID: {PF['line_animation']}, guid: {G}, type: 3}}\n      propertyPath: _arrayPool\n      value: \n      objectReference: {{fileID: {S['pool_script']}}}")
    m.append(f"    - target: {{fileID: {PF['root_go']}, guid: {G}, type: 3}}\n      propertyPath: m_Name\n      value: {name}\n      objectReference: {{fileID: 0}}")
    m.append(f"    - target: {{fileID: {PF['root_go']}, guid: {G}, type: 3}}\n      propertyPath: m_IsActive\n      value: 1\n      objectReference: {{fileID: 0}}")
    m.append(f"    - target: {{fileID: {PF['line_renderer']}, guid: {G}, type: 3}}\n      propertyPath: m_Positions.Array.size\n      value: {len(pts)}\n      objectReference: {{fileID: 0}}")
    for j, (px, py) in enumerate(pts):
        m.append(f"    - target: {{fileID: {PF['line_renderer']}, guid: {G}, type: 3}}\n      propertyPath: m_Positions.Array.data[{j}].x\n      value: {px}\n      objectReference: {{fileID: 0}}")
        m.append(f"    - target: {{fileID: {PF['line_renderer']}, guid: {G}, type: 3}}\n      propertyPath: m_Positions.Array.data[{j}].y\n      value: {py}\n      objectReference: {{fileID: 0}}")
        m.append(f"    - target: {{fileID: {PF['line_renderer']}, guid: {G}, type: 3}}\n      propertyPath: m_Positions.Array.data[{j}].z\n      value: 0\n      objectReference: {{fileID: 0}}")
    m.append(f"    - target: {{fileID: {PF['line_renderer']}, guid: {G}, type: 3}}\n      propertyPath: m_Parameters.widthMultiplier\n      value: {w}\n      objectReference: {{fileID: 0}}")
    m.append(f"    - target: {{fileID: {PF['head_collision']}, guid: {G}, type: 3}}\n      propertyPath: rayLength\n      value: 2\n      objectReference: {{fileID: 0}}")

    for axis, val in [("x", pos[0]), ("y", pos[1]), ("z", 0)]:
        m.append(f"    - target: {{fileID: {PF['root_transform']}, guid: {G}, type: 3}}\n      propertyPath: m_LocalPosition.{axis}\n      value: {val}\n      objectReference: {{fileID: 0}}")
    for axis, val in [("w", 1), ("x", "-0"), ("y", "-0"), ("z", "-0")]:
        m.append(f"    - target: {{fileID: {PF['root_transform']}, guid: {G}, type: 3}}\n      propertyPath: m_LocalRotation.{axis}\n      value: {val}\n      objectReference: {{fileID: 0}}")
    for axis in ["x", "y", "z"]:
        m.append(f"    - target: {{fileID: {PF['root_transform']}, guid: {G}, type: 3}}\n      propertyPath: m_LocalEulerAnglesHint.{axis}\n      value: 0\n      objectReference: {{fileID: 0}}")

    for axis in ["x", "y", "z"]:
        m.append(f"    - target: {{fileID: {PF['head_sprite_tr']}, guid: {G}, type: 3}}\n      propertyPath: m_LocalScale.{axis}\n      value: 0.74999994\n      objectReference: {{fileID: 0}}")
    m.append(f"    - target: {{fileID: {PF['head_transform']}, guid: {G}, type: 3}}\n      propertyPath: m_LocalPosition.x\n      value: {lp[0]}\n      objectReference: {{fileID: 0}}")
    m.append(f"    - target: {{fileID: {PF['head_transform']}, guid: {G}, type: 3}}\n      propertyPath: m_LocalPosition.y\n      value: {lp[1]}\n      objectReference: {{fileID: 0}}")
    for axis, val in [("w", 1), ("x", "-0"), ("z", "-0")]:
        m.append(f"    - target: {{fileID: {PF['head_transform']}, guid: {G}, type: 3}}\n      propertyPath: m_LocalRotation.{axis}\n      value: {val}\n      objectReference: {{fileID: 0}}")

    mods = "\n".join(m)

    return f"""--- !u!1001 &{ids['pi']}
PrefabInstance:
  m_ObjectHideFlags: 0
  serializedVersion: 2
  m_Modification:
    serializedVersion: 3
    m_TransformParent: {{fileID: {lines_tr_id}}}
    m_Modifications:
{mods}
    m_RemovedComponents: []
    m_RemovedGameObjects: []
    m_AddedGameObjects: []
    m_AddedComponents: []
  m_SourcePrefab: {{fileID: {LINE_PREFAB_FILEID}, guid: {LINE_PREFAB_GUID}, type: 3}}
--- !u!120 &{ids['slr']} stripped
LineRenderer:
  m_CorrespondingSourceObject: {{fileID: {PF['line_renderer']}, guid: {LINE_PREFAB_GUID}, type: 3}}
  m_PrefabInstance: {{fileID: {ids['pi']}}}
  m_PrefabAsset: {{fileID: 0}}
--- !u!4 &{ids['str']} stripped
Transform:
  m_CorrespondingSourceObject: {{fileID: {PF['root_transform']}, guid: {LINE_PREFAB_GUID}, type: 3}}
  m_PrefabInstance: {{fileID: {ids['pi']}}}
  m_PrefabAsset: {{fileID: 0}}"""

def gen_meta(guid):
    return f"""fileFormatVersion: 2
guid: {guid}
PrefabImporter:
  externalObjects: {{}}
  userData: 
  assetBundleName: 
  assetBundleVariant: 
"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    levels = generate_levels()

    for level_num, lines in levels.items():
        yaml_content = generate_level_yaml(level_num, lines)
        prefab_path = os.path.join(OUTPUT_DIR, f"Level {level_num}.prefab")
        with open(prefab_path, "w", encoding="utf-8") as f:
            f.write(yaml_content)
        
        print(f"Generated Level {level_num} ({len(lines)} lines)")

        meta_path = prefab_path + ".meta"
        if not os.path.exists(meta_path):
            with open(meta_path, "w", encoding="utf-8") as f:
                f.write(gen_meta(gen_guid()))

if __name__ == "__main__":
    main()
