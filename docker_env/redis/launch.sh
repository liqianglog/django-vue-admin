cur_path=`pwd`
# docker pull redis:latest
docker run -d \
    -p 6379:6379 \
    -v $cur_path/redis.conf:/etc/redis/redis.conf \
    --privileged=true \
    --name docker-redis \
    redis:latest \
    redis-server /etc/redis/redis.conf
