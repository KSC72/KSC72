git config  user.name "Schwarz Knut ESK UILD5"
git config  user.email "knut.Schwarz@zf.com"
git clone https://zf-git.emea.zf-world.com/scm/esp_pilot_temp/ee9940_demo_4.git
cd ee9940_demo_4
git init
echo ee940_demo_4 > readme.md
echo *.bak > .gitignore
git add readme.md
git add .gitignore
git commit -m "Initial Commit"
git remote add origin https://zf-git.emea.zf-world.com/scm/esp_pilot_temp/ee9940_demo_4.git
git push -u origin HEAD:master