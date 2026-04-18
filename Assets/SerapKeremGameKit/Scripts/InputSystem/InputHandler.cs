using SerapKeremGameKit._Singletons;
using UnityEngine;
using SerapKeremGameKit._InputSystem.Data;

namespace SerapKeremGameKit._InputSystem
{
    public class InputHandler : MonoSingleton<InputHandler>
    {
        [Header("Input Settings")]
        [SerializeField, Tooltip("Scriptable object for managing player input.")]
        private PlayerInputSO _playerInput;

        private bool _isInputLocked = false; // Indicates whether input is currently locked

        public bool IsInputLocked { get => _isInputLocked; }

        protected override void Awake()
        {
            base.Awake();
        }

        private void Update()
        {
            if (_isInputLocked) return; 
            
            _playerInput.ResetFrame();
            ProcessMouseInput();
        }

        private void ProcessMouseInput()
        {
            // Use Touch input if available for faster response on mobile
            if (Input.touchCount > 0)
            {
                Touch touch = Input.GetTouch(0);
                Vector3 touchPos = touch.position;

                if (touch.phase == TouchPhase.Began)
                {
                    _playerInput.SetMouseDown(touchPos);
                }
                else if (touch.phase == TouchPhase.Moved || touch.phase == TouchPhase.Stationary)
                {
                    _playerInput.SetMouseHeld(touchPos);
                }
                else if (touch.phase == TouchPhase.Ended || touch.phase == TouchPhase.Canceled)
                {
                    _playerInput.SetMouseUp(touchPos);
                }
            }
            else // Fallback to Mouse input for Editor and non-touch devices
            {
                Vector3 mousePosition = Input.mousePosition;

                if (Input.GetMouseButtonDown(0))
                {
                    _playerInput.SetMouseDown(mousePosition);
                }
                else if (Input.GetMouseButton(0))
                {
                    _playerInput.SetMouseHeld(mousePosition);
                }
                else if (Input.GetMouseButtonUp(0))
                {
                    _playerInput.SetMouseUp(mousePosition);
                }
            }
        }

        public void UnlockInput()
        {
            _isInputLocked = false;
        }

        public void LockInput()
        {
            _isInputLocked = true;
        }
    }
}