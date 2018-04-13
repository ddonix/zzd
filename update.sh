m=`date +%Y-%m-%d_%H:%M:%S`
m1=$1\|$m
git add .
git commit -m $m1
git push origin 语法结构调整
