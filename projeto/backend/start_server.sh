echo 'Opening MongoDB'

gnome-terminal --tab --active -- bash -c "
sudo rm /var/lib/mongodb/mongod.lock
sudo mongod --dbpath /var/lib/mongodb/ --repair
sudo mongod --dbpath /var/lib/mongodb/ --journal
; exec bash"

sleep 5

echo 'Opening Server'

gnome-terminal --tab --active -- bash -c "
python3 -B backend.py
; exec bash"

sleep 10

echo 'Opening Research Assistant'

python3 -B research_assistant.py