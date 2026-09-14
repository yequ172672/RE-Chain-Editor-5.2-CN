<!-- FORK-MAINTENANCE -->
## 分支作者与维护说明

本分支由 **yequ172672** 维护，负责 Blender 5.2 适配、中文本地化和 OWOTS 支持。保留原作者及贡献者署名与原项目许可证。

- 分叉仓库：[RE-Chain-Editor-5.2-CN](https://github.com/yequ172672/RE-Chain-Editor-5.2-CN/tree/feat/onimusha-wots)
- 问题反馈：[分支 Issues](https://github.com/yequ172672/RE-Chain-Editor-5.2-CN/issues)
- 插件内“检查更新”查询本分叉的发行版 / 标签；更新版本菜单另提供 `feat/onimusha-wots` 开发分支。开发分支更新是手动安装分支快照，不代表按提交检测新版本。

<!-- /FORK-MAINTENANCE -->

# RE-Chain-Editor-5.2-CN

本分叉提供 Blender 5.2 下的 Onimusha: Way of the Sword 适配与简体中文界面。维护代码位于 [`feat/onimusha-wots`](https://github.com/yequ172672/RE-Chain-Editor-5.2-CN/tree/feat/onimusha-wots) 分支；`main` 保留上游版本。

在 Blender「编辑 → 偏好设置 → 界面 → 翻译」中选择简体中文，并启用界面和工具提示翻译。插件会随 Blender 语言切换，英文环境仍显示英文；文件格式标识、游戏代号和操作符接口保持原样。

建议安装打包后的 `RE-Chain-Editor-5.2-CN.zip`。ZIP 文件名可以带 `5.2-CN`，但 ZIP 内部的顶层模块目录必须保持 `RE-Asset-Library-main`、`RE-Mesh-Editor-main`、`RE-Chain-Editor-main`，以兼容已有插件设置。不要直接安装 GitHub「Code → Download ZIP」源码包，也不要把内部目录改成带点号的 `*-5.2-CN`；Blender 会把点号当作 Python 模块分隔符，导致 `No module named '...-5'`。安装新版时替换同名旧插件，避免同时启用多个副本。

---

# End Of Support Notice

I am ending development of my RE Engine addons. No further updates or support will be provided.

Feel free to fork the project if you want to.

---

![REChainEditorTitle](https://github.com/NSACloud/RE-Chain-Editor/assets/46909075/e74f6ac0-e7c7-4f26-94af-0cf1ff9e95ee)

**V14.0 (2/27/2026)**

[Change Log](https://github.com/NSACloud/RE-Chain-Editor?tab=readme-ov-file#change-log)

This addon allows for importing and exporting of RE Engine chain (physics bone) files from Blender.

Also supports collision shape (.clsp) files.

![Blender Preview](https://github.com/user-attachments/assets/d8c2ebd7-01bb-48ac-963b-6e9f921627cb)

### [Download RE Chain Editor](https://github.com/NSACloud/RE-Chain-Editor/archive/refs/heads/main.zip)

## Features
 - Allows for importing and exporting of RE Engine chain (and chain2) files.
 - Can create new chain files entirely within Blender.
 - Presets of chain configurations can be saved and shared.



## Change Log

### V14.0 - 2/27/2026
* Added Resident Evil 9 support.
* When using Align Bone Tails to Axis, roll will automatically be set to 0.

### V13.0 - 2/6/2026
* Added Monster Hunter Stories 3 support.
* Fixed issue where Blender would get stuck if Align Angle Limits to Next Node was run on a chain group that has a jiggle node on the last chain node.

### V12.1 - 12/17/2025
* Updated MH Wilds chain2 version to 14.

### V12.0 - 12/15/2025
* Added Pragmata support.
* When a chain collection is selected in the export menu, the file name will change automatically.

### V11.4 - 10/26/2025
* Improved compatibility with the new batch exporter in RE Mesh Editor.

### V11.3 - 8/19/2025
* Fixed issue where collision capsule offsets weren't imported.
* Fixed error that occurred when importing Alma's summer outfit chain file.

### V11.2 - 7/16/2025
* Fixed issues with geometry nodes on Blender 4.5.

### V11.1 - 6/1/2025
* Fixed issue where exporting a CLSP file with a sphere collision would cause an error.

### V11.0 - 2/28/2025
* Added support for the full release of Monster Hunter Wilds.
* Added unknown values to the chain2 header for MH Wilds.
* Added dropdown menu for setting CFIL paths on chain settings.
* Fixed issue where certain flags on chain settings attribute flags would behave incorrectly.
* Fixed issue where collision capsules could be misaligned.

### V10.1 - 1/18/2025
* Fixed chain2 chain link export issue.

### V10.0 - 1/18/2025

* Added chain2 import/export support.
* Labelled all previously unknown values (with exception of chain2 setting subdata).
* Added new chain setting presets for MH Wilds.
* Added new menus for configuring attribute flags, click the drop down menu on the right of an attribute flag value to change it.
* Chain groups are now represented visually via a line through all of it's nodes.
* Added support for chain sub groups. These allow for chain groups to be assigned different chain and node settings based on their subgroup ID.
* Chain sub groups nodes are represented with purple angle limit cones.
* Moved all chain editor file import/export options into File > Import/Export > RE Chain Editor.
* Added constraint joint field to chain nodes.
* Added field in the Pose Mode RE Chain menu to create and assign chain settings to newly created chain groups.
* Fixed issue with assignment of chain settings to groups.
* Removed "Chain Entries" collection to make the chain header hierarchy less confusing.
* Changed chain jiggle settings to make them more usable at their default settings.
* Newly imported chain and clsp files will be grouped in the same collection as the mesh and mdf files.
* Fixed compatibility issue with Blender 4.3.
* Fixed issue where copying chain node settings with the clipboard would not update the collision radius of a node when pasted.
* UI/UX improvements.
* Added license.

### V9.1 - 7/25/2024

* Reverted changes made to chain settings indices in the previous version as it causes issues with exported chains in certain situations.

### V9.0 - 7/9/2024

* Added Collision Shape Preset (.clsp) import and export support.

This is Capcom's new file format used for storing chain (and gpuc) collisions.

For an explanation on how the CLSP collision system works, see this video from Capcom R&D: 

https://www.youtube.com/watch?v=RPx6HPxqosE

* Fixed issue where exported chain and wind settings were referenced by their ID instead of index.

<details>
  <summary>Older Version Change Logs</summary>

### V8.1 - 5/22/2024

* Fixed incompatibility with Blender 3.4 - 3.6

### V8 - 5/20/2024

NOTE: If you're updating from a previous version, you have to delete any chains saved to a blend file and reimport the chain file for them to work properly.

* Visuals have been overhauled. Chain objects now have colors and more accurately represent their functionality visually.
* Chain link collisions have been added. This adds collision between linked chains and can greatly reduce clipping.
* Chain links can have collisions assigned to them by using the "Create Chain Link Collision" button with a chain link selected.
* Chain links now draw a line between the chain groups they are attached to.
* Added support for tapered capsules. This allows for collision capsules to have a different radius on each end. This is only supported on chain version 46 and above. If exporting an older version, the end radius will be corrected to match the start radius. 
* Chain objects are now organized into collections to make managing them easier.
* The naming scheme of chain collisions and chain links have been changed to visually show what bones they attach to.
* Bones assigned to chains are now colored green.
* The RE Chain Visiblity panel has been organized into sub menus with several new options added.
* The last angle limit cone of a chain is now hidden by default. This is because the last chain node typically isn't used. This can be changed under Visibility > Angle Limit Settings > Hide Last Node Cone.
* Fixed issue where collisions were not imported correctly in RE2/RE3 RT.
* Minor bug fixes

### V7 - 4/28/2024

* Added RE Toolbox integration. Any chain files exported will be added to RE Toolbox's batch export list.
* Fixed bug with getting the armature object to attach chains to.


### V6 - 4/20/2024

If you are updating to V6, uncheck RE Chain Editor in the addons menu and restart Blender before installing the new version.

* Added support for meshes imported with RE Mesh Editor.
* Added addon updater functionality, the addon can now be updated directly from Preferences > Add-ons > RE Chain Editor
* Chains now use collections. This allows for multiple chain files to be in a scene at the same time.
* Added Target Armature import option. This allows you to specify which armature to attach the chain to.
* Added Merge Chain Collection import option. This allows for newly chain files to be merged with an existing chain collection.
* Added Active Chain Collection field to the Object Mode Tools and Pose Mode Tools panels. This determines where newly created chain objects will be assigned.
* Added Chain Collection export option. This allows you to specify which chain collection to export.
* Added Hide Non Collisions option to the Visibility panel.
* Chain collisions can now be moved and scaled like normal objects to set their position and radius. Previously, these would have to be set in collision settings menu.
* The default angle limit orientation for newly created chains has been altered so that the first angle limit points towards the next bone.
* Added Dragon's Dogma 2 support (untested)
* Various bug fixes

### V5 - 9/11/2023

* Fixed an issue where Street Fighter 6 chain settings did not import or export correctly. Any previously imported chains saved in a blend file should be reimported.
* Fixed issue causing crashes with SF6 due to certain data being missing when importing certain chain files.
* Chain collisions now show the bone they're connected to in their name.

NOTE: Due to them containing lots of currently unmapped data, certain SF6 chain files such as Kimberly's cannot be imported without them having issues in game when exported.

### V4 - 4/16/2023

* Added support for RE:Verse.
* Added experimental features under the Pose Mode tools. This allows for things such as chains connected to chains and single bone capsule collisions. Be warned that there is no error checking if you make a mistake. Use at your own risk.
* Minor bug fixes.

### V3 - 4/13/2023

* Added support for Resident Evil 4.
* Moved exporting of all chain versions to a single export menu. Choose which game to export for in the top right when exporting.
 
### V2 - 2/18/2023

If you are updating to V2 from a previous version, any chain files previously saved to Blender have to be reimported.

This is because certain settings have been stored differently compared to the previous version and it will cause issues when exporting.

**New Features:**
* Angle limit orientation is now set automatically when creating new chains. Manual adjustments may still be required at times.
* Chain nodes now have cones to display angle limits.
* In the Object Mode Tools panel, added 2 new buttons for aligning angle limits and setting an angle limit radius ramp across a chain.
* In the Object Mode Visibility panel, added buttons for hiding non chain objects to make selecting things quicker.
* In the Pose Mode Tools panel, added 2 new buttons for renaming bone chains and aligning bone tails to an axis.
* Angle limit object orientations can now be copied and pasted using the clipboard.
* Added support for collision filter file (.cfil) paths to chain settings.
* Added support for collision subdata (For RE2 RT).
* Several minor bug fixes.
 
 </details>
 
 ## Supported Games
 - **Monster Hunter Rise: Sunbreak**
 - **Resident Evil 2 Remake**
 - **Resident Evil 3 Remake**
 - **Resident Evil 4 Remake**
 - **Resident Evil 8**
 - **Devil May Cry 5**
 - **Street Fighter 6**
 - **Dragon's Dogma 2**
 - **Dead Rising Deluxe Remaster**
 - **Monster Hunter Wilds**
 
Support for more games may be added in the future.

## Requirements
* [Blender 2.93 or higher](https://www.blender.org/download/)
* [RE Mesh Editor](https://github.com/NSACloud/RE-Mesh-Editor)

OR
* [Blender RE Mesh Noesis Wrapper (Deprecated)](https://github.com/NSACloud/Blender-RE-Mesh-Noesis-Wrapper)
## Installation
Download the addon by clicking Code > Download Zip.

In Blender, go to Edit > Preferences > Addons, then click "Install" in the top right.

Navigate to the downloaded zip file for this addon and click "Install Addon". The addon should then be usable.

To update this addon, navigate to Preferences > Add-ons > RE Chain Editor and press the "Check for update" button.

## Usage Guide

The full guide can be found here.

https://github.com/mhvuze/MonsterHunterRiseModding/wiki/Editing-Chains-with-RE-Chain-Editor

**TL;DR Usage Guide**

1. Import a mesh and add bones to be used as physics bones to the armature.
2. Create a chain header, then a chain settings object in the RE Chain tab in Object mode.
3. Switch to pose mode, select the start bone and press "Create Chain From Bone" for each chain.
4. (Optional) Add collisions to bones by selecting a bone and pressing "Create Collision From Bone".
5. Parent the chain group objects to the chain settings objects in the outliner
6. (Optional) Create wind settings and parent the chain settings to it to give it wind effects.
7. Configure chain objects in the Object properties tab, or apply presets
8. Adjust the chain node XYZ angle limits if necessary
9. Export from File > Export > RE Chain Editor

**For additional help, go here:**

[Monster Hunter Modding Discord](https://discord.gg/gJwMdhK)

[Modding Haven Discord](https://discord.gg/modding-haven-718224210270617702)

 ## Credits
 - [AsteriskAmpersand](https://github.com/AsteriskAmpersand) - Advice and inspiration from CTC Editor
- [Statyk](https://www.youtube.com/channel/UC2nEkiSL_X7xh6QHJcS0Wjw) - Beta testing and feedback
- [AlphaZomega](https://github.com/alphazolam/) - RE Chain 010 Template, Modified this addon to work in all games and other bugfixes/additions
- [CG Cookie](https://github.com/CGCookie) - Addon updater module

## 鬼武者：剑之道 Chain2 / FBXSkel 导出

- 物理链选择 **RE Chain2 → 鬼武者：剑之道**，扩展名为 `.chain2.17`。本地游戏索引中有 443 个 Chain2 文件，没有旧 `.chain` 文件。
- 骨架选择 **RE FBXSkel → 怪猎荒野 / 物语 3 / 鬼武者：剑之道 (.7)**，扩展名为 `.fbxskel.7`。导出窗口优先采用目标对象/集合记录的导入版本。
- “RE9 导出后改一个字节”仅验证适用于 FBXSkel：偏移 `0x00` 的 `08` 改为 `07`，同时扩展名必须为 `.7`。现在直接选择 `.7`，无需手改。337 个原始骨架全部逐字节写回一致。
- Chain2 不能如此转换：RE9 v15 与鬼武者 v17 的 Header 分别为 128 与 112 字节，表偏移和布局不同，必须通过 v17 写出。
- 443 个原始 Chain2 全部通过读取—写入—重读字段校验及重复写入稳定性检查。5 个文件中的 81 条 free-link 已支持原样保留参数/端点并重定位；暂不提供 free-link 的独立编辑或合并，不允许带这些数据降级导出为旧版本。
- 若对应 Mesh 缺少部分链骨骼，导入 Chain2 时启用 **Import Unknown Hashes / 导入未知哈希** 可保留相关记录。未匹配的骨骼不会因此获得正确的视口绑定；正常物理预览仍需完整骨架。旧场景里已经丢失的记录需从原始文件重新导入。

Blender 5.2 已验证 3 个角色骨架的层级、变换与缩放，以及普通 Chain2 的 22 组/82 节点和带 free-link 样本的导出、保存重开。骨架局部变换最大误差小于 `2.4e-6`。这些是二进制和 Blender 验证，尚未完成游戏内物理/动画验收。
