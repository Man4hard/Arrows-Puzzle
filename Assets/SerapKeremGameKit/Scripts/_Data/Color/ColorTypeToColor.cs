using UnityEngine;
using SerapKeremGameKit._Enums;

namespace SerapKeremGameKit._Color
{
    public static class ColorTypeToColor
    {
        public static Color GetColor(ColorType colorType)
        {
            return colorType switch
            {
                ColorType._0Empty => Color.clear,
                ColorType._1Green => new Color(0.65f, 0.93f, 0.79f), // Pastel Mint
                ColorType._2Blue => new Color(0.68f, 0.85f, 0.90f), // Pastel Baby Blue
                ColorType._3Red => new Color(1.00f, 0.60f, 0.60f), // Pastel Coral Red
                ColorType._4Yellow => new Color(0.99f, 0.93f, 0.65f), // Pastel Lemon
                ColorType._5Purple => new Color(0.82f, 0.73f, 0.91f), // Pastel Lavender
                ColorType._6Pink => new Color(1.00f, 0.71f, 0.80f), // Pastel Rose
                ColorType._7Orange => new Color(1.00f, 0.80f, 0.60f), // Pastel Peach
                ColorType._8Turquoise => new Color(0.55f, 0.88f, 0.82f), // Pastel Aqua
                ColorType._9DarkBlue => new Color(0.40f, 0.50f, 0.65f), // Muted Denim
                ColorType._qBrown => new Color(0.80f, 0.65f, 0.55f), // Mocha
                ColorType._wBlack => new Color(0.20f, 0.20f, 0.20f), // Soft Charcoal
                ColorType._eNone => new Color(0f, 0f, 0f, 0f), 
                _ => Color.black 
            };
        }
    }
}