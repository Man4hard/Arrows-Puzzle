using UnityEngine;
using UnityEngine.Advertisements;
using System;
using SerapKeremGameKit._Singletons;
using SerapKeremGameKit._Logging;

namespace SerapKeremGameKit._Ads
{
    public class AdManager : MonoSingleton<AdManager>, IUnityAdsInitializationListener, IUnityAdsLoadListener, IUnityAdsShowListener
    {
        [SerializeField] private string _androidGameId = "1234567";
        [SerializeField] private string _iOSGameId = "1234568";
        [SerializeField] private bool _testMode = true;
        
        [SerializeField] private string _rewardedAdUnitIdAndroid = "Rewarded_Android";
        [SerializeField] private string _rewardedAdUnitIdIOS = "Rewarded_iOS";
        [SerializeField] private string _interstitialAdUnitIdAndroid = "Interstitial_Android";
        [SerializeField] private string _interstitialAdUnitIdIOS = "Interstitial_iOS";

        private string _gameId;
        private string _rewardedAdUnitId;
        private string _interstitialAdUnitId;

        private Action _onRewardedAdCompleted;
        private Action _onAdClosed;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
        private static void AutoInitialize()
        {
            if (!IsInitialized)
            {
                GameObject go = new GameObject("AdManager");
                go.AddComponent<AdManager>();
                DontDestroyOnLoad(go);
            }
        }

        protected override void Awake()
        {
            base.Awake();
            if (Instance != this) return;
            InitializeAds();
        }

        private void InitializeAds()
        {
#if UNITY_IOS
            _gameId = _iOSGameId;
            _rewardedAdUnitId = _rewardedAdUnitIdIOS;
            _interstitialAdUnitId = _interstitialAdUnitIdIOS;
#else
            _gameId = _androidGameId;
            _rewardedAdUnitId = _rewardedAdUnitIdAndroid;
            _interstitialAdUnitId = _interstitialAdUnitIdAndroid;
#endif

            if (!Advertisement.isInitialized && Advertisement.isSupported)
            {
                Advertisement.Initialize(_gameId, _testMode, this);
            }
        }

        public void LoadRewardedAd()
        {
            Advertisement.Load(_rewardedAdUnitId, this);
        }

        public void LoadInterstitialAd()
        {
            Advertisement.Load(_interstitialAdUnitId, this);
        }

        public void ShowRewardedAd(Action onCompleted, Action onClosed = null)
        {
            _onRewardedAdCompleted = onCompleted;
            _onAdClosed = onClosed;
            Advertisement.Show(_rewardedAdUnitId, this);
            LoadRewardedAd(); // preload next
        }

        public void ShowInterstitialAd(Action onClosed = null)
        {
            _onAdClosed = onClosed;
            Advertisement.Show(_interstitialAdUnitId, this);
            LoadInterstitialAd(); // preload next
        }

        // --- Interfaces ---

        public void OnInitializationComplete()
        {
            TraceLogger.Log("Unity Ads initialization complete.");
            LoadRewardedAd();
            LoadInterstitialAd();
        }

        public void OnInitializationFailed(UnityAdsInitializationError error, string message)
        {
            TraceLogger.LogError($"Unity Ads Initialization Failed: {error.ToString()} - {message}");
        }

        public void OnUnityAdsAdLoaded(string adUnitId)
        {
            TraceLogger.Log("Ad Loaded: " + adUnitId);
        }

        public void OnUnityAdsFailedToLoad(string adUnitId, UnityAdsLoadError error, string message)
        {
            TraceLogger.LogError($"Error loading Ad Unit {adUnitId}: {error.ToString()} - {message}");
        }

        public void OnUnityAdsShowFailure(string adUnitId, UnityAdsShowError error, string message)
        {
            TraceLogger.LogError($"Error showing Ad Unit {adUnitId}: {error.ToString()} - {message}");
            _onAdClosed?.Invoke();
        }

        public void OnUnityAdsShowStart(string adUnitId) { }
        public void OnUnityAdsShowClick(string adUnitId) { }

        public void OnUnityAdsShowComplete(string adUnitId, UnityAdsShowCompletionState showCompletionState)
        {
            if (adUnitId.Equals(_rewardedAdUnitId) && showCompletionState == UnityAdsShowCompletionState.COMPLETED)
            {
                TraceLogger.Log("Rewarded Ad Completed. Granting reward.");
                _onRewardedAdCompleted?.Invoke();
            }

            _onAdClosed?.Invoke();
        }
    }
}
