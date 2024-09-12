1. FK（Forward Kinematics）控制器：

    Spine1: 添加控制器以操控脊柱的旋转。
    Chest: 添加控制器以操控胸部的旋转。
    Neck: 添加控制器以操控颈部的旋转。
    Head: 添加控制器以操控头部的旋转。
    Shoulder: 添加控制器以操控肩部的旋转。
    Elbow: 添加控制器以操控肘部的旋转。
    Wrist: 添加控制器以操控手腕的旋转。
    Hip: 添加控制器以操控髋部的旋转。
    Knee: 添加控制器以操控膝部的旋转。
    Ankle: 添加控制器以操控脚踝的旋转。

2. IK（Inverse Kinematics）控制器：

    Spine1: IK 目标用于控制整个脊柱链的弯曲。
    Shoulder: IK 控制器用于控制肩部到肘部的动作。
    Elbow: IK 控制器用于控制肘部到手腕的动作。
    Hip: IK 控制器用于控制髋部到膝部的动作。
    Knee: IK 控制器用于控制膝部到脚踝的动作。

3. 手部控制器：

    Wrist: 控制手腕的旋转和位置。
    MiddleFinger1, ThumbFinger1, IndexFinger1, Cup: 分别为每个手指的主要关节添加控制器。
    FingerEnd: 为每个手指的末端添加控制器，以便精细调整手指的动作。

4. 脚部控制器：

    Heel: 控制脚跟的旋转和位置。
    Toes: 控制脚趾的旋转和位置。
    FootSideInner / FootSideOuter: 控制脚的内侧和外侧。

5. 附加控制器：

    Neck: 添加控制器以控制颈部的转动范围和姿势。
    HeadEnd: 控制头部的细微调整。
    Jaw: 控制下巴的开合。
    Scapula: 控制肩胛骨的动作，帮助模拟肩部的自然运动。

6. 约束和目标：

    目标约束：在 IK 控制器中使用目标约束来引导骨骼链。
    点约束：用于固定骨骼位置。
    方向约束：用于限制骨骼的旋转方向。
