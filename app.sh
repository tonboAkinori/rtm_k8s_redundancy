#!/bin/bash

# Nodeの情報からIPアドレスを取得する
NODE_IP_LIST=($(kubectl get nodes -o json | jq '.items[].status.addresses[] | select(.type=="InternalIP") | .address '))

# Master以外のノードのアドレスをログ表示するために、添字が1以降のものを表示
echo ${NODE_IP_LIST[@]:1}

## Masterを含めたノード数
NODE_SUM=$(kubectl get nodes -o json | jq  '.items | length')

## Master以外のノード数
WORKER_NUM=$(($NODE_SUM-1)) 

## ノード状態の一時保存
TMP_NODE_STATUS='True'

## 接続中ノード番号
CONNECTING_NODE_NUMBER=0

## Manager のポート情報を格納しておく
declare -A MANAGER_PORT_LIST=(
    [192.168.11.3]=30281
    [192.168.11.4]=30282
)


## 初回接続 ###############################################################################################################
for num in $(eval echo {1..$WORKER_NUM}); do
    
    # Master 以外のノードのステータスを確認する
    TMP_NODE_STATUS=$(kubectl get nodes -o json | jq -r .items[$num].status.conditions[3].status)
    
    if [ $TMP_NODE_STATUS = 'True' ]; then
	echo "Connectting ${NODE_IP_LIST[$num]}"
	# 接続中のノード番号保持
	CONNECTING_NODE_NUMBER=$num
	CHANGE_IP_STR=($(kubectl get nodes -o json | jq '.items['$num'].status.addresses[] | select(.type=="InternalIP") | .address '))
	CHANGE_IP=$(echo $CHANGE_IP_STR | sed "s/\"//g")
	python man_ctl.py $CHANGE_IP ${MANAGER_PORT_LIST[$CHANGE_IP]}
	break
    fi
done


## 接続中のノードを監視 ###################################################################################################

err_counter=0

while [ $TMP_NODE_STATUS != 'Unknown' ]
do
    sleep 1

    # ノードの状態を確認する(Unknownで不正な状態と判定する）
    # 接続中のノードステータスを確認する
    TMP_NODE_STATUS=$(kubectl get nodes -o json | jq -r .items[$CONNECTING_NODE_NUMBER].status.conditions[3].status)

    
    if [ $TMP_NODE_STATUS = 'Unknown' ]; then

	err_counter=$((err_counter + 1))

	if [ $err_counter -lt 3 ]; then
	    TMP_NODE_STATUS='True'
	    continue
	fi

	echo ""
	echo " Node [$CONNECTING_NODE_NUMBER] Status: Error"
	err_counter=0
	
	# Redy 状態のワーカーノードを探す
	for num in $(eval echo {1..$WORKER_NUM}); do


	    # Master 以外のノードのステータスで探す
	    SEARCH_STATUS=$(kubectl get nodes -o json | jq -r .items[$num].status.conditions[3].status)

	    if [ $SEARCH_STATUS = 'True' ]; then
		echo " Node Change ...."
		CONNECTING_NODE_NUMBER=$num
		TMP_NODE_STATUS='True'
		CHANGE_IP=$(kubectl get nodes -o json | jq '.items['$num'].status.addresses[] | select(.type=="InternalIP") | .address ')
		CHANGE_IP=$(echo $CHANGE_IP | sed "s/\"//g")
		
		echo "Connectting $CHANGE_IP"
		python man_ctl.py $CHANGE_IP ${MANAGER_PORT_LIST[$CHANGE_IP]}
		break
	    fi
	done
	#全ノードが駄目なら終了
	if [ $TMP_NODE_STATUS = 'Unknown' ]; then
	    echo "All Node is Error"
	    break
	fi
    fi
    echo "Node [$CONNECTING_NODE_NUMBER] Status: Normal"
done
