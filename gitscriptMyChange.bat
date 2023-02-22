chcp 65001
cd EE9940_DEMO_4_MY
git.exe checkout --force master 
git.exe branch --force task/master/5692810_myDemoTask
git.exe checkout --force task/master/5692810_myDemoTask
echo "change1_f1" >> file1.txt
git.exe add file1.txt
git.exe commit -m "change 1f1" 
echo "change2_f1" >> file1.txt
git.exe add file1.txt
git.exe commit -m "change 2f1" 
echo "change3_f1" >> file1.txt
git.exe add file1.txt
git.exe commit -m "change 3f1" 
git.exe checkout --force master
