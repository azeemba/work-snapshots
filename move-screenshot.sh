
set -eux
cd "C:\\Users\\Z\\Pictures\\Screenshots"
latest=$(ls --sort=time --time=creation -1 | head -n1)
epoch_time=$(stat -c '%W' "$latest")
timestamp=$(date -d@${epoch_time} +"%Y-%m-%d_%H_%M")

target="E:\\QuickBackups\\daily-captures\\${timestamp}.png"
mv "$latest" "$target"

cd -
bash convert-screenshots.sh