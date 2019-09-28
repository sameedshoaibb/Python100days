# Python100days

git log --oneline

##To create a new branch
git branch rehman-feature

## To show all the branches
git branch -a

## To move to the other branch
git checkout rehman-feature (Now we can start working on this new branch

[[git checkout -b rehman-feature]]

##Now make new file
git add .
git commit -m "added new feature"
git push origin master

##To delete the feature branch
1- goto master branch
2- git branch -D rehman-feature

##To merge the brach a to master
git merge rehman-feature

## To start working in a code
git pull ____ master
