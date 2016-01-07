name=$1
path=$2

nvm use
hexo new post $name -p $path
