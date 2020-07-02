cd ../../
python -m IoT.level2.init_db --drop
python -m IoT.level4.init_db --drop
python -m IoT.level4b.init_db --drop

python -m IoT.level2.run &
echo $!
python -m IoT.level4.run &
echo $!
python -m IoT.level4b.run &
echo $!

echo $$