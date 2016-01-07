name=$1
path=$2

# Firstly do `nvm use`
hexo new post $name -p $path
