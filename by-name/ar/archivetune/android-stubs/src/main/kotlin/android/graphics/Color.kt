package android.graphics

object Color {
    @JvmStatic fun colorToHSV(color: Int, hsv: FloatArray) {}
    @JvmStatic fun parseColor(colorString: String): Int = 0
    @JvmStatic fun rgb(red: Int, green: Int, blue: Int): Int = 0
    @JvmStatic fun argb(alpha: Int, red: Int, green: Int, blue: Int): Int = 0
    const val BLACK = -16777216
    const val DKGRAY = -12303292
    const val GRAY = -7829368
    const val LTGRAY = -3355444
    const val WHITE = -1
    const val RED = -65536
    const val GREEN = -16711936
    const val BLUE = -16776961
    const val YELLOW = -256
    const val CYAN = -16711681
    const val MAGENTA = -65281
    const val TRANSPARENT = 0
}
