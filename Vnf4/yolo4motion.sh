#!/bin/bash

# calculated
BUILD_ARCH=$(uname -m | sed -e 's/aarch64.*/arm64/' -e 's/x86_64.*/amd64/' -e 's/armv.*/arm/')

# parameters
SERVICE='{"label":"yolo4motion","id":"com.github.dcmartin.open-horizon.yolo4motion","version":"'${SERVICE_VERSION:-0.1.0}'","arch":"'${SERVICE_ARCH:-${BUILD_ARCH}}'","ports":{"service":'${SERVICE_PORT:-80}',"host":'${HOST_PORT:-4662}'}}'
MOTION='{"group":"'motion'","client":"'motionCam'","camera":"'webcam'"}'
MQTT='{"host":"'192.168.1.8'","port":'${MQTT_PORT:-1883}',"username":"'sakxam'","password":"'sakxam'"}'
YOLO='{"config":"'${YOLO_CONFIG:-tiny}'","entity":"'${YOLO_ENTITY:-all}'","scale":"'${YOLO_SCALE:-none}'","threshold":'${YOLO_THRESHOLD:-0.25}'}'
DEBUG='{"debug":'${DEBUG:-false}',"level":"'"${LOG_LEVEL:-info}"'","logto":"'"${LOGTO:-/dev/stderr}"'"}'

# notify
echo 'SERVICE: '$(echo "${SERVICE}" | jq -c '.') &> /dev/stderr
echo 'MOTION: '$(echo "${MOTION}" | jq -c '.') &> /dev/stderr
echo 'MQTT: '$(echo "${MQTT}" | jq -c '.') &> /dev/stderr
echo 'YOLO: '$(echo "${YOLO}" | jq -c '.') &> /dev/stderr
echo 'DEBUG: '$(echo "${DEBUG}" | jq -c '.') &> /dev/stderr

# specify
LABEL=$(echo "${SERVICE:-null}" | jq -r '.label')
ARCH=$(echo "${SERVICE:-null}" | jq -r '.arch')
VERS=$(echo "${SERVICE:-null}" | jq -r '.version')
ID=$(echo "${SERVICE:-null}" | jq -r '.id')
EXT_PORT=$(echo "${SERVICE}" | jq -r '.ports.host')
INT_PORT=$(echo "${SERVICE}" | jq -r '.ports.service') 

# container name
NAME=${SERVICE_NAME:-${LABEL}}

# cleanup
echo "Removing any existing container: ${LABEL}" &> /dev/stderr
docker rm -f ${NAME} &> /dev/null

# start up
echo "Starting new container: ${NAME}; id: ${ID}; architecture: ${ARCH}; version: ${VERS}; host: ${EXT_PORT}; service: ${INT_PORT}" &> /dev/stderr
CID=$(balena run -d \
  --privileged \
  --name ${NAME} \
  --mount type=tmpfs,destination=/tmpfs,tmpfs-size=81920000,tmpfs-mode=1777 \
  --publish=${EXT_PORT}:${INT_PORT} \
  --restart=unless-stopped \
  -e SERVICE_LABEL=${LABEL} \
  -e SERVICE_VERS=${VERS} \
  -e SERVICE_PORT=${INT_PORT} \
  -e MQTT_HOST=$(echo "${MQTT}" | jq -r '.host') \
  -e MQTT_PORT=$(echo "${MQTT}" | jq -r '.port') \
  -e MQTT_USERNAME=$(echo "${MQTT}" | jq -r '.username') \
  -e MQTT_PASSWORD=$(echo "${MQTT}" | jq -r '.password') \
  -e MOTION_GROUP=$(echo "${MOTION}" | jq -r '.group') \
  -e MOTION_CLIENT=$(echo "${MOTION}" | jq -r '.client') \
  -e YOLO4MOTION_CAMERA=$(echo "${MOTION}" | jq -r '.camera') \
  -e YOLO4MOTION_TOPIC_EVENT=event/end \
  -e YOLO4MOTION_TOPIC_PAYLOAD=image/end \
  -e YOLO4MOTION_USE_MOCK=false \
  -e YOLO4MOTION_TOO_OLD=300 \
  -e YOLO_CONFIG=$(echo "${YOLO}" | jq -r '.config') \
  -e YOLO_ENTITY=$(echo "${YOLO}" | jq -r '.entity') \
  -e YOLO_SCALE=$(echo "${YOLO}" | jq -r '.scale') \
  -e YOLO_THRESHOLD=$(echo "${YOLO}" | jq -r '.threshold') \
  -e YOLO_PERIOD=60 \
  -e LOG_LEVEL=$(echo "${DEBUG}" | jq -r '.level') \
  -e LOGTO=$(echo "${DEBUG}" | jq -r '.logto') \
  -e DEBUG=$(echo "${DEBUG}" | jq -r '.debug') \
  "dcmartin/${ARCH}_${ID}:${VERS}" 2> /dev/stderr)

# report
if [ "${CID:-null}" != 'null' ]; then
  echo 'Container '${LABEL}' started; status: "curl http://localhost:'$(echo "${SERVICE}" | jq -r '.ports.host')'"; id: '"${CID}" &> /dev/stderr
else
  echo "Container ${LABEL} failed" &> /dev/stderr
fi
echo '{"name":"'${NAME}'","id":"'${CID:-null}'","service":'"${SERVICE}"',"motion":'"${MOTION}"',"yolo":'"${YOLO}"',"mqtt":'"${MQTT}"',"debug":'"${DEBUG}"'}' | jq
