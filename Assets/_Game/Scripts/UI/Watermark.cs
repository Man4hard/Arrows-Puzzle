using UnityEngine;
using UnityEngine.UI;
using TMPro;

namespace _Game.UI
{
    public class Watermark : MonoBehaviour
    {
        private void Awake()
        {
            CreateWatermark();
        }

        private void CreateWatermark()
        {
            GameObject watermarkGO = new GameObject("Watermark");
            watermarkGO.transform.SetParent(this.transform, false);

            TextMeshProUGUI text = watermarkGO.AddComponent<TextMeshProUGUI>();
            text.text = "Developed By TAYYAB";
            text.fontSize = 24;
            text.color = new Color(0.5f, 0.5f, 0.5f, 0.5f); // Gray with some transparency
            text.alignment = TextAlignmentOptions.BottomCenter;

            RectTransform rectTransform = watermarkGO.GetComponent<RectTransform>();
            rectTransform.anchorMin = new Vector2(0.5f, 0);
            rectTransform.anchorMax = new Vector2(0.5f, 0);
            rectTransform.pivot = new Vector2(0.5f, 0);
            rectTransform.anchoredPosition = new Vector2(0, 20); // 20 units from the bottom
            rectTransform.sizeDelta = new Vector2(400, 50);

            // Ensure it doesn't block raycasts
            text.raycastTarget = false;
        }
    }
}
