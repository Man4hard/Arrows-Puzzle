using UnityEditor;
using UnityEngine;
public static class PlayModeTest {
    public static void Run() {
        EditorApplication.OpenScene("Assets/SerapKeremGameKit/Scenes/TestScene.unity");
        EditorApplication.isPlaying = true;
        // Wait a few seconds, then exit
        EditorApplication.update += () => {
            if (Time.realtimeSinceStartup > 3f) {
                EditorApplication.isPlaying = false;
                EditorApplication.Exit(0);
            }
        };
    }
}
