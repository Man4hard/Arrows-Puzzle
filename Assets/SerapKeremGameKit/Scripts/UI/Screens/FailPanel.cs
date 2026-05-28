using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace SerapKeremGameKit._UI
{
	public sealed class FailPanel : UIPanel
    {
        [SerializeField] private Image _failIcon;
        [SerializeField] private TextMeshProUGUI _coinText;
        [SerializeField] private Button _restartButton;
        [SerializeField] private UIRootController _uiRoot;

		private Button _watchAdButton;

		private void Awake()
		{
			if (_restartButton != null) _restartButton.BindOnClick(this, OnRestartClicked);
			
			// Dynamically create a Watch Ad button by cloning the Restart button
			if (_restartButton != null)
			{
				_watchAdButton = Instantiate(_restartButton, _restartButton.transform.parent);
				_watchAdButton.transform.SetSiblingIndex(_restartButton.transform.GetSiblingIndex()); // Put above restart
				
				// Try to change text
				TextMeshProUGUI text = _watchAdButton.GetComponentInChildren<TextMeshProUGUI>();
				if (text != null) text.text = "Watch Ad to Continue";
				
				_watchAdButton.onClick.RemoveAllListeners();
				_watchAdButton.BindOnClick(this, OnWatchAdClicked);
			}
		}

		protected override void OnDestroy()
		{
			base.OnDestroy();
		}

        public void Setup(int rewardedCoins, UIRootController uiRoot)
        {
            if (_coinText != null) _coinText.text = rewardedCoins.ToString();
            _uiRoot = uiRoot;
        }

        private void OnRestartClicked()
        {
#if UNITY_IOS || UNITY_ANDROID
			if (SerapKeremGameKit._Ads.AdManager.IsInitialized)
			{
				SerapKeremGameKit._Ads.AdManager.Instance.ShowInterstitialAd(() => {
					if (_uiRoot != null) _uiRoot.OnRestartConfirmed();
				});
				return;
			}
#endif
			if (_uiRoot != null) _uiRoot.OnRestartConfirmed();
        }

		private void OnWatchAdClicked()
		{
#if UNITY_IOS || UNITY_ANDROID
			if (SerapKeremGameKit._Ads.AdManager.IsInitialized)
			{
				SerapKeremGameKit._Ads.AdManager.Instance.ShowRewardedAd(() => {
					// Give lives and resume
					if (_Game.UI.LivesManager.IsInitialized)
					{
						_Game.UI.LivesManager.Instance.ResetLives();
					}
					
					// Hide this panel and resume
					gameObject.SetActive(false);
					
					// Resume game logic
					SerapKeremGameKit._Managers.StateManager.Instance.SetOnStart();
					if (SerapKeremGameKit._InputSystem.InputHandler.Instance != null) 
					{
						SerapKeremGameKit._InputSystem.InputHandler.Instance.UnlockInput();
					}
				});
			}
#endif
		}

		public void SetUIRoot(UIRootController uiRoot)
		{
			_uiRoot = uiRoot;
		}
    }
}



