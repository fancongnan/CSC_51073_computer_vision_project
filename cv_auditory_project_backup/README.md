## File Structure and System Configuration

For the **Kinesthetic Sonics** system to load and function correctly, the following file structure and manual configuration steps are required:

### 1. File Placement and Dependencies

The primary TouchDesigner project file, **`cv_auditory_project.toe`**, must be located in the same directory as the **`toxes`** folder.

* This is essential for the main project file to correctly instantiate and reference all dependent components (sub-networks) stored within the `toxes` directory. These components, often custom modules or complex logic encapsulated as **`.tox`** files, rely on relative file paths for successful initialization.

### 2. Audio Source Configuration

TouchDesigner project files specify absolute or relative file paths that **do not automatically adjust** when downloaded or moved to a new host machine. Therefore, manual intervention is necessary for audio playback:

* **Action Required:** To ensure sound generation, the user must manually re-specify the file path within the **`Audio File In CHOP`** operator(s) located inside the main `.toe` file.
* The **`File`** parameter of these operators must be pointed to the specific audio assets residing in the **`audio_source`** folder of the local directory.

### 3. Audio Mapping Reference Table

Since file paths are local, please refer to the table below to map the correct source files (located in the **`audio_source`** folder) to their corresponding **`Audio File In`** operators within the project network:

| Operator Name (Node) | Target File Name | Sound Category |
| :--- | :--- | :--- |
| **`audiofilein11`** | `beat1.mp3` | Rhythm / Beat |
| **`audiofilein12`** | `beat2.mp3` | Rhythm / Beat |
| **`audiofilein3`** | `beat3.mp3` | Rhythm / Beat |
| **`audiofilein4`** | `beat4.mp3` | Rhythm / Beat |
| **`audiofilein9`** | `electronics1.mp3` | Synth / FX |
| **`audiofilein10`** | `electronics2.mp3` | Synth / FX |
| **`audiofilein5`** | `environment1.mp3` | Ambience |
| **`audiofilein6`** | `environment2.mp3` | Ambience |
| **`audiofilein7`** | `latin1.mp3` | Melodic / Style |
| **`audiofilein8`** | `latin2.mp3` | Melodic / Style |

> **Note:** Ensure all files are loaded from the `audio_source` directory to maintain correct playback.


---

**Summary of Action Items:**

| File/Folder | Requirement | Action |
| :--- | :--- | :--- |
| **`cv_auditory_project.toe`** | Must be alongside **`toxes`** | Ensure correct relative path for sub-modules. |
| **`Audio File In CHOP`** | Collate path after transfer. | **Manually update** the **`File`** parameter. |


