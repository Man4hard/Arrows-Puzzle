using System.Collections.Generic;
using UnityEngine;
public class HeartPanel : MonoBehaviour {
    [SerializeField] private List<GameObject> _hearts = new List<GameObject>();
    private int MaxHearts { get { return 3; } }
    public void Initialize() {
        int expectedHearts = MaxHearts;
        int totalHearts = _hearts.Count;
        if (expectedHearts < totalHearts) {
            RectTransform panelRect = GetComponent<RectTransform>();
            if (panelRect != null) {
                float ratio = (float)expectedHearts / totalHearts;
                float width = panelRect.anchorMax.x - panelRect.anchorMin.x;
                float centerX = (panelRect.anchorMin.x + panelRect.anchorMax.x) / 2f;
                float newWidth = width * ratio;
                panelRect.anchorMin = new Vector2(centerX - newWidth / 2f, panelRect.anchorMin.y);
                panelRect.anchorMax = new Vector2(centerX + newWidth / 2f, panelRect.anchorMax.y);
                for (int i = 0; i < expectedHearts; i++) {
                    if (_hearts[i] != null) {
                        RectTransform childRect = _hearts[i].GetComponent<RectTransform>();
                        if (childRect != null) {
                            childRect.anchorMin = new Vector2(childRect.anchorMin.x / ratio, childRect.anchorMin.y);
                            childRect.anchorMax = new Vector2(childRect.anchorMax.x / ratio, childRect.anchorMax.y);
                        }
                    }
                }
            }
        }
    }
}
