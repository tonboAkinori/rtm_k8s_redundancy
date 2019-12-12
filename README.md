動画反転システムの冗長構成サンプルシステム
===

目次
===
* [システム構成](#%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E6%A7%8B%E6%88%90)
  * [必要なもの](#%E5%BF%85%E8%A6%81%E3%81%AA%E3%82%82%E3%81%AE)
  * [静的構造](#%E9%9D%99%E7%9A%84%E6%A7%8B%E9%80%A0)
  * [ソフトウェアのインストール](#%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
    * [Kubernetes と Docker のインストール](#kubernetes-%E3%81%A8-docker-%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
    * [異常検出＆切り替えアプリをダウンロード](#%E7%95%B0%E5%B8%B8%E6%A4%9C%E5%87%BA%E5%88%87%E3%82%8A%E6%9B%BF%E3%81%88%E3%82%A2%E3%83%97%E3%83%AA%E3%82%92%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)
    * [jq のインストール](#jq-%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
    * [OpenRTM\-aist のインストール](#openrtm-aist-%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
    * [OpenCV コンポーネント (OpenCVCamera と CameraViewer) のインストール](#opencv-%E3%82%B3%E3%83%B3%E3%83%9D%E3%83%BC%E3%83%8D%E3%83%B3%E3%83%88-opencvcamera-%E3%81%A8-cameraviewer-%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
* [事前確認](#%E4%BA%8B%E5%89%8D%E7%A2%BA%E8%AA%8D)
* [構築](#%E6%A7%8B%E7%AF%89)
  * [環境に合わせたアプリ設定](#%E7%92%B0%E5%A2%83%E3%81%AB%E5%90%88%E3%82%8F%E3%81%9B%E3%81%9F%E3%82%A2%E3%83%97%E3%83%AA%E8%A8%AD%E5%AE%9A)
    * [man\_ctl\.py に ロボット側 PC の IP アドレスを記載する](#man_ctlpy-%E3%81%AB-%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88%E5%81%B4-pc-%E3%81%AE-ip-%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%82%92%E8%A8%98%E8%BC%89%E3%81%99%E3%82%8B)
    * [app\.sh に ワーカーノードの IP アドレスを記載する](#appsh-%E3%81%AB-%E3%83%AF%E3%83%BC%E3%82%AB%E3%83%BC%E3%83%8E%E3%83%BC%E3%83%89%E3%81%AE-ip-%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%82%92%E8%A8%98%E8%BC%89%E3%81%99%E3%82%8B)
  * [クラスター構築](#%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC%E6%A7%8B%E7%AF%89)
    * [マスター用 PC のマスターノード化](#%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC%E7%94%A8-pc-%E3%81%AE%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%8E%E3%83%BC%E3%83%89%E5%8C%96)
    * [ワーカー用 PC をワーカーノードとしてマスターノードへ登録](#%E3%83%AF%E3%83%BC%E3%82%AB%E3%83%BC%E7%94%A8-pc-%E3%82%92%E3%83%AF%E3%83%BC%E3%82%AB%E3%83%BC%E3%83%8E%E3%83%BC%E3%83%89%E3%81%A8%E3%81%97%E3%81%A6%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%8E%E3%83%BC%E3%83%89%E3%81%B8%E7%99%BB%E9%8C%B2)
    * [クラスタのネットワーク構築](#%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%81%AE%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E6%A7%8B%E7%AF%89)
    * [ワーカーノードにラベルを設定](#%E3%83%AF%E3%83%BC%E3%82%AB%E3%83%BC%E3%83%8E%E3%83%BC%E3%83%89%E3%81%AB%E3%83%A9%E3%83%99%E3%83%AB%E3%82%92%E8%A8%AD%E5%AE%9A)
  * [ワーカノードに Flip RTC を配置](#%E3%83%AF%E3%83%BC%E3%82%AB%E3%83%8E%E3%83%BC%E3%83%89%E3%81%AB-flip-rtc-%E3%82%92%E9%85%8D%E7%BD%AE)
  * [クラスタ/ロボット間通信のためのポート設定](#%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88%E9%96%93%E9%80%9A%E4%BF%A1%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%9D%E3%83%BC%E3%83%88%E8%A8%AD%E5%AE%9A)
  * [OpenCV コンポーネントを起動する](#opencv-%E3%82%B3%E3%83%B3%E3%83%9D%E3%83%BC%E3%83%8D%E3%83%B3%E3%83%88%E3%82%92%E8%B5%B7%E5%8B%95%E3%81%99%E3%82%8B)
  * [ロボット用 PC で RTC deamon (Manager) を起動する](#%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88%E7%94%A8-pc-%E3%81%A7-rtc-deamon-manager-%E3%82%92%E8%B5%B7%E5%8B%95%E3%81%99%E3%82%8B)
  * [クラスタ内の RTC と ロボット側 RTC の接続](#%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E5%86%85%E3%81%AE-rtc-%E3%81%A8-%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88%E5%81%B4-rtc-%E3%81%AE%E6%8E%A5%E7%B6%9A)
* [動作確認](#%E5%8B%95%E4%BD%9C%E7%A2%BA%E8%AA%8D)
  * [故障挿入](#%E6%95%85%E9%9A%9C%E6%8C%BF%E5%85%A5)
  * [冗長系への切り替え](#%E5%86%97%E9%95%B7%E7%B3%BB%E3%81%B8%E3%81%AE%E5%88%87%E3%82%8A%E6%9B%BF%E3%81%88)
* [改定履歴](#%E6%94%B9%E5%AE%9A%E5%B1%A5%E6%AD%B4)

# システム構成

## 必要なもの

- マスター用 PC 1台 (Raspberry PI 可)

  Kubernetes のマスターノードとなる PC。マスター用 PC は、ワーカー用 PC の異常を監視し、必要に応じて他のワーカーノード (=冗長系) に処理を切り替える。
- ワーカー用 PC 2台 (Raspberry PI 可)

  Kubernetes のワーカーノードとなる PC。ワーカー用 PC は、クラウド上の RTC を動かす。
    
- ロボット側 PC 1台

  ロボットのデバイス制御のためにロボットに搭載される PC。Kubernetes とは関係ない。

## 静的構造

![system](https://user-images.githubusercontent.com/45954537/70786986-21c2b400-1dd1-11ea-98da-6e0161343203.png)


## ソフトウェアのインストール

　各 PC に必要なソフトウェアの一覧を下表に示します。

| | Kubernetes | Docker | OpenRTM-aist + OpenCVコンポーネント | 異常検出＆切り替えアプリ | jq
:----:|:----:|:----:|:----:|:----:|:----:|
| マスター用 PC | ○ | ○ | - | ○ | ○ |
| ワーカー用 PC | ○ | ○ | - | - | - |
| ロボット側 PC | - | - | ○ | - | - |

### Kubernetes と Docker のインストール
　これらのインストールは、下記のURLを参照ください。

https://github.com/r-kurose/rtm_k8s/blob/master/index.md#インストール手順

### 異常検出＆切り替えアプリをダウンロード
　マスター用 PC で下記コマンドを実行し、異常検知とRTCの切り替えに必要なスクリプトを取得してください。
これらは、異常の検出や多重化の RTC 切り替えに使うスクリプトで動作確認で使用します。
```
wget https://raw.githubusercontent.com/r-kurose/rtm_k8s_redundancy/master/app.sh
wget https://raw.githubusercontent.com/r-kurose/rtm_k8s_redundancy/master/man_ctl.py
```

### jq のインストール
　異常検出＆切り替えアプリ の app.sh は  jq を使用します。マスター用 PC にインストールしてください。

- Windows の場合

  下記のURLからダウンロード、インストールしてください。

  https://stedolan.github.io/jq/

- Ubuntu の場合

  `sudo apt -y install jq`

### OpenRTM-aist のインストール
　ロボット側 PC に、下記のURLの手順に従って OpenRTM-aist をインストールしてください。
- Windows の場合

  https://www.openrtm.org/openrtm/ja/doc/installation/install_1_2/cpp_1_2/install_windows_1_2
- Ubuntu の場合

  https://www.openrtm.org/openrtm/ja/doc/installation/install_1_2/cpp_1_2/install_ubuntu_1_2

### OpenCV コンポーネント (OpenCVCamera と CameraViewer) のインストール
- Windows の場合

  　OpenRTM-aist がインストールされていれば、インストール済です。
  OpenRTM-aist をインストールしたフォルダ配下に OpenCVCameraComp と CameraViewer があります。    
  　詳細なインストール場所を知りたい方は以下を参照してください。

  https://www.openrtm.org/openrtm/ja/doc/installation/install_1_2/cpp_1_2/install_windows_1_2

- Ubuntu の場合

  　ソースコードからのビルドが必要です、以下からソースコードを取得してください。
 
  　https://github.com/OpenRTM/ImageProcessing
 
  - OpenCVのパッケージをインストールする
 
  `sudo apt install libopencv-dev`
 
  - OpenCVCameraのビルド

  ```
  cd ImageProcessing/opecv/components/OpenCVCamera
  cmake -S . -Bbuild
  cmake --build build
  ```

  - CameraViewerのビルド

  ```
  cd ImageProcessing/opecv/components/CameraViewer
  cmake -S . -Bbuild
  cmake --build build
  ```

# 事前確認

　念のために、カメラの映像が RTC を通して、表示できるかどうかを確認します。この確認は飛ばしてもかまいません。
手順は下記を参照してください。

https://www.openrtm.org/openrtm/ja/doc/installation/sample_components/opencvcameracomp


# 構築

## 環境に合わせたアプリ設定

### man_ctl.py に ロボット側 PC の IP アドレスを記載する

　27行目の IP アドレス部分 `192.168.11.70` を使用されているロボット側 PC の IP アドレスに書き換えてください。
ロボット用 PC に配置されている RTC を操作するのに必要な情報となります。
```
camera_ip_add = "corbaloc:iiop:ロボット側 PC の IP アドレス:2810/manager"
```
ここで、 IP アドレスは Windows なら "ipconfig"、Linux なら "ip address" などで取得します。

### app.sh に ワーカーノードの IP アドレスを記載する

　23行目と24行目にワーカノードの IP アドレス を記載してください。

```
  ## Manager のポート情報を格納しておく
  declare -A MANAGER_PORT_LIST=(
    [Flip-1を配置したノードのIPアドレス]=30281
    [Flip-2を配置したノードのIPアドレス]=30282
  )
```

## クラスター構築

最初にマスターノードを初期化し、その後にワーカーノードをマスターノードに登録します。

### マスター用 PC のマスターノード化
　マスター用 PC をマスターノードとするために、下記をおまじないとして実行してください。
```
kubeadm init --pod-network-cidr=10.244.0.0/16
```

### ワーカー用 PC をワーカーノードとしてマスターノードへ登録
```
kubeadm join <マスターノードの kubeadm init 実行で表示されるパラメーター>
```
確認方法: マスターノードで `kubectl get nodes` を実行するとノードが見えます。

### クラスタのネットワーク構築
　マスター用 PC で Kubernetes のネットワークを構築するために以下のおまじないを実行してください。
```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```
### ワーカーノードにラベルを設定
　マスター用 PC からワーカーノードにラベルを設定します。
このラベルは、正規の系と冗長系を区別するために使用されます。  
　マスター用 PC で下記を実行します。
```
kubectl label node <ワーカーノード名> flip-1=true
kubectl label node <ワーカーノード名> flip-2=true
```

## ワーカノードに Flip RTC を配置

　マスター用 PC で、下記のコマンドを実行してください。

```
kubectl apply -f https://raw.githubusercontent.com/r-kurose/rtm_k8s_redundancy/master/Flip-1.yaml
kubectl apply -f https://raw.githubusercontent.com/r-kurose/rtm_k8s_redundancy/master/Flip-2.yaml
```

## クラスタ/ロボット間通信のためのポート設定

　クラスタ外と通信できるようにポート設定を行います。下記のコマンドをマスター用 PC で実行してください。
```
kubectl apply -f https://raw.githubusercontent.com/r-kurose/rtm_k8s_redundancy/master/service.yaml
```
 
## OpenCV コンポーネントを起動する

　事前確認ですでに確認されている方は、OpenCVCamera と CameraViewer を再起動してアクティベートしてください。
ポート接続の手順をご存じの方は、再起動せずポート接続を解除していただくだけでも大丈夫です。
ポートの接続はこの後実行していただくスクリプトで行うので不要です。
 
##  ロボット用 PC で RTC deamon (Manager) を起動する
  
　ロボット側 PC にある RTC を操作するために使用します。

  - Windowsの場合
  
　　Windowsキーを押下して、Start C++ RTC deamon と検索して実行してください。

  - Ubuntuの場合
  
　　`rtcd -d` を実行してください  
  
## クラスタ内の RTC と ロボット側 RTC の接続

　マスター用 PC で `./app.sh` を実行してください。クラスタ内の Flip RTC を通して左右が反転したカメラ映像が出力されます。

# 動作確認

## 故障挿入

　擬似的に RTC が動作する PC を壊れたようにシステムに見せるために、ワーカー用 PC1 のケーブルを切断してください。

## 冗長系への切り替え 
　故障挿入後、しばらく立つと自動で別のワーカーノードにあるRTCへ切り替わり、カメラ映像の上下が反転します。
この処理は、マスター用 PC で起動している app.sh が実行しています。  
　ここで注意点として OpenRTM-aist の仕様により、別のノードにある RTC と切り替わるまでに分単位の時間が掛かることがあります。
これは OpenRTM-aist が存在しなくなった RTC にアクセスして、タイムアウト待ちになるケースが
あることが原因です。
Python版 OpenRTM-aist 1.2 では、暫定的な修正を加え、切り替え時間を4秒までに短縮できることは確認しています。
しかし、 OpenRTM-aist の仕様変更となるために対応方法は検討中です。

# 改定履歴

  - 2019-12-13: 初版
