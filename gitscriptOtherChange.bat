chcp 65001
cd EE9940_DEMO_OTHER
git.exe checkout --force master 
git.exe branch --force task/master/5692812_otherDemoTask
git.exe checkout --force task/master/5692812_otherDemoTask
echo "change1_f2" >> file2.txt
git.exe add file2.txt
git.exe commit -m "change 1f2" 
echo "change2_f2" >> file2.txt
git.exe add file2.txt
git.exe commit -m "change 2f2" 
echo "change3_f2" >> file2.txt
git.exe add file2.txt
git.exe commit -m "change 3f2" 
git.exe checkout --force master 