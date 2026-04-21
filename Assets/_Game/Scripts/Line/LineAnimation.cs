using System;
using UnityEngine;
using SerapKeremGameKit._Audio;
using SerapKeremGameKit._Haptics;

namespace _Game.Line
{
    public class LineAnimation : MonoBehaviour
    {
        private LineRenderer line;
        [SerializeField] private float speed = 5f;
        [SerializeField] private string _movementSoundKey = "click";
        [SerializeField] private AudioClip _clickSoundClip;

        private bool _isPlaying;
        private bool _forward;
        private Vector3 _direction;
        private Vector3[] positionsOrigin;
        private bool _isInitialized;
        private Vector3[] _tempPositionsArray;
        private Vector3ArrayPool _arrayPool;
        private float _visualZOffset;
        private AudioSource _audioSource;

        public bool IsPlaying => _isPlaying;
        public bool IsForward => _forward;
        public Vector3 Direction => _direction;
        public float VisualZOffset
        {
            get => _visualZOffset;
            set => _visualZOffset = value;
        }

        public event Action<bool> OnAnimationStarted;
        public event Action OnAnimationStopped;
        public event Action OnAnimationCompleted;
        public event Action OnLinePositionsChanged;

        public void Initialize(LineRenderer lineRenderer, Vector3ArrayPool arrayPool = null)
        {
            if (lineRenderer == null) return;

            line = lineRenderer;
            
            // Setup AudioSource for click sound
            _audioSource = gameObject.GetComponent<AudioSource>();
            if (_audioSource == null)
            {
                _audioSource = gameObject.AddComponent<AudioSource>();
                _audioSource.playOnAwake = false;
                _audioSource.spatialBlend = 0f;
            }
            if (_clickSoundClip != null)
            {
                _audioSource.clip = _clickSoundClip;
            }

            var count = line.positionCount;
            if (count < 2) return;

            positionsOrigin = new Vector3[count];
            for (int i = 0; i < count; i++)
            {
                positionsOrigin[i] = line.GetPosition(i);
            }

            var lastPoint = line.GetPosition(count - 1);
            _direction = lastPoint - line.GetPosition(count - 2);

            _arrayPool = arrayPool;

            _isInitialized = true;
            enabled = false;
        }

        public void Play(bool forwardDirection)
        {
            if (!_isInitialized || line == null || line.positionCount < 2)
                return;

            bool wasPlaying = _isPlaying;
            _forward = forwardDirection;
            _isPlaying = true;
            enabled = true;

            if (!wasPlaying)
            {
                OnAnimationStarted?.Invoke(forwardDirection);

                // Play click sound directly
                if (_audioSource != null && _audioSource.clip != null)
                {
                    _audioSource.Play();
                }
                
                if (AudioManager.IsInitialized && !string.IsNullOrEmpty(_movementSoundKey))
                    AudioManager.Instance.Play(_movementSoundKey);
                if (HapticManager.IsInitialized)
                    HapticManager.Instance.Play(HapticType.Selection);
            }
        }


        public void Stop()
        {
            if (_isPlaying)
            {
                _isPlaying = false;
                enabled = false;
                OnAnimationStopped?.Invoke();
            }

            if (_tempPositionsArray != null && _arrayPool != null)
            {
                _arrayPool.RecycleArray(_tempPositionsArray);
                _tempPositionsArray = null;
            }
        }

        private void OnDestroy()
        {
            if (_tempPositionsArray != null && _arrayPool != null)
            {
                _arrayPool.RecycleArray(_tempPositionsArray);
                _tempPositionsArray = null;
            }
        }

        private void Update()
        {
            if (!line || line.positionCount < 2)
            {
                _isPlaying = false;
                enabled = false;
                OnAnimationStopped?.Invoke();
                return;
            }

            if (_forward)
                AnimateForward();
            else
                AnimateBackward();
        }

        private void AnimateForward()
        {
            int count = line.positionCount;
            float moveDistance = speed * Time.deltaTime;
            
            // Optimization: Use a shared array to avoid multiple GetPosition/SetPosition calls
            Vector3[] positions = new Vector3[count];
            line.GetPositions(positions);

            // Move Head
            positions[count - 1] += _direction.normalized * moveDistance;

            // Move Tail - Make it slightly faster so it actually "fades" (shortens) over time
            float tailMoveDistance = moveDistance * 1.5f; 
            Vector3 nextPoint = positions[1];
            positions[0] = Vector3.MoveTowards(positions[0], nextPoint, tailMoveDistance);

            // Apply Z offset if needed in the same pass
            if (Mathf.Abs(_visualZOffset) > 0.001f)
            {
                for (int i = 0; i < count; i++) positions[i].z = _visualZOffset;
            }

            line.SetPositions(positions);
            OnLinePositionsChanged?.Invoke();

            // Check if segment should be removed
            if (Vector3.Distance(positions[0], nextPoint) < 0.05f) // Increased threshold for stability
            {
                int newCount = count - 1;
                if (newCount >= 2)
                {
                    line.positionCount = newCount;
                    Vector3[] nextPositions = new Vector3[newCount];
                    Array.Copy(positions, 1, nextPositions, 0, newCount);
                    line.SetPositions(nextPositions);
                }
                else
                {
                    line.positionCount = 0;
                    Stop(); // Use Stop() to ensure all flags are cleaned up
                    
                    // Force disable LineRendererHead to prevent it from getting stuck on screen
                    LineRendererHead head = GetComponentInChildren<LineRendererHead>(true);
                    if (head != null) head.gameObject.SetActive(false);

                    OnAnimationCompleted?.Invoke();
                }
                OnLinePositionsChanged?.Invoke();
            }
        }

        private void AnimateBackward()
        {
            int count = line.positionCount;
            float moveDistance = speed * Time.deltaTime;
            
            Vector3[] positions = new Vector3[count];
            line.GetPositions(positions);

            int lastIndex = count - 1;
            Vector3 originHeadPos = positionsOrigin[positionsOrigin.Length - 1];
            
            // Move Head Backward
            positions[lastIndex] = Vector3.MoveTowards(positions[lastIndex], originHeadPos, moveDistance);

            int countOrigin = positionsOrigin.Length;
            int targetIndex = countOrigin - count;

            if (targetIndex >= 0)
            {
                Vector3 targetTailPos = positionsOrigin[targetIndex];
                positions[0] = Vector3.MoveTowards(positions[0], targetTailPos, moveDistance);

                if (Vector3.Distance(positions[0], targetTailPos) < 0.05f) // Increased threshold
                {
                    if (targetIndex > 0)
                    {
                        // Add point back
                        int newCount = count + 1;
                        line.positionCount = newCount;
                        Vector3[] nextPositions = new Vector3[newCount];
                        nextPositions[0] = positionsOrigin[targetIndex - 1];
                        Array.Copy(positions, 0, nextPositions, 1, count);
                        line.SetPositions(nextPositions);
                    }
                    else if (Vector3.Distance(positions[lastIndex], originHeadPos) < 0.05f)
                    {
                        Stop(); // Ensure clean stop
                        OnAnimationCompleted?.Invoke();
                    }
                }
                else
                {
                    line.SetPositions(positions);
                }
                
                // Apply Z offset
                if (Mathf.Abs(_visualZOffset) > 0.001f)
                {
                    int currentCount = line.positionCount;
                    Vector3[] zPos = new Vector3[currentCount];
                    line.GetPositions(zPos);
                    for (int i = 0; i < currentCount; i++) zPos[i].z = _visualZOffset;
                    line.SetPositions(zPos);
                }
                
                OnLinePositionsChanged?.Invoke();
            }
        }
    }
}