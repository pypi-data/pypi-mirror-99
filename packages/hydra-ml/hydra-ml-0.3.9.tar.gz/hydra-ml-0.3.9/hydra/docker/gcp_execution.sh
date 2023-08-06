print_usage() {
  printf "Usage: TODO"
}

# Read bash arguments from flag
while getopts 'g:c:o:m:r:t:n:p:u:a:y:' flag; do
  case "${flag}" in
    g) GIT_URL="${OPTARG}" ;;
    c) COMMIT_SHA="${OPTARG}" ;;
    o) OAUTH_TOKEN="${OPTARG}" ;;
    m) MODEL_PATH="${OPTARG}" ;;
    r) REGION="${OPTARG}" ;;
    t) IMAGE_TAG="${OPTARG}" ;;
    u) IMAGE_URI="${OPTARG}" ;;
    a) GPU_COUNT="${OPTARG}" ;;
    y) GPU_TYPE="${OPTARG}" ;;
    n) MACHINE_NAME="${OPTARG}" ;;
    p) OPTIONS="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

# Move to Hydra package's docker directory
PROJECT_DIR=$(pwd)
DIR="$( dirname "${BASH_SOURCE[0]}" )"
cd $DIR

# Generate identifier for this training job
DATE=$(date +'%Y_%m_%d_%H_%M_%S')
HASH=$(( RANDOM % 1000 ))
JOB_NAME="job_${DATE}_id_${HASH}"

# Build Image URI
if [[ $IMAGE_URI == '' ]]; then
  if [[ $IMAGE_TAG == '' ]]; then
    export IMAGE_URI=gcr.io/hydra-gcp-test-291317/hydra_image:master
  else
    export IMAGE_URI=gcr.io/hydra-gcp-test-291317/hydra_image:${IMAGE_TAG}
  fi
else
  export IMAGE_URI=${IMAGE_URI}:${IMAGE_TAG}
fi

echo "[Hydra Info] Using" $MACHINE_NAME
echo "[Hydra Info] Using" $GPU_COUNT - $GPU_TYPE

# Submit training job
if [[ $GPU_COUNT == '0' ]]; then
  gcloud ai-platform jobs submit training $JOB_NAME \
    --master-image-uri $IMAGE_URI \
    --region=$REGION \
    --scale-tier="CUSTOM" \
    --master-machine-type=$MACHINE_NAME \
    -- \
    --git_url=$GIT_URL \
    --commit_sha=$COMMIT_SHA \
    --oauth_token=$OAUTH_TOKEN \
    --model_path=$MODEL_PATH \
    --platform='gcp' \
    --options="${OPTIONS}" \
    2>&1 | tee -a ${JOB_NAME}.log
else
  gcloud ai-platform jobs submit training $JOB_NAME \
    --master-image-uri $IMAGE_URI \
    --region=$REGION \
    --scale-tier="CUSTOM" \
    --master-machine-type=$MACHINE_NAME \
    --master-accelerator count=${GPU_COUNT},type=${GPU_TYPE} \
    -- \
    --git_url=$GIT_URL \
    --commit_sha=$COMMIT_SHA \
    --oauth_token=$OAUTH_TOKEN \
    --model_path=$MODEL_PATH \
    --platform='gcp' \
    --options="${OPTIONS}" \
    2>&1 | tee -a ${JOB_NAME}.log
fi

# Provide link for user to access the logs of their job on Google Cloud
gcloud ai-platform jobs describe $JOB_NAME 2>&1 | tee -a ${JOB_NAME}.log

# Move Log file to where the program is being called
cd ${PROJECT_DIR} && mkdir -p tmp/hydra
mv ${DIR}/${JOB_NAME}.log tmp/hydra/${JOB_NAME}.log
