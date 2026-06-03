using UnityEngine;
using UnityEditor;

public class TestWorldPos
{
    public static void Run()
    {
        var prefab = AssetDatabase.LoadAssetAtPath<GameObject>("Assets/_Game/Resources/Levels/Level 10.prefab");
        var obj = PrefabUtility.InstantiatePrefab(prefab) as GameObject;
        
        var bg = obj.transform.Find("Background");
        if (bg != null)
        {
            Debug.Log($"[DEBUG] Background Local Position: {bg.localPosition}");
            Debug.Log($"[DEBUG] Background World Position: {bg.position}");
            Debug.Log($"[DEBUG] Background Forward (World Z): {bg.forward}");
        }
        
        var lines = obj.transform.Find("LINES");
        if (lines != null && lines.childCount > 0)
        {
            var line = lines.GetChild(0);
            Debug.Log($"[DEBUG] Line 0 Local Position: {line.localPosition}");
            Debug.Log($"[DEBUG] Line 0 World Position: {line.position}");
        }
        
        var cam = obj.transform.Find("CamPoint");
        if (cam != null)
        {
            Debug.Log($"[DEBUG] CamPoint World Position: {cam.position}");
        }
        
        GameObject.DestroyImmediate(obj);
    }
}
