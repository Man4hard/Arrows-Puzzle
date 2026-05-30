import re

file_path = "ProjectSettings/ProjectSettings.asset"

with open(file_path, "r") as f:
    content = f.read()

# Replace applicationIdentifier for Android
content = re.sub(
    r"Android: com.UnityTechnologies.com.unity.template.urpblank",
    r"Android: com.man4hard.arrowspuzzle",
    content
)

# Enable ARM64 by adding 1 to AndroidArchitecture
# Default usually: AndroidArchitecture: 1 (ARMv7). ARM64 is 2. Both is 3. We'll set to 3.
content = re.sub(
    r"AndroidArchitecture: \d+",
    r"AndroidArchitecture: 3",
    content
)

# Ensure Target API is 34
content = re.sub(
    r"AndroidTargetSdkVersion: \d+",
    r"AndroidTargetSdkVersion: 34",
    content
)

# Ensure AppBundle is true (this might be in EditorUserBuildSettings which is in Library or UserSettings, but we can try adding to ProjectSettings if we want, or we can just leave it as instructions for the user)

with open(file_path, "w") as f:
    f.write(content)

print("ProjectSettings.asset modified successfully.")
