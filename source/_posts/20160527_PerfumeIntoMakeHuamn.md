---
title: 新しい骨をMakeHuamnモデルに入れ込む
date: 2016-05-28 11:04:20
tags: blender
categories: CG
---

-------------------------------------

# はじめに

## Makehuamn1.1.0を使った

- [Makehuman1.1.0](http://download.tuxfamily.org/makehuman/releases/1.1.0/makehuman-1.1.0-win32.zip)
- 05/15/2016リリースされた最新安定版です。

![makehuman-log](/images/20160525_makehuman_log.png)

## Blender2.77aを使った

- [Blender2.77a](http://mirror.cs.umn.edu/blender.org/release/Blender2.77/blender-2.77a-windows64.msi)
- 03/19/2016リリースされた最新版、前より100以上のバッグを修正した。

![makehuman-log](/images/20160525_blender_log.png)

## 随分重要なショートカット

CG系/PS系ソフトは、ショートカットやっぱり非常に重要です。
下記ショートカットは勉強途中で記録された重要な部分です。
特に「★」の部分、使わなければいけない。

- save user setting
    - key: ctrl-u
- enlarge/return selected window
    - key: ctrl-↑/↓
- mode change
    - key: tab, ctrl+tab
- soild/wireframe
    - key: z
- ★(de)select all
    - key: a
- add object
    - key: shift-a
- move to layer
    - m
- ★increament select
    - shift MRB(mouse right button)
- ★rectangle select
    - b
- ★region select
    - ctrl-MLB
- herical cut
    - ctrl-r
- zero rotation
    - alt-r
- IK(Inverse Kinematics constraint)
    - shift-i (under pose mode)
- join 2 mesh
    - ctrl-j
- ★add vertex-bone weight automaticly
    - select target mesh (RMB)
    - select target skeleton (shift-RMB)
    - ctrl-p (with automatic weight)
- 位置を微調整
    - shift常に押す

-------------------------------------

# makehumanの人体モデル

## モデルを作成

[makehumanの使い方資料](http://www.aversionofreality.com/blog/2014/1/14/makehuman-starting-tips)ご参考してください。

## 人体モデルをCOLLADAタイプでexport

blenderに導入する前、一回makehumanでexport必要です。今回COLLADAexportしました。
exportする時、幾つご注意しなければいけないポイントがある:

- 眼球のジオメトリを削除: Geometries→Eyes→None

![no_eyes](/images/20160525_no_eyes.png)

- リグをCmu mbに設定: Pose/Animate→Skeleton→Cmu mb

![cmu_mb](/images/20160525_cmu_mb.png)

- 姿勢をt-poseでリセット: Pose/Animate→Pose→Tag filter: Rest poses→Tpose

![reset_poses](/images/20160525_reset_poses.png)

- Exportについて: Files→Export
    - Mesh Format: Collada (dae)
    - Options: 全部チェックしない(perfumeのTPOSのrootは原点ですので、Feet on groundも無)
    - Orientation: Z up, face -Y
    - Bone orientation: Along local Y
    - Scale unites: meter

![export_setting](/images/20160526_export_setting_for_perfume.png)

- 全部設定したら、exportして、完了した。

----------------------------------------

# Blenderで人体モデルの骨を切り替え

## Makehumanモデルをimport

![type12](/images/20160526_import_type12_blender.png)

## Makehumanモデルの骨を見える様に設定する

![xray](/images/20160526_xray_bone.png)

## Makehumanモデル「骨」を消す

- まず「Object Mode」に行って
- MRB(マウスバ右ターン)で骨の任意場所でをタッチ
- 全ての骨を同時に選択(ハイライト)されたかどうか、確認する
- キーボード「x」を押して、Delete?を選択して、骨を消すことが完成

![delete_bone](/images/20160526_delete_bone.png)

## Makehumanモデルの「Vertex Groups」を消す

「Vertex Groups」というものはメッシュの一つプロパティーです。
Makehumanで生成されたモデル中、「Vertex Groups」を元々存在している。
我々はperfumeの骨を入れたいので、Makehuman元々の「Vertex Groups」を消さないいけない。

![vertexgroup](/images/20160526_delete_vertexgroup.png)

全部消したら、「Vertex Groups」は空き状態になる

![no_vertexgroup](/images/20160526_no_vertexgroup.png)

## Perfume BVHをimport

![perfumen_bvh](/images/20160526_import_perfumen_bvh_blender.png)

## Makehumanモデルのメッシュのscaleを変更

### PefumeとMakehumanの単位不一致

初めて導入されたPerfumeのskeletonサイズはMakehumanのメッシュの100倍。

![not_same_scale](/images/20160526_bvh_mesh_not_same_scale.png)

まずその二つモデルは同じscaleに変更行く。

### scale変更の二つ方法:

- 方法1. Makehuman皮膚 X 100倍 → 骨Binding
- 方法2. Perfume骨 X 0.01倍 → 骨Binding → Perfume骨 X 100倍

方法１のサイズ変更は一回のみ、今度採用しました。

### Makehuman皮膚 X 100倍 拡大した結果

「皮膚」と「骨」は同じレベルになった↓。

![mesh100times](/images/20160526_mesh100times_show.png)

具体的の作業は

- STEP1: 骨をTPOSEにする
- STEP2: 皮膚を100倍scaleする

![mesh100times](/images/20160526_mesh100times_operation.png)

## 骨と皮膚の位置を合わせる(手動)

関節の位置を調整して、なるべく皮膚の最中に埋め込むだけ。

- ご注意:
    - 個別関節の位置を調整したい場合は、Edit Modeしかない。
    - TPOSEで調整するので、全ての関節のRotationはゼロとするべき。
    - ショットカット使わなければいけないと思います。特に"b", "a", "ctrl-MLB"。

### 合わせる前:

![matching](/images/20160526_before_matching.png)

### 合わせる後:

![matching](/images/20160526_after_matching.png)

### 難しいところ

こちらの作業一番難しいところは「明確な基準」が定義し難いと思います。
でも、何回実験の結果をみて、骨と皮膚の相対位置は、最後の結果にそんなに敏感ではないです。
我々の目的は完璧なCG動画を作成ではないので、目安でしてください。


## 骨と皮膚の重み付け(自動)

骨と皮膚は、Blender内蔵の自動化重み付け機能がある。
色んなtutorialを見て、普通のやり方は「自動で生成」+「手動で微調整」です。

我々は、まず自動で生成した重みのみで、skeleton animationの性能を見ました。
やはりskeleton animation分野の元々難しいところ(肘、等)で、
ちょっと不自然な変形が存在する可能性がある(体型による)。

でも、我々の目的は完璧なCG動画を作成ではない、なおかつ作業時間を削減したいので、
自動で生成した重みを使って、手作業の微調整を要らないつもりで作業手順を定義した。

### Blender内蔵の自動化重み付け機能の使い方を説明する。

- STEP1: Object Modeに行く
- STEP2: 「a」を押して、全てのObjectをDeselect様にする
- STEP3: 「MRB」で皮膚を選択する
- STEP4: 「shift+MRB」で骨を選択する
- STEP5: 「ctrl+p」を押して、"With Automatic Weights"を選択する

![weights](/images/20160527_automatic_weights.png)

もし、皮膚はおかしい変形を発生していない、皮膚と骨の重み付け作業は完了した。

万が一、人体はおかしい変形を発生する場合は、骨と皮膚の位置をよく合わせないと思う。
そちらの作業に戻って、もう一度してください。

## モデル品質を確認するために、perfume danceを再生

我々導入したBVH中、perfume danceのmotion情報を入っている。
このmotionを再生して、先ほどの「皮膚」と「骨」のbinding品質を定性確認できる。

### モデルSkeleton Animationを生成

- STEP1: Rest Position → Pose Postion (しなければ、skeleton animationを見えない)
- STEP2: 再生

![play](/images/20160527_play.png)

### 結果例「makehuman皮膚+perfume骨」のskeleton animation

![play](/images/20160527_perfumen_skeleton_animation.png)

もし、皮膚はおかしい変形を発生していない、皮膚と骨の重み付け作業は完了した。

万が一、人体はおかしい変形を発生する場合は、骨と皮膚の位置をよく合わせないと思う。
そちらの作業に戻って、もう一度してください。

## 最後 モデル Export

### COLLADAでexport

File→Export→Collada

![play](/images/20160527_export_collada.png)

以上で、すべての作業完了。
