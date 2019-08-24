echo 'Opening MongoDB'

gnome-terminal --tab --active -- bash -c "
sudo rm /var/lib/mongodb/mongod.lock
sudo mongod --dbpath /var/lib/mongodb/ --repair
sudo mongod --dbpath /var/lib/mongodb/ --journal
; exec bash"

sleep 3

echo 'Opening Research Assistant'

gnome-terminal --tab --active -- bash -c "
python3 -B research_assistant.py
; exec bash"

sleep 3

echo 'Opening Server'

python3 -B backend.py