using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using SerapKeremGameKit._LevelSystem;
using SerapKeremGameKit._Managers;
using System.Linq;

public static class UpdateLevelManager
{
    [MenuItem("Tools/Update LevelManager")]
    public static void Run()
    {
        string prefabPath = "Assets/SerapKeremGameKit/Resources/Managers/LevelManager.prefab";
        GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath);
        if (prefab == null)
        {
            Debug.LogError("Could not find LevelManager prefab at " + prefabPath);
            return;
        }

        LevelManager lm = prefab.GetComponent<LevelManager>();
        if (lm == null)
        {
            Debug.LogError("Prefab does not have LevelManager component.");
            return;
        }

        string[] guids = AssetDatabase.FindAssets("t:GameObject", new[] { "Assets/_Game/Resources/Levels" });
        List<Level> allLevels = new List<Level>();

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            GameObject levelGO = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            Level lvl = levelGO.GetComponent<Level>();
            if (lvl != null)
            {
                allLevels.Add(lvl);
            }
        }

        // Sort by level number
        allLevels = allLevels.OrderBy(l => {
            string name = l.gameObject.name;
            string numStr = name.Replace("Level ", "");
            if (int.TryParse(numStr, out int num)) return num;
            return 999;
        }).ToList();

        // Use SerializedObject to modify private field
        SerializedObject so = new SerializedObject(lm);
        SerializedProperty levelsProp = so.FindProperty("_levels");
        
        levelsProp.ClearArray();
        levelsProp.arraySize = allLevels.Count;
        
        for (int i = 0; i < allLevels.Count; i++)
        {
            levelsProp.GetArrayElementAtIndex(i).objectReferenceValue = allLevels[i];
        }
        
        so.ApplyModifiedProperties();
        PrefabUtility.SavePrefabAsset(prefab);
        Debug.Log($"Successfully updated LevelManager prefab with {allLevels.Count} levels.");
    }
}
