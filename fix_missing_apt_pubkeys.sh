sudo apt-get update 2>&1 1>/dev/null | sed -ne 's/.*NO_PUBKEY //p' |
while read key; do
    echo 'Processing key:' "$key"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys "$key"
done