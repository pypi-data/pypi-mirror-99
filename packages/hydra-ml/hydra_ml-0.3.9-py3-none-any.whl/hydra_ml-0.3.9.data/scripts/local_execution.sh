print_usage() {
  printf "Usage: TODO"
}

# Read bash arguments from flag
while getopts 'g:c:o:m:p:a:t:u:' flag; do
  case "${flag}" in
    g) GIT_URL="${OPTARG}" ;;
    c) COMMIT_SHA="${OPTARG}" ;;
    o) OAUTH_TOKEN="${OPTARG}" ;;
    m) MODEL_PATH="${OPTARG}" ;;
    p) OPTIONS="${OPTARG}" ;;
    t) IMAGE_TAG="${OPTARG}" ;;
    u) IMAGE_URI="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

# Move to Hydra package's docker directory
PROJECT_DIR=$(PWD)
DIR="$( dirname "${BASH_SOURCE[0]}" )"
cd $DIR

# Generate identifier for this training job
DATE=$(date +'%Y_%m_%d_%H_%M_%S')
HASH=$(( RANDOM % 1000 ))
JOB_NAME="job_${DATE}_id_${HASH}"

# Build Image URI
if [[ $IMAGE_URI == '' ]]; then
  if [[ $IMAGE_TAG == '' ]]; then
    export IMAGE_URI=public.ecr.aws/l6k7f2t9/hydra:master
  else
    export IMAGE_URI=public.ecr.aws/l6k7f2t9/hydra:${IMAGE_TAG}
  fi
else
  export IMAGE_URI=${IMAGE_URI}:${IMAGE_TAG}
fi

# Build and run image
docker run \
  --rm \
  -v "$PROJECT_DIR/data":/home/data \
  $IMAGE_URI \
  --git_url=$GIT_URL \
  --commit_sha=$COMMIT_SHA \
  --oauth_token=$OAUTH_TOKEN \
  --model_path=$MODEL_PATH \
  --platform='local' \
  --options="$OPTIONS" \
  2>&1 | tee ${JOB_NAME}.log

# Move Log file to where the program is being called
cd - && mkdir -p tmp/hydra
mv ${DIR}/${JOB_NAME}.log tmp/hydra/
