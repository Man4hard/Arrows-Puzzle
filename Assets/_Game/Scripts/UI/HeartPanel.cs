using System.Collections.Generic;
using UnityEngine;
using SerapKeremGameKit._UI;

namespace _Game.UI
{
    public class HeartPanel : MonoBehaviour
    {
        [Header("Heart References")]
        [SerializeField] private List<HeartUI> _hearts = new List<HeartUI>();

        private bool _isInitialized = false;

        private int MaxHearts
        {
            get
            {
                if (LivesManager.IsInitialized && LivesManager.Instance != null)
                {
                    return LivesManager.Instance.MaxLivesCount;
                }
                return 5; // Fallback default
            }
        }

        public void Initialize()
        {
            if (_isInitialized) return;

            int expectedHearts = MaxHearts;
            int totalHearts = _hearts.Count;

            if (expectedHearts < totalHearts)
            {
                RectTransform panelRect = GetComponent<RectTransform>();
                if (panelRect != null)
                {
                    float ratio = (float)expectedHearts / totalHearts;
                    
                    // Center the panel but shrink its width
                    float width = panelRect.anchorMax.x - panelRect.anchorMin.x;
                    float centerX = (panelRect.anchorMin.x + panelRect.anchorMax.x) / 2f;
                    float newWidth = width * ratio;
                    
                    panelRect.anchorMin = new Vector2(centerX - newWidth / 2f, panelRect.anchorMin.y);
                    panelRect.anchorMax = new Vector2(centerX + newWidth / 2f, panelRect.anchorMax.y);
                    
                    // Adjust children anchors so they fill the new smaller panel
                    for (int i = 0; i < expectedHearts; i++)
                    {
                        if (_hearts[i] != null)
                        {
                            RectTransform childRect = _hearts[i].GetComponent<RectTransform>();
                            if (childRect != null)
                            {
                                childRect.anchorMin = new Vector2(childRect.anchorMin.x / ratio, childRect.anchorMin.y);
                                childRect.anchorMax = new Vector2(childRect.anchorMax.x / ratio, childRect.anchorMax.y);
                            }
                        }
                    }
                }
            }

            foreach (var heart in _hearts)
            {
                if (heart != null)
                {
                    heart.Initialize();
                }
            }

            _isInitialized = true;
        }

        public void UpdateHearts(int activeLives)
        {
            int max = MaxHearts;
            for (int i = 0; i < _hearts.Count; i++)
            {
                if (_hearts[i] != null)
                {
                    if (i >= max)
                    {
                        _hearts[i].gameObject.SetActive(false);
                    }
                    else
                    {
                        _hearts[i].gameObject.SetActive(true);
                        bool isActive = i < activeLives;
                        _hearts[i].SetActive(isActive);
                    }
                }
            }
        }

        public void ResetHearts()
        {
            UpdateHearts(MaxHearts);
        }
    }
}
