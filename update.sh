m=`date +%Y-%m-%d_%H:%M:%S`
m1=$1\|$m
git add *.txt *.py *.sh README
git commit -m $m1
git push origin master
