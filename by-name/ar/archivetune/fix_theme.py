import re
with open('app/src/main/kotlin/moe/rukamori/archivetune/ui/theme/Theme.kt', 'r') as f:
    c = f.read()

# Replace MaterialExpressiveTheme
c = re.sub(
    r'MaterialExpressiveTheme\(\s*colorScheme = animatedColorScheme,\s*motionScheme = motionScheme,\s*typography = typography,\s*shapes = expressiveShapes,\s*content = content,\s*\)',
    r'androidx.compose.material3.MaterialTheme(\n            colorScheme = animatedColorScheme,\n            typography = typography,\n            content = content,\n        )',
    c, flags=re.MULTILINE
)

c = re.sub(
    r'MaterialExpressiveTheme\(\s*colorScheme = animatedColorScheme,\s*motionScheme = motionScheme,\s*typography = typography,\s*shape = expressiveShapes,\s*content = content,\s*\)',
    r'androidx.compose.material3.MaterialTheme(\n            colorScheme = animatedColorScheme,\n            typography = typography,\n            content = content,\n        )',
    c, flags=re.MULTILINE
)

# Replace motionScheme usage
c = re.sub(
    r'val motionScheme =\s*remember\(disableAnimations\) \{\s*if \(disableAnimations\) DisabledMotionScheme else MotionScheme\.expressive\(\)\s*\}',
    '',
    c, flags=re.DOTALL
)
c = re.sub(
    r'@OptIn\(ExperimentalMaterial3ExpressiveApi::class\)\s*private object DisabledMotionScheme : MotionScheme \{.*?\n\}\n',
    '',
    c, flags=re.DOTALL
)

# Remove animateColorScheme usages
c = re.sub(
    r'val animatedColorScheme =\s*if \(disableAnimations\) \{\s*colorScheme\s*\} else \{\s*animateColorScheme\(\s*targetColorScheme = colorScheme,\s*animationSpec = motionScheme\.defaultEffectsSpec\(\),\s*\)\s*\}',
    'val animatedColorScheme = colorScheme',
    c, flags=re.DOTALL
)

# Replace dynamicDarkColorScheme and dynamicLightColorScheme FOR REAL THIS TIME!
c = re.sub(r'dynamicDarkColorScheme\(.*?\)', 'androidx.compose.material3.darkColorScheme()', c, flags=re.DOTALL)
c = re.sub(r'dynamicLightColorScheme\(.*?\)', 'androidx.compose.material3.lightColorScheme()', c, flags=re.DOTALL)

# Remove dynamicColorScheme
c = re.sub(
    r'dynamicColorScheme\(\s*seedColor = seedColor,\s*isDark = isDark,\s*contrastLevel = contrastLevel,\s*style = style,\s*\)',
    r'if (isDark) androidx.compose.material3.darkColorScheme() else androidx.compose.material3.lightColorScheme()',
    c, flags=re.DOTALL
)

# Remove dynamic imports
c = re.sub(r'import com.materialkolor.dynamic.*?\n', '', c, flags=re.MULTILINE)
c = re.sub(r'import androidx.compose.material3.MaterialExpressiveTheme.*?\n', '', c, flags=re.MULTILINE)
c = re.sub(r'import androidx.compose.material3.MotionScheme.*?\n', '', c, flags=re.MULTILINE)
c = re.sub(r'import androidx.compose.material3.dynamicDarkColorScheme.*?\n', '', c, flags=re.MULTILINE)
c = re.sub(r'import androidx.compose.material3.dynamicLightColorScheme.*?\n', '', c, flags=re.MULTILINE)


c = c.replace('LocalArchiveTuneFontFamily provides resolvedFontFamily,', 'LocalArchiveTuneFontFamily provides (resolvedFontFamily as androidx.compose.ui.text.font.SystemFontFamily),')
c = re.sub(r'fun Bitmap\.extractThemeColor\(\): Color \{.*?\n\}', 'fun Bitmap.extractThemeColor(): Color { return DefaultThemeColor }', c, flags=re.DOTALL)
c = re.sub(r'fun Bitmap\.extractGradientColors\(\): List<Color> \{.*?\n\}', 'fun Bitmap.extractGradientColors(): List<Color> { return listOf(androidx.compose.ui.graphics.Color(0xFF595959), androidx.compose.ui.graphics.Color(0xFF0D0D0D)) }', c, flags=re.DOTALL)
c = re.sub(r'fun extractWallpaperThemeColor\(context: Context\): Color\? \{.*?\n\}', 'fun extractWallpaperThemeColor(context: Context): Color? { return null }', c, flags=re.DOTALL)

with open('app/src/main/kotlin/moe/rukamori/archivetune/ui/theme/Theme.kt', 'w') as f:
    f.write(c)

with open('app/src/main/kotlin/moe/rukamori/archivetune/ui/theme/Type.kt', 'r') as f:
    c = f.read()

c = c.replace('val AppFontFamily = FontFamily(Font(R.font.poppins))', 'val AppFontFamily = androidx.compose.ui.text.font.FontFamily.Default as androidx.compose.ui.text.font.SystemFontFamily')
c = c.replace('val LyricsFontFamily = FontFamily(Font(R.font.sfprodisplaybold))', 'val LyricsFontFamily = androidx.compose.ui.text.font.FontFamily.Default as androidx.compose.ui.text.font.SystemFontFamily')

with open('app/src/main/kotlin/moe/rukamori/archivetune/ui/theme/Type.kt', 'w') as f:
    f.write(c)

with open('app/src/main/kotlin/moe/rukamori/archivetune/ui/svg/DynamicSVGImage.kt', 'w') as f:
    f.write("""package moe.rukamori.archivetune.ui.svg

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color

@Composable
fun DynamicSVGImage(
    modifier: Modifier = Modifier,
    contentDescription: String? = null,
    svgString: String,
    color: Color = Color.Unspecified
) {}
""")

with open('app/src/main/kotlin/moe/rukamori/archivetune/ui/theme/CustomFontLoader.kt', 'w') as f:
    f.write("""package moe.rukamori.archivetune.ui.theme

import android.content.Context
import android.net.Uri
import androidx.compose.ui.text.font.FontFamily

object CustomFontLoader {
    fun displayName(context: Context, uri: Uri): String = ""
    fun isSupportedTtf(context: Context, uri: Uri): Boolean = false
    suspend fun loadFontFamily(context: Context, uriString: String): FontFamily? = androidx.compose.ui.text.font.FontFamily.Default
}
""")

import glob
for file in glob.glob('app/src/main/kotlin/moe/rukamori/archivetune/**/*.kt', recursive=True):
    with open(file, 'r') as f:
        content = f.read()
    if 'MaterialExpressiveTheme' in content:
        content = content.replace('MaterialExpressiveTheme.', 'MaterialTheme.')
        content = content.replace('import androidx.compose.material3.MaterialExpressiveTheme', 'import androidx.compose.material3.MaterialTheme')
        with open(file, 'w') as f:
            f.write(content)

# Create CompositionLocals.kt to restore the composition locals from deleted MainActivity.kt
import os
os.makedirs('app/src/main/kotlin/moe/rukamori/archivetune', exist_ok=True)
with open('app/src/main/kotlin/moe/rukamori/archivetune/CompositionLocals.kt', 'w') as f:
    f.write("""package moe.rukamori.archivetune

import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.runtime.staticCompositionLocalOf
import moe.rukamori.archivetune.db.MusicDatabase
import moe.rukamori.archivetune.playback.DownloadUtil
import moe.rukamori.archivetune.playback.PlayerConnection
import moe.rukamori.archivetune.utils.SyncUtils

val LocalDatabase = staticCompositionLocalOf<MusicDatabase> { error("No database provided") }
val LocalPlayerConnection =
    staticCompositionLocalOf<PlayerConnection?> { error("No PlayerConnection provided") }
val LocalPlayerAwareWindowInsets =
    compositionLocalOf<WindowInsets> { error("No WindowInsets provided") }
val LocalDownloadUtil = staticCompositionLocalOf<DownloadUtil> { error("No DownloadUtil provided") }
val LocalSyncUtils = staticCompositionLocalOf<SyncUtils> { error("No SyncUtils provided") }
""")
