#!/bin/sh

echo "[*] Tìm container đang bị restart vòng lặp..."
RESTARTING_CONTAINERS=$(docker ps -a --filter "status=restarting" --format "{{.ID}}")

if [ -n "$RESTARTING_CONTAINERS" ]; then
  echo "[!] Đang có container restart liên tục, sẽ stop:"
  echo "$RESTARTING_CONTAINERS"
  for container in $RESTARTING_CONTAINERS; do
    docker stop "$container"
  done
else
  echo "[+] Không có container nào bị restart liên tục."
fi

echo "[*] Xoá container không dùng..."
docker container prune -f

echo "[*] Xoá image không dùng (kể cả dangling và unused)..."
docker image prune -a -f

echo "[+] Dọn dẹp Docker hoàn tất."
