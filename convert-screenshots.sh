set -eux
cd "E:\\QuickBackups\\daily-captures"

for img in $(ls -1 *.png); do
    magick.exe convert $img $(basename $img png)webp
    rm $img
done